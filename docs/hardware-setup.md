# Hardware Setup

## Airborne node

- ESP32 development board
- BMP280 temperature/pressure sensor (I²C)
- MPU6050 accelerometer/gyroscope (I²C)
- SX1278 433 MHz LoRa module (SPI)
- NEO-6M GPS module (UART interface for extended telemetry)
- UAV power distribution matched to the aircraft build

## Ground station

- ESP32 development board
- SX1278 433 MHz LoRa module
- USB connection to the monitoring computer

## Ground radio pin mapping

| SX1278 | ESP32 |
|---|---:|
| NSS / SS | GPIO 5 |
| RESET | GPIO 14 |
| DIO0 | GPIO 2 |
| SCK | GPIO 18 |
| MISO | GPIO 19 |
| MOSI | GPIO 23 |

## Radio profile

- Frequency: 433 MHz
- Spreading factor: 7
- Bandwidth: 125 kHz
- Coding rate: 4/5
- CRC: enabled
- TX power setting: 17 dBm

Verify board pinout, antenna connection and module supply requirements before powering the radio.
