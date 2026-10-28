"""Integration tests for ZTF queries through the multisurvey backend.

Requires the multisurvey API to support ZTF (fixes deployed).
To run against staging during development:

    ALERCE_CONFIG_PATH=staging_config.json pytest tests/integration/test_ztf_multisurvey.py -v
"""

import numpy as np
import pytest
from pandas import DataFrame

from alerce.core import Alerce

ZTF_OID: str = "ZTF18abbrrty"
ZTF_CANDID: int = 547355426215010007


@pytest.fixture
def ms_client() -> Alerce:
    return Alerce(ztf_backend="multisurvey")


@pytest.fixture
def legacy_client() -> Alerce:
    return Alerce()


# -- Acceptance: default behavior unchanged (#1) ----------------------------


def test_default_detections_have_legacy_fields(legacy_client: Alerce) -> None:
    result: list[dict] = legacy_client.query_detections(ZTF_OID, survey="ztf")
    det: dict = result[0]
    assert "candid" in det
    assert "fid" in det
    assert "measurement_id" not in det


def test_default_object_has_legacy_fields(legacy_client: Alerce) -> None:
    result: dict = legacy_client.query_object(ZTF_OID, survey="ztf")
    assert "ndet" in result or "meanra" in result
    assert "survey_id" not in result or "sid" not in result


# -- Acceptance: opt-in returns multisurvey data (#2) -----------------------


def test_ms_query_objects(ms_client: Alerce) -> None:
    result: list[dict] = ms_client.query_objects(
        survey="ztf", format="json", page_size=3
    )
    assert isinstance(result, list)
    assert len(result) > 0
    item: dict = result[0]
    assert "oid" in item
    assert "n_det" in item
    assert "firstmjd" in item
    assert "sid" in item


def test_ms_query_object(ms_client: Alerce) -> None:
    obj: dict = ms_client.query_object(ZTF_OID, survey="ztf")
    assert obj["n_det"] > 0
    assert obj["n_forced"] > 0
    assert obj["n_non_det"] > 0
    assert "sid" in obj
    assert "firstmjd" in obj


def test_ms_detections_have_multisurvey_fields(ms_client: Alerce) -> None:
    dets: list[dict] = ms_client.query_detections(ZTF_OID, survey="ztf")
    assert len(dets) > 0
    det: dict = dets[0]
    for field in ("measurement_id", "survey_id", "band_name", "mjd", "magpsf"):
        assert field in det, f"missing field: {field}"
    assert "candid" not in det
    assert "fid" not in det


def test_ms_non_detections(ms_client: Alerce) -> None:
    nds: list[dict] = ms_client.query_non_detections(ZTF_OID, survey="ztf")
    assert len(nds) > 0
    nd: dict = nds[0]
    for field in ("mjd", "band_name", "diffmaglim", "survey_id"):
        assert field in nd, f"missing field: {field}"


def test_ms_forced_photometry(ms_client: Alerce) -> None:
    fps: list[dict] = ms_client.query_forced_photometry(ZTF_OID, survey="ztf")
    assert len(fps) > 0
    fp: dict = fps[0]
    for field in ("measurement_id", "mjd", "band_name", "mag", "e_mag"):
        assert field in fp, f"missing field: {field}"


def test_ms_lightcurve_structure(ms_client: Alerce) -> None:
    lc: dict = ms_client.query_lightcurve(ZTF_OID, survey="ztf")
    assert isinstance(lc, dict)
    for key in ("detections", "non_detections", "forced_photometry"):
        assert key in lc, f"missing lightcurve key: {key}"
        assert isinstance(lc[key], list)
    assert len(lc["detections"]) > 0


def test_ms_probabilities(ms_client: Alerce) -> None:
    probs: list[dict] = ms_client.query_probabilities(ZTF_OID, survey="ztf")
    assert len(probs) > 0
    prob: dict = probs[0]
    for field in (
        "classifier_name",
        "classifier_version",
        "class_name",
        "probability",
        "ranking",
    ):
        assert field in prob, f"missing field: {field}"


# -- Acceptance: string OIDs accepted (#3) ----------------------------------


def test_string_oid_object(ms_client: Alerce) -> None:
    obj: dict = ms_client.query_object(ZTF_OID, survey="ztf")
    assert obj is not None
    assert obj["n_det"] > 0


def test_string_oid_detections(ms_client: Alerce) -> None:
    dets: list = ms_client.query_detections(ZTF_OID, survey="ztf")
    assert len(dets) > 0


def test_string_oid_list_objects(ms_client: Alerce) -> None:
    result: list[dict] = ms_client.query_objects(
        survey="ztf", format="json", oid=ZTF_OID
    )
    assert len(result) > 0
    assert result[0]["oid"] == ZTF_OID


# -- Magstats, features, classifiers, classes --------------------------------


def test_ms_magstats(ms_client: Alerce) -> None:
    stats: list[dict] = ms_client.query_magstats(ZTF_OID, survey="ztf")
    assert len(stats) > 0
    row: dict = stats[0]
    for field in (
        "magmean",
        "magmedian",
        "magsigma",
        "ndet",
        "firstmjd",
        "lastmjd",
        "band",
    ):
        assert field in row, f"missing field: {field}"


def test_ms_magstats_pandas(ms_client: Alerce) -> None:
    result: DataFrame = ms_client.query_magstats(ZTF_OID, survey="ztf", format="pandas")
    assert isinstance(result, DataFrame)
    assert len(result) > 0
    assert "magmean" in result.columns


def test_ms_features(ms_client: Alerce) -> None:
    feats: list[dict] = ms_client.query_features(ZTF_OID, survey="ztf")
    assert len(feats) > 0
    feat: dict = feats[0]
    for field in ("name", "value"):
        assert field in feat, f"missing field: {field}"


def test_ms_features_pandas(ms_client: Alerce) -> None:
    result: DataFrame = ms_client.query_features(ZTF_OID, survey="ztf", format="pandas")
    assert isinstance(result, DataFrame)
    assert len(result) > 0
    assert "name" in result.columns


def test_ms_feature_single(ms_client: Alerce) -> None:
    feats: list[dict] = ms_client.query_features(ZTF_OID, survey="ztf")
    first_name: str = feats[0]["name"]
    single: list[dict] = ms_client.query_feature(ZTF_OID, first_name, survey="ztf")
    assert len(single) > 0
    assert all(f["name"] == first_name for f in single)


def test_ms_classifiers(ms_client: Alerce) -> None:
    clfs: list[dict] = ms_client.query_classifiers(survey="ztf")
    assert len(clfs) > 0
    clf: dict = clfs[0]
    for field in ("classifier_name", "classifier_version", "classes"):
        assert field in clf, f"missing field: {field}"


def test_ms_classifiers_pandas(ms_client: Alerce) -> None:
    result: DataFrame = ms_client.query_classifiers(survey="ztf", format="pandas")
    assert isinstance(result, DataFrame)
    assert "classifier_name" in result.columns


def test_ms_classes(ms_client: Alerce) -> None:
    clfs: list[dict] = ms_client.query_classifiers(survey="ztf")
    clf: dict = clfs[0]
    classes: list[dict] = ms_client.query_classes(
        clf["classifier_name"],
        clf["classifier_version"],
        survey="ztf",
    )
    assert len(classes) > 0
    assert "name" in classes[0]


# -- Format handling --------------------------------------------------------


def test_format_detections_json(ms_client: Alerce) -> None:
    result: list = ms_client.query_detections(ZTF_OID, survey="ztf", format="json")
    assert isinstance(result, list)


def test_format_detections_pandas(ms_client: Alerce) -> None:
    result: DataFrame = ms_client.query_detections(
        ZTF_OID, survey="ztf", format="pandas"
    )
    assert isinstance(result, DataFrame)
    assert len(result) > 0
    assert "band_name" in result.columns
    assert "measurement_id" in result.columns


def test_format_object_json(ms_client: Alerce) -> None:
    result: dict = ms_client.query_object(ZTF_OID, survey="ztf", format="json")
    assert isinstance(result, dict)


def test_format_probabilities_pandas(ms_client: Alerce) -> None:
    result: DataFrame = ms_client.query_probabilities(
        ZTF_OID, survey="ztf", format="pandas"
    )
    assert isinstance(result, DataFrame)
    assert "classifier_name" in result.columns


# -- Stamps ------------------------------------------------------------------


def test_ms_get_stamps_numpy(ms_client: Alerce) -> None:
    stamps: list = ms_client.get_stamps(
        ZTF_OID, candid=ZTF_CANDID, survey="ztf", format="numpy"
    )
    assert len(stamps) == 3
    for arr in stamps:
        assert isinstance(arr, np.ndarray)
        assert arr.shape == (63, 63)


def test_ms_get_stamps_hdulist(ms_client: Alerce) -> None:
    stamps: dict = ms_client.get_stamps(
        ZTF_OID, candid=ZTF_CANDID, survey="ztf", format="HDUList"
    )
    assert isinstance(stamps, dict)
    expected_keys = {"cutoutScience", "cutoutTemplate", "cutoutDifference"}
    assert set(stamps.keys()) == expected_keys
    for hdu in stamps.values():
        assert hdu.data.shape == (63, 63)


def test_ms_get_stamps_measurement_id_kwarg(ms_client: Alerce) -> None:
    stamps: list = ms_client.get_stamps(
        ZTF_OID, measurement_id=ZTF_CANDID, survey="ztf", format="numpy"
    )
    assert len(stamps) == 3


def test_ms_get_stamps_auto_candid(ms_client: Alerce) -> None:
    stamps: list = ms_client.get_stamps(ZTF_OID, survey="ztf", format="numpy")
    assert len(stamps) == 3
    assert all(isinstance(s, np.ndarray) for s in stamps)


def test_ms_get_avro(ms_client: Alerce) -> None:
    import json

    data: bytes = ms_client.get_avro(
        ZTF_OID, candid=ZTF_CANDID, use_multisurvey_api=True, survey="ztf"
    )
    assert isinstance(data, bytes)
    assert len(data) > 100
    parsed = json.loads(data)
    assert "candidate" in parsed
    assert "objectId" in parsed


def test_ms_get_avro_auto_candid(ms_client: Alerce) -> None:
    data: bytes = ms_client.get_avro(ZTF_OID, use_multisurvey_api=True, survey="ztf")
    assert isinstance(data, bytes)
    assert len(data) > 100
