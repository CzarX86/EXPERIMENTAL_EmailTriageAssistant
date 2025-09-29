import os
import uuid

import requests


BASE_URL = os.environ.get("API_BASE_URL", "http://127.0.0.1:8765")
TOKEN = os.environ.get("API_BEARER", str(uuid.uuid4()))
HEADERS = {"Authorization": f"Bearer {TOKEN}"}


def test_semantic_search_returns_results_array():
    r = requests.get(f"{BASE_URL}/search", params={"q": "budget"}, headers=HEADERS, timeout=2)
    assert r.status_code == 200
    assert isinstance(r.json(), list)
