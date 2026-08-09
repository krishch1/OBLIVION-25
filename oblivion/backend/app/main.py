# oblivion/backend/app/main.py

import uuid
import json  # <<< ADD THIS IMPORT
from pathlib import Path
from fastapi import FastAPI, HTTPException
from fastapi.staticfiles import StaticFiles
from typing import Dict, Any
from fastapi.middleware.cors import CORSMiddleware

from tools.qr.qr_generator import generate_qr_code_file
from tools.pdf.pdf_generator import generate_pdf_file

app = FastAPI(title="Oblivion API")

STATIC_DIR = Path("generated_files")
STATIC_DIR.mkdir(exist_ok=True)

app.mount(f"/{STATIC_DIR}", StaticFiles(directory=STATIC_DIR), name="files")

origins = ["http://localhost:3000", "http://localhost:5173"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.post("/issue")
def issue_certificate(wipe_log: Dict[str, Any]):
    unique_id = uuid.uuid4()
    pdf_filename = f"{unique_id}.pdf"
    qr_filename = f"{unique_id}.png"

    pdf_path = STATIC_DIR / pdf_filename
    qr_path = STATIC_DIR / qr_filename

    log_hash = wipe_log.get("post_wipe_hash", "unknown_hash")

    # vvv THIS BLOCK IS THE ONLY CHANGE vvv
    # Instead of a fake URL, create a JSON string with the real data.
    qr_data_to_encode = {
        "status": "Verified by Oblivion",
        "deviceId": wipe_log.get("device_id"),
        "postWipeHash": log_hash
    }
    qr_data_string = json.dumps(qr_data_to_encode, indent=2)
    # ^^^ END OF CHANGE ^^^

    cert_data_for_pdf = {
        "Device ID": wipe_log.get("device_id"),
        "Timestamp": wipe_log.get("timestamp"),
        "Post-Wipe Hash": log_hash,
    }

    try:
        generate_pdf_file(cert_data_for_pdf, str(pdf_path))
        # Pass the new JSON string to the QR generator
        generate_qr_code_file(qr_data_string, str(qr_path))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to generate files: {e}")

    return {
        "deviceId": wipe_log.get("device_id"),
        "timestamp": wipe_log.get("timestamp"),
        "preWipeHash": wipe_log.get("pre_wipe_hash"),
        "postWipeHash": log_hash,
        "pdfUrl": f"/{STATIC_DIR}/{pdf_filename}",
        "qrUrl": f"/{STATIC_DIR}/{qr_filename}",
    }