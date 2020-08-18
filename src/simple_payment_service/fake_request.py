import logging
from random import randint
from typing import Any

logger = logging.getLogger(__name__)


class FakeError(Exception):
    pass


def send_fake_request(url: str, payload: Any) -> None:
    logger.info(f"Sending request data {payload} to {url}...")

    if randint(1, 3) == 1:
        raise FakeError(f"Failed sending request data {payload} to {url}.")

    logger.info(f"Response code from {url}: 200.")
