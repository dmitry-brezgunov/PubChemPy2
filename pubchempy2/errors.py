import requests


def handle_http_error(response: requests.Response):
    code = response.status_code
    msg = response.text

    match code:
        case 400:
            raise BadRequestError(msg)
        case 404:
            raise NotFoundError(msg)
        case 405:
            raise MethodNotAllowedError(msg)
        case 504:
            raise TimeoutError(msg)
        case 501:
            raise UnimplementedError(msg)
        case 500:
            raise ServerError(msg)
        case _:
            raise PubChemHTTPError()


class PubChemPyError(Exception):
    """Base class for all PubChemPy exceptions."""

    pass


class PubChemHTTPError(PubChemPyError):
    """Generic error class to handle all HTTP error codes."""

    def __init__(self, msg="Unspecified HTTP error"):
        self.msg = msg


class BadRequestError(PubChemHTTPError):
    """Request is improperly formed (syntax error in the URL, POST body, etc.)."""

    def __init__(self, msg="Request is improperly formed"):
        self.msg = msg


class NotFoundError(PubChemHTTPError):
    """The input record was not found (e.g. invalid CID)."""

    def __init__(self, msg="The input record was not found"):
        self.msg = msg


class MethodNotAllowedError(PubChemHTTPError):
    """Request not allowed (such as invalid MIME type in the HTTP Accept header)."""

    def __init__(self, msg="Request not allowed"):
        self.msg = msg


class TimeoutError(PubChemHTTPError):
    """The request timed out, from server overload or too broad a request.

    See :ref:`Avoiding TimeoutError <avoiding_timeouterror>` for more information.
    """

    def __init__(self, msg="The request timed out"):
        self.msg = msg


class UnimplementedError(PubChemHTTPError):
    """The requested operation has not (yet) been implemented by the server."""

    def __init__(self, msg="The requested operation has not been implemented"):
        self.msg = msg


class ServerError(PubChemHTTPError):
    """Some problem on the server side (such as a database server down, etc.)."""

    def __init__(self, msg="Some problem on the server side"):
        self.msg = msg
