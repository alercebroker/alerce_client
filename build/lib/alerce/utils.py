from pandas import DataFrame
from astropy.table import Table
from .exceptions import handle_error, FormatValidationError

class Result:
    def __init__(self, json_result, format="json"):
        self.json_result = json_result
        self.format = format

    def to_pandas(self, index=None, sort=None):
        dataframe = None
        if isinstance(self.json_result, list):
            dataframe = DataFrame(self.json_result)
        else:
            dataframe = DataFrame([self.json_result])
        if sort:
            dataframe.sort_values(sort, inplace=True)
        if index:
            dataframe.set_index(index, inplace=True)
        return dataframe

    def to_votable(self):
        return Table(self.json_result)

    def to_json(self):
        return self.json_result

    def result(self, index=None, sort=None):
        if self.format == "json":
            return self.to_json()
        if self.format == "pandas":
            return self.to_pandas(index, sort)
        if self.format == "votable":
            return self.to_votable()

class Client:
    def __init__(self, **kwargs):
        self.config = {}
        self.config.update(kwargs)
        self.allowed_formats = ["pandas", "votable", "json"]

    def load_config_from_file(self, path):
        pass

    def load_config_from_object(self, object):
        self.config.update(object)


    def _validate_format(self, format):
        format = format.lower()
        if not format in self.allowed_formats:
            raise FormatValidationError(
                "Format '%s' not in %s" % (format, self.allowed_formats), code=500
            )
        return format

    def _request(
        self, method, url, params=None, response_field=None, result_format="json"
    ):
        result_format = self._validate_format(result_format)
        resp = self.session.request(method, url, params=params)

        if resp.status_code >= 400:
            handle_error(resp)
        if response_field and result_format != "json":
            return Result(resp.json()[response_field], format=result_format)
        return Result(resp.json(), format=result_format)
