"""Tests for the ztf_backend opt-in mechanism.

``Alerce(ztf_backend="multisurvey")`` routes ``survey="ztf"`` calls through
the multisurvey client instead of the legacy ZTF client.  Without it (or
with ``ztf_backend="legacy"``), all ZTF calls go through the legacy client
as before.
"""

from unittest.mock import MagicMock

import pytest

from alerce import Alerce

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

    @pytest.fixture()
    def client(self):
        c = Alerce()
        _mock_search(c)
        return c

    def test_ztf_routes_to_legacy(self, client, method):
        getattr(client, method)(survey="ztf", **SEARCH_METHODS[method])
        getattr(client.legacy_ztf_client, method).assert_called_once()
        getattr(client.multisurvey_client, method).assert_not_called()

    def test_survey_none_routes_to_legacy(self, client, method):
        with pytest.warns(DeprecationWarning):
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

    @pytest.fixture()
    def client(self):
        c = Alerce()
        _mock_stamps(c)
        return c

    def test_ztf_routes_to_legacy(self, client, spec):
        common, leg, ms, kwargs = spec
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
