"""
This is a test application to receive webhooks from Pinpoint.
"""

import logging

from flask import Flask, abort, render_template, request

from verification import is_verified_request

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


@app.route("/webhook/<client>", methods=["POST"])
def webhook(client):
    """
    This is the webhook endpoint for the client.
    """
    event_type = request.json.get("event")
    if not is_verified_request(request):
        logger.error(
            "Invalid HMAC signature for client: %s event: %s", client, event_type
        )
        abort(401, description="Invalid HMAC signature")

    # Proceed with your logic
    logger.info(
        "Webhook received & verified for client: %s event: %s", client, event_type
    )
    return "Verified!", 200


if __name__ == "__main__":
    app.run(debug=True)
