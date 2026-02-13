from .utils import Client, load_config

import warnings


VALID_SURVEYS = ["lsst", "ztf"]


class AlerceSearchMultiSurvey(Client):
    def __init__(self):

        cfg = load_config(service="multisurvey")
        super().__init__(**cfg)

        self.url_ms = self.config["URL_MS"]
        self.routes_ms = self.config["ROUTES_MS"]

    def _get_survey_url(self, resource):
        return self.url_ms + self.routes_ms[resource]

    def _check_survey_validity(self, survey):
        if survey == "ztf":
            warnings.warn(
                "ZTF is not yet supported in the multisurvey API.", UserWarning
            )
            raise NotImplementedError(
                "ZTF is not yet supported in the multisurvey API."
            )
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
        for key in params.keys():
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

    def query_object(self, survey: str, oid, format: str = "json", **kwargs):
        self._check_survey_validity(survey)
        params = {"survey_id": survey, "oid": oid}
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
        raise NotImplementedError("Multisurvey query_magstats not implemented.")

    def query_features(
        self, survey: str, oid, format: str = "json", index=None, sort=None
    ):
        raise NotImplementedError("Multisurvey query_features not implemented.")

    def query_feature(self, survey: str, oid, name, format: str = "json", **kwargs):
        raise NotImplementedError("Multisurvey query_feature not implemented.")

    def query_classifiers(self, survey: str, format: str = "json", **kwargs):
        raise NotImplementedError("Multisurvey query_classifiers not implemented.")

    def query_classes(
        self,
        survey: str,
        classifier_name,
        classifier_version,
        format: str = "json",
        **kwargs,
    ):
        raise NotImplementedError("Multisurvey query_classes not implemented.")

    def add_band_name(self, messages):
        for message in messages:
            message["band_name"] = self.num_to_band(
                message["band_map"], message["band"]
            )
            del message["band_map"]

    def num_to_band(self, band_map, band):
        return band_map[str(band)]
