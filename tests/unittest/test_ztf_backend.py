"""Tests for the ztf_backend opt-in mechanism.

``Alerce(ztf_backend="multisurvey")`` routes ``survey="ztf"`` calls through
the multisurvey client instead of the legacy ZTF client.  Without it (or
with ``ztf_backend="legacy"``), all ZTF calls go through the legacy client
as before.
"""

from unittest.mock import MagicMock, patch

import pytest

from alerce import Alerce
from alerce.common_search import AlerceCommonSearch
from alerce.ms_search import AlerceSearchMultiSurvey

ZTF_OID = "ZTF18abeqwzl"

# {method: extra kwargs beyond survey}
SEARCH_METHODS = {
    "query_objects": {},
    "query_object": {"oid": ZTF_OID},
    "query_lightcurve": {"oid": ZTF_OID},
    "query_detections": {"oid": ZTF_OID},
    "query_non_detections": {"oid": ZTF_OID},
    "query_forced_photometry": {"oid": ZTF_OID},
    "query_probabilities": {"oid": ZTF_OID},
    "query_magstats": {"oid": ZTF_OID},
    "query_features": {"oid": ZTF_OID},
    "query_feature": {"oid": ZTF_OID, "name": "Amplitude"},
    "query_classifiers": {},
    "query_classes": {
        "classifier_name": "lc_classifier",
        "classifier_version": "1.0.0",
    },
}

# (common_method, legacy_method, ms_method, kwargs)
STAMP_METHODS = [
    (
        "plot_stamps",
        "plot_stamps",
        "multisurvey_plot_stamps",
        {"oid": ZTF_OID, "candid": 123},
    ),
    (
        "get_stamps",
        "get_stamps",
        "multisurvey_get_stamps",
        {"oid": ZTF_OID, "candid": 123},
    ),
]


def _mock_search(client):
    for m in SEARCH_METHODS:
        setattr(client.legacy_ztf_client, m, MagicMock(return_value=[]))
        setattr(client.multisurvey_client, m, MagicMock(return_value=[]))


def _mock_stamps(client):
    for _, leg, ms, _ in STAMP_METHODS:
        setattr(client.legacy_stamps_client, leg, MagicMock(return_value=[]))
        setattr(client.multisurvey_stamps_client, ms, MagicMock(return_value=[]))


class TestInit:
    def test_default_is_legacy(self):
        assert Alerce().ztf_backend == "legacy"

    def test_explicit_legacy(self):
        assert Alerce(ztf_backend="legacy").ztf_backend == "legacy"

    def test_multisurvey(self):
        assert Alerce(ztf_backend="multisurvey").ztf_backend == "multisurvey"

    def test_invalid_raises(self):
        with pytest.raises(ValueError, match="ztf_backend"):
            Alerce(ztf_backend="bogus")


class TestSearchLegacy:
    """Default: survey='ztf' -> legacy client."""

    @pytest.fixture(params=list(SEARCH_METHODS))
    def method(self, request):
        return request.param

    @pytest.fixture(autouse=True)
    def _reset_legacy_warned(self):
        AlerceCommonSearch._legacy_ztf_warned = False

    @pytest.fixture()
    def client(self):
        c = Alerce()
        _mock_search(c)
        return c

    def test_ztf_routes_to_legacy(self, client, method):
        with pytest.warns(FutureWarning, match="default ZTF backend will change"):
            getattr(client, method)(survey="ztf", **SEARCH_METHODS[method])
        getattr(client.legacy_ztf_client, method).assert_called_once()
        getattr(client.multisurvey_client, method).assert_not_called()

    def test_survey_none_routes_to_legacy(self, client, method):
        with pytest.warns((DeprecationWarning, FutureWarning)):
            getattr(client, method)(survey=None, **SEARCH_METHODS[method])
        getattr(client.legacy_ztf_client, method).assert_called_once()
        getattr(client.multisurvey_client, method).assert_not_called()


class TestSearchMultisurvey:
    """Opt-in: survey='ztf' -> multisurvey client."""

    @pytest.fixture(params=list(SEARCH_METHODS))
    def method(self, request):
        return request.param

    @pytest.fixture()
    def client(self):
        c = Alerce(ztf_backend="multisurvey")
        _mock_search(c)
        return c

    def test_ztf_routes_to_multisurvey(self, client, method):
        getattr(client, method)(survey="ztf", **SEARCH_METHODS[method])
        getattr(client.multisurvey_client, method).assert_called_once()
        getattr(client.legacy_ztf_client, method).assert_not_called()

    def test_survey_none_routes_to_multisurvey(self, client, method):
        with pytest.warns(DeprecationWarning):
            getattr(client, method)(survey=None, **SEARCH_METHODS[method])
        getattr(client.multisurvey_client, method).assert_called_once()
        getattr(client.legacy_ztf_client, method).assert_not_called()


class TestStampsLegacy:
    """Default: survey='ztf' stamps -> legacy stamps client."""

    @pytest.fixture(params=STAMP_METHODS, ids=[s[0] for s in STAMP_METHODS])
    def spec(self, request):
        return request.param

    @pytest.fixture(autouse=True)
    def _reset_legacy_warned(self):
        AlerceCommonSearch._legacy_ztf_warned = False

    @pytest.fixture()
    def client(self):
        c = Alerce()
        _mock_stamps(c)
        return c

    def test_ztf_routes_to_legacy(self, client, spec):
        common, leg, ms, kwargs = spec
        with pytest.warns(FutureWarning, match="default ZTF backend will change"):
            getattr(client, common)(survey="ztf", **kwargs)
        getattr(client.legacy_stamps_client, leg).assert_called_once()
        getattr(client.multisurvey_stamps_client, ms).assert_not_called()


class TestStampsMultisurvey:
    """Opt-in: survey='ztf' stamps -> multisurvey stamps client."""

    @pytest.fixture(params=STAMP_METHODS, ids=[s[0] for s in STAMP_METHODS])
    def spec(self, request):
        return request.param

    @pytest.fixture()
    def client(self):
        c = Alerce(ztf_backend="multisurvey")
        _mock_stamps(c)
        return c

    def test_ztf_routes_to_multisurvey(self, client, spec):
        common, leg, ms, kwargs = spec
        getattr(client, common)(survey="ztf", **kwargs)
        getattr(client.multisurvey_stamps_client, ms).assert_called_once()
        getattr(client.legacy_stamps_client, leg).assert_not_called()


class TestMultisurveyGuardRemoval:
    """The multisurvey clients should accept 'ztf' as a valid survey."""

    def test_search_accepts_ztf(self):
        client = Alerce()
        client.multisurvey_client._check_survey_validity("ztf")

    def test_stamps_accepts_ztf(self):
        client = Alerce()
        client.multisurvey_stamps_client._check_survey_validity("ztf")


class TestMsSearchMagstats:
    """Unit tests for AlerceSearchMultiSurvey.query_magstats."""

    @pytest.fixture()
    def ms(self):
        return AlerceSearchMultiSurvey()

    def test_calls_request_with_correct_params(self, ms):
        mock_result = MagicMock()
        mock_result.result.return_value = [{"magmean": 18.5, "band": "g"}]
        with patch.object(ms, "_request", return_value=mock_result) as req:
            ms.query_magstats("ztf", ZTF_OID)
            req.assert_called_once_with(
                "GET",
                url=ms._get_survey_url("magstats"),
                params={"survey_id": "ztf", "oid": ZTF_OID},
                result_format="json",
                response_field=None,
            )

    def test_passes_format_and_index_sort(self, ms):
        mock_result = MagicMock()
        with patch.object(ms, "_request", return_value=mock_result):
            ms.query_magstats(
                "ztf", ZTF_OID, format="pandas", index="band", sort="magmean"
            )
            mock_result.result.assert_called_once_with("band", "magmean")

    def test_rejects_invalid_survey(self, ms):
        with pytest.raises(ValueError, match="survey must be one of"):
            ms.query_magstats("invalid", ZTF_OID)


class TestMsSearchFeatures:
    """Unit tests for AlerceSearchMultiSurvey.query_features."""

    @pytest.fixture()
    def ms(self):
        return AlerceSearchMultiSurvey()

    def test_calls_request_with_correct_params(self, ms):
        mock_result = MagicMock()
        mock_result.result.return_value = [{"name": "Amplitude", "value": 0.5}]
        with patch.object(ms, "_request", return_value=mock_result) as req:
            ms.query_features("ztf", ZTF_OID)
            req.assert_called_once_with(
                "GET",
                url=ms._get_survey_url("features"),
                params={"survey_id": "ztf", "oid": ZTF_OID},
                result_format="json",
                response_field=None,
            )

    def test_passes_format_and_index_sort(self, ms):
        mock_result = MagicMock()
        with patch.object(ms, "_request", return_value=mock_result):
            ms.query_features(
                "ztf", ZTF_OID, format="pandas", index="name", sort="value"
            )
            mock_result.result.assert_called_once_with("name", "value")

    def test_rejects_invalid_survey(self, ms):
        with pytest.raises(ValueError, match="survey must be one of"):
            ms.query_features("invalid", ZTF_OID)


class TestMsSearchFeature:
    """Unit tests for AlerceSearchMultiSurvey.query_feature (single feature)."""

    @pytest.fixture()
    def ms(self):
        return AlerceSearchMultiSurvey()

    def test_calls_request_with_name_param(self, ms):
        mock_result = MagicMock()
        mock_result.result.return_value = [{"name": "Amplitude", "value": 0.5}]
        with patch.object(ms, "_request", return_value=mock_result) as req:
            ms.query_feature("ztf", ZTF_OID, "Amplitude")
            req.assert_called_once_with(
                "GET",
                url=ms._get_survey_url("features"),
                params={"survey_id": "ztf", "oid": ZTF_OID, "name": "Amplitude"},
                result_format="json",
                response_field=None,
            )

    def test_rejects_invalid_survey(self, ms):
        with pytest.raises(ValueError, match="survey must be one of"):
            ms.query_feature("invalid", ZTF_OID, "Amplitude")


class TestMsSearchClassifiers:
    """Unit tests for AlerceSearchMultiSurvey.query_classifiers."""

    @pytest.fixture()
    def ms(self):
        return AlerceSearchMultiSurvey()

    def test_calls_request_with_survey_id(self, ms):
        mock_result = MagicMock()
        mock_result.result.return_value = [{"classifier_name": "lc_classifier"}]
        with patch.object(ms, "_request", return_value=mock_result) as req:
            ms.query_classifiers("ztf")
            req.assert_called_once_with(
                "GET",
                url=ms._get_survey_url("classifiers"),
                params={"survey_id": "ztf"},
                result_format="json",
                response_field=None,
            )

    def test_forwards_classifier_name_kwarg(self, ms):
        mock_result = MagicMock()
        with patch.object(ms, "_request", return_value=mock_result) as req:
            ms.query_classifiers("ztf", classifier_name="lc_classifier")
            _, kwargs = req.call_args
            assert kwargs["params"]["classifier_name"] == "lc_classifier"

    def test_rejects_invalid_survey(self, ms):
        with pytest.raises(ValueError, match="survey must be one of"):
            ms.query_classifiers("invalid")


class TestMsSearchClasses:
    """Unit tests for AlerceSearchMultiSurvey.query_classes."""

    @pytest.fixture()
    def ms(self):
        return AlerceSearchMultiSurvey()

    def test_calls_request_with_classifier_params(self, ms):
        mock_result = MagicMock()
        mock_result.result.return_value = [{"name": "SNIa"}]
        with patch.object(ms, "_request", return_value=mock_result) as req:
            ms.query_classes("ztf", "lc_classifier", "2.2.0")
            req.assert_called_once_with(
                "GET",
                url=ms._get_survey_url("classes"),
                params={
                    "classifier_name": "lc_classifier",
                    "classifier_version": "2.2.0",
                },
                result_format="json",
                response_field=None,
            )

    def test_rejects_invalid_survey(self, ms):
        with pytest.raises(ValueError, match="survey must be one of"):
            ms.query_classes("invalid", "lc_classifier", "2.2.0")


class TestMsSearchQueryObjectsAliases:
    """Legacy param aliases in AlerceSearchMultiSurvey.query_objects."""

    @pytest.fixture()
    def ms(self):
        return AlerceSearchMultiSurvey()

    def test_ndet_aliased_to_n_det(self, ms):
        mock_result = MagicMock()
        mock_result.json_result = {"items": []}
        mock_result.result.return_value = []
        with patch.object(ms, "_request", return_value=mock_result) as req:
            with pytest.warns(DeprecationWarning, match="ndet.*n_det"):
                ms.query_objects("ztf", ndet=[10, 50])
            _, call_kwargs = req.call_args
            assert call_kwargs["params"]["n_det"] == [10, 50]
            assert "ndet" not in call_kwargs["params"]

    def test_order_by_ndet_aliased(self, ms):
        mock_result = MagicMock()
        mock_result.json_result = {"items": []}
        mock_result.result.return_value = []
        with patch.object(ms, "_request", return_value=mock_result) as req:
            with pytest.warns(DeprecationWarning, match="ndet.*n_det"):
                ms.query_objects("ztf", order_by="ndet")
            _, call_kwargs = req.call_args
            assert call_kwargs["params"]["order_by"] == "n_det"

    def test_order_by_deltajd_aliased(self, ms):
        mock_result = MagicMock()
        mock_result.json_result = {"items": []}
        mock_result.result.return_value = []
        with patch.object(ms, "_request", return_value=mock_result) as req:
            with pytest.warns(DeprecationWarning, match="deltajd.*deltamjd"):
                ms.query_objects("ztf", order_by="deltajd")
            _, call_kwargs = req.call_args
            assert call_kwargs["params"]["order_by"] == "deltamjd"

    def test_n_det_passes_without_warning(self, ms):
        mock_result = MagicMock()
        mock_result.json_result = {"items": []}
        mock_result.result.return_value = []
        with patch.object(ms, "_request", return_value=mock_result):
            import warnings as w
            with w.catch_warnings():
                w.simplefilter("error", DeprecationWarning)
                ms.query_objects("ztf", n_det=[10, 50])


class TestReturnSurveyExtra:
    """return_survey_extra param on query_object."""

    @pytest.fixture()
    def ms(self):
        return AlerceSearchMultiSurvey()

    def test_true_by_default(self, ms):
        mock_result = MagicMock()
        with patch.object(ms, "_request", return_value=mock_result) as req:
            ms.query_object("ztf", ZTF_OID)
            _, call_kwargs = req.call_args
            assert call_kwargs["params"]["return_survey_extra"] is True

    def test_false_omits_param(self, ms):
        mock_result = MagicMock()
        with patch.object(ms, "_request", return_value=mock_result) as req:
            ms.query_object("ztf", ZTF_OID, return_survey_extra=False)
            _, call_kwargs = req.call_args
            assert "return_survey_extra" not in call_kwargs["params"]

    def test_routes_through_common_search(self):
        client = Alerce(ztf_backend="multisurvey")
        _mock_search(client)
        client.query_object(ZTF_OID, survey="ztf", return_survey_extra=True)
        client.multisurvey_client.query_object.assert_called_once()
        _, call_kwargs = client.multisurvey_client.query_object.call_args
        assert call_kwargs["return_survey_extra"] is True

    def test_ignored_by_legacy(self):
        client = Alerce(ztf_backend="legacy")
        _mock_search(client)
        AlerceCommonSearch._legacy_ztf_warned = False
        with pytest.warns(FutureWarning):
            client.query_object(ZTF_OID, survey="ztf", return_survey_extra=True)
        client.legacy_ztf_client.query_object.assert_called_once()
        _, call_kwargs = client.legacy_ztf_client.query_object.call_args
        assert "return_survey_extra" not in call_kwargs
