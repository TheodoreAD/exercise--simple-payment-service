"""Integration tests for API route(s), simulating server use."""

import pytest


SUCCESS_MESSAGE_CHEAP = "Payment processed using Cheap gateway."
SUCCESS_MESSAGE_EXPENSIVE = "Payment processed using Expensive gateway."
SUCCESS_MESSAGE_PREMIUM = "Payment processed using Premium gateway."
FAILURE_MESSAGE_FAKE_REQUEST = "Failed to process payment due to gateway connectivity issue."
CASES = dict(
    PASS_CHEAP_GATEWAY=(
        {
            "CreditCardNumber": "4111 1111 1111 1111",
            "CardHolder": "John Smith",
            "ExpirationDate": "06-2121",
            "SecurityCode": "333",
            "Amount": "16.21",
        },
        (SUCCESS_MESSAGE_CHEAP, FAILURE_MESSAGE_FAKE_REQUEST),
    ),
    PASS_EXPENSIVE_GATEWAY=(
        {
            "CreditCardNumber": "4111 1111 1111 1111",
            "CardHolder": "John Smith",
            "ExpirationDate": "09-2119",
            "SecurityCode": "123",
            "Amount": "116.21",
        },
        (SUCCESS_MESSAGE_EXPENSIVE, SUCCESS_MESSAGE_CHEAP, FAILURE_MESSAGE_FAKE_REQUEST),
    ),
    PASS_PREMIUM_GATEWAY=(
        {
            "CreditCardNumber": "4111 1111 1111 1111",
            "CardHolder": "John Smith",
            "ExpirationDate": "09-2119",
            "SecurityCode": "123",
            "Amount": "1116.21",
        },
        (SUCCESS_MESSAGE_PREMIUM, FAILURE_MESSAGE_FAKE_REQUEST),
    ),
)
REQUEST_COUNT = 1000


@pytest.mark.parametrize("value, expected", CASES.values(), ids=CASES.keys())
def test_process_payment(client, value, expected):
    # we expect both failed and successful responses, since the fake requests fail randomly
    # we look for the correct gateways based on retry strategy
    responses = [client.post("/ProcessPayment", json=value) for _ in range(REQUEST_COUNT)]
    response_messages = [r.get_json() for r in responses]
    assert set(response_messages) == set(expected)
