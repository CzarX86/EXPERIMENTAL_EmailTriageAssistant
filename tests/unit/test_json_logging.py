import json
import logging

from src.lib.json_logging import configure_json_logging


def test_configure_json_logging_outputs_json(capfd):
    configure_json_logging(level="DEBUG")
    logging.getLogger(__name__).info("hello", extra={"foo": "bar"})
    out, err = capfd.readouterr()
    assert err == ""
    assert out.strip() != ""
    payload = json.loads(out.strip())
    assert payload["level"] == "INFO"
    assert payload["msg"] == "hello"
    assert payload["foo"] == "bar"
    assert "ts" in payload
