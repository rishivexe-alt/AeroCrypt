# Security Policy

AeroCrypt uses AES-128-GCM authenticated encryption. The ground receiver forwards telemetry only after authentication-tag verification. LoRa CRC supports radio-link error detection; AES-GCM provides payload confidentiality, integrity and authenticity.

The key in the public firmware is a development/demo key. Use securely provisioned key material for deployment. Do not commit operational keys, credentials, private identifiers or sensitive telemetry logs. For security reports, contact the repository maintainer privately through the GitHub profile contact channel.
