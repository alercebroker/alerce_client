from .search import AlerceSearch
from .crossmatch import AlerceXmatch
from .stamps import AlerceStamps
from .direct import AlerceDirect


class Alerce(AlerceSearch, AlerceXmatch, AlerceStamps, AlerceDirect):
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

    pass
