# AeroCrypt — Secure UAV Telemetry and Monitoring System

AeroCrypt is a secure UAV telemetry prototype combining a 250-size FPV-style quadcopter platform, AES-128-GCM authenticated encryption, SX1278 LoRa communication at 433 MHz, an ESP32 ground receiver, and a Python/Streamlit monitoring layer.

## System Architecture

```text
UAV SENSORS
  BMP280 + MPU6050 + GPS
        │
        ▼
     UAV ESP32
        │
        ▼
   AES-128-GCM
        │
        ▼
   SX1278 LoRa TX
      433 MHz
        │
      LoRa
        │
        ▼
   SX1278 LoRa RX
        │
        ▼
 Ground ESP32
 AES-GCM Verify/Decrypt
        │
        ▼
   USB Serial
        │
        ▼
 Python Telemetry Parser
        │
        ▼
 Streamlit Dashboard
```

## Core Features

- AES-128-GCM authenticated encryption
- SX1278 LoRa telemetry at 433 MHz
- ESP32 ground-side cryptographic verification and decryption
- BMP280 temperature/pressure telemetry
- MPU6050 acceleration and gyroscope telemetry
- RSSI and SNR monitoring
- Packet counter and telemetry history
- Streamlit real-time visualization
- CSV telemetry export
- Public-safe configuration with no real credentials

## UAV Platform

- 250-size ZMR250/QAV250-type carbon-fiber frame
- 4 × 2200 KV brushless motors
- 4 × 30 A ESCs
- KK2.1.0 flight controller
- Basic radio transmitter/receiver
- 3S LiPo battery
- Recommended starting battery: 1500 mAh, 40C, XT60
- Expected flight time: approximately 4–6 minutes depending on final build and flight conditions

## Telemetry

The demonstrated basic telemetry format is:

```text
packet,temp,pressure,ax,ay,az,gx,gy,gz
```

A future/extended 13-field format may include:

```text
packet,temp,pressure,ax,ay,az,gx,gy,gz,latitude,longitude,satellites,hdop
```

GPS fields should only be described as experimentally available when they are actually transmitted and verified.

## Security

The ground receiver performs AES-128-GCM authentication and decryption before forwarding accepted telemetry to the monitoring layer.

Successful processing is reported through:

```text
AEROCRYPT_SECURITY:VERIFIED
```

Failed authentication is rejected.

### Public repository rule

The AES key contained in the public firmware is an **example placeholder only**. Never replace it with a real deployment key in a public repository.

Do not publish:

- real AES keys
- Wi-Fi passwords
- private IP addresses
- MQTT credentials
- API tokens
- private keys
- personal names or email addresses
- personal computer/device names
- private logs containing identifiers

## Ground Receiver

The public ground-receiver firmware is located at:

`firmware/ground_receiver/AeroCrypt_Ground_Receiver_PUBLIC.ino`

The demonstrated LoRa configuration is:

- Frequency: 433 MHz
- Spreading factor: SF7
- Bandwidth: 125 kHz
- Coding rate: 4/5
- CRC: enabled
- TX power setting: 17 dBm
- USB serial: 115200 baud

## UAV Transmitter

`firmware/uav_transmitter/AeroCrypt_UAV_Transmitter_PUBLIC_BASELINE.ino` is a **public-safe reference/baseline implementation** for the packet contract. It is not presented as the original audited transmitter source.

The original development audit established the ground-side implementation and documented that the transmitter firmware was not part of the audited source tree. See `documentation/IMPLEMENTATION_STATUS.md`.

## Dashboard

The demonstrated monitoring application provides:

- receiver connection status
- LoRa status
- AES-GCM security status
- latest packet
- temperature and pressure
- accelerometer X/Y/Z
- gyroscope X/Y/Z
- GPS status
- RSSI/SNR
- packet count
- telemetry history
- CSV export

The public package includes the dependency specification and screenshots. The original dashboard source was not available as a raw source file in the project artifacts used to assemble this public package, so no invented replacement is presented as the original implementation.

## Python Dependencies

```text
streamlit
pyserial
pandas
plotly
```

Install with:

```bash
pip install -r dashboard/requirements.txt
```

## Demonstrated Experimental Observations

Representative captured dashboard values include approximately:

- Temperature: 28.48 °C
- Pressure: 918.07 hPa
- RSSI: around -40 to -45 dBm in the captured session
- SNR: approximately -0.5 to 8 dB across captured packets
- Latest captured packet: #2321
- Packets received in the captured state: 52
- Security state: AES-128-GCM VERIFIED

A separate reported field test at approximately 500 m line-of-sight recorded about 93% packet delivery, approximately -60 dBm RSSI, and approximately 5 dB SNR under the tested configuration. These are single reported test conditions, not universal LoRa performance specifications.

## Important Architecture Correction

AeroCrypt does **not** use MQTT or SQLite in its demonstrated ground telemetry pipeline.

The verified ground-side flow is:

```text
LoRa RX
→ AES-128-GCM decrypt/authenticate on ESP32
→ USB serial
→ Python parser
→ Streamlit session history
→ charts/table/export
```

Telemetry history in the dashboard is maintained in Streamlit session state and can be manually exported as CSV.

## Documentation

- `documentation/AeroCrypt_Project_Report.pdf`
- `documentation/architecture/aerocrypt_system_architecture.png`
- `documentation/IMPLEMENTATION_STATUS.md`
- `documentation/EXPERIMENTAL_RESULTS.md`
- `documentation/PUBLIC_RELEASE_SCOPE.md`
- `hardware/`
- `screenshots/`

## Safety

Remove propellers during bench testing of motors and control electronics. Follow appropriate LiPo charging, storage, wiring, and flight-safety procedures. The flight battery is a high-current source and must be selected for the actual motor, ESC, propeller, and aircraft-weight configuration.

## Project Scope

AeroCrypt is documented as a secure UAV telemetry and monitoring prototype. It does not claim autonomous flight control, a machine-learning IDS, GPS mapping, or a universal radio-performance benchmark unless those features are separately implemented and experimentally validated.
