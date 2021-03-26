.. image:: https://github.com/alercebroker/alerce_client_new/workflows/Tests/badge.svg 
.. image:: https://codecov.io/gh/alercebroker/alerce_client_new/branch/master/graph/badge.svg?token=ZUHW7C308N
  :target: https://codecov.io/gh/alercebroker/alerce_client_new
.. image:: https://readthedocs.org/projects/alerce/badge/?version=latest
:target: https://alerce.readthedocs.io/en/latest/?badge=latest
:alt: Documentation Status


Welcome to ALeRCE Python Client. 
================================================
`ALeRCE <http://alerce.science>`_ client is a Python library to interact with ALeRCE services and databases.

For full documentation please visit the official Documentation_:

.. _Documentation: https://alerce.readthedocs.io/en/latest/

Installing ALeRCE Client
========================

.. code-block:: bash

    pip install alerce


Or clone the repository and install from there

.. code-block:: bash

    git clone https://github.com/alercebroker/alerce_client.git
    cd alerce_client
    python setup.py install


Usage
===========
.. code-block:: python

    from alerce.core import Alerce
    alerce = Alerce()

    dataframe = alerce.query_objects(
        classifier="lc_classifier", 
        class_name="LPV", 
        format="pandas"
    )

    detections = alerce.query_detections("ZTF20aaelulu", format="pandas", sort="mjd")

    magstats = alerce.query_magstats("ZTF20aaelulu")

    

Configuration
==============
By default the `Alerce` object should be ready to use without any external configuration, but in case you need to adjust any parameters then you can configure the Alerce object in different ways.

At the client object initialization
------------------------------------
You can pass parameters to the `Alerce` class constructor to set the parameters for API connection.


For example using an API on localhost:
.. code-block:: python

    alerce = Alerce(ZTF_API_URL="http://localhost:5000")

From a dictionary object
--------------------------
You can pass parameters to the `Alerce` class from a dictionary object.

.. code-block:: python

    my_config = {
        "ZTF_API_URL": "http://localhost:5000"
    }
    alerce = Alerce()
    alerce.load_config_from_object(my_config)