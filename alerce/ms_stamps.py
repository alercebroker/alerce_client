import warnings
import gzip
import io
from .utils import Client, load_config
from astropy.io.fits import open as fits_open
from urllib.error import HTTPError
from alerce.ms_search import AlerceSearchMultiSurvey
from alerce.exceptions import CandidError
from .ms_stamp_utils import create_html_stamp_display, create_stamp_parameters
from IPython.display import HTML, display

VALID_SURVEYS = ["lsst", "ztf"]


class AlerceStampsMultisurvey(Client):
    def __init__(self):
        # load stamps-specific config and pass to Client
        cfg = load_config(service="stamps")

        self.ztf_types = {
            "science": "cutoutScience",
            "template": "cutoutTemplate",
            "difference": "cutoutDifference",
        }

        super().__init__(**cfg)

        # create a search client per instance so it can receive different configs if needed
        self.search_client = AlerceSearchMultiSurvey()

    def _in_ipynb(self):
        try:
            from IPython import get_ipython
            import os

            if "IPKernelApp" not in get_ipython().config:  # pragma: no cover
                raise ImportError("console")
                return False
            if "VSCODE_PID" in os.environ:  # pragma: no cover
                raise ImportError("vscode")
                return False
        except Exception:
            return False
        else:  # pragma: no cover
            return True

    def _get_first_detection(self, survey: str, oid: int):
        """
        Get the first detection with stamps available for a given object.
        """
        detections = self.search_client.query_detections(survey, oid, format="pandas")

        detections_with_stamps = detections[detections.has_stamp]

        if detections_with_stamps.empty:
            raise CandidError()

        measurement_id = detections_with_stamps.sort_values("mjd").iloc[0][
            "measurement_id"
        ]
        return int(measurement_id)

    def _check_survey_validity(self, survey):
        if survey == "ztf":
            warnings.warn(
                "ZTF is not yet supported in the stamp multisurvey API.", UserWarning
            )
            raise NotImplementedError(
                "ZTF is not yet supported in the multisurvey API."
            )
        if survey not in VALID_SURVEYS:
            raise ValueError(f"survey must be one of {VALID_SURVEYS}")

    def multisurvey_plot_stamps(self, survey, oid, candid=None):
        """
        Plot stamp in a notebook given oid and survey, measurement_id is optional.
        """
        self._check_survey_validity(survey)

        if candid is not None:
            measurement_id = candid
        else:
            measurement_id = self._get_first_detection(survey, oid)

        avro_url = self.config["STAMP_URL"] + self.config["AVRO_ROUTES"]["get_stamp"]

        science_url = create_stamp_parameters(
            oid, survey, measurement_id, self.ztf_types["science"], avro_url, "plot"
        )
        template_url = create_stamp_parameters(
            oid, survey, measurement_id, self.ztf_types["template"], avro_url, "plot"
        )
        difference_url = create_stamp_parameters(
            oid, survey, measurement_id, self.ztf_types["difference"], avro_url, "plot"
        )

        if not self._in_ipynb():
            warnings.warn("This method only works on Notebooks", RuntimeWarning)
            return

        images = create_html_stamp_display(
            oid, survey, measurement_id, science_url, template_url, difference_url
        )
        display(HTML(images))

    def multisurvey_get_stamps(
        self,
        survey,
        oid,
        candid=None,
        include_variance_and_mask=False,
        out_format="HDUList",
    ):
        """Download Stamps for an specific alert given oid and survey, measurement_id is optional."""
        self._check_survey_validity(survey)

        if candid is not None:
            measurement_id = candid
        else:
            measurement_id = self._get_first_detection(survey, oid)

        avro_url = self.config["STAMP_URL"] + self.config["AVRO_ROUTES"]["get_stamp"]

        try:
            stamp_types = [
                self.ztf_types["science"],
                self.ztf_types["template"],
                self.ztf_types["difference"],
            ]
            stamp_list = []

            for stamp_type in stamp_types:

                url = create_stamp_parameters(
                    oid, survey, measurement_id, stamp_type, avro_url, "get"
                )
                http_response = self.session.request("GET", url)

                if survey == "ztf" or survey == "lsst":
                    fits_buffer = gzip.open(io.BytesIO(http_response.content))
                else:
                    raise Exception(f"survey {survey} not valid")

                tmp_hdulist = fits_open(
                    io.BytesIO(fits_buffer.read()), ignore_missing_simple=True
                )

                if include_variance_and_mask:
                    stamp_list.append(tmp_hdulist)
                else:
                    stamp_list.append(tmp_hdulist[0])

            if out_format == "HDUList":
                hdudict = {}
                for stamp, stamp_type in zip(stamp_list, stamp_types):
                    hdudict[stamp_type] = stamp
                return hdudict
            elif out_format == "numpy":
                return [stamp.data.copy() for stamp in stamp_list]

        except HTTPError:
            warnings.warn("AVRO File not found.", RuntimeWarning)
            return None

    def multisurvey_get_avro(self, survey, oid, candid=None, **kwargs):
        """Download avro of some alert given oid and survey, measurement_id is optional."""

        self._check_survey_validity(survey)
        params = {"survey_id": survey, "oid": oid}
        if candid is not None:
            params["candid"] = candid
        params.update(kwargs)

        measurement_id = kwargs.get("measurement_id")

        if measurement_id is None:
            measurement_id = self._get_first_detection(survey, oid)

        try:
            url = self.config["STAMP_URL"] + self.config["AVRO_ROUTES"]["get_avro"]
            params = {"oid": kwargs.get("oid"), "measurement_id": measurement_id}
            http_response = self.session.request("GET", url, params=params)
            return http_response.content
        except HTTPError:
            warnings.warn("AVRO File not found.", RuntimeWarning)
            return None
