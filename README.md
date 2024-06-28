![image](https://github.com/alercebroker/alerce_client/workflows/Tests/badge.svg)[![codecov](https://codecov.io/gh/alercebroker/alerce_client/graph/badge.svg?token=Y2AQJ3SWFE)](https://codecov.io/gh/alercebroker/alerce_client)![image](https://readthedocs.org/projects/alerce/badge/?version=latest)


Welcome to ALeRCE Python Client.
================================

[ALeRCE](http://alerce.science) client is a Python library to interact
with ALeRCE services and databases.

For full documentation please visit the official
[Documentation](https://alerce.readthedocs.io/en/latest/):

Installing ALeRCE Client
========================

``` {.sourceCode .bash}
pip install alerce
```

Or clone the repository and install from there

``` {.sourceCode .bash}
git clone https://github.com/alercebroker/alerce_client.git
cd alerce_client
python setup.py install
```

Usage
=====

``` {.sourceCode .python}
from alerce.core import Alerce
alerce = Alerce()

dataframe = alerce.query_objects(
    classifier="lc_classifier", 
    class_name="LPV", 
    format="pandas"
)

detections = alerce.query_detections("ZTF20aaelulu", format="pandas", sort="mjd")

magstats = alerce.query_magstats("ZTF20aaelulu")

query='''
SELECT
    oid, sgmag1, srmag1, simag1, szmag1, sgscore1
FROM
    ps1_ztf
WHERE
    oid = 'ZTF20aaelulu'
'''
detections_direct = alerce.send_query(query, format="pandas")
```

Configuration
=============

By default the Alerce object should be ready to use without any external
configuration, but in case you need to adjust any parameters then you
can configure the Alerce object in different ways.

At the client object initialization
-----------------------------------

You can pass parameters to the Alerce class constructor to set the
parameters for API connection.

For example using the ZTF API on localhost:5000 and the DB API on localhost:5050 
``` {.sourceCode .python}
alerce = Alerce(ZTF_API_URL="<http://localhost:5000>", ZTF_DB_API_URL="<http://localhost:5050>")
```

From a dictionary object
------------------------

You can pass parameters to the Alerce class from a dictionary object.

``` {.sourceCode .python}
my_config = {
    "ZTF_API_URL": "http://localhost:5000"
    "ZTF_DB_API_URL": "http://localhost:5050"
}
alerce = Alerce()
alerce.load_config_from_object(my_config)
```
Contribuiting
=============
Each pull request must have at least one commit following the [angular commit guidelines](https://github.com/angular/angular.js/blob/master/DEVELOPERS.md#commits) for the semantic versioning to work.
