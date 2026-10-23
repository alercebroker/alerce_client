"""Tests for alerce.compat -- multisurvey-to-legacy conversion utilities."""

import pytest

from alerce.compat import FIELD_MAP, _OID_ENDPOINTS, decode_ztf_oid, to_legacy

# Pre-computed (master_id, ztf_name) pairs.
# Encoding: survey_prefix | (year * 26^7 + base26_seq)
# survey_prefix for ZTF = 1 << 55 = 36028797018963968
ZTF_OID_PAIRS = [
    (36028941604196290, "ZTF18abbrrty"),
    (36028941605553165, "ZTF18abeqwzl"),
    (36028797018963968, "ZTF00aaaaaaa"),  # minimum: year=0, seq=all 'a'
]


class TestDecodeZtfOid:
    @pytest.mark.parametrize("master_id, expected", ZTF_OID_PAIRS)
    def test_known_values(self, master_id, expected):
        assert decode_ztf_oid(master_id) == expected

    def test_format(self):
        result = decode_ztf_oid(ZTF_OID_PAIRS[0][0])
        assert result.startswith("ZTF")
        assert len(result) == 12
        assert result[3:5].isdigit()
        assert result[5:].isalpha()
        assert result[5:].islower()

    def test_roundtrip_encode_decode(self):
        """Verify decode inverts the upstream encoding algorithm."""
        oid = "ZTF21abcdefg"
        year = int(oid[3:5])
        seq_str = oid[5:12]
        encoded = 0
        for i, ch in enumerate(seq_str):
            encoded += (ord(ch) - ord("a")) * (26 ** (6 - i))
        encoded += year * (26**7)
        encoded += 1 << 55  # ZTF survey prefix
        assert decode_ztf_oid(encoded) == oid


class TestToLegacyFieldRenames:
    def test_object_renames(self):
        record = {"oid": 123, "n_det": 5, "deltamjd": 100.0, "meanra": 1.0}
        result = to_legacy("object", record)
        assert result["ndet"] == 5
        assert result["deltajd"] == 100.0
        assert result["meanra"] == 1.0
        assert "n_det" not in result
        assert "deltamjd" not in result

    def test_detections_renames(self):
        record = {"band": 1, "measurement_id": 999, "survey_id": 1, "mjd": 59000.0}
        result = to_legacy("detections", record)
        assert result["fid"] == 1
        assert result["candid"] == 999
        assert result["tid"] == 1
        assert result["mjd"] == 59000.0

    def test_non_detections_renames(self):
        record = {"band": 2, "survey_id": 1, "diffmaglim": 20.5}
        result = to_legacy("non_detections", record)
        assert result["fid"] == 2
        assert result["tid"] == 1
        assert result["diffmaglim"] == 20.5

    def test_forced_photometry_renames(self):
        record = {"band": 1, "measurement_id": 456}
        result = to_legacy("forced_photometry", record)
        assert result["fid"] == 1
        assert result["candid"] == 456

    def test_magstats_renames(self):
        record = {"band": 1, "magmean": 18.5}
        result = to_legacy("magstats", record)
        assert result["fid"] == 1
        assert result["magmean"] == 18.5

    def test_features_renames(self):
        record = {"band": 1, "name": "Amplitude", "value": 0.5}
        result = to_legacy("features", record)
        assert result["fid"] == 1

    def test_all_endpoints_covered(self):
        assert set(FIELD_MAP.keys()) == {
            "object", "detections", "non_detections",
            "forced_photometry", "magstats", "features",
        }


class TestToLegacyOidConversion:
    @pytest.mark.parametrize("endpoint", sorted(_OID_ENDPOINTS))
    def test_int_oid_decoded(self, endpoint):
        master_id = 36028941604196290
        record = {"oid": master_id, "band": 1}
        result = to_legacy(endpoint, record)
        assert result["oid"] == "ZTF18abbrrty"

    @pytest.mark.parametrize("endpoint", sorted(_OID_ENDPOINTS))
    def test_str_oid_unchanged(self, endpoint):
        record = {"oid": "ZTF18abbrrty", "band": 1}
        result = to_legacy(endpoint, record)
        assert result["oid"] == "ZTF18abbrrty"

    def test_no_oid_conversion_for_magstats(self):
        record = {"oid": 36028941604196290, "band": 1}
        result = to_legacy("magstats", record)
        assert result["oid"] == 36028941604196290

    def test_no_oid_conversion_for_features(self):
        record = {"oid": 36028941604196290, "band": 1}
        result = to_legacy("features", record)
        assert result["oid"] == 36028941604196290


class TestToLegacyListHandling:
    def test_list_of_records(self):
        records = [
            {"band": 1, "measurement_id": 100},
            {"band": 2, "measurement_id": 200},
        ]
        result = to_legacy("detections", records)
        assert isinstance(result, list)
        assert len(result) == 2
        assert result[0]["fid"] == 1
        assert result[0]["candid"] == 100
        assert result[1]["fid"] == 2

    def test_empty_list(self):
        assert to_legacy("detections", []) == []

    def test_single_record(self):
        record = {"band": 1}
        result = to_legacy("detections", record)
        assert isinstance(result, dict)
        assert result["fid"] == 1

    def test_list_with_oid_conversion(self):
        records = [
            {"oid": 36028941604196290, "band": 1},
            {"oid": 36028941605553165, "band": 2},
        ]
        result = to_legacy("detections", records)
        assert result[0]["oid"] == "ZTF18abbrrty"
        assert result[1]["oid"] == "ZTF18abeqwzl"


class TestToLegacyUnknownEndpoint:
    def test_returns_data_unchanged(self):
        record = {"foo": "bar"}
        result = to_legacy("nonexistent", record)
        assert result is record

    def test_list_returned_unchanged(self):
        records = [{"a": 1}]
        result = to_legacy("nonexistent", records)
        assert result is records


class TestToLegacyImmutability:
    def test_original_not_mutated(self):
        record = {"oid": 36028941604196290, "n_det": 5, "deltamjd": 100.0}
        to_legacy("object", record)
        assert "n_det" in record
        assert "oid" in record
        assert record["oid"] == 36028941604196290
