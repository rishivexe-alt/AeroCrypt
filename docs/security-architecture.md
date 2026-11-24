# Security Architecture

AeroCrypt uses AES-128-GCM authenticated encryption. The airborne node serializes the sensor payload, generates a 96-bit nonce using the ESP32 hardware random-number generator, encrypts the payload and appends the 128-bit GCM authentication tag.

The binary radio frame is `AC` magic bytes, protocol version, nonce, ciphertext and tag. The ground receiver validates framing, extracts cryptographic fields and performs GCM authenticated decryption. A packet that fails authentication is rejected and is not forwarded as telemetry.

The public firmware contains a development/demo key so both nodes can be built consistently. Use unique securely provisioned key material for deployment. Operational keys and credentials must never be committed to source control. A production deployment should also enforce replay freshness and authenticate relevant packet metadata as additional authenticated data.
