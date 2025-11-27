Multi-Survey Migration Guide
============================

As of version 2.0.0, the ALeRCE Client supports multiple astronomical surveys beyond ZTF. This guide helps you migrate your code to the new multi-survey API.

What's Changed
--------------

The main change is that **most query methods now require a ``survey`` parameter** to specify which survey's data you want to query.

Supported Surveys
^^^^^^^^^^^^^^^^^

Currently supported surveys:

- ``"ztf"`` - Zwicky Transient Facility
- ``"lsst"`` - Legacy Survey of Space and Time (Vera C. Rubin Observatory)

Backward Compatibility
----------------------

For backward compatibility, many methods still default to ``survey="ztf"`` when the parameter is not provided. However, this behavior is **deprecated** and will be removed in a future version.

When you omit the survey parameter, you'll see a deprecation warning:

.. code-block:: python

    client = Alerce()

    # This works but shows a deprecation warning
    objects = client.query_objects(ra=10.0, dec=-20.0, radius=30)
    # DeprecationWarning: survey not provided, defaulting to 'ztf'.
    # This will use the legacy ZTF client. This behavior will be
    # deprecated in future versions.

Migration Examples
------------------

Object Queries
^^^^^^^^^^^^^^

**Before (deprecated):**

.. code-block:: python

    from alerce.core import Alerce

    client = Alerce()

    # Implicitly uses ZTF
    objects = client.query_objects(
        ra=10.0,
        dec=-20.0,
        radius=30
    )

**After (recommended):**

.. code-block:: python

    from alerce.core import Alerce

    client = Alerce()

    # Explicitly specify survey
    ztf_objects = client.query_objects(
        survey="ztf",
        ra=10.0,
        dec=-20.0,
        radius=30
    )

    # Or query LSST data
    lsst_objects = client.query_objects(
        survey="lsst",
        ra=10.0,
        dec=-20.0,
        radius=30
    )

Lightcurve Queries
^^^^^^^^^^^^^^^^^^

**Before (deprecated):**

.. code-block:: python

    lightcurve = client.query_lightcurve("ZTF21aaeyldq")

**After (recommended):**

.. code-block:: python

    ztf_lightcurve = client.query_lightcurve("ZTF21aaeyldq", survey="ztf")
    lsst_lightcurve = client.query_lightcurve("LSST123456", survey="lsst")

Detections and Photometry
^^^^^^^^^^^^^^^^^^^^^^^^^^

**Before (deprecated):**

.. code-block:: python

    detections = client.query_detections("ZTF21aaeyldq")
    magstats = client.query_magstats("ZTF21aaeyldq")
    forced_phot = client.query_forced_photometry("ZTF21aaeyldq")

**After (recommended):**

.. code-block:: python

    detections = client.query_detections("ZTF21aaeyldq", survey="ztf")
    magstats = client.query_magstats("ZTF21aaeyldq", survey="ztf")
    forced_phot = client.query_forced_photometry("ZTF21aaeyldq", survey="ztf")

Stamps
^^^^^^

**Before (deprecated):**

.. code-block:: python

    stamps = client.get_stamps(oid="ZTF21aaeyldq", candid=1234567890)
    client.plot_stamps(oid="ZTF21aaeyldq", candid=1234567890)

**After (recommended):**

.. code-block:: python

    stamps = client.get_stamps(
        oid="ZTF21aaeyldq",
        candid=1234567890,
        survey="ztf"
    )

    client.plot_stamps(
        oid="ZTF21aaeyldq",
        candid=1234567890,
        survey="ztf"
    )

Features and Classifications
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

**Before (deprecated):**

.. code-block:: python

    features = client.query_features("ZTF21aaeyldq")
    probabilities = client.query_probabilities("ZTF21aaeyldq")

**After (recommended):**

.. code-block:: python

    features = client.query_features("ZTF21aaeyldq", survey="ztf")
    probabilities = client.query_probabilities("ZTF21aaeyldq", survey="ztf")

Best Practices
--------------

1. **Always specify the survey parameter** in your code to avoid deprecation warnings and ensure future compatibility.

2. **Use descriptive variable names** when querying multiple surveys:

   .. code-block:: python

       ztf_objects = client.query_objects(survey="ztf", ...)
       lsst_objects = client.query_objects(survey="lsst", ...)

3. **Check survey availability** before querying if you're writing reusable code:

   .. code-block:: python

       valid_surveys = ["ztf", "lsst"]

       for survey in valid_surveys:
           try:
               objects = client.query_objects(survey=survey, ...)
           except ValueError as e:
               print(f"Survey {survey} not available: {e}")

Migration Checklist
-------------------

Use this checklist to update your code:

.. code-block:: text

    ☐ Add survey="ztf" to all query_objects() calls
    ☐ Add survey="ztf" to all query_object() calls
    ☐ Add survey="ztf" to all query_lightcurve() calls
    ☐ Add survey="ztf" to all query_detections() calls
    ☐ Add survey="ztf" to all query_non_detections() calls
    ☐ Add survey="ztf" to all query_forced_photometry() calls
    ☐ Add survey="ztf" to all query_magstats() calls
    ☐ Add survey="ztf" to all query_probabilities() calls
    ☐ Add survey="ztf" to all query_features() calls
    ☐ Add survey="ztf" to all query_feature() calls
    ☐ Add survey="ztf" to all get_stamps() calls
    ☐ Add survey="ztf" to all plot_stamps() calls
    ☐ Run your test suite to ensure everything works
    ☐ Remove any deprecation warning suppressions

Timeline
--------

- **Version 1.x.x**: ALeRCE Python client only supports queries related to ZTF.
- **Version 2.0.0**: Multiple surveys (ZTF, LSST). Survey parameter is optional with ZTF as default. In the future the survey parameter will be mandatory.

Questions?
----------

If you have questions about migrating your code, please:

- Check the API Reference documentation
- Review the tutorials for examples
- Open an issue on GitHub: https://github.com/alercebroker/alerce_client/issues

