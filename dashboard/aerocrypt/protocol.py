"""Typed parsers for the AeroCrypt ESP32 ground-receiver serial protocol."""
from __future__ import annotations
from dataclasses import dataclass, asdict
from datetime import datetime, timezone
from typing import Optional

@dataclass
class TelemetryPacket:
    packet: int
    temperature_c: float
    pressure_hpa: float
    accel_x_g: float
    accel_y_g: float
    accel_z_g: float
    gyro_x_dps: float
    gyro_y_dps: float
    gyro_z_dps: float
    latitude: Optional[float] = None
    longitude: Optional[float] = None
    satellites: Optional[int] = None
    hdop: Optional[float] = None
    received_at: str = ""
    def to_dict(self) -> dict:
        return asdict(self)

@dataclass
class LinkMetrics:
    rssi_dbm: Optional[int] = None
    snr_db: Optional[float] = None

def parse_telemetry(payload: str) -> TelemetryPacket:
    """Parse the nine-field base or thirteen-field GPS-extended CSV payload."""
    fields = [v.strip() for v in payload.strip().split(",")]
    if len(fields) not in (9, 13):
        raise ValueError(f"Expected 9 or 13 telemetry fields; received {len(fields)}")
    try:
        values = dict(packet=int(fields[0]), temperature_c=float(fields[1]),
            pressure_hpa=float(fields[2]), accel_x_g=float(fields[3]),
            accel_y_g=float(fields[4]), accel_z_g=float(fields[5]),
            gyro_x_dps=float(fields[6]), gyro_y_dps=float(fields[7]),
            gyro_z_dps=float(fields[8]))
        if len(fields) == 13:
            values.update(latitude=float(fields[9]), longitude=float(fields[10]),
                          satellites=int(fields[11]), hdop=float(fields[12]))
    except (TypeError, ValueError) as exc:
        raise ValueError(f"Telemetry contains an invalid numeric field: {exc}") from exc
    packet = TelemetryPacket(**values)
    packet.received_at = datetime.now(timezone.utc).astimezone().isoformat(timespec="seconds")
    return packet

def parse_link_metrics(line: str) -> Optional[LinkMetrics]:
    if not line.startswith("AEROCRYPT_LINK,"):
        return None
    fields = {}
    for item in line.split(",")[1:]:
        if "=" in item:
            key, value = item.split("=", 1)
            fields[key.strip().upper()] = value.strip()
    try:
        return LinkMetrics(int(fields["RSSI"]) if "RSSI" in fields else None,
                           float(fields["SNR"]) if "SNR" in fields else None)
    except ValueError as exc:
        raise ValueError(f"Invalid LoRa link metric: {exc}") from exc

def parse_security_status(line: str) -> Optional[dict]:
    prefix = "AEROCRYPT_SECURITY:"
    if not line.startswith(prefix):
        return None
    status = line[len(prefix):].strip()
    return {"verified": status.startswith("VERIFIED"), "status": status,
            "received_at": datetime.now(timezone.utc).astimezone().isoformat(timespec="seconds")}
