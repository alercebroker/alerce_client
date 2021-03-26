.. image:: https://github.com/alercebroker/alerce_client_new/workflows/Tests/badge.svg
.. image:: https://codecov.io/gh/alercebroker/alerce_client_new/branch/master/graph/badge.svg?token=ZUHW7C308N
  :target: https://codecov.io/gh/alercebroker/alerce_client_new
  

Welcome to ALeRCE Python Client. 
================================================
`ALeRCE <http://alerce.science>`_ client is a Python library to interact with ALeRCE services and databases.
For full documentation please visit the official Documentation_:

.. _Documentation: https://readthedocs.org/projects/alerce-new-python-client/

Installing ALeRCE Client
========================

.. code-block:: bash

    pip install git+https://git@github.com/alercebroker/alerce_client_new#egg=alerce_client


Or clone the repository and install from there

.. code-block:: bash

    git clone https://github.com/alercebroker/alerce_client_new.git
    cd alerce_client_new
    python setup.py install


Usage
===========
.. code-block:: python

    from alerce.core import Alerce
    alerce = Alerce()

    dataframe = alerce.query_objects(
        classifier="light curve", 
        class_name="LPV", 
        format="pandas"
    )

    detections = alerce.query_detections("ObjectID", format="pandas", sort="mjd")

    magstats = alerce.query_magstats("ObjectID")

    

Configuration
==============
By default the `Alerce` object should be ready to use without any external configuration, but in case you need to adjust any parameters then you can configure the Alerce object in different ways.

At the client object initialization
------------------------------------
You can pass parameters to the `Alerce` class constructor to set the parameters for API connection.

.. code-block:: python

    alerce = Alerce(ZTF_API_URL="https://ztf.alerce.online")

From a dictionary object
--------------------------
You can pass parameters to the `Alerce` class from a dictionary object.

.. code-block:: python

    my_config = {
        "ZTF_API_URL": "https://ztf.alerce.online"
    }
    alerce = Alerce()
    alerce.load_config_from_object(my_config)

From a config file
--------------------------
You can pass parameters to the `Alerce` class from a file

Take for example a ``config.py`` file:

.. code-block:: python
    
    import os

    api_url = os.getenv("API_URL")
    AlerceAPIConfig = {
        "ZTF_API_URL": api_url
    }

Then you can initialize the client like this:

.. code-block:: python

    alerce = Alerce()
    alerce.load_config_from_file("config.py")


ZTF API Access
==============

The ALeRCE ZTF API Wrapper gives an easy access to our database through the `ALeRCE ZTF API`_ service with Python.

.. _`ALeRCE ZTF API`: http://dev.api.alerce.online

Usage
-----------

.. code-block:: python

    from alerce.core import Alerce
    alerce = Alerce()

    dataframe = alerce.query_objects(
        classifier="light curve", 
        class_name="LPV", 
        format="pandas"
    )


Configuration
----------------
The available options and default values for ZTF API Client are:

.. code-block:: python

    "ZTF_API_URL": "http://dev.api.alerce.online",
    "ZTF_ROUTES": {
        "objects": "/objects",
        "single_object": "/objects/%s",
        "detections": "/objects/%s/detections",
        "non_detections": "/objects/%s/non_detections",
        "lightcurve": "/objects/%s/lightcurve",
        "magstats": "/objects/%s/magstats",
        "probabilities": "/objects/%s/probabilities"
    }


- ZTF_API_URL: The main url of the API
- ZTF_ROUTES: The routes for accessing resources. Keys inside this dictionary must remain the same.

Note: Right now there aren't multiple versions of the API or resources, so there is no need to change these parameters.

Making Queries
---------------
Making queries using the alerce client is easy. With your instance of `Alerce` class you have access to 
many methods that will allow you to make queries to one of the `ALeRCE ZTF API`_ routes.

For example, getting all the objects classified as LPV could be done like this:

.. code-block:: python

    from alerce.core import Alerce
    alerce = Alerce()

    dataframe = alerce.query_objects(
        classifier="light curve", 
        class_name="LPV",
        format="pandas"
    )


You can specify one of the following return formats: `pandas | votable | json` with json being the default.

There are other kind of queries, that are related to a specific object like *lightcurve*, *probabilities* and *magnitude statistics* queries. This queries require an object id to retrieve the data.

.. code-block:: python

    data = alerce.query_lightcurve("ZTF18abbuksn", format="json")


Notice that you can still specify a format.

There is one method for almost all of the routes available at `ALeRCE ZTF API`_ so we highly recommend that you take a look at that documentation too. It is documented with swagger ui so it is easy to explore and try out the different routes.


Examples
--------
This section contains examples for querying lists of objects and specific object information, as well as possible parameter values for filtering.


Querying list of objects
^^^^^^^^^^^^^^^^^^^^^^^^
To query lists of objects we use the `query_objects` method. We can pass the following parameters:

- format : str
     Return format. Can be one of 'pandas' | 'votable' | 'json'
- index : str
     Name of the column to use as index when format is 'pandas'
- sort : str
     Name of the column to sort when format is 'pandas'
- kwargs : dict
     These are all the parameters used to filter objects

The list of parameters available and their definition is described at `ALeRCE ZTF API`_. In this example we will filter object by class, number of observations and date of discovery. That means that we will use parameters classifier, class, ndet, and first_mjd, but we can also order our results, specify number of results and also a format, for example a pandas dataframe.

.. code-block:: python

   from alerce.core import Alerce
   client = Alerce() # no custom config needed

   objects = client.query_objects(classifier="stamp_classifier",
                                   class_name="SN",
                                   probability=0.7,
                                   ndet=[1, 50],
                                   order_by="probability",
                                   order_mode="DESC",
                                   first_mjd=59000,
                                   page_size=20, 
                                   format='pandas')


Ok, now we have a pandas dataframe with 20 objects that are classified as supernova with a probability higher than 0.7, with detections within 1 and 50, detection dates higher than 59000 and ordered by descending probability.

If you like to have parameters inside a dict for example that you can reuse later you can do the following:

.. code-block:: python

   params = {
      "classifier": "stamp_classifier",
      "class_name": "SN",
      "probability": 0.7
   }
   objects = client.query_objects(format="pandas", **params)


If you would like to search a different classifier or class take a look at `ALeRCE ZTF API`_. You can use two routes to get available classifiers and classes for every classifier.

- /classifiers/ : this will get you a list of classifiers and their metadata
- /classifiers/{name}/{version}/classes : this will get you a list of classes for a specified classifier version and name.

Querying a known list of objects
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
You can pass `query_objects` a list of object ids to retreive information of only those objects. You can even apply filters over that list if you wanted to.

.. code-block:: python

   oids = [
       "ZTF18accqogs",
       "ZTF19aakyhxi",
       "ZTF19abyylzv",
       "ZTF19acyfpno",
   ]
   objects = client.query_objects(oid=oids, format="pandas")


Querying single object information
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
There are multiple methods to get a specific object information.

- query_object gets a single object by id
- query_lightcurve gets detections and non detections of an object
- query_magstats gets magnitude statistics for a signle object
- query_probabilities gets classification information of a signle object
- query_features gets computed features of a single object

All this methods receive oid as required parameter and also format, index and sort parameters.

- oid : str
     The object identifier
- format : str
     Return format. Can be one of 'pandas' | 'votable' | 'json'
- index : str
     Name of the column to use as index when format is 'pandas'
- sort : str
     Name of the column to sort when format is 'pandas'

As an example we can get detections and non detections of an object that we can later use to plot the lightcurve

.. code-block:: python

  from alerce.core import Alerce
  client = Alerce()

  det = client.query_detections("ZTF18abkifng",
                                format="pandas",
                                sort="mjd")
  non_det = client.query_non_detections("ZTF18abkifng",
                                        format="pandas",
                                        sort="mjd")

  # what is returned by query_detections
  print(det)


Error Handling
##############
The ALeRCE Client has some useful error messages that you can manage when something goes wrong. If you specify a wrong search criteria or no objects were found with your query, then you will get one of the following errors:

- ZTFAPIError (code -1): this is the default error
- ParseError (code 400): this error is raised when there's an error with search parameters
- ObjectNotFoundError (code 404): this error is raised when no objects were returned in your query
- FormatValidationError (code 500): this error is raised when you set a not allowed return format

This errors usually give useful data on what you need to fix with your query.
In case you want to do something when an error happens you can capture the error as a regular python exception handling.

.. code-block:: python

    try:
        data = alerce.query_objects(**my_filters)
    except ObjectNotFoundError as e:
        print(e.message)
        # do something else
