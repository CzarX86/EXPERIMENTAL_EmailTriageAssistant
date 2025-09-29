from __future__ import annotations

import os
from datetime import datetime, timezone
from typing import Any

from flask import Flask, jsonify, request

from src.lib.json_logging import configure_json_logging


def create_app() -> Flask:
    configure_json_logging()
    app = Flask(__name__)

    # Simple Bearer token check; exempt /health
    @app.before_request
    def _auth_and_loopback_only():  # type: ignore[override]
        # Loopback-only: we'll bind to 127.0.0.1 when running. Here we defensively check remote_addr.
        ra = request.remote_addr or ""
        if ra not in ("127.0.0.1", "::1"):
            return ("Forbidden", 403)

        if request.path == "/health":
            return None

        auth = request.headers.get("Authorization", "")
        if not auth.startswith("Bearer "):
            return ("Unauthorized", 401)
        # For now, accept any non-empty bearer token. Later we will integrate Keychain.
        token = auth.removeprefix("Bearer ").strip()
        if not token:
            return ("Unauthorized", 401)
        return None

    @app.get("/health")
    def health():  # type: ignore[override]
        return ("OK", 200)

    @app.post("/ingest")
    def ingest():  # type: ignore[override]
        data: dict[str, Any] = request.get_json(silent=True) or {}
        source = data.get("source")
        if source not in {"m365", "imap", "mbox"}:
            return ("Bad Request", 400)
        return ("Accepted", 202)

    @app.post("/index")
    def index():  # type: ignore[override]
        return ("Accepted", 202)

    @app.post("/classify/<email_id>")
    def classify(email_id: str):  # type: ignore[override]
        now = datetime.now(timezone.utc).isoformat()
        # Return a stub classification
        return (
            jsonify(
                {
                    "email_id": email_id,
                    "label": "acao",
                    "confidence": 0.5,
                    "created_at": now,
                }
            ),
            200,
        )

    @app.post("/suggest/<email_id>")
    def suggest(email_id: str):  # type: ignore[override]
        now = datetime.now(timezone.utc).isoformat()
        return (
            jsonify({"email_id": email_id, "text": "stub reply", "created_at": now}),
            200,
        )

    @app.get("/explain/<email_id>")
    def explain(email_id: str):  # type: ignore[override]
        return (
            jsonify(
                {
                    "email_id": email_id,
                    "label": "acao",
                    "confidence": 0.5,
                    "key_factors": {
                        "keywords": [],
                        "vip": False,
                        "time_window": None,
                        "thread_activity": None,
                        "mentions": [],
                    },
                    "similar_emails": [],
                    "feedback_influence": [],
                }
            ),
            200,
        )

    @app.get("/search")
    def search():  # type: ignore[override]
        q = request.args.get("q")
        if not q:
            return ("Bad Request", 400)
        return (jsonify([]), 200)

    @app.post("/feedback")
    def feedback():  # type: ignore[override]
        data = request.get_json(silent=True) or {}
        if not data.get("email_id") or data.get("type") not in {"approve", "reject", "correct"}:
            return ("Bad Request", 400)
        return ("Accepted", 200)

    @app.post("/export")
    def export():  # type: ignore[override]
        return (jsonify({"path": "/tmp/bundle.enc"}), 200)

    @app.post("/import")
    def import_bundle():  # type: ignore[override]
        data = request.get_json(silent=True) or {}
        if not data.get("path"):
            return ("Bad Request", 400)
        return ("Accepted", 202)

    return app


def run() -> None:
    app = create_app()
    # Bind loopback only
    app.run(host="127.0.0.1", port=int(os.getenv("API_PORT", "8765")), debug=False, use_reloader=False, threaded=True)


if __name__ == "__main__":
    run()
