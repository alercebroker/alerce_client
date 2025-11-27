Multi Survey Access
####################

The ALeRCE Multi Survey API Wrapper gives an easy access to our database through the `ALeRCE Multi Survey API`_ service with Python. This API allows you to search between ZTF and LSST surveys by specifying the survey parameter.

.. _`ALeRCE Multi Survey API`: https://api.staging.alerce.online/multisurvey/

Usage
======

.. code-block:: python

    from alerce.core import Alerce
    alerce = Alerce()

    # Query objects from ZTF survey
    dataframe = alerce.query_objects(survey="ztf")

    # Query objects from LSST survey
    dataframe = alerce.query_objects(survey="lsst")


The dataframe will have several columns, the output specification can be found in :ref:`Object Response`

Supported Surveys
=================

The Multi Survey API currently supports the following surveys:

- **ztf**: Zwicky Transient Facility
- **lsst**: Legacy Survey of Space and Time

You must specify one of these surveys in your queries using the ``survey`` parameter.

Query objects
=============

We will use the :func:`~alerce.core.Alerce.query_objects` method, this method will query the ALeRCE Multi Survey API and get a page of results, each result has some statistics of the object and a classification.

The filters are passed as arguments to the method, including the required ``survey`` parameter. A list of valid arguments can be found in the :func:`~alerce.core.Alerce.query_objects` API reference page.

For example, getting all the objects classified as LPV from ZTF could be done like this:

.. code-block:: python

    dataframe = alerce.query_objects(
        survey="ztf",
        classifier="lc_classifier",
        class_name="LPV",
        format="pandas"
    )

For LSST objects:

.. code-block:: python

    dataframe = alerce.query_objects(
        survey="lsst",
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
     objects = alerce.query_objects(survey="ztf", **params)

Getting Single Object
=====================

To get information about a single object, use the :func:`~alerce.core.Alerce.query_object` method:

.. code-block:: python

    # Get single object from ZTF
    object_info = alerce.query_object(
        oid="ZTF18abbuksn",
        survey="ztf",
        format="json"
    )

.. code-block:: python

    # Get single object from LSST
    object_info = alerce.query_object(
        oid="45121627560013194",
        survey="lsst",
        format="json"
    )


Getting Classifier List
========================

In ALeRCE we will have multiple classifiers and each classifier will have a list of classes, also called Taxonomy. Note that classifier availability may vary between surveys.

For some filters we want to check a specific classifier, to list the current classifiers available we can use the :func:`~alerce.core.Alerce.query_classifiers` method.

.. code-block:: python

  # Getting list of classifiers
  classifiers = alerce.query_classifiers()

The *classifier_name* field should be used as a filter in :func:`~alerce.core.Alerce.query_objects` method, also if the *classifier_name* and version is already known we can request the list of possible classes with :func:`~alerce.core.Alerce.query_classes`

.. code-block:: python

   # Getting classes for a classifier and version
   classes = alerce.query_classes("lc_classifier",
                                  "hierarchical_random_forest_1.0.0")

Querying a known list of objects
================================

You can pass :func:`~alerce.core.Alerce.query_objects` a list of object ids to retrieve information of only those objects. You can even apply filters over that list if you wanted to. Remember to specify the survey parameter.

.. code-block:: python

   # ZTF
   oids = [
       "ZTF18accqogs",
       "ZTF19aakyhxi",
       "ZTF19abyylzv",
       "ZTF19acyfpno",
   ]
   objects = alerce.query_objects(
       oid=oids,
       survey="ztf",
       format="pandas"
   )

.. code-block:: python

   # LSST
   oids = [
       "45121627560013194",
       "45121627560603538",
       "45121627559904665",
       "45121627560013211",
   ]
   objects = alerce.query_objects(
       oid=oids,
       survey="lsst",
       format="pandas"
   )

Query Lightcurve
=================

To get the lightcurve for an object the method :func:`~alerce.core.Alerce.query_lightcurve` can be used, this will return a dictionary with Detections and Non-detections for that object, also we can get them separately with :func:`~alerce.core.Alerce.query_detections` and :func:`~alerce.core.Alerce.query_non_detections`.
Also, there is a method to access the forced photometries of an object :func:`~alerce.core.Alerce.query_forced_photometry`.

.. code-block:: python

    # Getting detections for an object from LSST
    detections = alerce.query_detections(
        oid="45121627560013211",
        survey="lsst",
        format="json"
    )

    # Getting non detections for an object from LSST
    non_detections = alerce.query_non_detections(
        oid="45121627560013211",
        survey="lsst", 
        format="json"
    )

    # Getting forced photometry for an object from LSST
    forced_photometry = alerce.query_forced_photometry(
        oid="45121627560013211",
        survey="lsst",
        format="json"
    )
    
    # Getting lightcurve for an object from LSST
    lsst_lightcurve = alerce.query_lightcurve(
        oid="45121627560013211",
        survey="lsst",
        format="json"
    )

    # Example with ZTF object
    lightcurve = alerce.query_lightcurve(
        oid="ZTF18abbuksn",
        survey="ztf",
        format="json"
    )


Query Magstats
=================

To get the magstats for an object using the different classifiers implemented by ALeRCE we will use :func:`~alerce.core.Alerce.query_magstats`

.. code-block:: python

  # Getting magstats for a ztf object
  ztf_magstats = alerce.query_magstats(
    survey="ztf",
    oid="ZTF18abbuksn",
    )

  # Getting magstats for a lsst object
  lsst_magstats = alerce.query_magstats(
    survey="lsst",
    oid="45121627560013211"
    )

Query Probability
==================

To get the probabilities for an object using the different classifiers implemented by ALeRCE we will use :func:`~alerce.core.Alerce.query_probabilities`

.. code-block:: python

  # Getting probabilities for a ztf object
  ztf_probabilities = alerce.query_probabilities(
    survey="ztf",
    classifier="LC_classifier_BHRF_forced_phot",
    oid="ZTF18abbuksn"
    )

  # Getting probabilities for a lsst object
  lsst_probabilities = alerce.query_probabilities(
    survey="lsst",
    classifier="lc_classifier_lsst",
    oid="45121627560013211"
    )


Query Features
================

In development

Migration from ZTF API
======================

If you are migrating from the ZTF-only API, the main change is that you now need to explicitly specify the ``survey`` parameter in your method calls.

**Method Names**

The method names remain the same:

- ``query_objects()`` - Now requires ``survey`` parameter
- ``query_object()`` - Now requires ``survey`` parameter
- ``query_lightcurve()`` - Now requires ``survey`` parameter
- ``query_detections()`` - Now requires ``survey`` parameter
- ``query_non_detections()`` - Now requires ``survey`` parameter
- ``query_forced_photometry()`` - Now requires ``survey`` parameter
- ``query_magstats()`` - Now requires ``survey`` parameter
- ``query_probabilities()`` - Now requires ``survey`` parameter

**Required Survey Parameter**

All methods now require a ``survey`` parameter to specify which survey you're querying:

.. code-block:: python

    # Old ZTF API (deprecated - will show warning)
    objects = alerce.query_objects(class_name="SN")
    
    # New Multi Survey API (recommended)
    objects = alerce.query_objects(survey="ztf", class_name="SN")

**Parameter Changes**

- **New required parameter**: Add ``survey="ztf"`` or ``survey="lsst"`` to all method calls
- **Object ID formats vary by survey**:
  - ZTF: ``"ZTF18abbuksn"`` (string format)
  - LSST: ``45121627560013211`` (numeric format)

Error Handling
===============

The ALeRCE Multi Survey Client has useful error messages that you can manage when something goes wrong. If you specify a wrong search criteria, invalid survey, or no objects were found with your query, then you will get one of the following errors:

- **ValueError**: Raised when survey is not in valid surveys (`ztf`, `lsst`)
- **ParseError (code 400)**: Raised when there's an error with search parameters
- **ObjectNotFoundError (code 404)**: Raised when no objects were returned in your query
- **FormatValidationError (code 500)**: Raised when you set a not allowed return format

These errors usually give useful data on what you need to fix with your query.
In case you want to do something when an error happens you can capture the error as a regular python exception handling.

.. code-block:: python

    try:
        data = alerce.query_objects(survey="ztf", **my_filters)
    except ValueError as e:
        if "survey must be one of" in str(e):
            print("Invalid survey specified. Use 'ztf' or 'lsst'")
        else:
            print(f"Error: {e}")
        # do something else

Valid Survey Check
==================

The Multi Survey API validates that you specify a valid survey. The valid surveys are:

.. code-block:: python

    VALID_SURVEYS = ["lsst", "ztf"]

If you specify an invalid survey, you'll get a ValueError:

.. code-block:: python

    # This will raise a ValueError
    try:
        objects = alerce.query_objects(survey="invalid_survey")
    except ValueError as e:
        print(e)  # survey must be one of ['ztf', 'lsst']

Complete Example
================

Here's a complete example showing how to use the Multi Survey API:

.. code-block:: python

    from alerce.core import Alerce
    
    # Initialize the client
    alerce = Alerce()
    
    # Query objects from ZTF
    ztf_objects = alerce.query_objects(
        survey="ztf",
        classifier="lc_classifier", 
        class_name="SN",
        probability=0.8,
        format="pandas"
    )
    
    # Query objects from LSST  
    lsst_objects = alerce.query_objects(
        survey="lsst",
        classifier="lc_classifier",
        class_name="SN", 
        probability=0.8,
        format="pandas"
    )
    
    # Get lightcurve for a specific ZTF object
    if len(ztf_objects) > 0:
        oid = ztf_objects.iloc[0]['oid']
        lightcurve = alerce.query_lightcurve(
            oid=oid,
            survey="ztf",
            format="json"
        )
        
        # Get detections separately
        detections = alerce.query_detections(
            oid=oid,
            survey="ztf", 
            format="pandas"
        )