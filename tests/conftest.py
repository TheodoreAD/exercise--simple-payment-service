from simple_payment_service import api

import pytest


@pytest.fixture
def client():
    with api.app.test_client() as client:
        yield client
