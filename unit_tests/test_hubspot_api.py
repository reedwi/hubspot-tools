import logging

import pytest

from hubspot_tools.api import TokenAuthenticator, API
from hubspot_tools.errors import HubspotInvalidToken
from hubspot_tools.constants import PRIVATE_APP_CREDENTIALS

logger = logging.getLogger("unittest_api")


@pytest.fixture(name="valid_credential")
def valid_credential() -> str:
    return "pat-na1-8g8g8g8g-b868-4273-97e5-095760ea417f"  # Not actually valid, but built in correct structure


@pytest.fixture(name="too_short_credential")
def too_short_credential() -> str:
    return "pat-na1-8g8g8g8g-b868-4273-97e5-095760ea4"


@pytest.fixture(name="too_long_credential")
def too_long_credential() -> str:
    return "pat-na1-8g8g8g8g-b868-4273-97e5-095760ea4"


@pytest.fixture(name="non_match_credential")
def non_match_credential() -> str:
    return "pac-na1-8g8g8g8g-b868-4273-97e5-095760ea417f"


def test_valid_token(valid_credential: str):
    token_auth = TokenAuthenticator(token=valid_credential)
    assert token_auth.token


def test_too_short_credential(too_short_credential: str):
    with pytest.raises(HubspotInvalidToken):
        TokenAuthenticator(token=too_short_credential)


def test_too_long_credential(too_long_credential: str):
    with pytest.raises(HubspotInvalidToken):
        TokenAuthenticator(token=too_long_credential)


def test_non_match_credential(non_match_credential: str):
    with pytest.raises(HubspotInvalidToken):
        TokenAuthenticator(token=non_match_credential)


def test_api():
    api = API(private_app_credentials=PRIVATE_APP_CREDENTIALS)
    assert api
