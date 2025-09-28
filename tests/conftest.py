import os

import pytest

from src.lib.json_logging import configure_json_logging


@pytest.fixture(autouse=True)
def _setup_logging():
    # Default to INFO for tests; can be overridden per test
    os.environ.setdefault("LOG_LEVEL", "INFO")
    configure_json_logging()
    yield
