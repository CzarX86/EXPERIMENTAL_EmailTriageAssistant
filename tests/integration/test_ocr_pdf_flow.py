import os
import uuid

import requests


BASE_URL = os.environ.get("API_BASE_URL", "http://127.0.0.1:8765")
TOKEN = os.environ.get("API_BEARER", str(uuid.uuid4()))
HEADERS = {"Authorization": f"Bearer {TOKEN}"}


def test_ocr_pdf_flow():
    # For now, we simulate that an email with PDF/image was processed
    email_id = "pdf-email-1"
    # Suggest should still return text, implying OCR-parsed content could be considered
    r = requests.post(f"{BASE_URL}/suggest/{email_id}", headers=HEADERS, timeout=2)
    assert r.status_code == 200
    s = r.json()
    assert set(["email_id", "text"]) <= set(s.keys())
