import pytest
from alerce.core import Alerce
from alerce.exceptions import ObjectNotFoundError


@pytest.fixture
def client():
    return Alerce()


ZTF_OID = "ZTF18abeqwzl"
# Verified on api-lsst.alerce.online and Fink/LSST (2026-11-05).
LSST_OID = 313721466436714578
# Not in the database: a single missing OID returns 404, a list returns empty.
LSST_MISSING_OID = 169298433191444990


def test_query_non_detections_ztf_legacy_signature(client):
    # Test the legacy signature without survey parameter
    # It should default to ZTF but raise a deprecation warning
    with pytest.warns(DeprecationWarning):
        result = client.query_non_detections(ZTF_OID)
    print("ZTF non-detections (legacy signature):", result)
    assert result is not None


def test_query_non_detections_ztf(client):
    result = client.query_non_detections(ZTF_OID, survey="ztf")
    print("ZTF non-detections:", result)
    assert result is not None


def test_query_non_detections_lsst(client):
    # LSST alerts carry no non-detections (n_non_det is 0 for every LSST
    # object), so an existing object returns an empty list rather than 404.
    result = client.query_non_detections(LSST_OID, survey="lsst")
    assert result == []


def test_query_non_detections_lsst_missing_oid(client):
    with pytest.raises(ObjectNotFoundError):
        client.query_non_detections(LSST_MISSING_OID, survey="lsst")


def test_query_non_detections_lsst_missing_oid_list(client):
    result = client.query_non_detections(
        [LSST_MISSING_OID, LSST_MISSING_OID + 1], survey="lsst"
    )
    assert result == []


def test_query_non_detections_invalid_survey(client):
    with pytest.raises(ValueError):
        client.query_non_detections(ZTF_OID, survey="invalid_survey")
