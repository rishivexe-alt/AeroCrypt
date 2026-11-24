# Operation Guide

## Dashboard

1. Install Python 3.10 or newer.
2. Create and activate a virtual environment.
3. Install `dashboard/requirements.txt`.
4. Run `streamlit run dashboard/app.py` from the repository root.
5. Choose Demo mode to explore the dashboard, or Serial mode to connect the ground ESP32.
6. Select the receiver's serial port at 115200 baud and click Connect.
7. Monitor the latest packet, sensor values, motion plots, GPS fields, RSSI/SNR, packet history and CSV export.

## Firmware

Build each PlatformIO project from its respective directory. The transmitter and receiver must use matching key material and LoRa settings.

## Tests

```bash
cd dashboard
python -m unittest discover -s tests -v
```
