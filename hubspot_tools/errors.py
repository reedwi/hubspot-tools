import requests
from requests import HTTPError


class HubspotError(Exception):
    def __init__(
        self,
        internal_message: str = None,
        message: str = None,
        exception: BaseException = None,
        response: requests.Response = None,
    ) -> None:
        super().__init__(internal_message, message, exception)
        self.response = response


class HubspotInvalidToken(HubspotError):
    """Structure of token is incorrect"""


class HubspotTimeout(HTTPError):
    """502/504 HubSpot has processing limits in place to prevent a single client from causing degraded performance,
    and these responses indicate that those limits have been hit. You'll normally only see these timeout responses
    when making a large number of requests over a sustained period. If you get one of these responses,
    you should pause your requests for a few seconds, then retry.
    """


class HubspotInvalidAuth(HubspotError):
    """401 Unauthorized"""


class HubspotAccessDenied(HubspotError):
    """403 Forbidden"""


class HubspotRateLimited(HTTPError):
    """429 Rate Limit Reached"""


class HubspotBadRequest(HubspotError):
    """400 Bad Request"""


class HubspotDuplicate(HubspotError):
    """409 Conflict"""
