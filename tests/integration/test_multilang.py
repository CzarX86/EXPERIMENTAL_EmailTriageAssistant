import os
import uuid

import requests


BASE_URL = os.environ.get("API_BASE_URL", "http://127.0.0.1:8765")
TOKEN = os.environ.get("API_BEARER", str(uuid.uuid4()))
HEADERS = {"Authorization": f"Bearer {TOKEN}"}


def test_multilang_preferred_language_override_placeholder():
    email_id = "ml-email-1"
    # Future: pass preferred language via header or payload; here we assert basic success
    r = requests.post(f"{BASE_URL}/suggest/{email_id}", headers=HEADERS, timeout=2)
    assert r.status_code == 200
    s = r.json()
    assert "text" in s
