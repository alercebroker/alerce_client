from .search import AlerceSearch
from .crossmatch import AlerceXmatch
from .stamps import AlerceStamps


class Alerce(AlerceSearch, AlerceXmatch, AlerceStamps):
    """
    The main client class that has all the methods for accessing the different services.

    Parameters
    -----------
    **kwargs
        Keyword arguments used for setting the configuration of each service

    Attributes
    -----------
    ztf_url
        The url of the ZTF API
    """
    def __init__(self, **kwargs):
       super().__init__(**kwargs)

    def load_config_from_file(self, path):
        pass

    def load_config_from_object(self, object):
        """
        Sets configuration parameters from a dictionary object.

        Parameters
        ------------
        object : dict
            The dictionary containing the config.
        """
        super().load_config_from_object(object)
