# Ground Receiver Pin Configuration

## ESP32 ↔ SX1278

| SX1278 signal | ESP32 GPIO |
|---|---:|
| NSS / SS | GPIO 5 |
| RESET | GPIO 14 |
| DIO0 | GPIO 2 |
| SCK | GPIO 18 |
| MISO | GPIO 19 |
| MOSI | GPIO 23 |

The pin mapping above is the documented ground-receiver configuration. Confirm wiring against the actual board before powering the radio.

## LoRa settings

- Frequency: 433 MHz
- Spreading factor: 7
- Bandwidth: 125 kHz
- Coding rate: 4/5
- CRC: enabled
- TX power setting: 17 dBm
