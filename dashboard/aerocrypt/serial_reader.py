"""Serial discovery and line-oriented reads for the AeroCrypt ground receiver."""
from __future__ import annotations
import serial
from serial.tools import list_ports

def available_ports() -> list[str]:
    return [port.device for port in list_ports.comports()]

def open_receiver(port: str, baudrate: int = 115200) -> serial.Serial:
    return serial.Serial(port=port, baudrate=baudrate, timeout=0.05)

def read_available_lines(connection: serial.Serial, max_lines: int = 80) -> list[str]:
    lines = []
    for _ in range(max_lines):
        raw = connection.readline()
        if not raw:
            break
        lines.append(raw.decode("utf-8", errors="replace").strip())
    return lines
