import requests
import pandas as pd
from astropy.table import Table, Column
from IPython.display import HTML
from astropy.io.fits import HDUList
from astropy.io.fits import open as fits_open

import warnings
from json.decoder import JSONDecodeError


class AlerceParseError(Exception):
    pass


class AlerceOidError(Exception):
    pass


class AlerceAPI(object):
    """ALeRCE API Wrapper.

    Parameters
    ----------
    ztf_url : :py:class:`str`
        URL for ALeRCE ZTF data access API.     (default ALeRCE current url).
    catsHTM_url : :py:class:`str`
        URL for catsHTM service.                (default ALeRCE current url).

    """

    def __init__(self, **kwargs):
        warnings.warn(
            "This python client will be deprecated soon. Please visit https://github.com/alercebroker/alerce_client_new for information on the future client",
            DeprecationWarning,
            stacklevel=2,
        )

        self.ztf_url = "http://ztf.alerce.online"
        if "ztf_url" in kwargs.keys():
            self.ztf_url = kwargs["ztf_url"]

        self.catsHTM_url = "http://catshtm.alerce.online"
        if "catsHTM_url" in kwargs.keys():
            self.catsHTM_url = kwargs["catsHTM_url"]

        self.avro_url = "http://avro.alerce.online"
        if "avro_url" in kwargs.keys():
            self.avro_url = kwargs["avro_url"]

        self.oid = ""
        self.session = requests.Session()

    def query(self, params, format="votable"):
        """Query the ALeRCE API to get matching objects into a pandas dataframe.

        Parameters
        ----------
        params : :py:class:`dict`
            Dictionary of parameters for the API. The current fields to query the db are the following:

            .. code-block:: json

            {
               total :  number (if not set the total is counted and the query is slower) ,
               records_per_pages :  number (default 20) ,
               page :  number (default 1) ,
               sortBy :  :py:class:`str` columnName (default nobs) ,
               query_parameters : {
                 filters : {
                  //ZTF object id
                   oid :  ZTFXXXXXX ,
                  //Number of detections
                   nobs : {
                     min :  int ,
                     max :  int
                  },
                  //Late Classifier (Random Forest)
                   classrf :  string or int ,
                   pclassrf :  float [0-1] ,
                  //Early Classifier (Stamp Classifier)
                   classearly :  list, string or int ,
                   pclassearly :  float [0-1] ,
                 }
                 //Coordinate based search (RA,DEC) and Search Radius.
                 coordinates : {
                     ra :  float degrees ,
                     dec :  float degrees ,
                     sr :  float degrese
                 },
                 dates : {
                 //First detection (Discovery date)
                   firstmjd : {
                     min :  float mjd ,
                     max :  float mjd
                  }
                }
              }
            }

            for a more updated available fields check `ZTF API documentation <https://alerceapi.readthedocs.io/en/latest/ztf_db.html>`_
        format : :py:class:`str`
            Output format [votable|pandas]

        Returns
        -------
        :class:`astropy.table.Table` or :class:`pandas.DataFrame`
            The response contains the objects matching the filtering parameters with their statistics.

        """

        r = self.session.post(url="%s/query" % self.ztf_url, json=params)
        try:
            response = r.json()
        except JSONDecodeError:
            return None

        result = response["result"]
        query_results = Table([result[key] for key in result])

        if format == "pandas":
            query_results = query_results.to_pandas()
            query_results.set_index("oid", inplace=True)

        return query_results

    def get_sql(self, params):
        """Get the SQL statement executed on the database given a set of filters

        Parameters
        ----------
        params : :py:class:`dict`
            Same parameters used in :meth:`alerce.api.AlerceAPI.query()`

        Returns
        -------
        :py:class:`string`
            SQL Statement.

        """

        r = self.session.post(url="%s/get_sql" % self.ztf_url, json=params)

        return r.content.decode("utf-8")

    def get_detections(self, oid, format="votable"):
        """Get detections for an object.

        Parameters
        ----------
        oid : :py:class:`str`
            object ID in ALeRCE DBs.
        format : :py:class:`str`
            Output format [votable|pandas]

        Returns
        -------
        :class:`astropy.table.Table` or :class:`pandas.DataFrame`
            VoTable or DataFrame with detections.

            The schema used is the same as ZTF (`schema <https://zwickytransientfacility.github.io/ztf-avro-alert/schema.html>`_), also
            the fields with `_corr` suffix are corrected magnitudes with the object reference magnitude.

        """

        # oid
        params = {"oid": oid}

        # show api results
        r = self.session.post(url="%s/get_detections" % self.ztf_url, json=params)
        try:
            response = r.json()
        except JSONDecodeError:
            return None

        if len(response["result"]["detections"]) > 0:
            detections = Table(response["result"]["detections"])
        else:
            return None

        if format == "pandas":
            detections = detections.to_pandas()
            detections.sort_values("mjd", inplace=True)
            detections.set_index("candid", inplace=True)
            return detections

        return detections

    def get_non_detections(self, oid, format="votable"):
        """Get Non detections for an object.

        Parameters
        ----------
        oid : :py:class:`str`
            object ID in ALeRCE DBs.
        format : :py:class:`str`
            Output format [votable|pandas]

        Returns
        -------
        :class:`astropy.table.Table` or :class:`pandas.DataFrame`
            VoTable or DataFrame with non detections.

        """

        params = {"oid": oid}

        # show api results
        r = self.session.post(url="%s/get_non_detections" % self.ztf_url, json=params)
        try:
            response = r.json()
        except JSONDecodeError:
            return

        if len(response["result"]["non_detections"]) > 0:
            non_detections = Table(response["result"]["non_detections"])
        else:
            return None

        if format == "pandas":
            non_detections = non_detections.to_pandas()
            non_detections.sort_values("mjd", inplace=True)
            non_detections.set_index("mjd", inplace=True)

            return non_detections

        return non_detections

    def get_stats(self, oid, format="votable"):
        """Get object aggregated statistics.

        Parameters
        ----------
        oid : :py:class:`str`
            object ID in ALeRCE DBs.
        format : :py:class:`str`
            Output format [votable|pandas]

        Returns
        -------
        :class:`astropy.table.Table` or :class:`pandas.Series`
            VoTable or Series with the object statistics.

        """

        params = {"oid": oid}

        r = self.session.post(url="%s/get_stats" % self.ztf_url, json=params)

        try:
            response = r.json()
        except JSONDecodeError:
            return None

        stats = response["result"]["stats"]

        self.oid = oid
        self.meanra = stats["meanra"]
        self.meandec = stats["meandec"]
        self.firstMJD = stats["firstmjd"]

        if format == "votable":
            stats = {key: [stats[key]] for key in stats}
            stats = Table(stats)
        elif format == "pandas":
            stats = pd.Series(stats)
        else:
            return None

        return stats

    def get_probabilities(self, oid, early=True, late=True, format="votable"):
        """Get probabilities for a given object.


        Parameters
        ----------
        oid : :py:class:`str`
            object ID in ALeRCE DBs.
        early : :py:class:`bool`
            Get probabilities from Early Classifier.
        late : :py:class:`bool`
            Get probabilities from Late Classifier.
        format : :py:class:`str`
            Output format [votable|pandas]

        Returns
        -------
        :py:class:`dict`
            :py:class:`dict`ionary with the following structure:
              {
                "early": :class:`astropy.table.Table` or :class:`pandas.Series`,

                "late": :class:`astropy.table.Table` or :class:`pandas.Series`
              }


        """

        params = {"oid": oid}

        # show api results
        r = self.session.post(url="%s/get_probabilities" % self.ztf_url, json=params)

        if early:
            try:
                if format == "pandas":
                    df_early = pd.Series(
                        r.json()["result"]["probabilities"]["early_classifier"]
                    )
                elif format == "votable":
                    resp = r.json()["result"]["probabilities"]["early_classifier"]
                    df_early = Table({key: [resp[key]] for key in resp})
                else:
                    df_early = None

            except JSONDecodeError:
                return None

        if late:
            try:
                if format == "pandas":
                    df_late = pd.Series(
                        r.json()["result"]["probabilities"]["late_classifier"]
                    )
                elif format == "votable":
                    resp = r.json()["result"]["probabilities"]["late_classifier"]
                    df_late = Table({key: [resp[key]] for key in resp})
                else:
                    df_late = None

            except JSONDecodeError:
                return None

        result = {}
        if early:
            result["early"] = df_early
        if late:
            result["late"] = df_late

        return result

    def get_features(self, oid, format="votable"):
        """Get features given object.

        Parameters
        ----------
        oid : :py:class:`str`
            object ID in ALeRCE DBs.
        format : :py:class:`str`
            Output format [votable|pandas]

        Returns
        -------
        :class:`astropy.table.Table` or :class:`pandas.Series`
            Features calculated for the late classification.

        """

        params = {"oid": oid}

        # show api results
        r = self.session.post(url="%s/get_features" % self.ztf_url, json=params)

        try:
            resp = r.json()
        except JSONDecodeError:
            return None

        if format == "pandas":
            features = pd.Series(resp["result"]["features"])
        elif format == "votable":
            resp = {key: [resp[key]] for key in resp}
            features = Table(resp)
        else:
            return None

        return features

    def catsHTM_conesearch(self, oid, radius, catalog_name="all", format="votable"):
        """catsHTM conesearch given an object and catalog_name.

        Parameters
        ----------
        oid : :py:class:`str`
            object ID in ALeRCE DBs.
        catalog_name : :py:class:`str`
            catsHTM Catalog name, `"all"` can be used to query all available catalogs. List of available catalogs can be found in `here <https://alerceapi.readthedocs.io/en/latest/catshtm.html#id1>`_.
        radius : :py:class:`float`
            Conesearch radius in arcsec.
        format : :py:class:`str`
            Output format [votable|pandas]

        Returns
        -------
        :py:class:`dict`
            Dictionary with the following structure:
            {
                <catalog_name>: :class:`astropy.table.Table` or :class:`pandas.DataFrame`
            }

        """

        if oid != self.oid:
            self.get_stats(oid)

        params = {
            "catalog": "%s" % catalog_name,
            "ra": "%f" % self.meanra,
            "dec": "%f" % self.meandec,
            "radius": "%f" % radius,
        }
        if catalog_name != "all":
            result = self.session.get(
                url="%s/conesearch" % self.catsHTM_url, params=params
            )
        else:
            result = self.session.get(
                url="%s/conesearch_all" % self.catsHTM_url, params=params
            )

        votables = {}

        try:
            if "catalogs" not in result.json().keys():
                return
        except:
            return

        for idx, r in enumerate(result.json()["catalogs"]):

            key = list(r.keys())[0]
            if r[key] == {}:
                continue
            t = Table()
            for field in r[key].keys():
                data = r[key][field][
                    "values"
                ]  # list(map(lambda x: x["value"], r[key][field]))
                t.add_column(Column(data, name=field))
                t[field].unit = r[key][field]["units"]
            t["cat_name"] = Column(["catsHTM_%s" % key], name="cat_name")
            if format == "pandas":
                t = t.to_pandas()
            votables[key] = t

        return votables

    def catsHTM_crossmatch(self, oid, radius=100, catalog_name="all", format="votable"):
        """catsHTM crossmatch given an object and catalog_name.

        Parameters
        ----------
        oid : :py:class:`str`
            object ID in ALeRCE DBs.
        catalog_name : :py:class:`str`
            catsHTM Catalog name, `"all"` can be used to query all available catalogs. List of available catalogs can be found in `here <https://alerceapi.readthedocs.io/en/latest/catshtm.html#id1>`_.
        radius : :py:class:`float`
            Crossmatch radius in arcsec. (Default 100 arcsec)
        format : :py:class:`str`
            Output format [votable|pandas]

        Returns
        -------
        :py:class:`dict`
            Dictionary with the following structure:
            {
                <catalog_name>: :class:`astropy.table.Table` or :class:`pandas.Series`
            }

        """

        if oid != self.oid:
            self.get_stats(oid)

        params = {
            "catalog": "%s" % catalog_name,
            "ra": "%f" % self.meanra,
            "dec": "%f" % self.meandec,
            "radius": "%f" % radius,
        }
        if catalog_name != "all":
            result = self.session.get(
                url="%s/crossmatch" % self.catsHTM_url, params=params
            )
        else:
            result = self.session.get(
                url="%s/crossmatch_all" % self.catsHTM_url, params=params
            )
        votables = {}

        try:
            results = result.json()
        except JSONDecodeError:
            return None

        for idx, catalog_result in enumerate(results):

            catalog_name = list(catalog_result.keys())[0]
            if format == "pandas":
                t = {}
            elif format == "votable":
                t = Table()
            else:
                return None

            catalog_data = catalog_result[catalog_name]
            for field in catalog_data:
                data = catalog_data[field]["value"]
                unit = catalog_data[field]["unit"]
                if format == "pandas":
                    t[field] = data
                elif format == "votable":
                    t.add_column(Column([data], name=field))
                    t[field].unit = unit
                    t["cat_name"] = Column(
                        ["catsHTM_%s" % catalog_name], name="cat_name"
                    )
                else:
                    return None
            if format == "pandas":
                votables[catalog_name] = pd.Series(t)
            else:
                votables[catalog_name] = t

        return votables

    def catsHTM_redshift(self, oid, radius, format="votable"):
        """Get redshift given an object.

        Parameters
        ----------
        oid : :py:class:`str`
            object ID in ALeRCE DBs.
        radius : :py:class:`float`
            catsHTM conesearch radius in arcsec.
        format : :py:class:`str`
            Output format [votable|pandas]

        Returns
        -------
        :py:class:`float`
            Check if redshift is in a catsHTM xmatch response.

        """

        # get ra, dec
        if oid != self.oid:
            self.get_stats(oid)

        # search data in catsHTM
        xmatches = self.catsHTM_crossmatch(oid, catalog_name="all", radius=radius)

        # check whether redshift exists
        for catname in xmatches:
            for col in xmatches[catname].keys():
                if col == "z":
                    return float(xmatches[catname][col])

        # check whether photometric redshift exists
        for catname in xmatches:
            for col in xmatches[catname].keys():
                if col in ["zphot", "z_phot"]:
                    return float(xmatches[catname][col])

        return

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

    def plot_stamp(self, oid, candid=None):
        """Plot stamp in a notebook given oid. It uses IPython HTML.

        Parameters
        ----------
        oid : :py:class:`str`
            object ID in ALeRCE DBs.
        candid : :py:class:`int`
            Candid of the stamp to be displayed, if not set shows the Discovery stamp (first one).

        Returns
        -------
            Display the stamps on a jupyter notebook.

        """
        ""

        # if candid is None, get minimum candid
        if candid is None:
            candid = min(self.get_detections(oid, format="pandas").index)

        if not self._in_ipynb():
            warnings.warn("This method only works on Notebooks", RuntimeWarning)
            return

        science = "%s/get_stamp?oid=%s&candid=%s&type=science&format=png" % (
            self.avro_url,
            oid,
            candid,
        )
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
            science.replace("science", "template"),
            science.replace("science", "difference"),
        )
        display(HTML(images))

    def get_stamps(self, oid, candid=None):
        """Download Stamps for an specific alert.

        Parameters
        ----------
        oid : :py:class:`str`
            object ID in ALeRCE DBs.
        candid : :py:class:`int` (default First Stamps)
            Candid of the stamp to be displayed, if not set shows the Discovery stamp (first one).

        Returns
        -------
        :class:`astropy.io.fits.HDUList`
            Science, Template and Difference stamps for an specific alert.

        """

        if candid is None:
            detections = self.get_detections(oid, format="pandas")
            if detections is None:
                return None
            candid = min(detections.index)

        hdulist = HDUList()
        for stamp_type in ["science", "template", "difference"]:
            tmp_hdulist = fits_open(
                "%s/get_stamp?oid=%s&candid=%s&type=%s&format=fits"
                % (self.avro_url, oid, candid, stamp_type)
            )
            hdu = tmp_hdulist[0]
            hdu.header["STAMP_TYPE"] = stamp_type
            hdulist.append(hdu)
        return hdulist
