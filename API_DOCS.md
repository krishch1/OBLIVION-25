# Oblivion API Documentation

## Base URL
`http://localhost:8001`

---

### Issue Certificate
Generates a new wipe certificate, saves the PDF and QR code as files, and returns URLs to access them.

* **Endpoint:** `POST /issue`
* **Request Body:** A JSON object representing the wipe log.
  ```json
  {
    "device_id": "OBL-WIN11-DEMO-001",
    "timestamp": "2025-09-22T16:16:57.629Z",
    "pre_wipe_hash": "a1b2c3d4e5f6...",
    "post_wipe_hash": "f0e9d8c7b6a5..."
  }
  ```
* **Success Response (200 OK):** A JSON object containing certificate details and file URLs.
  ```json
  {
      "deviceId": "OBL-WIN11-DEMO-001",
      "timestamp": "2025-09-22T16:16:57.629Z",
      "preWipeHash": "a1b2c3d4e5f6...",
      "postWipeHash": "f0e9d8c7b6a5...",
      "pdfUrl": "/generated_files/some-uuid.pdf",
      "qrUrl": "/generated_files/some-uuid.png"
  }
  ```