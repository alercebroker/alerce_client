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
    # Pass survey explicitly; this default will be removed in a future
    # release.

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

ZTF Backend Selection
---------------------

When querying ZTF data, you can choose which backend serves the request.
The default is ``"legacy"`` (the original ZTF-only API). Setting
``ztf_backend="multisurvey"`` routes ZTF queries through the new
multi-survey API, which shares the same interface as LSST queries.

.. code-block:: python

    from alerce.core import Alerce

    # Legacy backend (current default)
    client = Alerce()

    # Multi-survey backend (opt-in)
    client = Alerce(ztf_backend="multisurvey")

The legacy default will change to ``"multisurvey"`` in a future release.
A ``FutureWarning`` is emitted once per session when the legacy backend
handles a ZTF query.

Field Differences
^^^^^^^^^^^^^^^^^

The multi-survey backend renames several fields relative to the legacy API:

.. list-table::
   :header-rows: 1

   * - Endpoint
     - Legacy field
     - Multi-survey field
   * - detections, non_detections, forced_photometry, magstats, features
     - ``fid``
     - ``band``
   * - detections, forced_photometry
     - ``candid``
     - ``measurement_id``
   * - detections, non_detections
     - ``tid``
     - ``survey_id``
   * - object
     - ``ndet``
     - ``n_det``
   * - object
     - ``deltajd``
     - ``deltamjd``

The ``oid`` field also changes from a string (``"ZTF18abbrrty"``) to an
integer encoding. See the ``alerce.compat`` module below for automatic
conversion.

Survey-specific fields (``g_r_max``, ``corrected``, ``stellar``, etc.)
are included by default via the ``return_survey_extra`` parameter on
``query_object``.

Compatibility Utilities
^^^^^^^^^^^^^^^^^^^^^^^

The ``alerce.compat`` module converts multi-survey responses back to the
legacy field names and OID format:

.. code-block:: python

    from alerce.compat import to_legacy, decode_ztf_oid

    client = Alerce(ztf_backend="multisurvey")

    # Get detections from the multi-survey backend
    detections = client.query_detections("ZTF18abbrrty", survey="ztf")

    # Convert to legacy field names + string OIDs
    legacy_detections = to_legacy("detections", detections)
    # "band" -> "fid", "measurement_id" -> "candid", int oid -> "ZTF..."

    # Or decode a single OID
    name = decode_ztf_oid(36028941604196290)  # "ZTF18abbrrty"

``to_legacy`` accepts a single record (dict) or a list of records and
returns a copy; the original data is not mutated.

Timeline
--------

- **Version 1.x.x**: ALeRCE Python client only supports queries related to ZTF.
- **Version 2.0.0**: Multiple surveys (ZTF, LSST). Survey parameter is optional with ZTF as default. In the future the survey parameter will be mandatory.
- **Next**: The default ``ztf_backend`` will change from ``"legacy"`` to ``"multisurvey"``.

Questions?
----------

If you have questions about migrating your code, please:

- Check the API Reference documentation
- Review the tutorials for examples
- Open an issue on GitHub: https://github.com/alercebroker/alerce_client/issues

