# AeroCrypt Ground Monitoring Dashboard

The Streamlit application reads the ESP32 ground receiver's USB serial output, parses authenticated telemetry and link diagnostics, and renders a live monitoring console.

## Run

```bash
python -m pip install -r requirements.txt
streamlit run app.py
```

## Input modes

- **Demo mode** — generated telemetry for dashboard walkthroughs.
- **Serial mode** — live line-oriented records from the ESP32 receiver at 115200 baud.

## Modules

- `aerocrypt/protocol.py` — telemetry data model and serial protocol parsers.
- `aerocrypt/serial_reader.py` — serial port discovery and line collection.
- `app.py` — Streamlit interface, plots, packet history and CSV export.
- `tests/test_protocol.py` — parser and input-validation tests.
