from .ms_stamps import AlerceStampsMultisurvey
from .stamps import AlerceStamps
import warnings


class AlerceCommonStamps:
    """
    AlerceCommonStamps provides a unified interface for retrieving and displaying
    stamps from multiple surveys, including ZTF and LSST.

    This class routes stamp queries to the appropriate survey-specific client based on the
    survey parameter. Users interact with the Alerce class which inherits from this,
    providing a single entry point for all stamp operations.
    """

    def __init__(self, **kwargs):
        """
        Initializes the AlerceCommonStamps class with clients for legacy ZTF
        and multisurvey stamps.

        Parameters
        ----------
        """
        self.legacy_stamps_client = AlerceStamps()
        self.multisurvey_stamps_client = AlerceStampsMultisurvey()
        self.valid_surveys = ["ztf", "lsst"]

    def plot_stamps(self, oid, candid=None, measurement_id=None, survey=None):
        """
        Plot stamp in a notebook given oid. It uses IPython HTML.

        Parameters
        ----------
        oid : str
            Object ID in ALeRCE DBs.
        candid : int, optional
            Candid of the stamp to be displayed. If None, uses the first detection.
        measurement_id : int, optional
            Alias for candid parameter (for multisurvey compatibility).
        survey : str, optional
            The survey to query. If None, defaults to 'ztf'. Note: relying on
            the default (omitting the `survey` parameter) is deprecated and will be removed in
            a future release; callers should explicitly pass the desired survey (e.g. `survey='ztf'`).

        Returns
        -------
        None
            Displays the stamps on a jupyter notebook.

        Raises
        ------
        ValueError
            If the survey is not in the list of valid surveys.
        """

        candid = candid or measurement_id

        if survey is None:
            survey = "ztf"
            warnings.warn(
                "survey not provided, defaulting to 'ztf'. This will use the legacy ZTF client. This behavior will be deprecated in future versions.",
                DeprecationWarning,
            )

        if survey == "ztf":
            return self.legacy_stamps_client.plot_stamps(oid=oid, candid=candid)
        elif survey in self.valid_surveys:
            return self.multisurvey_stamps_client.multisurvey_plot_stamps(
                oid=oid, candid=candid, survey=survey
            )
        else:
            raise ValueError(f"survey must be one of {self.valid_surveys}")

    def get_stamps(
        self,
        oid,
        candid=None,
        measurement_id=None,
        include_variance_and_mask=False,  # NEW
        format="HDUList",
        survey=None,
    ):
        """
        Download Stamps for a specific alert.

        Parameters
        ----------
        oid : str
            Object ID in ALeRCE DBs.
        candid : int, optional
            Candid of the stamp to be downloaded. If None, uses the first detection.
        measurement_id : int, optional
            Alias for candid parameter (for multisurvey compatibility).

        format : str
            Output format. Options: 'HDUList' | 'numpy'
        survey : str, optional
            The survey to query. If None, defaults to 'ztf'. Note: relying on
            the default (omitting the `survey` parameter) is deprecated and will be removed in
            a future release; callers should explicitly pass the desired survey (e.g. `survey='ztf'`).
        include_variance_and_mask : bool
            If True, returns extra planes of the image cutouts.
        Returns
        -------
        HDUList or list
            Science, Template and Difference stamps for a specific alert.
            Returns HDUList if format='HDUList', otherwise list of numpy arrays.

        Raises
        ------
        ValueError
            If the survey is not in the list of valid surveys.
        """

        candid = candid or measurement_id

        if survey is None:
            survey = "ztf"
            warnings.warn(
                "survey not provided, defaulting to 'ztf'. This will use the legacy ZTF client. This behavior will be deprecated in future versions.",
                DeprecationWarning,
            )

        if survey == "ztf":
            return self.legacy_stamps_client.get_stamps(
                oid=oid, candid=candid, format=format
            )
        elif survey in self.valid_surveys:
            return self.multisurvey_stamps_client.multisurvey_get_stamps(
                oid=oid,
                candid=candid,
                include_variance_and_mask=include_variance_and_mask,
                survey=survey,
            )
        else:
            raise ValueError(f"survey must be one of {self.valid_surveys}")

    def get_avro(self, oid, candid=None, use_multisurvey_api=False, survey=None):
        """
        Download avro of some alert.

        Parameters
        ----------
        oid : str
            Object ID in ALeRCE DBs.
        candid : int, optional
            Candid of the avro to be downloaded. If None, uses the first detection.
        use_multisurvey_api : bool
            If True, uses the multisurvey API. Requires `survey` parameter.
        survey : str, optional
            The survey to query. Required when use_multisurvey_api is True.

        Returns
        -------
        bytes
            Avro data of a given alert.

        Raises
        ------
        ValueError
            If use_multisurvey_api is True and survey is not provided.
        NotImplementedError
            If multisurvey get_avro is not implemented.
        """
        if use_multisurvey_api:
            if survey is None:
                raise ValueError(
                    "survey must be provided when use_multisurvey_api is True"
                )
            if not hasattr(self.multisurvey_stamps_client, "multisurvey_get_avro"):
                raise NotImplementedError("Multisurvey get_avro not implemented.")
            return self.multisurvey_stamps_client.multisurvey_get_avro(
                survey=survey, oid=oid, candid=candid
            )
        else:
            return self.legacy_stamps_client.get_avro(oid, candid=candid)
