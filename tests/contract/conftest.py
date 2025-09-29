import os
import pytest


@pytest.fixture(scope="session", autouse=True)
def _contract_env_only():
    """Ensure contract tests see BASE_URL if root didn't set it.

    Root-level tests/conftest.py is responsible for starting the API server
    and setting API_BASE_URL/API_BEARER. This is a no-op safety net to avoid
    starting duplicate servers here.
    """
    os.environ.setdefault("API_BEARER", "testtoken")
    os.environ.setdefault("API_BASE_URL", os.environ.get("API_BASE_URL", "http://127.0.0.1:8765"))
    yield
