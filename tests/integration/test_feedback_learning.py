import os
import uuid

import requests


BASE_URL = os.environ.get("API_BASE_URL", "http://127.0.0.1:8765")
TOKEN = os.environ.get("API_BEARER", str(uuid.uuid4()))
HEADERS = {"Authorization": f"Bearer {TOKEN}"}


def test_feedback_improves_future_suggestions_placeholder():
    email_id = "fb-email-1"
    # Get a suggestion
    r1 = requests.post(f"{BASE_URL}/suggest/{email_id}", headers=HEADERS, timeout=2)
    assert r1.status_code == 200
    s1 = r1.json()

    # Send feedback (approve)
    r2 = requests.post(
        f"{BASE_URL}/feedback",
        json={"email_id": email_id, "type": "approve", "corrected_text": None},
        headers=HEADERS,
        timeout=2,
    )
    assert r2.status_code == 200

    # Get another suggestion; later we will assert learning effects
    r3 = requests.post(f"{BASE_URL}/suggest/{email_id}", headers=HEADERS, timeout=2)
    assert r3.status_code == 200
    s3 = r3.json()
    assert set(["email_id", "text"]) <= set(s3.keys())
