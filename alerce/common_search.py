from .ztf_search import ZTFSearch
from .ms_search import AlerceSearchMultiSurvey
from .utils import Client
import warnings


class AlerceCommonSearch(Client):

    def __init__(self, **kwargs):
        ztf_config = kwargs.get("ztf_config", {})
        lsst_config = kwargs.get("lsst_config", {})
        self.legacy_ztf_client = ZTFSearch(**ztf_config)
        self.multisurvey_client = AlerceSearchMultiSurvey(**lsst_config)
        self.valid_surveys = ["ztf", "lsst"]

    def query_objects(
        self,
        format="pandas",
        index=None,
        sort=None,
        survey: str | None = None,
        **kwargs,
    ):
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
        if survey is None:
            survey = "ztf"
            warnings.warn(
                "survey not provided, defaulting to 'ztf'. This will use the legacy ZTF client. This behavior will be deprecated in future versions.",
                DeprecationWarning,
            )

        if survey == "ztf":
            return self.legacy_ztf_client.query_object(oid, format=format, **kwargs)
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
        if survey is None:
            survey = "ztf"
            warnings.warn(
                "survey not provided, defaulting to 'ztf'. This will use the legacy ZTF client. This behavior will be deprecated in future versions.",
                DeprecationWarning,
            )

        if survey == "ztf":
            return self.legacy_ztf_client.query_classifiers(format=format, **kwargs)
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
        if survey is None:
            survey = "ztf"
            warnings.warn(
                "survey not provided, defaulting to 'ztf'. This will use the legacy ZTF client. This behavior will be deprecated in future versions.",
                DeprecationWarning,
            )

        if survey == "ztf":
            return self.legacy_ztf_client.query_classes(
                classifier_name, classifier_version, format=format, **kwargs
            )
        elif survey in self.valid_surveys:
            if not hasattr(self.multisurvey_client, "query_classes"):
                raise NotImplementedError("Multisurvey query_classes not implemented.")
            return self.multisurvey_client.query_classes(
                survey, classifier_name, classifier_version, format=format, **kwargs
            )
        else:
            raise ValueError(f"survey must be one of {self.valid_surveys}")
