ZTF API Access
====================

The ALeRCE ZTF API Wrapper gives an easy access to our database through the `ALeRCE ZTF API`_ service with Python.

.. _`ALeRCE ZTF API`: http://dev.api.alerce.online

Usage
###########
.. code-block:: python

    from alerce.core import Alerce
    alerce = Alerce()

    dataframe = alerce.query_objects(
        classifier="light curve", 
        class_name="LPV", 
        format="pandas"
    )

Configuration
###################
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

There are multiple ways to provide configuration to the client object `Alerce`.

As initialization parameters
------------------------------
You can pass parameters to the `Alerce` class constructor to set the parameters for API connection.

.. code-block:: python

    alerce = Alerce(ZTF_API_URL="https://ztf.alerce.online")


From a dictionary object
----------------------
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



Making Queries
################
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

A detail of the methods and their parameters is available here: :ref:`code_documentation`

Examples
--------
This section contains examples for querying lists of objects and specific object information, as well as possible parameter values for filtering.


Querying list of objects
^^^^^^^^^^^^^^^^
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


Ok, now we have a pandas dataframe with 20 objects that are classified as supernova with a probability higher than 0.7, with detections within 1 and 50, detection dates higher than 59000 and ordered by descending probability.::

  #output
  oid ndethist  ...  probability     step_id_corr
  0   ZTF18abxiess       12  ...     0.930340  corr_bulk_0.0.1
  1   ZTF20aazozim        8  ...     0.928160  corr_bulk_0.0.1
  2   ZTF20aazpaki       11  ...     0.923856  corr_bulk_0.0.1
  3   ZTF19acxpkpv      182  ...     0.922730  corr_bulk_0.0.1
  4   ZTF20aazvfcr       43  ...     0.921205  corr_bulk_0.0.1
  5   ZTF19abuxjkr        1  ...     0.919503  corr_bulk_0.0.1
  6   ZTF19aaeoqtf        3  ...     0.919234  corr_bulk_0.0.1
  7   ZTF18acbwazl       66  ...     0.918884  corr_bulk_0.0.1
  8   ZTF19ablunad        3  ...     0.916169  corr_bulk_0.0.1
  9   ZTF18abwwmjk        2  ...     0.913723  corr_bulk_0.0.1
  10  ZTF18abvjkvw        1  ...     0.909659  corr_bulk_0.0.1
  11  ZTF20aawxjqu        7  ...     0.906943  corr_bulk_0.0.1
  12  ZTF18acmzvqx       17  ...     0.906293  corr_bulk_0.0.1
  13  ZTF20abcxoog        6  ...     0.905301  corr_bulk_0.0.1
  14  ZTF20abbplei       41  ...     0.905135  corr_bulk_0.0.1
  15  ZTF18acbwayo       53  ...     0.904713  corr_bulk_0.0.1
  16  ZTF19aarhzen       42  ...     0.904626  corr_bulk_0.0.1
  17  ZTF19aaeoqqj        5  ...     0.903898  corr_bulk_0.0.1
  18  ZTF18aciguoe        4  ...     0.903845  corr_bulk_0.0.1
  19  ZTF20aazonbk        5  ...     0.903069  corr_bulk_0.0.1

  [20 rows x 23 columns]

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
^^^^^^^^^^^^^^^^^^^^^^^
You can pass `query_objects` a list of object ids to retreive information of only those objects. You can even apply filters over that list if you wanted to.

.. code-block:: python

   oids = [
       "ZTF18accqogs",
       "ZTF19aakyhxi",
       "ZTF19abyylzv",
       "ZTF19acyfpno",
   ]
   objects = client.query_objects(oid=oids, format="pandas")

::

   #output
   oid ndethist  ncovhist  ...  classifier  probability     step_id_corr
   0  ZTF18accqogs        3        60  ...        None         None  corr_bulk_0.0.1
   1  ZTF19aakyhxi        2       142  ...        None         None  corr_bulk_0.0.1
   2  ZTF19abyylzv        1        94  ...        None         None  corr_bulk_0.0.1
   3  ZTF19acyfpno        4       489  ...        None         None  corr_bulk_0.0.1
   
   [4 rows x 23 columns]


Querying single object information
^^^^^^^^^^^^^^^^^^^^^^
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


::

   #output
   mjd              candid  fid  ...     step_id_corr  phase  parent_candid
   0   58330.161493  576161491515015015    1  ...  corr_bulk_0.0.1   None              0
   1   58336.239676  582239671515015017    1  ...  corr_bulk_0.0.1   None              0
   2   58340.177674  586177671515015004    2  ...  corr_bulk_0.0.1   None              0
   3   58340.328461  586328461515015004    1  ...  corr_bulk_0.0.1   None              0
   4   58344.164931  590164931515015007    1  ...  corr_bulk_0.0.1   None              0
   5   58344.183819  590183811515015026    2  ...  corr_bulk_0.0.1   None              0
   6   58348.342211  594342211515015010    1  ...  corr_bulk_0.0.1   None              0
   7   58351.311910  597311901515015009    1  ...  corr_bulk_0.0.1   None              0
   8   58354.220961  600220961515015028    2  ...  corr_bulk_0.0.1   None              0
   9   58357.297882  603297881515015001    2  ...  corr_bulk_0.0.1   None              0
   10  58363.180243  609180241515015010    1  ...  corr_bulk_0.0.1   None              0

   [11 rows x 33 columns]


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

.. _code_documentation:

Client Documentation
#####################
.. autoclass:: alerce.core.Alerce
    :members:
    :inherited-members:
