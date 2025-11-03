survey_urls_routes = {
    "ztf": {"api": "ZTF_API_URL_MS", "route": "ZTF_ROUTES_MS"},
    "lsst": {"api": "LSST_API_URL", "route": "LSST_ROUTES"},
}


def get_service_config(service: str):
    """Return a minimal mapping with api and route keys for the given service.

    This function intentionally keeps the small legacy shape expected by callers of
    `ms_search_utils` while sourcing values from the canonical config module.
    """
    from .config import load_config

    svc = service.lower()
    if svc == "ztf":
        cfg = load_config(service="ztf")
        return {
            "ZTF_API_URL_MS": cfg.get("ZTF_API_URL", ""),
            "ZTF_ROUTES_MS": cfg.get("ZTF_ROUTES", {}),
        }
    if svc == "lsst":
        # no dedicated lsst section in canonical config; return sensible defaults
        return {
            "LSST_API_URL": "http://127.0.0.1:",
            "LSST_ROUTES": {},
        }
    raise ValueError(f"Unknown service {service}")
