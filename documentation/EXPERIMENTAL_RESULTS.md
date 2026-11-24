# Experimental Results

## Captured monitoring session

| Parameter | Captured observation |
|---|---:|
| Radio | SX1278 LoRa |
| Frequency | 433 MHz |
| Receiver | ESP32 |
| Cryptography | AES-128-GCM |
| Security state | AES-128-GCM VERIFIED |
| Example latest packet | #2276 / #2321 across captured views |
| Temperature | Approximately 28.49 °C |
| Pressure | Approximately 918.08 hPa |
| Acceleration Z | Approximately 1.009 g |
| Gyroscope Y | Approximately 1.06 °/s |
| RSSI | Approximately -43 dBm in a captured state |
| SNR | Approximately 0.25 dB in a captured state |
| GPS panel | Displays GPS acquisition status and positional fields |

## Reported line-of-sight field run

A field run at approximately 500 m line-of-sight recorded approximately 93% packet delivery, RSSI around -60 dBm and SNR around 5 dB under the tested configuration.

## Dashboard evidence

The repository includes captured views for the overall dashboard, environmental telemetry, accelerometer, gyroscope, packet history and security/GPS status in `screenshots/`.
