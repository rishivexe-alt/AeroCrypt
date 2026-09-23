# AeroCrypt Architecture

The architecture diagram shows:

1. BMP280 / MPU6050 / GPS telemetry
2. UAV ESP32 processing
3. AES-128-GCM protection
4. SX1278 433 MHz LoRa transmission
5. Ground SX1278 reception
6. ESP32 ground-side authentication/decryption
7. USB serial
8. Python monitoring/parser layer
9. Streamlit dashboard

The separate Industrial IoT architecture containing MQTT, gas/distance sensing, SQLite, and the Industrial IoT IDS is intentionally not part of AeroCrypt.
