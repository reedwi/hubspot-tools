import requests

class HubspotError(Exception):
    def __init__(
        self, 
        internal_message: str = None,
        message: str = None,
        exception: BaseException = None,
        response: requests.Response = None
    ) -> None:
        super().__init__(internal_message, message, exception)
        self.response = response


class HubspotInvalidToken(HubspotError):
    '''Structure of token is incorrect'''