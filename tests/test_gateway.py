"""Unit tests"""

from decimal import Decimal

import pytest

from simple_payment_service import gateway

AMOUNT_CASES = dict(
    CHEAP_FAIL_LOWER_BOUND=(0, None),
    CHEAP_PASS_RANDOM=(10, gateway.CHEAP_GATEWAY),
    EXPENSIVE_PASS_LOWER_BOUND=(20, gateway.EXPENSIVE_GATEWAY),
    EXPENSIVE_PASS_RANDOM=(100, gateway.EXPENSIVE_GATEWAY),
    EXPENSIVE_PASS_UPPER_BOUND=(500, gateway.EXPENSIVE_GATEWAY),
    PREMIUM_PASS_RANDOM=(1000, gateway.PREMIUM_GATEWAY),
)


@pytest.mark.parametrize("value, expected", AMOUNT_CASES.values(), ids=AMOUNT_CASES.keys())
def test_is_amount_qualified(value, expected):
    assert gateway.get_gateway_by_amount(Decimal(value)) is expected
