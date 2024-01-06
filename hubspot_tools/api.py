# built-in
from typing import Any, Mapping
import logging
import re

# installed packages
import requests
from requests.auth import AuthBase

# custom
from hubspot_tools.constants import PRIVATE_APP_CREDENTIALS
from hubspot_tools.errors import HubspotInvalidToken


logger = logging.getLogger(__name__)

class TokenAuthenticator(AuthBase):
    def __call__(self, request):
        request.headers.update(self.get_auth_header())
        return request
    
    def get_auth_header(self) -> Mapping[str, Any]:
        if self.auth_header:
            return {self.auth_header: self.token}
        return {}
    
    def struture_valid(self) -> None:
        pattern = r"^pat-[a-zA-Z0-9]{3}-[a-zA-Z0-9]{8}-[a-zA-Z0-9]{4}-[a-zA-Z0-9]{4}-[a-zA-Z0-9]{4}-[a-zA-Z0-9]{12}"

        if len(self._token) != 44:
            raise HubspotInvalidToken(
                internal_message='Token is not 44 characters in length'
            )
        elif not re.match(pattern, self._token):
            raise HubspotInvalidToken(
                internal_message='Token does not follow correct structure of "pat-XXX-XXXXXXXX-XXXX-XXXX-XXXX-XXXXXXXXXXXX"'
            )
    
    @property
    def auth_header(self) -> str:
        return self._auth_header

    @property
    def token(self) -> str:
        return f'{self._auth_method} {self._token}'

    def __init__(
        self, 
        token: str, 
        auth_method: str = 'Bearer', 
        auth_header: str = 'Authorization'
    ) -> None:
        self._auth_header = auth_header
        self._auth_method = auth_method
        self._token = token
        self.struture_valid()


class API:
    BASE_URL = 'https://api.hubapi.com'
    USER_AGENT = 'Hubspot Tools'

    def authenticator(self) -> TokenAuthenticator:
        return TokenAuthenticator(token=PRIVATE_APP_CREDENTIALS)

    def __init__(self, private_app_credentials: str):
        self._session = requests.Session()
        self.credentials = private_app_credentials

        self._session.auth = self.authenticator()

        self._session.headers = {
            "Content-Type": "application/json",
            "User-Agent": self.USER_AGENT,
        }

    def get():
        pass

    def post():
        pass

    def put():
        pass

    def delete():
        pass