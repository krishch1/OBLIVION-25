// oblivion/frontend/oblivion-ui/src/Certificate.jsx

import React, { useState } from 'react';
import './Certificate.css';

function Spinner() { return <div className="spinner"></div>; }

const API_BASE_URL = 'http://localhost:8001';

function Certificate() {
  const [certificateData, setCertificateData] = useState(null);
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState(null);

  const handleGenerateCertificate = async () => {
    setIsLoading(true);
    setError(null);
    setCertificateData(null);

    const wipeLogData = {
      "device_id": "OBL-WIN11-DEMO-001",
      "timestamp": new Date().toISOString(),
      "pre_wipe_hash": "a1b2c3d4e5f6a1b2c3d4e5f6a1b2c3d4e5f6a1b2c3d4e5f6a1b2c3d4e5f6",
      "post_wipe_hash": "f0e9d8c7b6a5f0e9d8c7b6a5f0e9d8c7b6a5f0e9d8c7b6a5f0e9d8c7b6a5"
    };

    try {
      const response = await fetch(`${API_BASE_URL}/issue`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(wipeLogData),
      });
      if (!response.ok) {
        throw new Error(`Network response was not ok: ${response.statusText}`);
      }
      const data = await response.json();
      setCertificateData(data);
    } catch (err) {
      setError(err.message);
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div className="page-container">
      <div className="controls">
        <button onClick={handleGenerateCertificate} className="generate-button" disabled={isLoading}>
          {isLoading ? <Spinner /> : 'Generate Wipe Certificate'}
        </button>
      </div>

      {error && <div className="error-message">{error}</div>}

      {certificateData && (
        <div className="certificate-container">
          <div className="certificate-header">
            <h1>Certificate of Data Wipe</h1>
          </div>
          <div className="certificate-body">
            <div className="detail-row">
              <span className="detail-label">Device ID:</span>
              <span className="detail-value">{certificateData.deviceId}</span>
            </div>
            <div className="detail-row">
              <span className="detail-label">Timestamp (UTC):</span>
              <span className="detail-value">{certificateData.timestamp}</span>
            </div>
            <div className="detail-row">
              <span className="detail-label">Post-Wipe Hash (SHA256):</span>
              <span className="detail-value code">{certificateData.postWipeHash.substring(0, 12)}...</span>
            </div>
          </div>
          <div className="certificate-footer">
            {/* The image src is now a direct URL to the backend */}
            <img src={`${API_BASE_URL}${certificateData.qrUrl}`} alt="Verification QR Code" className="qr-code" />

            {/* The download button is now a simple link */}
            <a href={`${API_BASE_URL}${certificateData.pdfUrl}`} download className="download-button">
              Download PDF
            </a>
          </div>
        </div>
      )}
    </div>
  );
}

export default Certificate;