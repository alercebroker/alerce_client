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


def test_query_lightcurve_ztf_legacy(client):
    with pytest.warns(DeprecationWarning):
        result = client.query_lightcurve(ZTF_OID)
    print("Legacy ZTF lightcurve:", result)
    assert result is not None


def test_query_lightcurve_lsst(client):
    result = client.query_lightcurve(LSST_OID, survey="lsst")
    assert set(result) == {"detections", "non_detections", "forced_photometry"}
    assert len(result["detections"]) > 0
    assert len(result["forced_photometry"]) > 0
    for key in ("detections", "forced_photometry"):
        assert {d["oid"] for d in result[key]} == {LSST_OID}


def test_query_lightcurve_lsst_missing_oid(client):
    with pytest.raises(ObjectNotFoundError):
        client.query_lightcurve(LSST_MISSING_OID, survey="lsst")


def test_query_lightcurve_lsst_missing_oid_list(client):
    result = client.query_lightcurve(
        [LSST_MISSING_OID, LSST_MISSING_OID + 1], survey="lsst"
    )
    assert result == {"detections": [], "non_detections": [], "forced_photometry": []}


def test_query_lightcurve_invalid_survey(client):
    with pytest.raises(ValueError):
        client.query_lightcurve(ZTF_OID, survey="invalid")
