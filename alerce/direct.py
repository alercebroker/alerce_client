from .utils import Client


class AlerceDirect(Client):

    """Handles direct request to the postgres database using the available http API"""

    def __init__(self, **kwargs):
        default_config = {
            "ZTF_DB_API_URL": "https://dev-api.alerce.online/dbquery/v1/db/",
        }
        default_config.update(kwargs)
        super().__init__(**default_config)

    def __get_url(self):
        return f"{self.config['ZTF_DB_API_URL']}"

    def send_query(self, query, format="csv", index=None, sort=None):
        """Sends the query directly to the API, returning the reply in the specified format

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

class AlerceMongo(Client):
    """Handles direct request to the mongo database using the available http API"""

    def __init__(self, **kwargs):
        default_config = {
            "ZTF_MONGO_API_URL": "https://dev-api.alerce.online/dbquery/v1/mongo/",
        }
        default_config.update(kwargs)
        super().__init__(**default_config)

    def __get_url(self):
        return f"{self.config['ZTF_MONGO_API_URL']}"

    def mongo_findOne(self, data, format="json", index=None, sort=None):
        """Sends the query directly to the /findOne endpoint of the API, returning the reply in the specified format

        :data: Data to be sent to the API
        :format: Format to be returned
        :index: index if format is pandas
        :sort: sorting column if format is pandas
        :returns: reply in the format specified

        """
        return self.__mongo_send('findOne', 'document', data, format, index, sort)

    def mongo_find(self, data, format="json", index=None, sort=None):
        """Sends the query directly to the /find endpoint of the API, returning the reply in the specified format

        :data: Data to be sent to the API
        :format: Format to be returned
        :index: index if format is pandas
        :sort: sorting column if format is pandas
        :returns: reply in the format specified

        """
        return self.__mongo_send('find', 'documents', data, format, index, sort)

    def mongo_aggregate(self, data, format="json", index=None, sort=None):
        """Sends the query directly to the /aggregate endpoint of the API, returning the reply in the specified format

        :data: Data to be sent to the API
        :format: Format to be returned
        :index: index if format is pandas
        :sort: sorting column if format is pandas
        :returns: reply in the format specified

        """
        return self.__mongo_aggregate('aggregate', 'documents', data, format, index, sort)

    def __mongo_send(self, endpoint, response_field, data, format="csv", index=None, sort=None):
        q = self._request(
            "POST",
            self.__get_url() + endpoint,
            json=data,
            result_format=format,
            response_format="json",
            response_field=response_field
        )
        return q.result(index, sort)
