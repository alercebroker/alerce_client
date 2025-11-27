from .common_search import AlerceCommonSearch
from .crossmatch import AlerceXmatch
from .common_stamps import AlerceCommonStamps


class Alerce(AlerceCommonSearch, AlerceXmatch, AlerceCommonStamps):
    """
    The ALeRCE Client for accessing astronomical data from multiple surveys.

    This is the main entry point for the ALeRCE Python Client. It provides unified
    access to query astronomical objects, photometry, classifications, stamps, and
    perform crossmatching operations across multiple surveys.

    Examples
    --------
    Basic usage:

    >>> from alerce.core import Alerce
    >>> client = Alerce()

    Query objects from ZTF:

    >>> objects = client.query_objects(
    ...     survey="ztf",
    ...     ra=10.0,
    ...     dec=-20.0,
    ...     radius=30
    ... )

    Get a lightcurve:

    >>> lc = client.query_lightcurve("ZTF21aaeyldq", survey="ztf")

    Retrieve stamps:

    >>> stamps = client.get_stamps(
    ...     oid="ZTF21aaeyldq",
    ...     candid=1234567890,
    ...     survey="ztf"
    ... )

    Notes
    -----
    Most methods require a ``survey`` parameter to specify which survey's data
    to query. Currently supported surveys are "ztf" and "lsst". While some
    methods still default to "ztf" for backward compatibility, this behavior
    is deprecated and will be removed in future versions. Always explicitly
    specify the survey parameter.

    See Also
    --------
    migration_guide : Guide for migrating to the multi-survey API
    """

    def __init__(self, **kwargs):
        AlerceCommonSearch.__init__(self, **kwargs)
        AlerceXmatch.__init__(self, **kwargs)
        AlerceCommonStamps.__init__(self, **kwargs)
