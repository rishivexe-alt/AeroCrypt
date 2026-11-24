# AeroCrypt File Index

| Path | Purpose |
|---|---|
| `README.md` | Project overview, architecture, quick start and feature summary |
| `firmware/uav_transmitter/` | ESP32 airborne sensing, packet formation, AES-GCM encryption and LoRa transmission |
| `firmware/ground_receiver/` | ESP32 LoRa reception, AES-GCM authentication/decryption and serial telemetry output |
| `dashboard/app.py` | Streamlit ground-station dashboard |
| `dashboard/aerocrypt/` | Telemetry and serial protocol modules |
| `dashboard/tests/` | Dashboard protocol tests |
| `hardware/` | Hardware components, pin mapping, power system and interfaces |
| `docs/` | Setup, operation, packet protocol and security documentation |
| `documentation/PROJECT_REPORT.md` | Project report |
| `documentation/architecture/` | System architecture diagram |
| `documentation/EXPERIMENTAL_RESULTS.md` | Captured telemetry and field-test observations |
| `screenshots/` | UAV hardware and dashboard screenshots |
| `samples/` | Example receiver serial output and telemetry payloads |
