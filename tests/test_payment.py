"""Unit tests"""

from datetime import datetime
from decimal import Decimal

import pytest

from simple_payment_service import payment


CARD_NUMBER_CASES = dict(
    VISA_PASS_LUHN=("4111 1111 1111 1111", "4111111111111111"),
    VISA_FAIL_LUHN=("4111 1111 1111 1112", None),
    MC_PASS_LUHN=("5500-0000-0000-0004", "5500000000000004"),
    MC_FAIL_LUHN=("5500 0000 0000 0005", None),
    FAIL_IIN=("0000 0000 0000 0000", None),
)
CARD_HOLDER_NAME_CASES = dict(
    PASS_STRICT=("John Smith", "JOHN SMITH"),
    PASS_SLOPPY=("  john smith ", "JOHN SMITH"),
    FAIL_DIGITS=("John Smith 25", None),
    FAIL_UNDERSCORE=("John_Smith", None),
    FAIL_UNICODE=("SØRENSEN", None),
)
CARD_EXPIRATION_CASES = dict(
    PASS=("09-2119", datetime(2119, 9, 1)),
    FAIL_EXPIRED=("09-2019", None),
    FAIL_DELIMITER=("09.2119", None),
    FAIL_FORMAT=("01-09-2119", None),
)
CARD_SECURITY_CODE_CASES = dict(
    PASS=("123", "123"), FAIL_LENGTH_SHORT=("12", None), FAIL_LENGTH_LONG=("1234", None), FAIL_LETTERS=("abc", None),
)
AMOUNT_CASES = dict(
    PASS_INTEGER=("123", Decimal(123)),
    PASS_DECIMAL=("123.45", Decimal("123.45")),
    PASS_EXPONENTIAL=("1.23e2", Decimal(123)),
    FAIL_NEGATIVE=("-123.45", None),
    FAIL_ZERO=("0", None),
    FAIL_LETTERS=("abc", None),
)


@pytest.mark.parametrize("value, expected", CARD_NUMBER_CASES.values(), ids=CARD_NUMBER_CASES.keys())
def test_try_parse_card_number(value, expected):
    result, message = payment.try_parse_card_number(value)
    assert result == expected


@pytest.mark.parametrize("value, expected", CARD_HOLDER_NAME_CASES.values(), ids=CARD_HOLDER_NAME_CASES.keys())
def test_try_parse_card_holder_name(value, expected):
    result, message = payment.try_parse_card_holder_name(value)
    assert result == expected


@pytest.mark.parametrize("value, expected", CARD_EXPIRATION_CASES.values(), ids=CARD_EXPIRATION_CASES.keys())
def test_try_parse_card_expiration(value, expected):
    result, message = payment.try_parse_card_expiration(value)
    assert result == expected


@pytest.mark.parametrize("value, expected", CARD_SECURITY_CODE_CASES.values(), ids=CARD_SECURITY_CODE_CASES.keys())
def test_try_parse_card_security_code(value, expected):
    result, message = payment.try_parse_card_security_code(value)
    assert result == expected


@pytest.mark.parametrize("value, expected", AMOUNT_CASES.values(), ids=AMOUNT_CASES.keys())
def test_try_parse_amount(value, expected):
    result, message = payment.try_parse_amount(value)
    assert result == expected
