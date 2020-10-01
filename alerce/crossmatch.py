import requests

from astropy.table import Table, Column

from .utils import Client
from .exceptions import handle_error


class AlerceXmatch(Client):
    CATALOG_TRANSLATE = {
        "2MASS": "TMASS",
        "2MASSxsc": "TMASSxsc",
        "GAIA/DR1": "GAIADR1",
        "GAIA/DR2": "GAIADR2",
        "SDSS/DR10": "SDSSDR10",
    }

    def __init__(self, **kwargs):
        self.session = requests.Session()
        default_config = {
            "CATSHTM_API_URL": "http://catshtm.alerce.online",
            "CATSHTM_ROUTES": {
                "conesearch": "/conesearch",
                "conesearch_all": "/conesearch_all",
                "crossmatch": "/crossmatch",
                "crossmatch_all": "/crossmatch_all",
            },
        }
        default_config.update(kwargs)
        super().__init__(**default_config)

    def _request_catshtm(self, method, url, params=None, result_format="json"):
        result_format = self._validate_format(result_format)
        resp = self.session.request(method, url, params=params)
        if resp.status_code >= 400:
            handle_error(resp)

        return resp.json()

    def _format_all(self, catalog_list, result_format="json"):
        votables = {}
        for idx, r in enumerate(catalog_list):
            key = list(r.keys())[0]
            if r[key] == {}:
                continue
            t = Table()
            for field in r[key].keys():
                data = (
                    r[key][field]["values"]
                    if "values" in r[key][field]
                    else [r[key][field]["value"]]
                )
                t.add_column(Column(data, name=field))
                t[field].unit = (
                    r[key][field]["units"]
                    if "units" in r[key][field]
                    else r[key][field]["unit"]
                )
            t["cat_name"] = Column(["catsHTM_%s" % key], name="cat_name")
            if result_format == "pandas":
                t = t.to_pandas()
                if len(t) == 1:
                    t = t.iloc[0]
                    t.name = "catsHTM_%s" % key
            votables[key] = t
        return votables

    def _format_one(self, catalog, result_format="json"):
        catalog_name = list(catalog.keys())[0]
        catalog_data = catalog[catalog_name]
        t = Table()
        for field in catalog_data.keys():
            data = (
                catalog_data[field]["values"]
                if "values" in catalog_data[field]
                else [catalog_data[field]["value"]]
            )
            t.add_column(Column(data, name=field))
            t[field].unit = (
                catalog_data[field]["units"]
                if "units" in catalog_data[field]
                else catalog_data[field]["unit"]
            )
        t["cat_name"] = Column(["catsHTM_%s" % catalog_name], name="cat_name")
        if result_format == "pandas":
            t = t.to_pandas()
            if len(t) == 1:
                t = t.iloc[0]
                t.name = "catsHTM_%s" % catalog_name
        return t

    def catshtm_catalog_translator(self, catalog):
        return self.CATALOG_TRANSLATE.get(catalog, catalog)

    def catshtm_conesearch(self, ra, dec, radius, catalog_name="all", format="pandas"):
        """
        catsHTM conesearch given an object and catalog_name.

        Parameters
        ----------
        ra : :py:class:`float`
            Right ascension in Degrees.
        def : :py:class:`float`
            Declination in Degrees.
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
                <catalog_name>: :class:`astropy.table.Table` or :class:`pandas.DataFrame` or :py:class:`dict`
            }
        """
        params = {
            "catalog": "%s" % self.catshtm_catalog_translator(catalog_name),
            "ra": ra,
            "dec": dec,
            "radius": "%f" % radius,
        }
        if params["catalog"] == "all":
            q = self._request_catshtm(
                "GET",
                url=self.config["CATSHTM_API_URL"]
                + self.config["CATSHTM_ROUTES"]["conesearch_all"],
                result_format=format,
                params=params,
            )
            q = self._format_all(q["catalogs"], result_format=format)
        else:
            q = self._request_catshtm(
                "GET",
                url=self.config["CATSHTM_API_URL"]
                + self.config["CATSHTM_ROUTES"]["conesearch"],
                result_format=format,
                params=params,
            )
            if isinstance(q, dict) and len(q) == 0:
                return None
            q = self._format_one(q, result_format=format)
        return q

    def catshtm_crossmatch(self, ra, dec, radius, catalog_name="all", format="pandas"):
        """
        catsHTM crossmatch given an object and catalog_name.

        Parameters
        ----------
        ra : :py:class:`float`
            Right ascension in Degrees.
        def: :py:class:`float`
            Declination in Degrees.
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
        params = {
            "catalog": "%s" % self.catshtm_catalog_translator(catalog_name),
            "ra": "%f" % ra,
            "dec": "%f" % dec,
            "radius": "%f" % radius,
        }
        if catalog_name == "all":
            q = self._request_catshtm(
                "GET",
                url=self.config["CATSHTM_API_URL"]
                + self.config["CATSHTM_ROUTES"]["crossmatch_all"],
                result_format=format,
                params=params,
            )
            q = self._format_all(q, result_format=format)
        else:
            q = self._request_catshtm(
                "GET",
                url=self.config["CATSHTM_API_URL"]
                + self.config["CATSHTM_ROUTES"]["crossmatch"],
                result_format=format,
                params=params,
            )
            q = self._format_one({catalog_name: q}, result_format=format)

        return q

    def catshtm_redshift(self, ra, dec, radius, format="votable", verbose=False):
        """
        Get redshift given an object.

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
        params = {"ra": "%f" % ra, "dec": "%f" % dec, "radius": "%f" % radius}

        xmatches = self.catshtm_crossmatch(
            ra=ra, dec=dec, radius=radius, catalog_name="all"
        )
        for catname in xmatches:
            for col in xmatches[catname].keys():
                if col == "z":
                    if verbose:
                        print(f"Redshift found: {catname}[{col}]")
                    return float(xmatches[catname][col])

        # check whether photometric redshift exists
        for catname in xmatches:
            for col in xmatches[catname].keys():
                if col in ["zphot", "z_phot"]:
                    return float(xmatches[catname][col])

        if verbose:
            print("No redshift found.")
        return None
