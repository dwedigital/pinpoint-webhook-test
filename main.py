"""
This is a test application to receive webhooks from Pinpoint.
"""

import logging

from flask import Flask, abort, jsonify, render_template, request
from flask_cors import CORS, cross_origin

from verification import is_verified_request

logging.basicConfig(
    level=logging.INFO,
    filename="app.log",
    format="%(asctime)s - %(levelname)s - %(message)s",
)
logger = logging.getLogger(__name__)

app = Flask(__name__)

CORS(app)


@app.route("/")
def index():
    """
    This is the main route of the application.
    """
    return render_template("index.html")


@app.route("/webhook/<client>", methods=["POST"])
@cross_origin()
def webhook(client):
    """
    This is the webhook endpoint for the client.
    """
    if not is_verified_request(request):
        logger.error("Invalid HMAC signature for client: %s", client)
        abort(401, description="Invalid HMAC signature")

    # Proceed with your logic
    logger.info("Webhook received & verified for client: %s", client)
    return "Verified!", 200


if __name__ == "__main__":
    app.run(debug=True)
