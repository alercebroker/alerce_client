import warnings

from .utils import Client, load_config

VALID_SURVEYS = ["lsst", "ztf"]

_PARAM_ALIASES = {"ndet": "n_det"}
_ORDER_BY_ALIASES = {"ndet": "n_det", "deltajd": "deltamjd"}


class AlerceSearchMultiSurvey(Client):
    def __init__(self):

        cfg = load_config(service="multisurvey")
        super().__init__(**cfg)

        self.url_ms = self.config["URL_MS"]
        self.routes_ms = self.config["ROUTES_MS"]

    def _get_survey_url(self, resource):
        return self.url_ms + self.routes_ms[resource]

    def _check_survey_validity(self, survey):
        if survey not in VALID_SURVEYS:
            raise ValueError(f"survey must be one of {VALID_SURVEYS}")

    def query_objects(
        self, survey: str, format: str = "json", index=None, sort=None, **kwargs
    ):
        valid_params = [
            "oid",
            "survey",
            "classifier",
            "class_name",
            "ranking",
            "n_det",
            "probability",
            "firstmjd",
            "lastmjd",
            "ra",
            "dec",
            "radius",
            "page",
            "page_size",
            "count",
            "order_by",
            "order_mode",
        ]
        self._check_survey_validity(survey)
        params = {"survey": survey}
        params.update(kwargs)
        for old, new in _PARAM_ALIASES.items():
            if old in params:
                warnings.warn(
                    f"Parameter '{old}' is deprecated, use '{new}' instead.",
                    DeprecationWarning,
                    stacklevel=3,
                )
                params[new] = params.pop(old)
        if "order_by" in params and params["order_by"] in _ORDER_BY_ALIASES:
            old_val = params["order_by"]
            new_val = _ORDER_BY_ALIASES[old_val]
            warnings.warn(
                f"order_by='{old_val}' is deprecated, use '{new_val}' instead.",
                DeprecationWarning,
                stacklevel=3,
            )
            params["order_by"] = new_val
        for key in params:
            if key not in valid_params:
                raise ValueError(f"Invalid parameter: {key}")
        q = self._request(
            "GET",
            url=self._get_survey_url("objects"),
            params=params,
            result_format=format,
            response_field=None,
        )
        q.json_result = q.json_result["items"]
        return q.result(index, sort)

    def query_object(
        self,
        survey: str,
        oid,
        format: str = "json",
        return_survey_extra: bool = True,
        **kwargs,
    ):
        self._check_survey_validity(survey)
        params = {"survey_id": survey, "oid": oid}
        if return_survey_extra:
            params["return_survey_extra"] = True
        params.update(kwargs)
        q = self._request(
            "GET",
            url=self._get_survey_url("single_object"),
            params=params,
            result_format=format,
            response_field=None,
        )
        return q.result()

    def query_lightcurve(self, survey: str, oid, format: str = "json"):
        self._check_survey_validity(survey)
        params = {"survey_id": survey, "oid": oid}
        q = self._request(
            "GET",
            url=self._get_survey_url("lightcurve"),
            params=params,
            result_format=format,
            response_field=None,
        )
        for key in q.json_result.keys():
            self.add_band_name(q.json_result[key])
        return q.result()

    def query_detections(
        self,
        survey: str,
        oid: int,
        format: str = "json",
        index=None,
        sort=None,
    ):
        self._check_survey_validity(survey)

        params = {"survey_id": survey, "oid": oid}

        q = self._request(
            "GET",
            url=self._get_survey_url("detections"),
            params=params,
            result_format=format,
            response_field=None,
        )
        self.add_band_name(q.json_result)
        return q.result(index, sort)

    def query_non_detections(
        self, survey: str, oid, format: str = "json", index=None, sort=None
    ):
        self._check_survey_validity(survey)
        params = {"survey_id": survey, "oid": oid}

        q = self._request(
            "GET",
            url=self._get_survey_url("non_detections"),
            params=params,
            result_format=format,
            response_field=None,
        )
        self.add_band_name(q.json_result)
        return q.result(index, sort)

    def query_forced_photometry(
        self, survey: str, oid, format: str = "json", index=None, sort=None
    ):
        self._check_survey_validity(survey)
        params = {"survey_id": survey, "oid": oid}

        q = self._request(
            "GET",
            url=self._get_survey_url("forced_photometry"),
            params=params,
            result_format=format,
            response_field=None,
        )
        self.add_band_name(q.json_result)
        return q.result(index, sort)

    def query_probabilities(
        self, survey: str, oid, format: str = "json", index=None, sort=None
    ):
        self._check_survey_validity(survey)
        params = {"survey_id": survey, "oid": oid}

        url = self._get_survey_url("probabilities")

        q = self._request(
            "GET",
            url=url,
            params=params,
            result_format=format,
            response_field=None,
        )

        return q.result(index, sort)

    def query_magstats(
        self, survey: str, oid, format: str = "json", index=None, sort=None
    ):
        self._check_survey_validity(survey)
        params = {"survey_id": survey, "oid": oid}
        q = self._request(
            "GET",
            url=self._get_survey_url("magstats"),
            params=params,
            result_format=format,
            response_field=None,
        )
        return q.result(index, sort)

    def query_features(
        self, survey: str, oid, format: str = "json", index=None, sort=None
    ):
        self._check_survey_validity(survey)
        params = {"survey_id": survey, "oid": oid}
        q = self._request(
            "GET",
            url=self._get_survey_url("features"),
            params=params,
            result_format=format,
            response_field=None,
        )
        return q.result(index, sort)

    def query_feature(self, survey: str, oid, name, format: str = "json", **kwargs):
        self._check_survey_validity(survey)
        params = {"survey_id": survey, "oid": oid, "name": name}
        params.update(kwargs)
        q = self._request(
            "GET",
            url=self._get_survey_url("features"),
            params=params,
            result_format=format,
            response_field=None,
        )
        return q.result()

    def query_classifiers(self, survey: str, format: str = "json", **kwargs):
        self._check_survey_validity(survey)
        params = {"survey_id": survey}
        params.update(kwargs)
        q = self._request(
            "GET",
            url=self._get_survey_url("classifiers"),
            params=params,
            result_format=format,
            response_field=None,
        )
        return q.result()

    def query_classes(
        self,
        survey: str,
        classifier_name,
        classifier_version,
        format: str = "json",
        **kwargs,
    ):
        self._check_survey_validity(survey)
        params = {
            "classifier_name": classifier_name,
            "classifier_version": classifier_version,
        }
        params.update(kwargs)
        q = self._request(
            "GET",
            url=self._get_survey_url("classes"),
            params=params,
            result_format=format,
            response_field=None,
        )
        return q.result()

    def add_band_name(self, messages):
        for message in messages:
            message["band_name"] = self.num_to_band(
                message["band_map"], message["band"]
            )
            del message["band_map"]

    def num_to_band(self, band_map, band):
        return band_map[str(band)]
