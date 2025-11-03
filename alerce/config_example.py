import copy
import json
from typing import Any, Dict, Optional

########################################
## WARNING: This is an example config file.
## Do not put sensitive information here.
## Instead, create a separate config file
## config.py in your working directory
## and import it as needed.
## A proper config.py file will be
## included in the release versions.
########################################

# Canonical defaults for the library
configs: Dict[str, Any] = {
    "multisurvey": {
        "URL_MS": "http://localhost:",
        "ROUTES_MS": {
            "objects": "8000/list_objects",
            "single_object": "8000/object",
            "detections": "8001/detections",
            "forced_photometry": "8001/forced-photometry",
            "non_detections": "8001/non_detections",
            "lightcurve": "8001/lightcurve",
            "probabilities": "8003/probability",
        },
    },
    "ztf": {
        "ZTF_API_URL": "https://api.alerce.online/ztf/v1/",
        "ZTF_ROUTES": {
            "objects": "/objects",
            "single_object": "/objects/%s",
            "detections": "/objects/%s/detections",
            "non_detections": "/objects/%s/non_detections",
            "lightcurve": "/objects/%s/lightcurve",
            "magstats": "/objects/%s/magstats",
            "probabilities": "/objects/%s/probabilities",
            "features": "/objects/%s/features",
            "single_feature": "/objects/%s/features/%s",
            "classifiers": "/classifiers",
            "classifier_classes": "/classifiers/%s/%s/classes",
        },
    },
    "stamps": {
        "STAMP_URL": "http://localhost:8009",
        "AVRO_ROUTES": {"get_stamp": "/stamp", "get_avro": "/get_avro"},
    },
}

# Backwards-compatible alias (some modules import stamp_config directly)
stamp_config = copy.deepcopy(configs["stamps"])


def _deep_merge(a: Dict[str, Any], b: Dict[str, Any]) -> Dict[str, Any]:
    """Deep-merge b into a and return a new dict (does not mutate inputs)."""
    out = copy.deepcopy(a)
    for k, v in (b or {}).items():
        if k in out and isinstance(out[k], dict) and isinstance(v, dict):
            out[k] = _deep_merge(out[k], v)
        else:
            out[k] = copy.deepcopy(v)
    return out


def load_config(
    service: Optional[str] = None,
    path: Optional[str] = None,
    overrides: Optional[Dict[str, Any]] = None,
) -> Dict[str, Any]:
    """
    Load and return configuration merged in the order:
      defaults (from `configs`) -> optional JSON file at `path` -> `overrides` dict

    - If `service` is provided (e.g. 'ztf', 'multisurvey', 'stamps'), a dict for that service is returned.
    - If `service` is None, the full merged configs dict is returned.

    The JSON file may contain partial configuration (only keys to override).
    """
    base = copy.deepcopy(configs)

    if path:
        try:
            with open(path, "r") as fh:
                file_cfg = json.load(fh)
            base = _deep_merge(base, file_cfg)
        except FileNotFoundError:
            raise

    if overrides:
        base = _deep_merge(base, overrides)

    if service:
        svc = service.lower()
        return copy.deepcopy(base.get(svc, {}))

    return base
