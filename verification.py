"""
This module contains functions to verify the authenticity of a request from Pinpoint.
"""

import base64
import hashlib
import hmac
import os

import dotenv

dotenv.load_dotenv()

SIGNING_SECRET = os.getenv("SIGNING_SECRET")


def compute_hmac(body: bytes) -> str:
    """Compute Base64-encoded HMAC SHA256 of the request body."""
    digest = hmac.new(
        key=SIGNING_SECRET.encode("utf-8"), msg=body, digestmod=hashlib.sha256
    ).digest()
    return base64.b64encode(digest).decode("utf-8")


def is_verified_request(req) -> bool:
    """Compare computed HMAC with header in a timing-safe manner."""
    hmac_header = req.headers.get("PINPOINT-HMAC-SHA256")
    if not hmac_header:
        return False

    computed = compute_hmac(req.get_data())
    # Timing-safe comparison
    return hmac.compare_digest(computed, hmac_header)
