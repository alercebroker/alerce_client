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
    dataframe = alerce.multisurvey_query_objects(survey="ztf")
    
    # Query objects from LSST survey
    dataframe = alerce.multisurvey_query_objects(survey="lsst")


The dataframe will have several columns, the output specification can be found in :ref:`Object Response`

Supported Surveys
=================

The Multi Survey API currently supports the following surveys:

- **ztf**: Zwicky Transient Facility
- **lsst**: Legacy Survey of Space and Time

You must specify one of these surveys in your queries using the ``survey`` or ``survey_id`` parameter.

Query objects
=============

We will use the :func:`~alerce.core.Alerce.multisurvey_query_objects` method, this method will query the ALeRCE Multi Survey API and get a page of results, each result has some statistics of the object and a classification.

The filters are passed as arguments to the method, including the required ``survey`` parameter. A list of valid arguments can be found in the :func:`~alerce.core.Alerce.multisurvey_query_objects` API reference page.

For example, getting all the objects classified as LPV from ZTF could be done like this:

.. code-block:: python

    dataframe = alerce.multisurvey_query_objects(
        survey="ztf",
        classifier="lc_classifier",
        class_name="LPV",
        format="pandas"
    )

For LSST objects:

.. code-block:: python

    dataframe = alerce.multisurvey_query_objects(
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
        "survey": "ztf",
        "classifier": "stamp_classifier",
        "class_name": "SN",
        "probability": 0.7
     }
     objects = alerce.multisurvey_query_objects(**params)

Getting Single Object
=====================

To get information about a single object, use the :func:`~alerce.core.Alerce.multisurvey_query_object` method:

.. code-block:: python

    # Get single object from ZTF
    object_info = alerce.multisurvey_query_object(
        oid="ZTF18abbuksn", 
        survey="ztf",
        format="json"
    )

.. code-block:: python

    # Get single object from LSST
    object_info = alerce.multisurvey_query_object(
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

The *classifier_name* field should be used as a filter in :func:`~alerce.core.Alerce.multisurvey_query_objects` method, also if the *classifier_name* and version is already known we can request the list of possible classes with :func:`~alerce.core.Alerce.query_classes`

.. code-block:: python

   # Getting classes for a classifier and version
   classes = alerce.query_classes("lc_classifier",
                                  "hierarchical_random_forest_1.0.0")

Querying a known list of objects
================================

You can pass `multisurvey_query_objects` a list of object ids to retrieve information of only those objects. You can even apply filters over that list if you wanted to. Remember to specify the survey parameter.

.. code-block:: python

   # ZTF
   oids = [
       "ZTF18accqogs",
       "ZTF19aakyhxi",
       "ZTF19abyylzv",
       "ZTF19acyfpno",
   ]
   objects = alerce.multisurvey_query_objects(
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
   objects = alerce.multisurvey_query_objects(
       oid=oids, 
       survey="lsst",
       format="pandas"
   )

Query Lightcurve
=================

To get the lightcurve for an object the method :func:`~alerce.core.Alerce.multisurvey_query_lightcurve` can be used, this will return a dictionary with Detections and Non-detections for that object, also we can get them separately with :func:`~alerce.core.Alerce.multisurvey_query_detections` and :func:`~alerce.core.Alerce.multisurvey_query_non_detections`.
Also, there is a method to access the forced photometries of an object :func:`~alerce.core.Alerce.multisurvey_query_forced_photometry`.

.. code-block:: python

    # Getting detections for an object from LSST
    detections = alerce.multisurvey_query_detections(
        oid="45121627560013211",
        survey="lsst",
        format="json"
    )

    # Getting non detections for an object from LSST
    non_detections = alerce.multisurvey_query_non_detections(
        oid="45121627560013211",
        survey="lsst", 
        format="json"
    )

    # Getting forced photometry for an object from LSST
    forced_photometry = alerce.multisurvey_query_forced_photometry(
        oid="45121627560013211",
        survey="lsst",
        format="json"
    )
    
    # Getting lightcurve for an object from LSST
    lsst_lightcurve = alerce.multisurvey_query_lightcurve(
        oid="45121627560013211",
        survey="lsst",
        format="json"
    )

    # Example with ZTF object
    lightcurve = alerce.multisurvey_query_lightcurve(
        oid="ZTF18abbuksn",
        survey="ztf",
        format="json"
    )


Query Magstats
=================

To get the magstats for an object using the different classifiers implemented by ALeRCE we wil use :func:`~alerce.core.Alerce.multisurvey_query_magstats`

.. code-block:: python

  # Getting detections for a ztf object
  ztf_magstats = alerce.multisurvey_query_magstats(
    survey = "ztf",
    oid = "ZTF18abbuksn",
    )

  # Getting detections for a lsst object
  lsst_magstats = alerce.multisurvey_query_magstats(
    survey = "lsst",
    oid = "45121627560013211"
    )

Query Probability
==================

To get the probabilities for an object using the different classifiers implemented by ALeRCE we wil use :func:`~alerce.core.Alerce.multisurvey_query_probabilities`

.. code-block:: python

  # Getting detections for a ztf object
  ztf_probabilities = alerce.multisurvey_query_probabilities(
    survey = "ztf",
    classifier = "LC_classifier_BHRF_forced_phot",
    oid = "ZTF18abbuksn"
    )

  # Getting detections for a lsst object
  lssst_probabilities = alerce.multisurvey_query_probabilities(
    survey = "lsst",
    classifier = "lc_classifier_lsst",
    oid = "45121627560013211"
    )


Query Features
================

In development

Migration from ZTF API
======================

If you are migrating from the ZTF-only API, here are the main changes:

**Method Names**

- ``query_objects()`` → ``multisurvey_query_objects()``
- ``query_object()`` → ``multisurvey_query_object()``
- ``query_lightcurve()`` → ``multisurvey_query_lightcurve()``
- ``query_detections()`` → ``multisurvey_query_detections()``
- ``query_non_detections()`` → ``multisurvey_query_non_detections()``
- ``query_forced_photometry()`` → ``multisurvey_query_forced_photometry()``
- ``query_magstats()`` → ``multisurvey_query_magstats()``
- ``query_probabilities()`` → ``multisurvey_query_probabilities()``

**Required Survey Parameter**
All multi-survey methods now require a `survey` parameter:

.. code-block:: python

    # Old ZTF API
    objects = alerce.query_objects(class_name="SN")
    
    # New Multi Survey API
    objects = alerce.multisurvey_query_objects(survey="ztf", class_name="SN")

**Parameter Changes**

- **New required parameter**: Add ``survey="ztf"`` or ``survey="lsst"`` to all multi-survey method calls
- **Flexible survey specification**: You can use either ``survey`` or ``survey_id`` parameter
- **Object ID formats vary by survey**:
  - ZTF: ``"ZTF18abbuksn"`` (string format)
  - LSST: ``45121627560013211`` (numeric format)
Error Handling
===============

The ALeRCE Multi Survey Client has useful error messages that you can manage when something goes wrong. If you specify a wrong search criteria, invalid survey, or no objects were found with your query, then you will get one of the following errors:

- **Exception**: Raised when survey_id is not in valid surveys (`ztf`, `lsst`)
- **ParseError (code 400)**: Raised when there's an error with search parameters
- **ObjectNotFoundError (code 404)**: Raised when no objects were returned in your query
- **FormatValidationError (code 500)**: Raised when you set a not allowed return format

These errors usually give useful data on what you need to fix with your query.
In case you want to do something when an error happens you can capture the error as a regular python exception handling.

.. code-block:: python

    try:
        data = alerce.multisurvey_query_objects(**my_filters)
    except Exception as e:
        if "not in ['lsst', 'ztf']" in str(e):
            print("Invalid survey specified. Use 'ztf' or 'lsst'")
        else:
            print(f"Error: {e}")
        # do something else

Valid Survey Check
==================

The Multi Survey API validates that you specify a valid survey. The valid surveys are:

.. code-block:: python

    VALID_SURVEYS = ["lsst", "ztf"]

If you specify an invalid survey, you'll get an exception:

.. code-block:: python

    # This will raise an exception
    try:
        objects = alerce.multisurvey_query_objects(survey="invalid_survey")
    except Exception as e:
        print(e)  # survey_id: invalid_survey not in ['lsst', 'ztf']

Complete Example
================

Here's a complete example showing how to use the Multi Survey API:

.. code-block:: python

    from alerce.core import Alerce
    
    # Initialize the client
    alerce = Alerce()
    
    # Query objects from ZTF
    ztf_objects = alerce.multisurvey_query_objects(
        survey="ztf",
        classifier="lc_classifier", 
        class_name="SN",
        probability=0.8,
        format="pandas"
    )
    
    # Query objects from LSST  
    lsst_objects = alerce.multisurvey_query_objects(
        survey="lsst",
        classifier="lc_classifier",
        class_name="SN", 
        probability=0.8,
        format="pandas"
    )
    
    # Get lightcurve for a specific ZTF object
    if len(ztf_objects) > 0:
        oid = ztf_objects.iloc[0]['oid']
        lightcurve = alerce.multisurvey_query_lightcurve(
            oid=oid,
            survey="ztf",
            format="json"
        )
        
        # Get detections separately
        detections = alerce.multisurvey_query_detections(
            oid=oid,
            survey="ztf", 
            format="pandas"
        )