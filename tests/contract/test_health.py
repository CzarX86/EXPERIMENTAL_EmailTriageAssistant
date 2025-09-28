import os
import uuid

import requests


BASE_URL = os.environ.get("API_BASE_URL", "http://127.0.0.1:8765")


def test_health_requires_auth_if_global_security():
    # OpenAPI sets global bearerAuth, but many health endpoints are exempt.
    # We'll assert that health is accessible without token (common practice) OR
    # if the implementation requires it, it must return 401 not 200 when missing.
    # This test is to formalize the contract: choose ONE and make it stable.
    try:
        resp = requests.get(f"{BASE_URL}/health", timeout=1)
    except Exception:
        # Server not running yet; tests are expected to fail before implementation.
        assert False, "API server not running"

    assert resp.status_code in (200, 401)


def test_health_ok_when_authorized_or_public():
    token = os.environ.get("API_BEARER", str(uuid.uuid4()))
    headers = {"Authorization": f"Bearer {token}"}
    try:
        resp = requests.get(f"{BASE_URL}/health", headers=headers, timeout=1)
    except Exception:
        assert False, "API server not running"

    # If health is public, 200 expected; if auth required, 200 with token
    assert resp.status_code == 200
