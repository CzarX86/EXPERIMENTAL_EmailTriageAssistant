import os
import uuid

import requests


BASE_URL = os.environ.get("API_BASE_URL", "http://127.0.0.1:8765")


def _auth_headers():
    token = os.environ.get("API_BEARER", str(uuid.uuid4()))
    return {"Authorization": f"Bearer {token}"}


def test_ingest_m365_accepts_request():
    payload = {"source": "m365", "options": {}}
    try:
        resp = requests.post(f"{BASE_URL}/ingest", json=payload, headers=_auth_headers(), timeout=2)
    except Exception:
        assert False, "API server not running"
    assert resp.status_code == 202
