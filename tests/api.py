import unittest
import pandas as pd
from alerce.api import AlerceAPI
from astropy.table import Table, Column

class TestAlerceAPI(unittest.TestCase):

    oid= "ZTF19abueupg"
    api = AlerceAPI()

    def test_query(self):
        params = {
            "query_parameters":{
            "filters":{
                "nobs":{
                        "min": 2,
                        "max": 3
                    }
                }
            }
        }

        resp = self.api.query(params)
        self.assertEqual(type(resp), Table)

        resp = self.api.query(params,format="pandas")
        self.assertEqual(type(resp), pd.DataFrame)


    def test_get_sql(self):
        params = {
            "query_parameters":{
            "filters":{
                "nobs":{
                        "min": 3,
                        "max": 5
                    }
                }
            }
        }
        sql = self.api.get_sql(params)
        self.assertEqual(type(sql),str)
    def test_get_detections(self):
        detections = self.api.get_detections(self.oid)
        self.assertEqual(type(detections), Table)

        detections = self.api.get_detections("TESTO")
        self.assertEqual(detections, None)

        detections = self.api.get_detections(self.oid,format="pandas")
        self.assertEqual(type(detections), pd.DataFrame)


    def test_get_non_detections(self):
        non_detections = self.api.get_non_detections(self.oid)
        self.assertEqual(type(non_detections), Table)

        non_detections = self.api.get_non_detections("TESTO")
        self.assertEqual(non_detections, None)

        non_detections = self.api.get_non_detections(self.oid,format="pandas")
        self.assertEqual(type(non_detections), pd.DataFrame)

    def test_get_stats(self):
        stats = self.api.get_stats(self.oid)
        self.assertEqual(type(stats), Table)

        stats = self.api.get_stats(self.oid, format="pandas")
        self.assertEqual(type(stats), pd.Series)

        stats = self.api.get_stats("TESTO")
        self.assertEqual(stats, None)

    def test_get_probabilities(self):
        probs = self.api.get_probabilities(self.oid)
        self.assertEqual(type(probs), dict)
        self.assertEqual(type(probs["early"]), Table)
        self.assertEqual(type(probs["late"]), Table)

        probs = self.api.get_probabilities(self.oid,format="pandas")
        self.assertEqual(type(probs), dict)
        self.assertEqual(type(probs["early"]), pd.Series)
        self.assertEqual(type(probs["late"]), pd.Series)

        probs = self.api.get_probabilities("TESTO")
        self.assertEqual(type(probs), dict)
        self.assertEqual(type(probs["early"]),Table)
        self.assertEqual(type(probs["late"]),Table)


    def test_get_features(self):
        features = self.api.get_features(self.oid)
        self.assertEqual(type(features), Table)

        features = self.api.get_features(self.oid,format="pandas")
        self.assertEqual(type(features), pd.Series)

        features = self.api.get_features("TESTO")
        self.assertEqual(type(features), Table)


    def test_catsHTM_conesearch(self):
        conesearch = self.api.catsHTM_conesearch(self.oid,radius=100)
        self.assertEqual(type(conesearch),dict)
        for key in conesearch:
            self.assertEqual(type(conesearch[key]),Table)

        conesearch = self.api.catsHTM_conesearch(self.oid,radius=100,format="pandas")
        self.assertEqual(type(conesearch),dict)
        for key in conesearch:
            self.assertEqual(type(conesearch[key]),pd.DataFrame)

        conesearch = self.api.catsHTM_conesearch("TESTO",radius=100)
        self.assertEqual(type(conesearch),dict)
        for key in conesearch:
            self.assertEqual(type(conesearch[key]),Table)
    def test_catsHTM_xmatch(self):
        xmatch = self.api.catsHTM_crossmatch(self.oid,radius=100)
        self.assertEqual(type(xmatch),dict)
        for key in xmatch:
            self.assertEqual(type(xmatch[key]),Table)

        xmatch = self.api.catsHTM_crossmatch(self.oid,radius=100,format="pandas")
        self.assertEqual(type(xmatch),dict)
        for key in xmatch:
            self.assertEqual(type(xmatch[key]),pd.Series)
    def test_catsHTM_redshift(self):
        redshift = self.api.catsHTM_redshift(self.oid,radius=100)
        self.assertEqual(type(redshift),float)


    # def test_plot_stamp(self):
    #     pass


if __name__ == '__main__':
    unittest.main()
