import requests


def handle_error(response, response_format="json"):
    # TODO: The direct API uses code 400 for user input error (bad requests, etc), what should be done here then?
    codes = {-1: APIError, 400: ParseError, 404: ObjectNotFoundError}
    message = "Unknown API error."
    error = "Unknown API error."
    if response_format == "json":
        try:
            error = response.json().get("errors", {})
            message = response.json().get("message")
        except requests.exceptions.JSONDecodeError:
            pass
    elif response_format == "csv":
        error = response.content.decode("utf-8")
        message = response.content.decode("utf-8")
    code = response.status_code
    data = error

    raise codes.get(code, APIError)(
        message=message, code=code, data=data, response=response
    )


class APIError(Exception):
    response = None
    data = {}
    message = "An error with the API occurred."
    code = -1

    def __init__(self, message=None, code=None, data={}, response=None):
        self.response = response
        if message:
            self.message = message
        if code:
            self.code = code
        if data:
            self.data = data

    def __str__(self):
        if self.code:
            ret = {"Error code": self.code, "Message": self.message, "Data": self.data}
            return str(ret)
        return self.message


class CandidError(Exception):
    response = None
    data = {}
    message = "Object has no stamps."
    code = -1


class ParseError(APIError):
    pass


class FormatValidationError(ParseError):
    pass


class ObjectNotFoundError(APIError):
    ## TODO add logic for including oid in error message
    pass
