import logging
import re
from dataclasses import dataclass
from datetime import datetime
from typing import Dict, Any, Optional, Tuple, List
from decimal import Decimal, InvalidOperation

logger = logging.getLogger(__name__)


@dataclass
class Payment:
    card_number: str
    card_holder: str
    card_expiration: datetime
    card_security_code: str
    amount: Decimal

    @classmethod
    def from_dict(cls, payload: Dict[str, Any]) -> Tuple[Optional["Payment"], List[str]]:
        try:
            card_number_raw = payload["CreditCardNumber"]
            card_holder_raw = payload["CardHolder"]
            card_expiration_raw = payload["ExpirationDate"]
            card_security_code_raw = payload["SecurityCode"]
            amount_raw = payload["Amount"]
        except KeyError as ex:
            return None, [str(ex)]

        args, messages = zip(
            try_parse_card_number(card_number_raw),
            try_parse_card_holder_name(card_holder_raw),
            try_parse_card_expiration(card_expiration_raw),
            try_parse_card_security_code(card_security_code_raw),
            try_parse_amount(amount_raw),
        )
        if not all(a is not None for a in args):
            return None, list(messages)

        return cls(*args), [""]


def try_parse_card_holder_name(value: str) -> Tuple[Optional[str], str]:
    result = value.strip().upper()
    success, message = validate_card_holder_name_upper(result)

    return (result, "") if success else (None, message)


def validate_card_holder_name_upper(value: str) -> Tuple[bool, str]:
    if not 2 <= len(value) <= 40:
        return False, "Invalid name length."

    for c in value:
        ordinal = ord(c)
        if not (ordinal == 32 or 65 <= ordinal <= 90):
            return False, "Invalid characters in name, expected ASCII letters or space."

    return True, ""


def try_parse_card_number(value: str) -> Tuple[Optional[str], str]:
    result = value.replace("-", " ").replace(" ", "")
    success, message = validate_card_number(result)

    return (result, "") if success else (None, message)


CARD_NUMBER_IIN_RANGES = [(4000, 4999), (5100, 5599), (2221, 2720)]
CARD_NUMBER_LENGTHS = [16]


def validate_card_number(value: str) -> Tuple[bool, str]:
    # https://en.wikipedia.org/wiki/Payment_card_number
    # [in the interest of time] considering only Visa and Mastercard

    if not len(value) in CARD_NUMBER_LENGTHS:
        return False, f"Invalid card number length, expected {CARD_NUMBER_LENGTHS}."

    iin_check_value = int(value[:4])

    if not any(lo <= iin_check_value <= hi for lo, hi in CARD_NUMBER_IIN_RANGES):
        return False, f"Invalid card IIN, expected {CARD_NUMBER_IIN_RANGES}."

    # https://en.wikipedia.org/wiki/Luhn_algorithm
    # verify checksum is divisible by 10
    #   (sum of odd digits) + (sum of (sums of digits of double each even digit))
    digits = [int(i) for i in value]
    odd = digits[1::2]
    even = digits[::2]

    checksum = sum(o + sum(divmod(2 * e, 10)) for o, e in zip(odd, even))

    if checksum % 10 != 0:
        return False, "Invalid card number, expected digits to verify Luhn algorithm."

    return True, ""


CARD_EXPIRATION_FORMAT = "%m-%Y"


def try_parse_card_expiration(value: str) -> Tuple[Optional[datetime], str]:
    try:
        result = datetime.strptime(value, CARD_EXPIRATION_FORMAT)
    except ValueError:
        return None, f"Invalid card expiration date format, expected {CARD_EXPIRATION_FORMAT}."

    if result < datetime.utcnow():
        return None, "Invalid card expiration date (in the past)."

    return result, ""


SECURITY_CODE_PATTERN = re.compile(r"^\d{3}$")


def try_parse_card_security_code(value: str) -> Tuple[Optional[str], str]:
    if not SECURITY_CODE_PATTERN.match(value):
        return None, f"Invalid card security code, expected {SECURITY_CODE_PATTERN.pattern}."

    return value, ""


def try_parse_amount(value: str) -> Tuple[Optional[Decimal], str]:
    try:
        result = Decimal(value)
    except InvalidOperation:
        return None, "Invalid amount format, expected decimal."
    if result <= 0:
        return None, "Invalid amount, expected positive."

    return result, ""
