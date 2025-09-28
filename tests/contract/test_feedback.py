import os
import uuid

import requests


BASE_URL = os.environ.get("API_BASE_URL", "http://127.0.0.1:8765")


def test_feedback_accepts():
    token = os.environ.get("API_BEARER", str(uuid.uuid4()))
    headers = {"Authorization": f"Bearer {token}"}
    payload = {"email_id": "test-email-1", "type": "approve", "corrected_text": None}
    try:
        resp = requests.post(f"{BASE_URL}/feedback", json=payload, headers=headers, timeout=2)
    except Exception:
        assert False, "API server not running"
    assert resp.status_code == 200
