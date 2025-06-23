"""
This is a test application to receive webhooks and optionally verify them.
"""

import logging
import os
import subprocess
import sys
from parser import parse_logs

import dotenv
from flask import Flask, abort, jsonify, render_template, request

from verification import is_verified_request

dotenv.load_dotenv()

NGROK_URL = os.getenv("NGROK_URL")
PORT = "8000"

logging.basicConfig(
    level=logging.INFO,
    filename="app.log",
    format="%(asctime)s - %(levelname)s - %(message)s",
)
logger = logging.getLogger(__name__)

app = Flask(__name__)


@app.route("/")
def index():
    """
    This is the main route of the application.
    """
    return render_template("index.html")


@app.route("/signed_webhook/<client>", methods=["POST"])
def signed_webhook(client):
    """
    Route for testing signing and verification of webhooks
    """
    event_type = request.json.get("event")
    if not is_verified_request(request):
        logger.error(
            "SIGNED | Invalid HMAC signature | client: %s | event: %s",
            client,
            event_type,
        )
        abort(401, description="Invalid HMAC signature")

    # Proceed with your logic
    logger.info(
        "SIGNED | client: %s | event: %s",
        client,
        event_type,
    )
    return "Verified!", 200


@app.route("/unsigned_webhook/<client>", methods=["POST"])
def unsigned_webhook(client):
    """Route for testing unsigned webhook events"""
    event_type = request.json.get("event")
    logger.info("UNSIGNED | client: %s | event: %s", client, event_type)
    return "Verified!", 200


@app.route("/logs", methods=["GET"])
def get_logs():
    client_filter = request.args.get("client")
    event_filter = request.args.get("event")
    level_filter = request.args.get("level")

    logs = parse_logs()

    if client_filter:
        logs = [log for log in logs if log["client"] == client_filter]
    if event_filter:
        logs = [log for log in logs if log["event"] == event_filter]
    if level_filter:
        logs = [log for log in logs if log["level"] == level_filter]

    return jsonify({"data": logs})


if __name__ == "__main__":
    gunicorn_process = subprocess.Popen(
        ["gunicorn", "main:app", "--bind", f"0.0.0.0:{PORT}"]
    )
    ngrok_command = (
        ["ngrok", "http", f"--url={NGROK_URL}", f"{PORT}"]
        if NGROK_URL
        else ["ngrok", "http", f"{PORT}"]
    )
    ngrok_process = subprocess.Popen(ngrok_command, text=True)

    try:
        gunicorn_process.wait()
        ngrok_process.terminate()
    except KeyboardInterrupt:
        gunicorn_process.terminate()
        ngrok_process.terminate()
        sys.exit(0)
