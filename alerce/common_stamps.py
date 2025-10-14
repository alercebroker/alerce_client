from .ms_stamps import AlerceStampsMultisurvey
from .stamps import AlerceStamps
from .utils import Client
import warnings

class AlerceCommonStamps(Client):
    def __init__(self, **kwargs):
        legacy_config = kwargs.get("legacy_config", {})
        ms_stamp_config = kwargs.get("ms_stamp_config", {})
        self.legacy_stamps_client = AlerceStamps(**legacy_config)
        self.multisurvey_stamps_client = AlerceStampsMultisurvey(**ms_stamp_config)

    def plot_stamps(
        self, oid, candid=None, survey=None
    ):
        
        if survey is None:
            survey = "ztf"
            warnings.warn(
                "survey not provided, defaulting to 'ztf'. This will use the legacy ZTF client. This behavior will be deprecated in future versions.",
                DeprecationWarning,
            )

        if survey == "ztf":
            return self.legacy_stamps_client.plot_stamps(
                oid=oid, candid=candid
            )
        elif survey in self.valid_surveys:
            return self.multisurvey_stamps_client.multisurvey_plot_stamps(
                oid=oid, candid=candid, survey=survey
            )
        else:
            raise ValueError(f"survey must be one of {self.valid_surveys}")

    def get_stamps(
        self,
        oid,
        candid=None,
        format="HDUList",
        survey=None,
    ):
        if survey is None:
            survey = "ztf"
            warnings.warn(
                "survey not provided, defaulting to 'ztf'. This will use the legacy ZTF client. This behavior will be deprecated in future versions.",
                DeprecationWarning,
            )

        if survey == "ztf":
            return self.legacy_stamps_client.get_stamps(
                oid=oid, candid=candid, format=format
            )
        elif survey in self.valid_surveys:
            return self.multisurvey_stamps_client.multisurvey_get_stamps(
                oid=oid, candid=candid, survey=survey
            )
        else:
            raise ValueError(f"survey must be one of {self.valid_surveys}")
    def get_avro(
        self, oid, candid=None, use_multisurvey_api=False, survey=None
    ):
        if use_multisurvey_api:
            if survey is None:
                raise ValueError(
                    "survey must be provided when use_multisurvey_api is True"
                )
            if not hasattr(self.multisurvey_stamps_client, "multisurvey_get_avro"):
                raise NotImplementedError("Multisurvey get_avro not implemented.")
            return self.multisurvey_stamps_client.multisurvey_get_avro(
                survey=survey, oid=oid, candid=candid
            )
        else:
            return self.legacy_stamps_client.get_avro(oid, candid=candid)
