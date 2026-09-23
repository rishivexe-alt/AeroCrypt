# Security Policy

## Public Repository Rules

Never commit real credentials or secrets.

Do not publish:

- AES keys used for real deployments
- Wi-Fi passwords
- MQTT credentials
- API tokens
- private keys
- private IP addresses
- personal identifiers
- private logs

The cryptographic material in public examples is placeholder material only.

## Reporting

If a secret is accidentally committed, remove it from the working tree and rotate/revoke the affected credential before publishing again.
