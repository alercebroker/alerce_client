from .ms_stamps import AlerceStampsMultisurvey
from .stamps import AlerceStamps
from .utils import Client


class AlerceCommonStamps(Client):
    def __init__(self, **kwargs):
        legacy_config = kwargs.get("legacy_config", {})
        ms_stamp_config = kwargs.get("ms_stamp_config", {})
        self.legacy_stamps_client = AlerceStamps(**legacy_config)
        self.multisurvey_stamps_client = AlerceStampsMultisurvey(**ms_stamp_config)

    def plot_stamps(
        self, oid, candid=None, use_multisurvey_api=False, survey=None, **kwargs
    ):
        if use_multisurvey_api:
            if survey is None:
                raise ValueError(
                    "survey must be provided when use_multisurvey_api is True"
                )
            if not hasattr(self.multisurvey_stamps_client, "multisurvey_plot_stamps"):
                raise NotImplementedError("Multisurvey plot_stamps not implemented.")
            return self.multisurvey_stamps_client.multisurvey_plot_stamps(
                survey=survey, oid=oid, candid=candid, **kwargs
            )
        else:
            return self.legacy_stamps_client.plot_stamps(oid, candid=candid, **kwargs)

    def get_stamps(
        self,
        oid,
        candid=None,
        format="HDUList",
        use_multisurvey_api=False,
        survey=None,
        **kwargs
    ):
        if use_multisurvey_api:
            if survey is None:
                raise ValueError(
                    "survey must be provided when use_multisurvey_api is True"
                )
            if not hasattr(self.multisurvey_stamps_client, "multisurvey_get_stamps"):
                raise NotImplementedError("Multisurvey get_stamps not implemented.")
            return self.multisurvey_stamps_client.multisurvey_get_stamps(
                survey=survey, oid=oid, candid=candid, format=format, **kwargs
            )
        else:
            # Only pass supported arguments to legacy method
            legacy_kwargs = {}
            if candid is not None:
                legacy_kwargs["candid"] = candid
            if format is not None:
                legacy_kwargs["format"] = format
            return self.legacy_stamps_client.get_stamps(oid, **legacy_kwargs)

    def get_avro(
        self, oid, candid=None, use_multisurvey_api=False, survey=None, **kwargs
    ):
        if use_multisurvey_api:
            if survey is None:
                raise ValueError(
                    "survey must be provided when use_multisurvey_api is True"
                )
            if not hasattr(self.multisurvey_stamps_client, "multisurvey_get_avro"):
                raise NotImplementedError("Multisurvey get_avro not implemented.")
            return self.multisurvey_stamps_client.multisurvey_get_avro(
                survey=survey, oid=oid, candid=candid, **kwargs
            )
        else:
            return self.legacy_stamps_client.get_avro(oid, candid=candid, **kwargs)
