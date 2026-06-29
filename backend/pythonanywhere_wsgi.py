"""
PythonAnywhere WSGI entrypoint for the HEATSHIELD INDIA backend.

PythonAnywhere's free hosting serves WSGI apps directly. This wrapper keeps the
same prediction logic as the FastAPI app without requiring an ASGI bridge.
"""

import json
import sys
from pathlib import Path

from pydantic import ValidationError


PROJECT_ROOT = Path(__file__).resolve().parent.parent

if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from backend.main import PredictionInput, health_check, predict_temperature  # noqa: E402


CORS_HEADERS = [
    ("Access-Control-Allow-Origin", "*"),
    ("Access-Control-Allow-Methods", "GET, POST, OPTIONS"),
    ("Access-Control-Allow-Headers", "Content-Type"),
]


def json_response(start_response, status, payload):
    body = json.dumps(payload).encode("utf-8")
    headers = [
        ("Content-Type", "application/json"),
        ("Content-Length", str(len(body))),
        *CORS_HEADERS,
    ]
    start_response(status, headers)
    return [body]


def read_json_body(environ):
    try:
        length = int(environ.get("CONTENT_LENGTH") or 0)
    except ValueError:
        length = 0

    raw_body = environ["wsgi.input"].read(length) if length else b"{}"
    return json.loads(raw_body.decode("utf-8"))


def application(environ, start_response):
    method = environ.get("REQUEST_METHOD", "GET").upper()
    path = environ.get("PATH_INFO", "/")

    if method == "OPTIONS":
        start_response("204 No Content", CORS_HEADERS)
        return [b""]

    if method == "GET" and path == "/":
        return json_response(start_response, "200 OK", health_check())

    if method == "POST" and path == "/predict":
        try:
            payload = read_json_body(environ)
            data = PredictionInput(**payload)
            result = predict_temperature(data)
            status = "200 OK" if result.get("status") == "success" else "400 Bad Request"
            return json_response(start_response, status, result)
        except (json.JSONDecodeError, ValidationError) as exc:
            return json_response(
                start_response,
                "400 Bad Request",
                {"status": "error", "message": str(exc)},
            )
        except Exception as exc:
            return json_response(
                start_response,
                "500 Internal Server Error",
                {"status": "error", "message": str(exc)},
            )

    return json_response(
        start_response,
        "404 Not Found",
        {"status": "error", "message": "Endpoint not found"},
    )
