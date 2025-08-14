Multisurvey Stamps Access
##################

The ALeRCE Stamps API Wrapper gives an easy access to our stamps API that can be used to retrieve stamps and full avro information of a specific alert.

Quickstart
===========

.. code-block:: python

    from alerce.core import Alerce
    #Import ALeRCE Client
    client = Alerce()

    ztf_stamps = client.multisurvey_get_stamps(
        oid = "ZTF18abkifng",
        survey = "ztf"
    )

    lsst_stamps = client.multisurvey_get_stamps(
        oid = "45121627560013194",
        survey = "lsst"
    )

Migration from ZTF API
======================

If you are migrating from the ZTF-only Stamps API, here are the main changes:

**Method Names**

- ``get_stamps()`` → ``multisurvey_get_stamps()``
- ``plot_stamps()`` → ``multisurvey_plot_stamps()``

**Required Survey Parameter**
All multi-survey methods now require a `survey` parameter:

.. code-block:: python

    # Old ZTF Stamp API
    objects = alerce.get_stamps(oid="ZTF18abkifng")
    
    # New Multi Survey Stamp API
    objects = alerce.multisurvey_get_stamps(survey="ztf", oid="ZTF18abkifng")

**Parameter Changes**

- Add ``survey="ztf"`` or ``survey="lsst"`` to all multi-survey method calls
- **Object ID formats vary by survey**:
  - ZTF: ``"ZTF18abbuksn"`` (string format)
  - LSST: ``45121627560013211`` (numeric format)
Making Queries
===============

There are two operations you can perform with stamps. Getting the stamps of an object and if you are on a jupyter notebook you can plot the stamps.

- :func:`~alerce.core.Alerce.multisurvey_get_stamps` method will allow you to get stamps of the first detection of an object id. You can also specify a candid to retrieve stamps of a different detection.
- :func:`~alerce.core.Alerce.multisurvey_plot_stamps` works the same as `multisurvey_get_stamps` but will plot the stamps using IPython HTML if you are in a notebook environment.

Examples
---------

.. code-block:: python

   # Getting specific stamp
   ztf_stamps = client.multisurvey_get_stamps(
        oid ="ZTF18abkifng", 
        survey = "ztf"
        measurement_id = 576161491515015015
    )

    lstt_stamps = client.multisurvey_get_stamps(
        oid ="45121627560013194", 
        survey = "lsst"
        measurement_id = 45121627560013194
    )

   # Plot stamps on jupyter notebook
   client.multisurvey_plot_stamps(
        oid ="ZTF18abkifng", 
        survey = "ztf"
        measurement_id = 576161491515015015
    )

    client.multisurvey_plot_stamps(
        oid ="45121627560013194", 
        survey = "lsst"
        measurement_id = 576161491515015015
    )
