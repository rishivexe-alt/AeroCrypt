# Implementation Status

## Verified / Audited

The development audit established the following ground-side implementation:

```text
SX1278 LoRa RX
→ AES-128-GCM authentication/decryption on ESP32
→ clean USB serial telemetry
→ Python telemetry parser
→ Streamlit session-state history
→ charts/table/CSV export
```

The audited source tree contained:

- `Blackbox/Blackbox.ino` — ESP32 ground receiver
- `Dashboard/receiver_dashboard.py` — Streamlit dashboard
- `requirements.txt`
- legacy `receiver.py`
- legacy `ground_data.csv`

## Public ZIP Status

This public ZIP contains:

- a public-safe ground receiver implementation aligned with the documented AeroCrypt architecture
- a public-safe UAV transmitter baseline/reference
- dashboard requirements and documentation
- screenshots
- architecture documentation
- the professional project report

The original transmitter firmware was not part of the audited source tree. The included transmitter file is therefore explicitly labeled a **baseline/reference implementation**, not the original audited transmitter source.

The original dashboard source was not available as raw source bytes in the artifacts used for this ZIP. No fabricated dashboard implementation is included.

## Data Persistence

The demonstrated dashboard uses Streamlit session-state history and manual CSV export. SQLite is not part of the demonstrated AeroCrypt ground pipeline.

## GPS

GPS fields are supported by the documented extended telemetry architecture, but the captured experiment reported GPS waiting for signal and the demonstrated basic telemetry packet contained nine fields without transmitted GPS coordinates.
