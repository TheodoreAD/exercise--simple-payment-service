import logging
from dataclasses import asdict

from flask import Flask, request, jsonify, json
from werkzeug.exceptions import HTTPException

from .payment import Payment
from .gateway import get_gateway_by_amount, get_first_gateway

logging.basicConfig()
logger = logging.getLogger("payserv")

app = Flask(__name__)


@app.errorhandler(HTTPException)
def handle_exception(e):
    """Return JSON instead of HTML for HTTP errors."""
    # start with the correct headers and status code from the error
    response = e.get_response()
    # replace the body with JSON
    response.data = json.dumps({"code": e.code, "name": e.name, "description": e.description})
    response.content_type = "application/json"

    return response


def start_app():
    logger.setLevel(logging.INFO)
    app.run()


def start_app_dev():
    logger.setLevel(logging.DEBUG)
    app.run(debug=True)


@app.route("/ProcessPayment", methods=["POST"])
def process_payment():
    try:
        payment, messages = Payment.from_dict(request.json)
    except ValueError:
        logger.exception("Failed to decode JSON payload.")
        return jsonify("Failed to decode JSON payload."), 400

    if payment is None:
        logger.error(f"Failed to parse payment payload: {messages}.")
        return jsonify({messages}), 400

    gateway = get_gateway_by_amount(payment.amount) or get_first_gateway()
    logger.info(f"Using gateway {asdict(gateway)}...")
    success, success_gateway = gateway.try_perform_payment(payment)

    if not success:
        return jsonify("Failed to process payment due to gateway connectivity issue."), 500

    return jsonify(f"Payment processed using {success_gateway.name} gateway."), 200
