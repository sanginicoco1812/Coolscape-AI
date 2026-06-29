"""
PythonAnywhere WSGI entrypoint for the HEATSHIELD INDIA FastAPI backend.

In the PythonAnywhere WSGI configuration file, add the project root to
sys.path and expose this module's `application` object.
"""

import sys
from pathlib import Path

from a2wsgi import ASGIMiddleware


PROJECT_ROOT = Path(__file__).resolve().parent.parent

if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from backend.main import app as fastapi_app  # noqa: E402


application = ASGIMiddleware(fastapi_app)
