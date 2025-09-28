import os
import uuid

import requests


BASE_URL = os.environ.get("API_BASE_URL", "http://127.0.0.1:8765")


def test_export_returns_path():
    token = os.environ.get("API_BEARER", str(uuid.uuid4()))
    headers = {"Authorization": f"Bearer {token}"}
    try:
        resp = requests.post(f"{BASE_URL}/export", headers=headers, timeout=2)
    except Exception:
        assert False, "API server not running"
    assert resp.status_code == 200
    data = resp.json()
    assert "path" in data
