from .utils import Client


class AlerceDirect(Client):

    """Handles direct request to the database using the available http API"""

    def __init__(self, **kwargs):
        default_config = {
            "ZTF_DB_API_URL": "https://dev-api.alerce.online/dbquery/v1/db/",
        }
        default_config.update(kwargs)
        super().__init__(**default_config)

    def __get_url(self):
        return f"{self.config['ZTF_DB_API_URL']}"

    def send_query(self, query, format="csv", index=None, sort=None):
        """Sends the query directly to the API, returning the byte reply directly

        :query: query for the database
        :format: Format to be returned
        :index: index if format is pandas
        :sort: sorting column if format is pandas
        :returns: reply in the format specified

        """
        data = {"query": query}
        q = self._request(
            "POST",
            self.__get_url(),
            data=data,
            result_format=format,
            response_format="csv",
        )
        return q.result(index, sort)
