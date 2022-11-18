from pandas import DataFrame
from astropy.table import Table
from .exceptions import handle_error, FormatValidationError
import requests


class Result:
    def __init__(self, json_result, format="json"):
        # TODO: results are no longer on json only
        self.json_result = json_result
        self.format = format

    # TODO: cases must be added for when the result is csv

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

    # TODO
    def to_csv(self):
        pass

    def result(self, index=None, sort=None):
        if self.format == "json":
            return self.to_json()
        if self.format == "pandas":
            return self.to_pandas(index, sort)
        if self.format == "votable":
            return self.to_votable()
        if self.format == 'csv':
            return self.to_csv()


class Client:
    def __init__(self, **kwargs):
        self.session = requests.Session()
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

        # TODO: add a case for when the response is expected to be csv. Direct API cant NOT return json requests.
        if resp.status_code >= 400:
            handle_error(resp)
        if response_field and result_format != "json":
            return Result(resp.json()[response_field], format=result_format)
        return Result(resp.json(), format=result_format)
