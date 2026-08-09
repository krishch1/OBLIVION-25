import hashlib
import json
import base64
from datetime import datetime

from fastapi import FastAPI, status, HTTPException
from pydantic import BaseModel

# --- Real Modules (Imported from the 'tools' directory) ---
# These replace the placeholder classes from Day 1.
from tools.signing import sign_helper
from tools.pdf import pdf_generator
from tools.qr import qr_generator

# --- Pydantic Models ---

class WipeLog(BaseModel):
    device_id: str
    wipe_method: str
    start_time: str
    end_time: str
    pre_wipe_hash: str
    post_wipe_hash: str

class IssueResponse(BaseModel):
    message: str = "Certificate issued successfully."
    certificate_hash: str
    signature: str
    pdf_base64: str
    qr_code_base64: str

# In-memory database for the demo
certificate_db = {}

# --- FastAPI App ---

app = FastAPI(
    title="Oblivion Backend API",
    description="API for secure data wipe certification.",
    version="0.1.0"
)

@app.get("/health", tags=["Monitoring"])
def get_health():
    """Check if the API is running."""
    return {"status": "OK", "timestamp": datetime.utcnow().isoformat()}

@app.post("/oblivion/issue", response_model=IssueResponse, status_code=status.HTTP_201_CREATED, tags=["Certification"])
def issue_certificate(log: WipeLog):
    """
    Receives wipe log data, signs it, generates PDF/QR assets, and issues a certificate.
    """
    log_json = json.dumps(log.dict(), sort_keys=True)
    signature = sign_helper.sign_data(log_json)
    certificate_hash = hashlib.sha256(signature.encode('utf-8')).hexdigest()

    certificate_data = {
        "wipe_log": log.dict(),
        "signature": signature,
        "issued_at": datetime.utcnow().isoformat(),
        "certificate_hash": certificate_hash
    }

    verification_url = f"/oblivion/verify/{certificate_hash}"
    qr_bytes = qr_generator.generate_qr_code(verification_url)
    qr_code_base64 = base64.b64encode(qr_bytes).decode('utf-8')

    pdf_bytes = pdf_generator.generate_pdf(certificate_data)
    pdf_base64 = base64.b64encode(pdf_bytes).decode('utf-8')

    certificate_db[certificate_hash] = certificate_data
    
    return {
        "certificate_hash": certificate_hash,
        "signature": signature,
        "pdf_base64": pdf_base64,
        "qr_code_base64": qr_code_base64
    }

@app.get("/oblivion/verify/{certificate_hash}", tags=["Certification"])
def verify_certificate(certificate_hash: str):
    """
    Verifies the integrity and authenticity of a stored certificate.
    """
    certificate = certificate_db.get(certificate_hash)
    if not certificate:
        raise HTTPException(status_code=404, detail="Certificate not found for the given hash.")

    original_log_json = json.dumps(certificate["wipe_log"], sort_keys=True)
    signature = certificate["signature"]
    is_valid = sign_helper.verify_signature(original_log_json, signature)

    if not is_valid:
        raise HTTPException(
            status_code=400,
            detail={
                "status": "INVALID",
                "message": "Signature verification failed. The certificate is not authentic."
            }
        )
    
    return {
        "status": "VALID",
        "message": "Certificate signature is authentic and data is verified.",
        "certificate": certificate
    }

