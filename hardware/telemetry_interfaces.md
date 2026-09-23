# Telemetry Interfaces

## Sensor interfaces

- BMP280: I2C
- MPU6050: I2C
- NEO-6M GPS: UART in the extended architecture
- SX1278 LoRa: SPI

## Ground output

The ground ESP32 forwards accepted telemetry through USB serial at 115200 baud.

Basic telemetry format:

```text
packet,temp,pressure,ax,ay,az,gx,gy,gz
```

Extended format:

```text
packet,temp,pressure,ax,ay,az,gx,gy,gz,latitude,longitude,satellites,hdop
```
