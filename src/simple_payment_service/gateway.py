import logging
from dataclasses import dataclass, asdict
from time import sleep
from typing import Optional, Tuple
from decimal import Decimal

from .payment import Payment
from .fake_request import FakeError, send_fake_request

logger = logging.getLogger(__name__)


# in the interest of tests running quickly
RETRY_DELAY_SECONDS = 0.001


@dataclass
class Gateway:
    name: str
    url: str
    retry_count: int = 0
    retry_self: bool = False
    retry_other: Optional["Gateway"] = None
    min_amount: Decimal = Decimal(0)
    include_min_amount: bool = False
    max_amount: Optional[Decimal] = None
    include_max_amount: bool = False

    def is_amount_qualified(self, amount: Decimal) -> bool:
        respects_lower_bound = amount > self.min_amount or (self.include_min_amount and amount == self.min_amount)
        respects_upper_bound = (
            self.max_amount is None
            or amount < self.max_amount
            or (self.include_max_amount and amount == self.max_amount)
        )

        return respects_lower_bound and respects_upper_bound

    def try_perform_payment(self, payment: Payment) -> Tuple[bool, Optional["Gateway"]]:
        payload = asdict(payment)
        logger.info(f"Attempting payment {payload} with gateway {self.name}...")

        try:
            send_fake_request(self.url, payload)
            return True, self

        except FakeError:
            logger.info(f"Failed payment attempt with gateway {self.name}.")

        retry_gateway = self if self.retry_self else self.retry_other

        if retry_gateway is not None and retry_gateway.retry_perform_payment(payment, self.retry_count):
            return True, retry_gateway

        return False, None

    def retry_perform_payment(self, payment: Payment, retry_count: int) -> bool:
        payload = asdict(payment)
        for _ in range(retry_count):
            sleep(RETRY_DELAY_SECONDS)
            try:
                logger.info(f"Retrying payment {payload} with gateway {self.name}...")
                send_fake_request(self.url, payload)
                return True

            except FakeError:
                logger.info(f"Failed payment attempt with gateway {self.name}.")

        return False


CHEAP_GATEWAY = Gateway(
    name="Cheap", url="https://pay.cheapgate.com/api/route", min_amount=Decimal(0), max_amount=Decimal(20),
)
EXPENSIVE_GATEWAY = Gateway(
    name="Expensive",
    url="https://pay.expgate.com/api/route",
    retry_count=1,
    retry_other=CHEAP_GATEWAY,
    # used 20 instead of 21 as in the description to avoid the gap
    min_amount=Decimal(20),
    max_amount=Decimal(500),
    include_min_amount=True,
    include_max_amount=True,
)
PREMIUM_GATEWAY = Gateway(
    name="Premium", url="https://pay.premgate.com/api/route", retry_count=3, retry_self=True, min_amount=Decimal(500),
)
GATEWAYS = (CHEAP_GATEWAY, EXPENSIVE_GATEWAY, PREMIUM_GATEWAY)


def get_gateway_by_amount(amount: Decimal) -> Optional[Gateway]:
    for gateway in GATEWAYS:
        if gateway.is_amount_qualified(amount):
            return gateway

    return None


def get_first_gateway() -> Gateway:
    return GATEWAYS[0]
