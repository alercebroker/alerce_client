survey_urls_routes = {
    "ztf": {"api": "ZTF_API_URL", "route": "ZTF_ROUTES"},
    "lsst": {"api": "LSST_API_URL", "route": "LSST_ROUTES"},
}

configs = {
    "ztf": {
        "ZTF_API_URL": "https://api.staging.alerce.online/multisurvey/",
        "ZTF_ROUTES": {
            "objects": "object_api/list_objects",
            "single_object": "object_api/object",
            "detections": "lightcurve_api/detections",
            "forced_photometry": "lightcurve_api/forced-photometry",
            "non_detections": "lightcurve_api/non_detections",
            "lightcurve": "lightcurve_api/lightcurve",
        },
    },
    "lsst": {
        "LSST_API_URL": "http://127.0.0.1:",
        "LSST_ROUTES": {
            "objects": "8000//list_objects",
            "single_object": "8000//object",
            "detections": "8001//detections",
            "forced_photometry": "8001//forced-photometry",
            "non_detections": "8001//non_detections",
            "lightcurve": "8001//lightcurve",
            "magstats": "8002//magstats",
        },
    },
}
