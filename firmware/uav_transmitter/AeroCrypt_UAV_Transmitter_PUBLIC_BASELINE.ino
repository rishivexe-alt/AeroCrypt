#include <Wire.h>
#include <SPI.h>
#include <LoRa.h>
#include <Adafruit_BMP280.h>
#include <Adafruit_MPU6050.h>
#include <Adafruit_Sensor.h>
#include "mbedtls/gcm.h"
#include "esp_system.h"

static const uint8_t AES_KEY[16] = {
  0x00, 0x11, 0x22, 0x33,
  0x44, 0x55, 0x66, 0x77,
  0x88, 0x99, 0xAA, 0xBB,
  0xCC, 0xDD, 0xEE, 0xFF
};

static const char *NODE_ROLE = "UAV_NODE";

static const int LORA_SS   = 5;
static const int LORA_RST  = 14;
static const int LORA_DIO0 = 2;
static const long LORA_FREQ = 433E6;

static const size_t NONCE_LEN = 12;
static const size_t TAG_LEN   = 16;
static const uint8_t MAGIC0 = 'A';
static const uint8_t MAGIC1 = 'C';
static const uint8_t VERSION = 1;

Adafruit_BMP280 bmp;
Adafruit_MPU6050 mpu;

uint32_t packetCounter = 0;

bool encryptGCM(const uint8_t *plaintext, size_t plainLen,
                const uint8_t *nonce,
                uint8_t *ciphertext, uint8_t *tag) {
  mbedtls_gcm_context gcm;
  mbedtls_gcm_init(&gcm);

  int rc = mbedtls_gcm_setkey(&gcm, MBEDTLS_CIPHER_ID_AES, AES_KEY, 128);
  if (rc != 0) {
    mbedtls_gcm_free(&gcm);
    return false;
  }

  rc = mbedtls_gcm_crypt_and_tag(
    &gcm,
    MBEDTLS_GCM_ENCRYPT,
    plainLen,
    nonce, NONCE_LEN,
    nullptr, 0,          
    plaintext,
    ciphertext,
    TAG_LEN,
    tag
  );

  mbedtls_gcm_free(&gcm);
  return rc == 0;
}

void fillNonce(uint8_t nonce[NONCE_LEN]) {
  // ESP32 hardware RNG.
  for (size_t i = 0; i < NONCE_LEN; i += 4) {
    uint32_t r = esp_random();
    size_t remaining = NONCE_LEN - i;
    size_t copyLen = remaining < 4 ? remaining : 4;
    memcpy(nonce + i, &r, copyLen);
  }
}

void sendTelemetry() {
  sensors_event_t accel, gyro, tempEvent;
  mpu.getEvent(&accel, &gyro, &tempEvent);

  float temperature = bmp.readTemperature();
  float pressure = bmp.readPressure() / 100.0f;

  char plain[220];
  int n = snprintf(
    plain, sizeof(plain),
    "%lu,%.2f,%.2f,%.4f,%.4f,%.4f,%.4f,%.4f,%.4f",
    (unsigned long)packetCounter,
    temperature,
    pressure,
    accel.acceleration.x / 9.80665f,
    accel.acceleration.y / 9.80665f,
    accel.acceleration.z / 9.80665f,
    gyro.gyro.x * 57.2957795f,
    gyro.gyro.y * 57.2957795f,
    gyro.gyro.z * 57.2957795f
  );

  if (n <= 0 || n >= (int)sizeof(plain)) {
    return;
  }

  uint8_t nonce[NONCE_LEN];
  uint8_t ciphertext[220];
  uint8_t tag[TAG_LEN];

  fillNonce(nonce);

  if (!encryptGCM(
        (const uint8_t *)plain,
        (size_t)n,
        nonce,
        ciphertext,
        tag)) {
    return;
  }

  LoRa.beginPacket();
  LoRa.write(MAGIC0);
  LoRa.write(MAGIC1);
  LoRa.write(VERSION);
  LoRa.write(nonce, NONCE_LEN);
  LoRa.write(ciphertext, n);
  LoRa.write(tag, TAG_LEN);
  LoRa.endPacket();

  packetCounter++;
}

void setup() {
  Serial.begin(115200);
  delay(500);

  Wire.begin();

  if (!bmp.begin(0x76) && !bmp.begin(0x77)) {
    Serial.println("BMP280_INIT_FAILED");
    while (true) delay(1000);
  }

  if (!mpu.begin()) {
    Serial.println("MPU6050_INIT_FAILED");
    while (true) delay(1000);
  }

  LoRa.setPins(LORA_SS, LORA_RST, LORA_DIO0);

  if (!LoRa.begin(LORA_FREQ)) {
    Serial.println("LORA_INIT_FAILED");
    while (true) delay(1000);
  }

  LoRa.setTxPower(17);
  LoRa.setSpreadingFactor(7);
  LoRa.setSignalBandwidth(125E3);
  LoRa.setCodingRate4(5);
  LoRa.enableCrc();

  Serial.println("AEROCRYPT_UAV_TRANSMITTER_READY");
  Serial.print("ROLE=");
  Serial.println(NODE_ROLE);
}

void loop() {
  sendTelemetry();
  delay(1000);
}
