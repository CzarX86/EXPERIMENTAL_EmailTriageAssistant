import os
import uuid

import requests


BASE_URL = os.environ.get("API_BASE_URL", "http://127.0.0.1:8765")
TOKEN = os.environ.get("API_BEARER", str(uuid.uuid4()))
HEADERS = {"Authorization": f"Bearer {TOKEN}"}


def test_flow_ingest_classify_suggest_happy_path():
    # Ingest
    r = requests.post(f"{BASE_URL}/ingest", json={"source": "m365", "options": {}}, headers=HEADERS, timeout=2)
    assert r.status_code == 202

    # Classify
    email_id = "flow-email-1"
    r = requests.post(f"{BASE_URL}/classify/{email_id}", headers=HEADERS, timeout=2)
    assert r.status_code == 200
    c = r.json()
    assert set(["email_id", "label", "confidence", "created_at"]) <= set(c.keys())

    # Suggest
    r = requests.post(f"{BASE_URL}/suggest/{email_id}", headers=HEADERS, timeout=2)
    assert r.status_code == 200
    s = r.json()
    assert set(["email_id", "text", "created_at"]) <= set(s.keys())
