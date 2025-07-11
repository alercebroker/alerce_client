survey_urls_routes = {
            "ztf": {
                "api": "ZTF_API_URL",
                "route": "ZTF_ROUTES"
            },
            "lsst": {
                "api": "LSST_API_URL",
                "route": "LSST_ROUTES"
            },
        }

configs = {
    'ztf': {
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
    'lsst': {
        "LSST_API_URL": "https://api.alerce.online/lsst/v1/",
        "LSST_ROUTES": {
            "objects": "/objects",
            "single_object": "/objects/%s",
            "detections": "/objects/%s/lsst_detections",
            "non_detections": "/objects/%s/lsst_non_detections",
            "lightcurve": "/objects/%s/lsst_lightcurve",
            "magstats": "/objects/%s/lsst_magstats",
            "probabilities": "/objects/%s/lsst_probabilities",
            "features": "/objects/%s/lsst_features",
            "single_feature": "/objects/%s/lsst_features/%s",
            "classifiers": "/lsst_classifiers",
            "classifier_classes": "/lsst_classifiers/%s/%s/classes",
        },
    }
}