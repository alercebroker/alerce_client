Multisurvey Stamps Access
=========================

The ALeRCE Stamps API Wrapper gives an easy access to our stamps API that can be used to retrieve stamps and full avro information of a specific alert.

Quickstart
===========

.. code-block:: python

    from alerce.core import Alerce
    #Import ALeRCE Client
    client = Alerce()

    ztf_stamps = client.get_stamps(
        oid="ZTF18abkifng",
        survey="ztf"
    )

    lsst_stamps = client.get_stamps(
        oid="45121627560013194",
        survey="lsst"
    )

Migration from ZTF API
======================

If you are migrating from the ZTF-only Stamps API, the main change is that you now need to explicitly specify the ``survey`` parameter in your method calls.

**Method Names**

The method names remain the same:

- ``get_stamps()`` - Now requires ``survey`` parameter
- ``plot_stamps()`` - Now requires ``survey`` parameter

**Required Survey Parameter**

All methods now require a ``survey`` parameter to specify which survey you're querying:

.. code-block:: python

    # Old ZTF Stamp API (deprecated - will show warning)
    stamps = alerce.get_stamps(oid="ZTF18abkifng")

    # New Multi Survey Stamp API (recommended)
    stamps = alerce.get_stamps(oid="ZTF18abkifng", survey="ztf")

**Parameter Changes**

- **New required parameter**: Add ``survey="ztf"`` or ``survey="lsst"`` to all method calls
- **Object ID formats vary by survey**:
  - ZTF: ``"ZTF18abbuksn"`` (string format)
  - LSST: ``45121627560013211`` (numeric format)

Making Queries
===============

There are two operations you can perform with stamps. Getting the stamps of an object and if you are on a jupyter notebook you can plot the stamps.

- :func:`~alerce.core.Alerce.get_stamps` method will allow you to get stamps of the first detection of an object id. You can also specify a candid to retrieve stamps of a different detection.
- :func:`~alerce.core.Alerce.plot_stamps` works the same as `get_stamps` but will plot the stamps using IPython HTML if you are in a notebook environment.

Examples
---------

.. code-block:: python

   # Getting specific stamp
   ztf_stamps = client.get_stamps(
        oid="ZTF18abkifng",
        survey="ztf",
        measurement_id=576161491515015015
    )

   lsst_stamps = client.get_stamps(
        oid="45121627560013194",
        survey="lsst",
        measurement_id=45121627560013194
    )

   # Plot stamps on jupyter notebook
   client.plot_stamps(
        oid="ZTF18abkifng",
        survey="ztf",
        measurement_id=576161491515015015
    )

   client.plot_stamps(
        oid="45121627560013194",
        survey="lsst",
        measurement_id=576161491515015015
    )
