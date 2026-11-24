# AeroCrypt System Architecture

The architecture diagram follows the telemetry path from the airborne sensor node to the ground monitoring application:

1. BMP280 environmental measurements and MPU6050 motion measurements are acquired by the airborne ESP32.
2. The ESP32 forms the structured telemetry payload and protects it with AES-128-GCM.
3. The SX1278 transmits the authenticated encrypted frame over the 433 MHz LoRa link.
4. The ground SX1278 forwards the received frame to the ground ESP32.
5. The ground ESP32 authenticates and decrypts the telemetry before serial forwarding.
6. The Python serial parser converts telemetry and radio diagnostics into dashboard data.
7. The Streamlit dashboard displays live metrics, charts, packet history and export controls.

The hardware architecture includes a UART interface for the NEO-6M GPS module and an extended telemetry schema for positional data.
