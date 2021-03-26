Crossmatch Access
#################

The ALeRCE catsHTM API Wrapper gives an easy access to our crossmatch API that uses `catsHTM`_.

.. _`catsHTM`: https://github.com/maayane/catsHTM


Conesearch
===========

To get all the objects inside a radius in a specified catalog, we use
:func:`~alerce.core.Alerce.catshtm_conesearch`, where `ra`,`dec` is the
center of the search and `radius` is the search radius in [arcsec].


.. code-block:: python

    from alerce.core import Alerce
    #Import ALeRCE Client
    client = Alerce()
    ra = 10
    dec = 20
    radius = 1000
    catalog_name = "GAIA/DR1"
    cone_objects = client.catshtm_conesearch(ra,
                                    dec,
                                    radius,
                                    catalog_name,
                                    format="pandas")

.. note::

  Without the `catalog_name` argument the function will return a dictionary
  with all available catalogs and the value is the conesearch in those catalogs.

Crossmatch
===========

Similar to Conesearch, we look for the objects in a radius, but just get the
closest object (:func:`~alerce.core.Alerce.catshtm_crossmatch`). This method is better used for a small radius.

.. code-block:: python

    ra = 10
    dec = 20
    radius = 20
    catalog_name = "GAIA/DR1"
    xmatch_objects = client.catshtm_crossmatch(ra,
                                    dec,
                                    radius,
                                    catalog_name,
                                    format="pandas")

.. note::

  Without the `catalog_name` argument the function will return a dictionary
  with all available catalogs and the value is the crossmatch in those catalogs.

Redshift
=========

Search if there is available redshift in a `catsHTM` catalog given position
and a radius (:func:`~alerce.core.Alerce.catshtm_redshift`).

.. code-block:: python

    catalog_name = "GAIA/DR1"
    redshift = client.catshtm_redshift(ra,
                                       dec,
                                       radius,
                                       catalog_name)
