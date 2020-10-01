import warnings
from .utils import Client
from astropy.io.fits import HDUList
from astropy.io.fits import open as fits_open
from urllib.error import HTTPError
from alerce.search import AlerceSearch
from alerce.exceptions import CandidError


class AlerceStamps(Client):
    search_client = AlerceSearch()

    def __init__(self, **kwargs):
        default_config = {
            "AVRO_URL": "http://avro.alerce.online",
            "AVRO_ROUTES": {
                "get_stamp": "/get_stamp",
            },
        }
        default_config.update(kwargs)
        super().__init__(**default_config)

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
        except Exception as e:
            print(e)
            return False
        else:  # pragma: no cover
            return True

    def _get_first_detection(self, oid):
        detections = self.search_client.query_detections(oid, format="pandas")
        first_detection = detections[detections.has_stamp].candid.astype(int).min()
        try:
            first_detection = int(first_detection)
        except TypeError:
            raise CandidError()
        return first_detection

    def plot_stamp(self, oid, candid=None):
        """
        Plot stamp in a notebook given oid. It uses IPython HTML.

        Parameters
        ----------
        oid : :py:class:`str`
            object ID in ALeRCE DBs.
        candid : :py:class:`int`
            Candid of the stamp to be displayed.

        Returns
        -------
            Display the stamps on a jupyter notebook.
        """
        if not self._in_ipynb():
            warnings.warn("This method only works on Notebooks", RuntimeWarning)
            return

        if candid is None:
            candid = self._get_first_detection(oid)

        from IPython.display import HTML
        science = "%s?oid=%s&candid=%s&type=science&format=png" % (
            self.config["AVRO_URL"] + self.config["AVRO_ROUTES"]["get_stamp"],
            oid,
            candid,
        )
        template = science.replace("science", "template")
        difference = science.replace("science", "difference")
        images = """
        <div>ZTF oid: %s, candid: %s</div>
        <div>&emsp;&emsp;&emsp;&emsp;&emsp;
        Science
        &emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;
        Template
        &emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;
        Difference
        <div class="container">
        <div style="float:left;width:20%%"><img src="%s"></div>
        <div style="float:left;width:20%%"><img src="%s"></div>
        <div style="float:left;width:20%%"><img src="%s"></div>
        </div>
        """ % (
            oid,
            candid,
            science,
            template,
            difference,
        )
        display(HTML(images))

    def get_stamps(self, oid, candid=None):
        """Download Stamps for an specific alert.

        Parameters
        ----------
        oid : :py:class:`str`
            object ID in ALeRCE DBs.
        candid : :py:class:`int`
            Candid of the stamp to be displayed.

        Returns
        -------
        :class:`astropy.io.fits.HDUList`
            Science, Template and Difference stamps for an specific alert.
        """
        if candid is None:
            candid = self._get_first_detection(oid)
        try:
            hdulist = HDUList()
            for stamp_type in ["science", "template", "difference"]:
                tmp_hdulist = fits_open(
                    "%s?oid=%s&candid=%s&type=%s&format=fits"
                    % (
                        self.config["AVRO_URL"]
                        + self.config["AVRO_ROUTES"]["get_stamp"],
                        oid,
                        candid,
                        stamp_type,
                    )
                )
                hdu = tmp_hdulist[0]
                hdu.header["STAMP_TYPE"] = stamp_type
                hdulist.append(hdu)
            return hdulist
        except HTTPError:
            warnings.warn("AVRO File not found.", RuntimeWarning)
            return None
