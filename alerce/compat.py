"""Conversion utilities between multisurvey and legacy response formats."""

from __future__ import annotations

from typing import Any

FIELD_MAP: dict[str, dict[str, str]] = {
    "object": {
        "n_det": "ndet",
        "deltamjd": "deltajd",
    },
    "detections": {
        "band": "fid",
        "measurement_id": "candid",
        "survey_id": "tid",
    },
    "non_detections": {
        "band": "fid",
        "survey_id": "tid",
    },
    "forced_photometry": {
        "band": "fid",
        "measurement_id": "candid",
    },
    "magstats": {
        "band": "fid",
    },
    "features": {
        "band": "fid",
    },
}

_OID_ENDPOINTS = {"object", "detections", "non_detections", "forced_photometry"}

_SURVEY_PREFIX_BITS = 8
_OID_MASK = (1 << (63 - _SURVEY_PREFIX_BITS)) - 1


def decode_ztf_oid(master_id: int) -> str:
    """Convert a multisurvey integer OID back to a ZTF name.

    The master_id encodes the survey in its top 8 bits and a ZTF-specific
    payload in the remaining 55 bits: a two-digit year followed by a
    base-26 sequence of 7 lowercase letters.

    >>> decode_ztf_oid(36028941604196290)
    'ZTF18abbrrty'
    """
    raw = master_id & _OID_MASK
    year = (raw // (26**7)) % 100
    seq = raw % (26**7)
    letters: list[str] = []
    for i in range(6, -1, -1):
        letters.append(chr(int(seq // (26**i)) + ord("a")))
        seq = int(seq % (26**i))
    return f"ZTF{year:02d}{''.join(letters)}"


def to_legacy(
    endpoint: str, data: dict[str, Any] | list[dict[str, Any]]
) -> dict[str, Any] | list[dict[str, Any]]:
    """Rename multisurvey fields to their legacy equivalents.

    Parameters
    ----------
    endpoint : str
        One of: object, detections, non_detections, forced_photometry,
        magstats, features.
    data : dict or list[dict]
        A single record or list of records from the multisurvey backend.

    Returns
    -------
    dict or list[dict]
        A copy with renamed keys and, for endpoints where the multisurvey
        API changed ``oid`` from string to integer, the integer OID decoded
        back to the original ZTF name.
    """
    mapping = FIELD_MAP.get(endpoint, {})
    convert_oid = endpoint in _OID_ENDPOINTS
    if not mapping and not convert_oid:
        return data
    if isinstance(data, list):
        return [_convert(record, mapping, convert_oid) for record in data]
    return _convert(data, mapping, convert_oid)


def _convert(
    record: dict[str, Any], mapping: dict[str, str], convert_oid: bool
) -> dict[str, Any]:
    out = {mapping.get(k, k): v for k, v in record.items()}
    if convert_oid and "oid" in out and isinstance(out["oid"], int):
        out["oid"] = decode_ztf_oid(out["oid"])
    return out
