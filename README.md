# Project Oblivion: Certified Data Sanitization

**Project Oblivion** is a secure data sanitization and verification toolkit. It provides a robust mechanism to securely wipe data from storage devices and issues a cryptographically signed "Wipe Certificate" as a tamper-proof guarantee that the sanitization process was completed successfully. This project was developed for the **Smart India Hackathon (SIH) 2025**.

---

## The Problem: Data Remanence

Simply "deleting" a file doesn't remove it from a storage device. The data often remains and can be recovered by forensic tools. Project Oblivion solves this by using secure shredding techniques and providing a verifiable audit trail.

---

## Core Functionality

1. **Secure Wipe**: A shell script (`wipe_script.sh`) performs a secure, multi-pass overwrite of data on a target device or file.
    
2. **Forensic Proof**: The script calculates the SHA256 hash of the target before and after the wipe. A successful wipe is proven by the change in these hashes.
    
3. **Certificate Issuance**: The log of the wipe operation (including device details, timestamps, and hashes) is sent to a secure backend API.
    
4. **Digital Signature**: The backend uses an ECDSA key pair to digitally sign the wipe log, creating a JSON-based Wipe Certificate. This signature guarantees that the log has not been altered.
    
5. **Verification**: A public endpoint allows anyone to submit a Wipe Certificate and verify its digital signature, confirming its authenticity.
    

---

## Technical Stack

- **Backend**: Python, FastAPI
    
- **Cryptography**: Python `cryptography` library for ECDSA signatures
    
- **Scripting**: Bash (`shred`, `dd`, `sha256sum`)
    
- **Containerization**: Docker, Docker Compose
    
- **Document Generation**: FPDF2 for PDFs, QR Code
    

---

## Final Repository Structure

```text
oblivion-sih2025/
├── tools/
│   ├── pdf/
│   ├── qr/
│   └── signing/
├── oblivion/
│   ├── backend/
│   │   ├── app/
│   │   │   └── main.py
│   │   ├── Dockerfile
│   │   └── requirements.txt
│   ├── docs/
│   ├── frontend/
│   │   └── oblivion-ui/
│   └── scripts/
│       └── wipe_script.sh
└── docker-compose.yml
```

---

## Setup and Demo Flow

### 1. Prerequisites

- Docker
    
- Docker Compose
    
- An API client like `curl` or Postman
    

### 2. Run the Backend Service

Clone the repository and start the backend service using Docker Compose.

```bash
git clone https://github.com/thatguygarv/oblivion-sih2025.git
cd oblivion-sih2025
docker-compose up --build
```

The backend API will be running and accessible at `http://localhost:8004`.

---

## 3. Execute a Certified Wipe (Demo Steps)

This process simulates a secure wipe and the issuance of a certificate.

### A. Run the Wipe Script

Execute the `wipe_script.sh`. This script will create a temporary log file (`wipe_log.json`) in the same directory.

```bash
# Make the script executable
chmod +x ./oblivion/scripts/wipe_script.sh

# Run the script
./oblivion/scripts/wipe_script.sh
```

### B. Issue a Certificate

Use the generated `wipe_log.json` as the payload to call the `/issue` endpoint. This will return a signed certificate.

```bash
# Using curl to send the log to the backend
curl -X POST "http://localhost:8004/issue" \
  -H "Content-Type: application/json" \
  -d @wipe_log.json
```

### C. Verify the Certificate

The response from the `/issue` endpoint will contain a `log_hash`. Use this hash to call the verification endpoint to confirm the certificate's authenticity.

```bash
# Replace <log_hash_from_previous_step> with the actual hash
curl http://localhost:8004/verify/<log_hash_from_previous_step>
```

A successful verification will return:

```json
{"is_signature_valid": true}
```

---

## Notes & Security Considerations

- Always run wipe scripts with caution. Targeting the wrong device will cause irreversible data loss.
    
- Prefer hardware-backed key storage (HSM or secure enclave) for production ECDSA private keys.
    
- Keep logs and private keys access-controlled and encrypted at rest.
    
- Provide clear user prompts and confirmations in the frontend to avoid accidental wipes.
    

---
