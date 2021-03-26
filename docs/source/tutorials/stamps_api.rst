ZTF Stamps Access
##################

The ALeRCE Stamps API Wrapper gives an easy access to our stamps API that can be used to retrieve stamps and full avro information of a specific alert.

Quickstart
===========

.. code-block:: python

    from alerce.core import Alerce
    #Import ALeRCE Client
    client = Alerce()

    stamps = client.get_stamps("ZTF18abkifng")


Making Queries
===============

There are two operations you can perform with stamps. Getting the stamps of an object and if you are on a jupyter notebook you can plot the stamps.

- :func:`~alerce.core.Alerce.get_stamps` method will allow you to get stamps of the first detection of an object id. You can also specify a candid to retrieve stamps of a different detection.
- :func:`~alerce.core.Alerce.plot_stamps` works the same as `get_stamps` but will plot the stamps using IPython HTML if you are in a notebook environment.

Examples
---------

.. code-block:: python

   # Getting specific stamp
   stamps = client.get_stamps("ZTF18abkifng",
                              candid = 576161491515015015)

   # Plot stamps on jupyter notebook
   client.plot_stamps(oid = "ZTF18abkifng",
                      candid = 576161491515015015)
