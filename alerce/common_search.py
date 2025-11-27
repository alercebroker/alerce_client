from .ztf_search import ZTFSearch
from .ms_search import AlerceSearchMultiSurvey
import warnings


class AlerceCommonSearch:
    """
    AlerceCommonSearch provides a unified interface for querying astronomical data
    from multiple surveys, including ZTF and LSST. It supports querying objects,
    lightcurves, detections, non-detections, and other related data.

    This class routes queries to the appropriate survey-specific client based on the
    survey parameter. Users interact with the Alerce class which inherits from this,
    providing a single entry point for all queries.
    """

    def __init__(self, **kwargs):
        """
        Initializes the AlerceCommonSearch class with clients for legacy ZTF
        and multisurvey data.
        """
        self.legacy_ztf_client = ZTFSearch()
        self.multisurvey_client = AlerceSearchMultiSurvey()
        self.valid_surveys = ["ztf", "lsst"]

    def query_objects(
        self,
        format="pandas",
        index=None,
        sort=None,
        survey: str | None = None,
        **kwargs,
    ):
        """
        Gets a list of objects filtered by specified parameters.

        Parameters
        ----------
        format : str
            Return format. Can be one of 'pandas' | 'votable' | 'json'
        index : str
            Name of the column to use as index when format is 'pandas'
        sort : str
            Name of the column to sort when format is 'pandas'
        survey : str | None
            The survey to query. If None, defaults to 'ztf'. Note: relying on
            the default (omitting the `survey` parameter) is deprecated and will be removed in
            a future release; callers should explicitly pass the desired survey (e.g. `survey='ztf'`).
        **kwargs
            Keyword arguments specific to the survey being queried. For ZTF, these can include:
            classifier, class_name, ndet, probability, firstmjd, lastmjd, ra, dec, radius,
            page, page_size, count, order_by, order_mode.

        Returns
        -------
        The queried objects data in the specified format

        Raises
        ------
        ValueError
            If the survey is not in the list of valid surveys.
        """
        if survey is None:
            survey = "ztf"
            warnings.warn(
                "survey not provided, defaulting to 'ztf'. This will use the legacy ZTF client. This behavior will be deprecated in future versions.",
                DeprecationWarning,
            )

        if survey == "ztf":
            return self.legacy_ztf_client.query_objects(
                format=format, index=index, sort=sort, **kwargs
            )
        elif survey in self.valid_surveys:
            return self.multisurvey_client.query_objects(
                survey, format=format, index=index, sort=sort, **kwargs
            )
        else:
            raise ValueError(f"survey must be one of {self.valid_surveys}")

    def query_object(
        self,
        oid,
        format="json",
        survey: str | None = None,
        **kwargs,
    ):
        """
        Gets a single object by object id

        Parameters
        ----------
        oid : str
            The object identifier
        format : str
            Return format. Can be one of 'pandas' | 'votable' |
            'json'
        survey: str | None
            The survey to query. If None, defaults to 'ztf'. Note: relying on the default
            (omitting the `survey` parameter) is deprecated and will be removed in a future
            release; callers should explicitly pass the desired survey (e.g. `survey='ztf'`).
        kwargs: dict
            Additional parameters specific to the multisurvey API

        Returns
        -------
        The object data in the specified format

        """
        if survey is None:
            survey = "ztf"
            warnings.warn(
                "survey not provided, defaulting to 'ztf'. This will use the legacy ZTF client. This behavior will be deprecated in future versions.",
                DeprecationWarning,
            )

        if survey == "ztf":
            # legacy ZTFSearch.query_object does not accept arbitrary kwargs; forward only supported args
            return self.legacy_ztf_client.query_object(oid, format=format)
        elif survey in self.valid_surveys:
            return self.multisurvey_client.query_object(
                survey, oid, format=format, **kwargs
            )
        else:
            raise ValueError(f"survey must be one of {self.valid_surveys}")

    def query_lightcurve(
        self,
        oid,
        format="json",
        survey: str | None = None,
    ):
        """
        Gets the lightcurve (detections and non_detections) of a given object

        Parameters
        ----------
        oid : str
            The object identifier
        format : str
            Return format. Can be one of 'pandas' | 'votable' | 'json'
        survey : str | None
            The survey to query. If None, defaults to 'ztf'. Note: relying on the default
            (omitting the `survey` parameter) is deprecated and will be removed in a future
            release; callers should explicitly pass the desired survey (e.g. `survey='ztf'`).

        Returns
        -------
        The lightcurve data in the specified format

        """
        if survey is None:
            survey = "ztf"
            warnings.warn(
                "survey not provided, defaulting to 'ztf'. This will use the legacy ZTF client. This behavior will be deprecated in future versions.",
                DeprecationWarning,
            )

        if survey == "ztf":
            return self.legacy_ztf_client.query_lightcurve(oid, format=format)
        elif survey in self.valid_surveys:
            return self.multisurvey_client.query_lightcurve(survey, oid, format=format)
        else:
            raise ValueError(f"survey must be one of {self.valid_surveys}")

    def query_detections(
        self,
        oid: str | int,
        format: str = "json",
        survey: str | None = None,
        index=None,
        sort=None,
    ):
        """
        Gets all detections of a given object

        Parameters
        ----------
        oid : str | int
            The object identifier
        format : str
            Return format. Can be one of 'pandas' | 'votable' | 'json'
        survey : str | None
            The survey to query. If None, defaults to 'ztf'. Note: relying on
            the default (omitting the `survey` parameter) is deprecated and will be removed in a future
            release; callers should explicitly pass the desired survey (e.g. `survey='ztf'`).
        index : str
            The name of the column to use as index when format is 'pandas'
        sort : str
            The name of the column to sort when format is 'pandas'

        Returns
        -------
        The detections data in the specified format

        """
        if survey is None:
            survey = "ztf"
            warnings.warn(
                "survey not provided, defaulting to 'ztf'. This will use the legacy ZTF client. This behavior will be deprecated in future versions.",
                DeprecationWarning,
            )

        if survey == "ztf":
            return self.legacy_ztf_client.query_detections(
                oid, format=format, index=index, sort=sort
            )
        elif survey in self.valid_surveys:
            return self.multisurvey_client.query_detections(
                survey, oid, format=format, index=index, sort=sort
            )
        else:
            raise ValueError(f"survey must be one of {self.valid_surveys}")

    def query_non_detections(
        self,
        oid: str | int,
        format: str = "json",
        survey: str | None = None,
        index=None,
        sort=None,
    ):
        """
        Gets all non detections of a given object

        Parameters
        ----------
        oid : str | int
            The object identifier
        format : str
            Return format. Can be one of 'pandas' | 'votable' | 'json'
        survey : str | None
            The survey to query. If None, defaults to 'ztf'. Note: relying on
            the default (omitting the `survey` parameter) is deprecated and will be removed in
            future release; callers should explicitly pass the desired survey (e.g. `survey='ztf'`).
        index : str
            The name of the column to use as index when format is 'pandas'
        sort : str
            The name of the column to sort when format is 'pandas'

        Returns
        -------
        The non-detections data in the specified format

        """
        if survey is None:
            survey = "ztf"
            warnings.warn(
                "survey not provided, defaulting to 'ztf'. This will use the legacy ZTF client. This behavior will be deprecated in future versions.",
                DeprecationWarning,
            )

        if survey == "ztf":
            return self.legacy_ztf_client.query_non_detections(
                oid, format=format, index=index, sort=sort
            )
        elif survey in self.valid_surveys:
            return self.multisurvey_client.query_non_detections(
                survey, oid, format=format, index=index, sort=sort
            )
        else:
            raise ValueError(f"survey must be one of {self.valid_surveys}")

    def query_forced_photometry(
        self,
        oid,
        format="json",
        survey: str | None = None,
        index=None,
        sort=None,
    ):
        """
        Gets all forced photometry of a given object

        Parameters
        ----------
        oid : str
            The object identifier
        format : str
            Return format. Can be one of 'pandas' | 'votable' | 'json'
        survey : str | None
            The survey to query. If None, defaults to 'ztf'. Note: relying on
            the default (omitting the `survey` parameter) is deprecated and will be removed in
            future release; callers should explicitly pass the desired survey (e.g. `survey='ztf'`).
        index : str
            The name of the column to use as index when format is 'pandas'
        sort : str
            The name of the column to sort when format is 'pandas'

        Returns
        -------
        The forced photometry data in the specified format

        """
        if survey is None:
            survey = "ztf"
            warnings.warn(
                "survey not provided, defaulting to 'ztf'. This will use the legacy ZTF client. This behavior will be deprecated in future versions.",
                DeprecationWarning,
            )

        if survey == "ztf":
            return self.legacy_ztf_client.query_forced_photometry(
                oid, format=format, index=index, sort=sort
            )
        elif survey in self.valid_surveys:
            return self.multisurvey_client.query_forced_photometry(
                survey, oid, format=format, index=index, sort=sort
            )
        else:
            raise ValueError(f"survey must be one of {self.valid_surveys}")

    def query_magstats(
        self,
        oid,
        format="json",
        survey: str | None = None,
        index=None,
        sort=None,
    ):
        """
        Gets all magnitude statistics of a given object

        Parameters
        ----------
        oid : str
            The object identifier
        format : str
            Return format. Can be one of 'pandas' | 'votable' | 'json'
        survey : str | None
            The survey to query. If None, defaults to 'ztf'. Note: relying on
            the default (omitting the `survey` parameter) is deprecated and will be removed in
            future release; callers should explicitly pass the desired survey (e.g. `survey='ztf'`).
        index : str
            The name of the column to use as index when format is 'pandas'
        sort : str
            The name of the column to sort when format is 'pandas'

        Returns
        -------
        The magnitude statistics data in the specified format

        """
        if survey is None:
            survey = "ztf"
            warnings.warn(
                "survey not provided, defaulting to 'ztf'. This will use the legacy ZTF client. This behavior will be deprecated in future versions.",
                DeprecationWarning,
            )

        if survey == "ztf":
            return self.legacy_ztf_client.query_magstats(
                oid, format=format, index=index, sort=sort
            )
        elif survey in self.valid_surveys:
            return self.multisurvey_client.query_magstats(
                survey, oid, format=format, index=index, sort=sort
            )
        else:
            raise ValueError(f"survey must be one of {self.valid_surveys}")

    def query_probabilities(
        self,
        oid,
        format="json",
        survey: str | None = None,
        index=None,
        sort=None,
    ):
        """
        Gets all probabilities of a given object

        Parameters
        ----------
        oid : str
            The object identifier
        format : str
            Return format. Can be one of 'pandas' | 'votable' | 'json'
        survey : str | None
            The survey to query. If None, defaults to 'ztf'. Note: relying on
            the default (omitting the `survey` parameter) is deprecated and will be removed in
            future release; callers should explicitly pass the desired survey (e.g. `survey='ztf'`).
        index : str
            The name of the column to use as index when format is 'pandas'
        sort : str
            The name of the column to sort when format is 'pandas'

        Returns
        -------
        The probabilities data in the specified format

        """
        if survey is None:
            survey = "ztf"
            warnings.warn(
                "survey not provided, defaulting to 'ztf'. This will use the legacy ZTF client. This behavior will be deprecated in future versions.",
                DeprecationWarning,
            )

        if survey == "ztf":
            return self.legacy_ztf_client.query_probabilities(
                oid, format=format, index=index, sort=sort
            )
        elif survey in self.valid_surveys:
            if not hasattr(self.multisurvey_client, "query_probabilities"):
                raise NotImplementedError(
                    "Multisurvey query_probabilities not implemented."
                )
            return self.multisurvey_client.query_probabilities(
                survey, oid, format=format, index=index, sort=sort
            )
        else:
            raise ValueError(f"survey must be one of {self.valid_surveys}")

    def query_features(
        self,
        oid,
        format="json",
        survey: str | None = None,
        index=None,
        sort=None,
    ):
        """
        Gets features of a given object

        Parameters
        ----------
        oid : str
            The object identifier
        format : str
            Return format. Can be one of 'pandas' | 'votable' | 'json'
        survey : str | None
            The survey to query. If None, defaults to 'ztf'. Note: relying on
            the default (omitting the `survey` parameter) is deprecated and will be removed in
            a future release; callers should explicitly pass the desired survey (e.g. `survey='ztf'`).
        index : str
            The name of the column to use as index when format is 'pandas'
        sort : str
            The name of the column to sort when format is 'pandas'

        Returns
        -------
        The features data in the specified format
        """

        if survey is None:
            survey = "ztf"
            warnings.warn(
                "survey not provided, defaulting to 'ztf'. This will use the legacy ZTF client. This behavior will be deprecated in future versions.",
                DeprecationWarning,
            )

        if survey == "ztf":
            return self.legacy_ztf_client.query_features(
                oid, format=format, index=index, sort=sort
            )
        elif survey in self.valid_surveys:
            if not hasattr(self.multisurvey_client, "query_features"):
                raise NotImplementedError("Multisurvey query_features not implemented.")
            return self.multisurvey_client.query_features(
                survey, oid, format=format, index=index, sort=sort
            )
        else:
            raise ValueError(f"survey must be one of {self.valid_surveys}")

    def query_feature(
        self,
        oid,
        name,
        format="json",
        survey: str | None = None,
    ):
        """
        Gets a single feature of a specified object id

        Parameters
        ----------
        oid : str
            The object identifier
        name : str
            The feature's name
        format : str
            Return format. Can be one of 'pandas' | 'votable' | 'json'
        survey : str | None
            The survey to query. If None, defaults to 'ztf'. Note: relying on
            the default (omitting the `survey` parameter) is deprecated and will be removed in
            a future release; callers should explicitly pass the desired survey (e.g. `survey='ztf'`).

        Returns
        -------
        The feature data in the specified format
        """
        if survey is None:
            survey = "ztf"
            warnings.warn(
                "survey not provided, defaulting to 'ztf'. This will use the legacy ZTF client. This behavior will be deprecated in future versions.",
                DeprecationWarning,
            )

        if survey == "ztf":
            return self.legacy_ztf_client.query_feature(oid, name, format=format)
        elif survey in self.valid_surveys:
            if not hasattr(self.multisurvey_client, "query_feature"):
                raise NotImplementedError("Multisurvey query_feature not implemented.")
            return self.multisurvey_client.query_feature(
                survey, oid, name, format=format
            )
        else:
            raise ValueError(f"survey must be one of {self.valid_surveys}")

    def query_classifiers(
        self,
        format="json",
        survey: str | None = None,
        **kwargs,
    ):
        """
        Gets all classifiers and their classes

        Parameters
        ----------
        format : str
            Return format. Can be one of 'pandas' | 'votable' | 'json'
        survey : str | None
            The survey to query. If None, defaults to 'ztf'. Note: relying on
            the default (omitting the `survey` parameter) is deprecated and will be removed in
            a future release; callers should explicitly pass the desired survey (e.g. `survey='ztf'`).
        **kwargs
            Additional keyword arguments for the multisurvey API

        Returns
        -------
        The classifiers data in the specified format
        """
        if survey is None:
            survey = "ztf"
            warnings.warn(
                "survey not provided, defaulting to 'ztf'. This will use the legacy ZTF client. This behavior will be deprecated in future versions.",
                DeprecationWarning,
            )

        if survey == "ztf":
            # legacy ZTFSearch.query_classifiers signature only expects format
            return self.legacy_ztf_client.query_classifiers(format=format)
        elif survey in self.valid_surveys:
            if not hasattr(self.multisurvey_client, "query_classifiers"):
                raise NotImplementedError(
                    "Multisurvey query_classifiers not implemented."
                )
            return self.multisurvey_client.query_classifiers(
                survey, format=format, **kwargs
            )
        else:
            raise ValueError(f"survey must be one of {self.valid_surveys}")

    def query_classes(
        self,
        classifier_name,
        classifier_version,
        format="json",
        survey: str | None = None,
        **kwargs,
    ):
        """
        Gets classes from a specified classifier

        Parameters
        ----------
        classifier_name : str
            The classifier unique name
        classifier_version : str
            The classifier's version
        format : str
            Return format. Can be one of 'pandas' | 'votable' | 'json'
        survey : str | None
            The survey to query. If None, defaults to 'ztf'. Note: relying on
            the default (omitting the `survey` parameter) is deprecated and will be removed in
            a future release; callers should explicitly pass the desired survey (e.g. `survey='ztf'`).
        **kwargs
            Additional keyword arguments for the multisurvey API

        Returns
        -------
        The classes data in the specified format
        """
        if survey is None:
            survey = "ztf"
            warnings.warn(
                "survey not provided, defaulting to 'ztf'. This will use the legacy ZTF client. This behavior will be deprecated in future versions.",
                DeprecationWarning,
            )

        if survey == "ztf":
            # legacy ZTFSearch.query_classes accepts only classifier_name, classifier_version and format
            return self.legacy_ztf_client.query_classes(
                classifier_name, classifier_version, format=format
            )
        elif survey in self.valid_surveys:
            if not hasattr(self.multisurvey_client, "query_classes"):
                raise NotImplementedError("Multisurvey query_classes not implemented.")
            return self.multisurvey_client.query_classes(
                survey, classifier_name, classifier_version, format=format, **kwargs
            )
        else:
            raise ValueError(f"survey must be one of {self.valid_surveys}")
