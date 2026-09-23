/*
  AeroCrypt - ESP32 Ground Receiver
  PUBLIC-SAFE RELEASE VERSION

  Purpose:
    SX1278 LoRa RX -> AES-128-GCM authenticate/decrypt -> USB Serial

  Public release rules:
    - Do NOT place real AES keys, Wi-Fi passwords, personal names, hostnames,
      private IPs, tokens, or credentials in this file.
    - The AES key below is an EXAMPLE PLACEHOLDER and must be replaced on
      both TX and RX for a real test, preferably through a private/local
      configuration mechanism.

  Packet format:
    [MAGIC 2B][VERSION 1B][NONCE 12B][CIPHERTEXT N B][TAG 16B]
  Plaintext:
    packet,temp,pressure,ax,ay,az,gx,gy,gz
  Optional GPS extension:
    packet,temp,pressure,ax,ay,az,gx,gy,gz,latitude,longitude,satellites,hdop

  LoRa configuration:
    433 MHz, SF7, BW125 kHz, CR4/5, CRC enabled, TX power 17 dBm.
*/

#include <SPI.h>
#include <LoRa.h>
#include "mbedtls/gcm.h"

// ---------------- PUBLIC-SAFE CONFIGURATION ----------------
static const uint8_t AES_KEY[16] = {
  0x00, 0x11, 0x22, 0x33,
  0x44, 0x55, 0x66, 0x77,
  0x88, 0x99, 0xAA, 0xBB,
  0xCC, 0xDD, 0xEE, 0xFF
};

// Generic project identifiers only; no personal/device identity is embedded.
static const char *NODE_ROLE = "GROUND_NODE";

// SX1278 wiring verified for the demonstrated ESP32 ground receiver.
static const int LORA_SS   = 5;
static const int LORA_RST  = 14;
static const int LORA_DIO0 = 2;
static const long LORA_FREQ = 433E6;

static const size_t NONCE_LEN = 12;
static const size_t TAG_LEN   = 16;
static const uint8_t MAGIC0 = 'A';
static const uint8_t MAGIC1 = 'C';
static const uint8_t VERSION = 1;

uint32_t acceptedPackets = 0;
uint32_t rejectedPackets = 0;

bool decryptGCM(const uint8_t *ciphertext, size_t cipherLen,
                const uint8_t *nonce, const uint8_t *tag,
                uint8_t *plaintext) {
  mbedtls_gcm_context gcm;
  mbedtls_gcm_init(&gcm);

  int rc = mbedtls_gcm_setkey(&gcm, MBEDTLS_CIPHER_ID_AES, AES_KEY, 128);
  if (rc != 0) {
    mbedtls_gcm_free(&gcm);
    return false;
  }

  rc = mbedtls_gcm_auth_decrypt(
    &gcm,
    cipherLen,
    nonce, NONCE_LEN,
    nullptr, 0,          // No AAD in the public packet format.
    tag, TAG_LEN,
    ciphertext,
    plaintext
  );

  mbedtls_gcm_free(&gcm);
  return rc == 0;
}

void printTelemetry(const char *plain, int rssi, float snr) {
  // Dashboard contract used by the AeroCrypt monitoring application.
  Serial.print("STREAMLIT_TELEMETRY:");
  Serial.println(plain);

  // Diagnostic line; the dashboard parser can ignore non-telemetry lines.
  Serial.print("AEROCRYPT_LINK,RSSI=");
  Serial.print(rssi);
  Serial.print(",SNR=");
  Serial.println(snr, 2);
}

void handlePacket(int packetSize) {
  if (packetSize < (2 + 1 + NONCE_LEN + TAG_LEN + 1)) {
    rejectedPackets++;
    Serial.println("AEROCRYPT_SECURITY:REJECTED:PACKET_TOO_SHORT");
    while (LoRa.available()) LoRa.read();
    return;
  }

  uint8_t magic0 = LoRa.read();
  uint8_t magic1 = LoRa.read();
  uint8_t version = LoRa.read();

  if (magic0 != MAGIC0 || magic1 != MAGIC1 || version != VERSION) {
    rejectedPackets++;
    Serial.println("AEROCRYPT_SECURITY:REJECTED:INVALID_HEADER");
    while (LoRa.available()) LoRa.read();
    return;
  }

  uint8_t nonce[NONCE_LEN];
  for (size_t i = 0; i < NONCE_LEN; ++i) {
    if (!LoRa.available()) {
      rejectedPackets++;
      return;
    }
    nonce[i] = (uint8_t)LoRa.read();
  }

  const int remaining = LoRa.available();
  if (remaining < (int)(TAG_LEN + 1)) {
    rejectedPackets++;
    Serial.println("AEROCRYPT_SECURITY:REJECTED:INVALID_LENGTH");
    while (LoRa.available()) LoRa.read();
    return;
  }

  const size_t cipherLen = (size_t)remaining - TAG_LEN;
  if (cipherLen >= 240) {
    rejectedPackets++;
    Serial.println("AEROCRYPT_SECURITY:REJECTED:PAYLOAD_TOO_LARGE");
    while (LoRa.available()) LoRa.read();
    return;
  }

  uint8_t ciphertext[240];
  uint8_t tag[TAG_LEN];
  uint8_t plaintext[240];

  for (size_t i = 0; i < cipherLen; ++i) {
    ciphertext[i] = (uint8_t)LoRa.read();
  }
  for (size_t i = 0; i < TAG_LEN; ++i) {
    tag[i] = (uint8_t)LoRa.read();
  }

  plaintext[cipherLen] = '\0';

  const int rssi = LoRa.packetRssi();
  const float snr = LoRa.packetSnr();

  if (!decryptGCM(ciphertext, cipherLen, nonce, tag, plaintext)) {
    rejectedPackets++;
    Serial.println("AEROCRYPT_SECURITY:REJECTED:GCM_AUTH_FAILED");
    return;
  }

  acceptedPackets++;

  Serial.print("AEROCRYPT_SECURITY:VERIFIED,PACKET=");
  Serial.println(acceptedPackets);

  printTelemetry((const char *)plaintext, rssi, snr);
}

void setup() {
  Serial.begin(115200);
  delay(500);

  Serial.println();
  Serial.println("AEROCRYPT_GROUND_RECEIVER");
  Serial.print("ROLE=");
  Serial.println(NODE_ROLE);
  Serial.println("SECURITY=AES-128-GCM");
  Serial.println("STATUS=INITIALIZING");

  LoRa.setPins(LORA_SS, LORA_RST, LORA_DIO0);

  if (!LoRa.begin(LORA_FREQ)) {
    Serial.println("STATUS=LORA_INIT_FAILED");
    while (true) {
      delay(1000);
    }
  }

  LoRa.setTxPower(17);
  LoRa.setSpreadingFactor(7);
  LoRa.setSignalBandwidth(125E3);
  LoRa.setCodingRate4(5);
  LoRa.enableCrc();

  Serial.println("STATUS=LORA_READY");
  LoRa.receive();
}

void loop() {
  int packetSize = LoRa.parsePacket();
  if (packetSize) {
    handlePacket(packetSize);
    LoRa.receive();
  }
}
