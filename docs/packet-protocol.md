# AeroCrypt Packet Protocol

## LoRa frame

| Field | Size | Description |
|---|---:|---|
| Magic | 2 bytes | ASCII `AC` |
| Version | 1 byte | Protocol version `0x01` |
| Nonce | 12 bytes | 96-bit AES-GCM nonce |
| Ciphertext | Variable | Encrypted telemetry CSV bytes |
| Authentication tag | 16 bytes | GCM authentication tag |

The receiver validates the frame length, magic marker and version before authenticated decryption.

## Telemetry payload

Base schema:

```text
packet,temp,pressure,ax,ay,az,gx,gy,gz
```

Extended GPS schema:

```text
packet,temp,pressure,ax,ay,az,gx,gy,gz,latitude,longitude,satellites,hdop
```

Units are °C, hPa, g and °/s.

## Ground receiver serial records

```text
AEROCRYPT_SECURITY:VERIFIED,PACKET=2276
STREAMLIT_TELEMETRY:2276,28.49,918.08,0.004,0.058,1.009,0.42,1.06,0.08
AEROCRYPT_LINK,RSSI=-43,SNR=5.25
```

Telemetry is emitted only after the ESP32 receiver successfully authenticates and decrypts the packet.
