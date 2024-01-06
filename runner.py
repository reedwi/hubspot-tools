import logging

from hubspot_tools.api import TokenAuthenticator, API
from hubspot_tools.constants import PRIVATE_APP_CREDENTIALS

logger = logging.getLogger('unittest_api')


def test_token():
    token_auth = TokenAuthenticator(token=PRIVATE_APP_CREDENTIALS)
    print(token_auth.token)

def test_api():
    api = API(private_app_credentials=PRIVATE_APP_CREDENTIALS)
    assert api

def main():
    test_token()

if __name__ == '__main__':
    main()