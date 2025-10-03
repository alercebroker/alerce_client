from .common_search import AlerceCommonSearch
from .crossmatch import AlerceXmatch
from .common_stamps import AlerceCommonStamps


class Alerce(AlerceCommonSearch, AlerceXmatch, AlerceCommonStamps):
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
        AlerceCommonSearch.__init__(self, **kwargs)
        AlerceXmatch.__init__(self, **kwargs)
        AlerceCommonStamps.__init__(self, **kwargs)
