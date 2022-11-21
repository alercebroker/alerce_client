from pandas import DataFrame
from astropy.table import Table
from .exceptions import handle_error, FormatValidationError
import requests
import abc


class Result:
    def __init__(self, format="json"):
        self.format = format

    @abc.abstractmethod
    def to_pandas(self, index=None, sort=None):
        """Convert the result to a pandas dataframe

        :index: index for the pandas dataframe
        :sort: sorting column for the dataframe
        :returns: the processed dataframe

        """
        pass

    @abc.abstractmethod
    def to_votable(self):
        pass

    @abc.abstractmethod
    def to_json(self):
       pass

    @abc.abstractmethod
    def to_csv(self):
        pass

    @abc.abstractmethod
    def result(self, index=None, sort=None):
        """Creates the result depending on the arguments and the expected format

        :index: if format is pandas, this is the index column
        :sort: if format is pandas, this is the sort column
        :returns: Result in the indicated formar

        """
        pass

class ResultJson(Result):
    """Object that holds a json type result"""
    def __init__(self, json_result, **kwargs):
        self.json_result = json_result
        super().__init__(**kwargs)
        print(self.format)

    def to_pandas(self, index=None, sort=None):
        dataframe = None
        if isinstance(self.json_result, list):
            dataframe = DataFrame(self.json_result)
        else:
            dataframe = DataFrame([self.json_result])
        if sort: dataframe.sort_values(sort, inplace=True)
        if index:
            dataframe.set_index(index, inplace=True)
        return dataframe

    def to_votable(self):
        return Table(self.json_result)

    def to_json(self):
        return self.json_result

    def to_csv(self, **kwargs):
        df = self.to_pandas(**kwargs)
        return df.to_csv()

    def result(self, index=None, sort=None):
        if self.format == "json":
            return self.to_json()
        if self.format == "pandas":
            return self.to_pandas(index, sort)
        if self.format == "votable":
            return self.to_votable()
        if self.format == "csv":
            return self.to_csv(index, sort)


class ResultCsv(Result):

    """Object that holds a csv type result"""

    def __init__(self, csv_result, **kwargs):
        self.csv_result = csv_result
        super().__init__(**kwargs)

    def to_pandas(self, index=None, sort=None):
        pass

    def to_votable(self):
        pass

    def to_csv(self):
        return self.csv_result

    def result(self, index=None, sort=None):
        if self.format == "pandas":
            return self.to_pandas(index, sort)
        if self.format == "votable":
            return self.to_votable()
        if self.format == "csv":
            return self.to_csv()




class Client:
    def __init__(self, **kwargs):
        self.session = requests.Session()
        self.config = {}
        self.config.update(kwargs)
        self.allowed_formats = ["pandas", "votable", "json", 'csv']

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
        self, method, url, params=None, response_field=None, result_format="json", response_format="json"
    ):
        result_format = self._validate_format(result_format)
        resp = self.session.request(method, url, params=params)

        if resp.status_code >= 400:
            handle_error(resp)
        if response_format == 'csv':
            return ResultCsv(resp, format=result_format)
        if response_field and result_format != "json":
            return ResultJson(resp.json()[response_field], format=result_format)
        return ResultJson(resp.json(), format=result_format)
