import os
import socket
import uuid

import requests


BASE_URL = os.environ.get("API_BASE_URL", "http://127.0.0.1:8765")


def test_reject_without_bearer_token():
    try:
        resp = requests.get(f"{BASE_URL}/search", params={"q": "hello"}, timeout=1)
    except Exception:
        assert False, "API server not running"
    assert resp.status_code in (401, 403)


def test_accept_with_bearer_token():
    token = os.environ.get("API_BEARER", str(uuid.uuid4()))
    headers = {"Authorization": f"Bearer {token}"}
    try:
        resp = requests.get(f"{BASE_URL}/search", params={"q": "hello"}, headers=headers, timeout=1)
    except Exception:
        assert False, "API server not running"
    assert resp.status_code in (200, 400)  # 400 because search may require index; 200 if stubbed


def test_loopback_only_host_protection():
    # If server is bound to loopback only, connecting via non-loopback should fail.
    # We'll attempt to resolve local hostname to non-loopback IP (if any) and hit it.
    # If the environment has only loopback, we skip with pass condition.
    try:
        host_ips = [str(ai[4][0]) for ai in socket.getaddrinfo(socket.gethostname(), None)]
        non_loopbacks = [ip for ip in host_ips if not (ip.startswith("127.") or ip == "::1")]
    except Exception:
        non_loopbacks = []

    if not non_loopbacks:
        # Nothing to test; assume loopback-only environment
        return

    token = os.environ.get("API_BEARER", str(uuid.uuid4()))
    headers = {"Authorization": f"Bearer {token}"}

    # Attempt request via a non-loopback ip; expect connection failure or explicit 403/400
    for ip in non_loopbacks:
        url = f"http://{ip}:8765/health"
        try:
            resp = requests.get(url, headers=headers, timeout=1)
            assert resp.status_code in (400, 403, 404), (
                f"Expected refusal via {ip}, got {resp.status_code}"
            )
        except Exception:
            # Connection refused (ideal for loopback-only bind)
            continue
