import os
import socket
import threading
import time
from contextlib import closing

import pytest
import requests

from src.lib.json_logging import configure_json_logging
from src.services.api import create_app


def _free_port() -> int:
    with closing(socket.socket(socket.AF_INET, socket.SOCK_STREAM)) as s:
        s.bind(("127.0.0.1", 0))
        s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        return int(s.getsockname()[1])


def pytest_sessionstart(session):
    """Start API server once for all tests so env is ready at import-time.

    We set API_BASE_URL/API_BEARER before any tests import globals like BASE_URL.
    If a server is already started (e.g., by another conftest), we skip.
    """
    if os.environ.get("API_SERVER_STARTED") == "1":
        return

    port = _free_port()
    os.environ.setdefault("API_PORT", str(port))
    os.environ.setdefault("API_BEARER", "testtoken")
    os.environ.setdefault("API_BASE_URL", f"http://127.0.0.1:{port}")

    app = create_app()

    def _run():
        app.run(host="127.0.0.1", port=port, debug=False, use_reloader=False, threaded=True)

    t = threading.Thread(target=_run, daemon=True)
    t.start()

    # Wait for server
    base = os.environ["API_BASE_URL"]
    deadline = time.time() + 5.0
    while time.time() < deadline:
        try:
            r = requests.get(f"{base}/health", timeout=0.5)
            if r.status_code in (200, 401):
                os.environ["API_SERVER_STARTED"] = "1"
                break
        except Exception:
            time.sleep(0.05)


@pytest.fixture(autouse=True)
def _setup_logging():
    # Default to INFO for tests; can be overridden per test
    os.environ.setdefault("LOG_LEVEL", "INFO")
    configure_json_logging()
    yield
