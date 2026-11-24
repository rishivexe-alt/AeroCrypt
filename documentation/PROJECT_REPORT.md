# AeroCrypt — Project Report

## 1. Project overview

AeroCrypt is an AES-128-GCM secured long-range UAV telemetry and ground-monitoring system. It is designed to collect environmental and motion measurements on an airborne embedded node, protect the telemetry with authenticated encryption, transmit the encrypted data over a 433 MHz LoRa link, and present authenticated measurements at a remote ground station.

The project combines embedded systems, sensor interfacing, cryptography, wireless communication, serial data acquisition, Python processing and interactive visualization in one end-to-end engineering platform.

## 2. Objectives

- Acquire temperature, atmospheric pressure, acceleration and angular-velocity measurements from onboard sensors.
- Organize sensor readings into a structured telemetry packet.
- Apply AES-128-GCM authenticated encryption before radio transmission.
- Establish a long-range telemetry path using SX1278 LoRa transceivers.
- Authenticate and decrypt packets at the ground receiver.
- Forward accepted telemetry to a computer through USB serial.
- Visualize live sensor values, radio-link metrics, packet history and security state.
- Export collected telemetry for offline analysis.

## 3. Hardware architecture

### Airborne node

The ESP32 is the primary sensing and processing controller. The BMP280 communicates over I²C and supplies temperature and atmospheric pressure. The MPU6050 also uses I²C and supplies three-axis acceleration and angular velocity. The SX1278 radio communicates with the ESP32 over SPI. The hardware architecture also defines a UART interface for the NEO-6M GPS module and an extended telemetry schema for positional information.

### Ground station

A second ESP32 interfaces with an SX1278 LoRa module. It receives the encrypted radio frame, validates its framing, performs AES-GCM authenticated decryption, and forwards accepted telemetry through USB serial at 115200 baud. The host computer runs the AeroCrypt dashboard.

## 4. Wireless communication and packet design

The radio profile uses 433 MHz, spreading factor 7, 125 kHz signal bandwidth, coding rate 4/5 and LoRa CRC. The binary application frame contains:

1. Two-byte `AC` magic marker.
2. One-byte protocol version.
3. A 12-byte AES-GCM nonce.
4. Variable-length ciphertext.
5. A 16-byte authentication tag.

The base plaintext telemetry schema is:

```text
packet,temp,pressure,ax,ay,az,gx,gy,gz
```

An extended schema appends latitude, longitude, satellite count and HDOP fields.

## 5. Cryptographic processing

The airborne ESP32 creates a fresh 96-bit nonce using the ESP32 hardware random-number generator. The payload is encrypted using AES-128-GCM and transmitted together with its nonce and authentication tag. At the ground station, the receiver extracts the cryptographic fields and invokes the GCM authenticated-decryption routine. The receiver emits the plaintext telemetry only when tag verification succeeds. Security events are represented on the serial interface using the `AEROCRYPT_SECURITY` message family.

## 6. Ground-station software

The Python/Streamlit application provides a monitoring interface for both demonstration and live serial input. Its protocol module converts the receiver's serial records into typed telemetry and link-metric objects. The serial adapter discovers available ports and reads line-oriented receiver output. The Streamlit application displays receiver state, security verification, latest packet information, temperature, pressure, acceleration, gyroscope values, RSSI, SNR, GPS fields, time-series charts and a packet-history table. Captured data can be downloaded as CSV.

## 7. Software organization

- `firmware/uav_transmitter/` contains the ESP32 airborne firmware and PlatformIO build configuration.
- `firmware/ground_receiver/` contains the ESP32 receiver firmware and PlatformIO build configuration.
- `dashboard/aerocrypt/protocol.py` defines telemetry models and serial protocol parsers.
- `dashboard/aerocrypt/serial_reader.py` handles serial-port discovery and line collection.
- `dashboard/app.py` implements the interactive monitoring interface.
- `dashboard/tests/` contains parser and message-validation tests.
- `hardware/` documents component selection, pin mapping, power and interfaces.
- `docs/` contains setup, operation, packet and security documentation.
- `screenshots/` contains hardware and monitoring-dashboard visuals.

## 8. Experimental observations

The captured dashboard sessions show authenticated AES-128-GCM telemetry, live environmental and inertial measurements, packet sequence information and LoRa link diagnostics. Example readings include a temperature near 28.49 °C, pressure near 918.08 hPa, acceleration components near 0.004 g, 0.058 g and 1.009 g, and RSSI values around -43 dBm in a captured state. A separate reported field test recorded approximately 500 m line-of-sight communication and approximately 93% packet delivery for its tested configuration.

## 9. Engineering outcome

AeroCrypt brings together embedded sensing, packet framing, authenticated encryption, long-range wireless communication, ground-side cryptographic verification and live monitoring. The result is a practical foundation for secure UAV telemetry, remote asset monitoring, environmental sensing and other distributed systems where data must travel across a wireless channel before being consumed by a monitoring application.
