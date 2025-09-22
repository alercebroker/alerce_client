from .crossmatch import AlerceXmatch
from .ms_stamps import AlerceStampsMultisurvey
from .direct import AlerceDirect
from .global_search import AlerceSearch


class Alerce(
    AlerceSearch, AlerceXmatch, AlerceStampsMultisurvey, AlerceDirect
):
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
