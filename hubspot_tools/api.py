# built-in
from typing import Any, Mapping, MutableMapping, Tuple, Union, List, Optional
import logging
import re
from http import HTTPStatus

# installed packages
import requests
from requests.auth import AuthBase

# custom
from hubspot_tools.constants import PRIVATE_APP_CREDENTIALS
from hubspot_tools.errors import (
    HubspotInvalidToken,
    HubspotAccessDenied,
    HubspotBadRequest,
    HubspotDuplicate,
    HubspotInvalidAuth,
    HubspotRateLimited,
    HubspotTimeout,
)


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
                internal_message="Token is not 44 characters in length"
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
        return f"{self._auth_method} {self._token}"

    def __init__(
        self,
        token: str,
        auth_method: str = "Bearer",
        auth_header: str = "Authorization",
    ) -> None:
        self._auth_header = auth_header
        self._auth_method = auth_method
        self._token = token
        self.struture_valid()


class API:
    BASE_URL = "https://api.hubapi.com"
    USER_AGENT = "Hubspot Tools"

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

    @staticmethod
    def _parse_errors(
        response: requests.Response,
        delete: bool = False
    ) -> Optional[Union[MutableMapping[str, Any], List[MutableMapping[str, Any]]]]:
        message = "Unknown error"

        if (
            response.headers.get("content-type") == "application/json;charset=utf-8"
            and response.status_code != HTTPStatus.OK
        ):
            message = response.json().get("message")

        match response.status_code:
            case HTTPStatus.BAD_REQUEST:
                message = f"Request to {response.url} didn't succeed. Please verify your credentials and try again.\nError message from Hubspot API: {message}"
                logger.warning(message)
            case HTTPStatus.FORBIDDEN:
                message = f"The authenticated user does not have permissions to access the URL {response.url}. Verify your permissions to access this endpoint."
                logger.warning(message)
            case HTTPStatus.UNAUTHORIZED:
                message = "The user cannot be authorized with provided credentials. Please verify that your credentails are valid and try again."
                raise HubspotInvalidAuth(internal_message=message, response=response)
            case HTTPStatus.TOO_MANY_REQUESTS:
                retry_after = response.headers.get("Retry-After")
                message = f"You have reached your Hubspot API limit. Can resume after {retry_after} seconds.\nSee https://developers.hubspot.com/docs/api/usage-details"
                raise HubspotRateLimited(
                    message,
                    response=response,
                )
            case [HTTPStatus.BAD_GATEWAY, HTTPStatus.SERVICE_UNAVAILABLE]:
                raise HubspotTimeout(message, response)
            case HTTPStatus.CONFLICT:
                message = "There is a conflict on a unique key that is causing error"
                raise HubspotDuplicate(message, response)
            case _:
                response.raise_for_status()
        
        if not delete:
            return response.json()

    def get(
        self, url: str, params: MutableMapping[str:Any] = None
    ) -> Tuple[
        Union[MutableMapping[str, Any], List[MutableMapping[str, Any]]],
        requests.Response,
    ]:
        response = self._session.get(self.BASE_URL + url, params=params)
        return self._parse_errors(response), response

    def post(
        self, url: str, data: Mapping[str:Any], params: MutableMapping[str:Any] = None
    ) -> Tuple[
        Union[MutableMapping[str, Any], List[MutableMapping[str, Any]]],
        requests.Response,
    ]:
        response = self._session.post(self.BASE_URL + url, params=params, json=data)
        return self._parse_errors(response), response

    def put(
        self, url: str, data: Mapping[str:Any], params: MutableMapping[str:Any] = None
    ) -> Tuple[
        Union[MutableMapping[str, Any], List[MutableMapping[str, Any]]],
        requests.Response,
    ]:
        response = self._session.put(self.BASE_URL + url, params=params, json=data)
        return self._parse_errors(response), response

    def patch(
        self, url: str, data: Mapping[str:Any], params: MutableMapping[str:Any] = None
    ) -> Tuple[
        Union[MutableMapping[str, Any], List[MutableMapping[str, Any]]],
        requests.Response,
    ]:
        response = self._session.patch(self.BASE_URL + url, params=params, json=data)
        return self._parse_errors(response), response

    def delete(
        self, url: str, params: MutableMapping[str:Any] = None
    ) -> Tuple[
        bool,
        requests.Response,
    ]:
        response = self._session.delete(self.BASE_URL + url, params=params)
        return self._parse_errors(response, True), response
