from .exceptions import FormatValidationError, ParseError, handle_error
from .utils import Result, Client

class AlerceDirect(Client):

    """Handles direct request to the database using the available http API"""

    def __init__(self, **kwargs):
        default_config = {
            "ZTF_DB_API_URL": "https://api.alerce.online/db/",
        }
        default_config.update(kwargs)
        # TODO: json must not be allowed for the direct client
        super().__init__(**default_config)

    def __get_url(self):
        return f"{self.config['ZTF_DB_API_URL']}"

    def send_query(self, query, format='csv'):
        """Sends the query directly to the API, returning the byte reply directly

        :query: query for the database
        :returns: byte reply

        """
        pass

