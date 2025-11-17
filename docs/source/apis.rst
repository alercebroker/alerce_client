API Reference
=============

The ALeRCE Client provides a unified interface for querying astronomical data from multiple surveys.

Getting Started
---------------

Import and instantiate the client:

.. code-block:: python

    from alerce.core import Alerce

    client = Alerce()

.. note::
   **Important: Survey Parameter**

   Most methods now require a ``survey`` parameter to specify which survey data to query.
   Currently supported surveys: ``"ztf"`` and ``"lsst"``.

   While some methods still default to ``"ztf"`` for backward compatibility, this behavior
   is deprecated and will be removed in future versions. **Always specify the survey explicitly.**

ALeRCE Client
-------------

.. autoclass:: alerce.Alerce
   :members:
   :inherited-members:
   :exclude-members: legacy_ztf_client, multisurvey_client, legacy_stamps_client, multisurvey_stamps_client, valid_surveys, session, CATALOG_TRANSLATE
   :member-order: groupwise
   :noindex:

Object Queries
^^^^^^^^^^^^^^

Methods for querying astronomical objects and their metadata.

.. autosummary::
   :nosignatures:

   alerce.Alerce.query_objects
   alerce.Alerce.query_object

Photometry Queries
^^^^^^^^^^^^^^^^^^

Methods for querying photometric measurements and statistics.

.. autosummary::
   :nosignatures:

   alerce.Alerce.query_lightcurve
   alerce.Alerce.query_detections
   alerce.Alerce.query_non_detections
   alerce.Alerce.query_forced_photometry
   alerce.Alerce.query_magstats

Classification & Features
^^^^^^^^^^^^^^^^^^^^^^^^^

Methods for querying object classifications and features.

.. autosummary::
   :nosignatures:

   alerce.Alerce.query_probabilities
   alerce.Alerce.query_features
   alerce.Alerce.query_feature
   alerce.Alerce.query_classifiers
   alerce.Alerce.query_classes

Stamps
^^^^^^

Methods for retrieving and visualizing image stamps.

.. autosummary::
   :nosignatures:

   alerce.Alerce.get_stamps
   alerce.Alerce.plot_stamps
   alerce.Alerce.get_avro

Crossmatching
^^^^^^^^^^^^^

Methods for crossmatching astronomical catalogs.

.. autosummary::
   :nosignatures:

   alerce.Alerce.catshtm_conesearch
   alerce.Alerce.catshtm_crossmatch
   alerce.Alerce.catshtm_redshift
   alerce.Alerce.catshtm_catalog_translator
