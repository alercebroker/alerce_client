ZTF Access
##########

The ALeRCE ZTF API Wrapper gives an easy access to our database through the `ALeRCE ZTF API`_ service with Python.

.. _`ALeRCE ZTF API`: http://dev.api.alerce.online

Usage
======

.. code-block:: python

    from alerce.core import Alerce
    alerce = Alerce()

    dataframe = alerce.query_objects()


The dataframe will have several columns, the output specification can be found in :ref:`Object Response`


Query objects
=============

We will use the :func:`~alerce.core.Alerce.query_objects` method, this method will query the ALeRCE ZTF API and get a page of results, each result has
some statistics of the object and a classification.

The filters are passed as arguments to the method, a list of valid arguments can be found in the :func:`~alerce.core.Alerce.query_objects` API reference page.

For example, getting all the objects classified as LPV could be done like this:

.. code-block:: python

    dataframe = alerce.query_objects(
        classifier="lc_classifier",
        class_name="LPV",
        format="pandas"
    )

You can specify one of the following return formats: `pandas | votable | json` with json being the default.

.. note::
  If you like to have parameters inside a dict for example that you can reuse later you can do the following:

  .. code-block:: python

     params = {
        "classifier": "stamp_classifier",
        "class_name": "SN",
        "probability": 0.7
     }
     objects = alerce.query_objects(**params)


Getting Classifier List
========================

In ALeRCE we will have multiple classifiers and each classifier will have a list of classes, also called Taxonomy.

For some filters we want to check an specific classifier, to list the current classifiers available we can use the :func:`~alerce.core.Alerce.query_classifiers` method.

.. code-block:: python

  # Getting list of classifiers
  classifiers = alerce.query_classifiers()


The *classifier_name* field should be used as a filter in :func:`~alerce.core.Alerce.query_objects` method, also if the *classifier_name* and version is already known we can
request the list of possible classes with :func:`~alerce.core.Alerce.query_classes`

.. code-block:: python

   # Getting classes for a classifier and version
   classes = alerce.query_classes("lc_classifier",
                                  "hierarchical_random_forest_1.0.0")

Querying a known list of objects
================================

You can pass `query_objects` a list of object ids to retreive information of only those objects. You can even apply filters over that list if you wanted to.

.. code-block:: python

  oids = [
      "ZTF18accqogs",
      "ZTF19aakyhxi",
      "ZTF19abyylzv",
      "ZTF19acyfpno",
  ]
  objects = alerce.query_objects(oid=oids, format="pandas")

Query Lightcurve
=================

To get the lightcurve for an object the method :func:`~alerce.core.Alerce.query_lightcurve` can be used, this will return
a dictionary with Detections and Non-detections for that object, also we can get them separetly with :func:`~alerce.core.Alerce.query_detections` and :func:`~alerce.core.Alerce.query_non_detections`.
Also, there is a method to access the forced photometries of an object :func:`~alerce.core.Alerce.query_forced_photometry`.

.. code-block:: python

    # Getting detections for an object
    detections = alerce.query_detections("ZTF18abbuksn",
                                         format="json")

    # Getting non detections for an object
    non_detections = alerce.query_non_detections("ZTF18abbuksn",
                                                 format="json")

    # Getting forced photometry for an object
    non_detections = alerce.query_forced_photometry("ZTF18abbuksn",
                                                 format="json")
    # Getting lightcurve for an object
    lightcurve = alerce.query_lightcurve("ZTF18abbuksn",
                                         format="json")

Query Probabilities
====================

To get the probabilities for an object using the different classifiers implemented by ALeRCE we wil use :func:`~alerce.core.Alerce.query_probabilities`

.. code-block:: python

  # Getting detections for an object
  probabilities = alerce.query_probabilities("ZTF18abbuksn")


Other Queries
==============

There are other more specific queries, to get more information from an object.

To get the features used by the `Light Curve Classifier <https://arxiv.org/abs/2008.03311>`_ ,
we can use :func:`~alerce.core.Alerce.query_features` or :func:`~alerce.core.Alerce.query_feature` for a single one.

(Check P. Sánchez-Sáez, et al. 2020 for more information on each feature)

.. code-block:: python

  # Getting all the features for an object as a dataframe
  features = alerce.query_features("ZTF18abbuksn", format="pandas")

  # Getting multiband period for an object
  mb_period = alerce.query_feature("ZTF18abbuksn", "Multiband_period")

For each filter ALeRCE calculate some statistics for an object, we can get
them with :func:`~alerce.core.Alerce.query_magstats`


.. code-block:: python

  # Getting magstats for an object
  magstats = alerce.query_magstats("ZTF18abbuksn")

Error Handling
===============

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
