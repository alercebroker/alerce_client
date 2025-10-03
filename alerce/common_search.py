from .ztf_search import ZTFSearch
from .ms_search import AlerceSearchMultiSurvey
from .utils import Client

# Problemas con esta solucion, el manejo de los kwargs
# para cada cliente es diferente, y no se pueden mezclar
#   Se puede normalizar esto -> agregar kwars en cada cliente
#   si lo usa bien, pero que no falle por agregarlos
# ademas de que no todos los clientes tienen los mismos metodos
#   Se puede hacer un catch de los metodos que no existan


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
        use_multisurvey_api: bool = False,
        survey: str | None = None,
        **kwargs
    ):
        if use_multisurvey_api:
            if survey is None:
                raise ValueError(
                    "survey must be provided when use_multisurvey_api is True"
                )
            return self.multisurvey_client.query_objects(
                survey=survey, format=format, index=index, sort=sort, **kwargs
            )
        else:
            return self.legacy_ztf_client.query_objects(
                format=format, index=index, sort=sort, **kwargs
            )

    def query_object(
        self,
        oid,
        format="json",
        use_multisurvey_api: bool = False,
        survey: str | None = None,
        **kwargs
    ):
        if use_multisurvey_api:
            if survey is None:
                raise ValueError(
                    "survey must be provided when use_multisurvey_api is True"
                )
            if not hasattr(self.multisurvey_client, "query_object"):
                raise NotImplementedError("Multisurvey query_object not implemented.")
            return self.multisurvey_client.query_object(
                survey=survey, oid=oid, format=format, **kwargs
            )
        else:
            return self.legacy_ztf_client.query_object(oid, format=format, **kwargs)

    def query_lightcurve(
        self,
        oid,
        format="json",
        use_multisurvey_api: bool = False,
        survey: str | None = None,
        **kwargs
    ):
        if use_multisurvey_api:
            if survey is None:
                raise ValueError(
                    "survey must be provided when use_multisurvey_api is True"
                )
            return self.multisurvey_client.query_lightcurve(
                survey=survey, oid=oid, format=format, **kwargs
            )
        else:
            return self.legacy_ztf_client.query_lightcurve(oid, format=format, **kwargs)

    def query_detections(
        self,
        oid: str | int,
        format: str = "json",
        use_multisurvey_api: bool = False,
        survey: str | None = None,
        index=None,
        sort=None,
        **kwargs
    ):
        if use_multisurvey_api:
            if survey is None:
                raise ValueError(
                    "survey must be provided when use_multisurvey_api is True"
                )
            return self.multisurvey_client.query_detections(
                survey, oid, format=format, index=index, sort=sort, **kwargs
            )
        else:
            return self.legacy_ztf_client.query_detections(
                oid, format=format, index=index, sort=sort, **kwargs
            )

    def query_non_detections(
        self,
        oid,
        format="json",
        use_multisurvey_api: bool = False,
        survey: str | None = None,
        index=None,
        sort=None,
        **kwargs
    ):
        if use_multisurvey_api:
            if survey is None:
                raise ValueError(
                    "survey must be provided when use_multisurvey_api is True"
                )
            return self.multisurvey_client.query_non_detections(
                survey=survey, oid=oid, format=format, index=index, sort=sort, **kwargs
            )
        else:
            return self.legacy_ztf_client.query_non_detections(
                oid, format=format, index=index, sort=sort, **kwargs
            )

    def query_forced_photometry(
        self,
        oid,
        format="json",
        use_multisurvey_api: bool = False,
        survey: str | None = None,
        index=None,
        sort=None,
        **kwargs
    ):
        if use_multisurvey_api:
            if survey is None:
                raise ValueError(
                    "survey must be provided when use_multisurvey_api is True"
                )
            return self.multisurvey_client.query_forced_photometry(
                survey=survey, oid=oid, format=format, index=index, sort=sort, **kwargs
            )
        else:
            return self.legacy_ztf_client.query_forced_photometry(
                oid, format=format, index=index, sort=sort, **kwargs
            )

    def query_magstats(
        self,
        oid,
        format="json",
        use_multisurvey_api: bool = False,
        survey: str | None = None,
        index=None,
        sort=None,
        **kwargs
    ):
        if use_multisurvey_api:
            if survey is None:
                raise ValueError(
                    "survey must be provided when use_multisurvey_api is True"
                )
            return self.multisurvey_client.query_magstats(
                survey=survey, oid=oid, format=format, index=index, sort=sort, **kwargs
            )
        else:
            return self.legacy_ztf_client.query_magstats(
                oid, format=format, index=index, sort=sort, **kwargs
            )

    def query_probabilities(
        self,
        oid,
        format="json",
        use_multisurvey_api: bool = False,
        survey: str | None = None,
        index=None,
        sort=None,
        **kwargs
    ):
        if use_multisurvey_api:
            if survey is None:
                raise ValueError(
                    "survey must be provided when use_multisurvey_api is True"
                )
            if not hasattr(self.multisurvey_client, "query_probabilities"):
                raise NotImplementedError(
                    "Multisurvey query_probabilities not implemented."
                )
            return self.multisurvey_client.query_probabilities(
                survey=survey, oid=oid, format=format, index=index, sort=sort, **kwargs
            )
        else:
            return self.legacy_ztf_client.query_probabilities(
                oid, format=format, index=index, sort=sort, **kwargs
            )

    def query_features(
        self,
        oid,
        format="json",
        use_multisurvey_api: bool = False,
        survey: str | None = None,
        index=None,
        sort=None,
        **kwargs
    ):
        if use_multisurvey_api:
            if survey is None:
                raise ValueError(
                    "survey must be provided when use_multisurvey_api is True"
                )
            if not hasattr(self.multisurvey_client, "query_features"):
                raise NotImplementedError("Multisurvey query_features not implemented.")
            return self.multisurvey_client.query_features(
                survey=survey, oid=oid, format=format, index=index, sort=sort, **kwargs
            )
        else:
            return self.legacy_ztf_client.query_features(
                oid, format=format, index=index, sort=sort, **kwargs
            )

    def query_feature(
        self,
        oid,
        name,
        format="json",
        use_multisurvey_api: bool = False,
        survey: str | None = None,
        **kwargs
    ):
        if use_multisurvey_api:
            if survey is None:
                raise ValueError(
                    "survey must be provided when use_multisurvey_api is True"
                )
            if not hasattr(self.multisurvey_client, "query_feature"):
                raise NotImplementedError("Multisurvey query_feature not implemented.")
            return self.multisurvey_client.query_feature(
                survey=survey, oid=oid, name=name, format=format, **kwargs
            )
        else:
            return self.legacy_ztf_client.query_feature(
                oid, name, format=format, **kwargs
            )

    def query_classifiers(
        self,
        format="json",
        use_multisurvey_api: bool = False,
        survey: str | None = None,
        **kwargs
    ):
        if use_multisurvey_api:
            if survey is None:
                raise ValueError(
                    "survey must be provided when use_multisurvey_api is True"
                )
            if not hasattr(self.multisurvey_client, "query_classifiers"):
                raise NotImplementedError(
                    "Multisurvey query_classifiers not implemented."
                )
            return self.multisurvey_client.query_classifiers(
                survey=survey, format=format, **kwargs
            )
        else:
            return self.legacy_ztf_client.query_classifiers(format=format, **kwargs)

    def query_classes(
        self,
        classifier_name,
        classifier_version,
        format="json",
        use_multisurvey_api: bool = False,
        survey: str | None = None,
        **kwargs
    ):
        if use_multisurvey_api:
            if survey is None:
                raise ValueError(
                    "survey must be provided when use_multisurvey_api is True"
                )
            if not hasattr(self.multisurvey_client, "query_classes"):
                raise NotImplementedError("Multisurvey query_classes not implemented.")
            return self.multisurvey_client.query_classes(
                survey=survey,
                classifier_name=classifier_name,
                classifier_version=classifier_version,
                format=format,
                **kwargs
            )
        else:
            return self.legacy_ztf_client.query_classes(
                classifier_name, classifier_version, format=format, **kwargs
            )
