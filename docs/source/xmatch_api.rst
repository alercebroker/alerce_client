Crossmatch API Access
=================
The ALeRCE catsHTM API Wrapper gives an easy access to our crossmatch API that uses `catsHTM`_.

.. _`catsHTM`: https://github.com/maayane/catsHTM

Usage
###########
.. code-block:: python

    from alerce.core import Alerce
    client = Alerce()

    ra = 10
    dec = 20
    radius = 3600
    catalog_name = "GAIA/DR1"

    objects = client.catshtm_conesearch(ra, dec, radius, catalog_name, format="pandas")


Configuration
###################
The available options and default values for catsHTM API Client are:

.. code-block:: python

    "CATSHTM_API_URL": "http://catshtm.alerce.online",
    "CATSHTM_ROUTES": {
      "conesearch": "/conesearch",
      "conesearch_all": "/conesearch_all",
      "crossmatch": "/crossmatch",
      "crossmatch_all": "/crossmatch_all"
    }


- CATSHTM_API_URL: The main url of the API
- CATSHTM_ROUTES: The routes for accessing resources. Keys inside this dictionary must remain the same.

Note: Right now there aren't multiple versions of the API or resources, so there is no need to change these parameters.

There are multiple ways to provide configuration to the client object `Alerce`.

As initialization parameters
------------------------------
You can pass parameters to the `Alerce` class constructor to set the parameters for API connection.

.. code-block:: python

    alerce = Alerce(CATSHTM_API_URL="http://catshtm.alerce.online")


From a dictionary object
----------------------
You can pass parameters to the `Alerce` class from a dictionary object.

.. code-block:: python

    my_config = {
        "CATSHTM_API_URL": "https://catshtm.alerce.online"
    }
    alerce = Alerce()
    alerce.load_config_from_object(my_config)

From a config file
--------------------------
You can pass parameters to the `Alerce` class from a file

Take for example a ``config.py`` file:

.. code-block:: python
    
    import os

    api_url = os.getenv("API_URL")
    AlerceAPIConfig = {
        "CATSHTM_API_URL": api_url
    }

Then you can initialize the client like this:

.. code-block:: python

    alerce = Alerce()
    alerce.load_config_from_file("config.py")

Making Queries
################
There are 3 queries that we can do using methods:

- catshtm_conesearch: performs conesearch at specified coordinates and radius
- catshtm_crossmatch: performs crossmatch at specified coordinates and radius
- catshtm_redshift: gets redshift of object at specified coordinates and radius

You can provide all 3 methods with ra, dec, radius and format parameters. A detailed view of methods and their parameters is available here: :ref:`code_documentation`

Examples
----------

.. code-block:: python

  from alerce.core import Alerce
  client = Alerce()

  objects = client.catshtm_conesearch(
        ra=357.73373, dec=14.20514, radius=10, format="pandas", catalog_name="GAIA/DR2"
  )

::

  #output
  A_G                           None
  Dec                        14.2051
  Epoch                       2015.5
  ErrDec                   0.0489854
  ErrPMDec                  0.103013
  ErrPMRA                   0.170827
  ErrPlx                      0.1104
  ErrRA                    0.0819471
  ErrRV                         None
  ExcessNoise               0.170845
  ExcessNoiseSig            0.992917
  MagErr_BP                0.0318054
  MagErr_G                0.00957389
  MagErr_RP                0.0286855
  Mag_BP                     17.3911
  Mag_G                      17.1829
  Mag_RP                     16.7614
  PMDec                     -2.01217
  PMRA                      0.942828
  Plx                      0.0577046
  RA                         357.734
  RA_Dec_Corr               0.413582
  RV                            None
  Teff                          None
  Teff_high                     None
  Teff_low                      None
  VarFlag                          1
  cat_name          catsHTM_GAIA/DR2
  Name: catsHTM_GAIA/DR2, dtype: object



.. _code_documentation:

Client Documentation
#####################
.. autoclass:: alerce.core.Alerce
    :members:
    :inherited-members:
