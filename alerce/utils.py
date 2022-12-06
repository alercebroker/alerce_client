from pandas import DataFrame, read_csv
from io import StringIO
from astropy.table import Table
from .exceptions import handle_error, FormatValidationError
import requests
import abc


class Result(abc.ABC):
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
    def to_csv(self, index=None, sort=None):
        pass

    def result(self, index=None, sort=None):
        """Creates the result depending on the arguments and the expected format

        :index: if format is pandas, this is the index column
        :sort: if format is pandas, this is the sort column
        :returns: Result in the indicated format

        """
        if self.format == "pandas":
            return self.to_pandas(index, sort)
        elif self.format == "votable":
            return self.to_votable()
        elif self.format == "csv":
            return self.to_csv()
        elif self.format == "json":
            return self.to_json()
        raise ValueError(f"Unrecognized format '{self.format}'")


class ResultJson(Result):
    """Object that holds a json type result"""

    def __init__(self, json_result, **kwargs):
        self.json_result = json_result
        super().__init__(**kwargs)

    def to_pandas(self, index=None, sort=None):
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

    def to_csv(self):
        df = self.to_pandas()
        return df.to_csv(index=False)


class ResultCsv(Result):

    """Object that holds a csv type result"""

    def __init__(self, csv_result_byte, **kwargs):
        self.csv_result = csv_result_byte.decode("utf-8")
        self.data = [x.split(",") for x in self.csv_result.split("\n")[1:-1]]

        self.columns = [x for x in self.csv_result.split("\n")[0].split(",")]
        super().__init__(**kwargs)

    def _rename_duplicates(self):
        counts = {}
        columns = self.columns.copy()
        for i, column in enumerate(columns):
            if column in counts:
                counts[column] += 1
                columns[i] = f"{column}_{counts[column] - 1}"
            else:
                counts[column] = 1
        return columns

    def to_pandas(self, index=None, sort=None):
        dataframe = read_csv(StringIO(self.csv_result))
        if sort:
            dataframe.sort_values(sort, inplace=True)
        if index:
            dataframe.set_index(index, inplace=True)
        return dataframe

    def to_votable(self):
        # TODO: Check if renaming the columns doesn't cause problems to the user
        columns = self._rename_duplicates()
        df = read_csv(StringIO(self.csv_result), names=columns, skiprows=1)
        df = df.convert_dtypes()
        table = Table.from_pandas(df)
        return table

    def to_json(self):
        columns = self._rename_duplicates()
        df = read_csv(StringIO(self.csv_result), names=columns, skiprows=1)
        return df.to_json(orient="records")

    def to_csv(self):
        return self.csv_result


class Client:
    def __init__(self, **kwargs):
        self.session = requests.Session()
        self.config = {}
        self.config.update(kwargs)
        self.allowed_formats = ["pandas", "votable", "json", "csv"]

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
        self,
        method,
        url,
        params=None,
        data=None,
        response_field=None,
        result_format="json",
        response_format="json",
    ):
        result_format = self._validate_format(result_format)

        resp = self.session.request(method, url, params=params, data=data)
        if resp.status_code >= 400:
            handle_error(resp, response_format)

        if response_format == "csv":
            return ResultCsv(resp.content, format=result_format)
        if response_field and result_format != "json" and result_format != "csv":
            return ResultJson(resp.json()[response_field], format=result_format)
        return ResultJson(resp.json(), format=result_format)
