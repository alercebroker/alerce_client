Stamps API Access
================
The ALeRCE Stamps API Wrapper gives an easy access to our stamps API that can be used to retreive stamps and full avro information of a specific alert.

Usage
###########
.. code-block:: python

    from alerce.core import Alerce
    client = Alerce()

    stamps = client.get_stamps("ObjectID") 

Configuration
###################
The available options and default values for stamps API Client are:

.. code-block:: python

    "AVRO_URL": "http://avro.alerce.online",
    "AVRO_ROUTES": {
      "get_stamp": "/get_stamp",
    }


- AVRO_URL: The main url of the API
- AVRO_ROUTES: The routes for accessing resources. Keys inside this dictionary must remain the same.

Note: Right now there aren't multiple versions of the API or resources, so there is no need to change these parameters.

There are multiple ways to provide configuration to the client object `Alerce`.

As initialization parameters
------------------------------
You can pass parameters to the `Alerce` class constructor to set the parameters for API connection.

.. code-block:: python

    alerce = Alerce(AVRO_URL="http://avro.alerce.online")


From a dictionary object
----------------------
You can pass parameters to the `Alerce` class from a dictionary object.

.. code-block:: python

    my_config = {
        "AVRO_URL": "http://catshtm.alerce.online"
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
        "AVRO_URL": api_url
    }

Then you can initialize the client like this:

.. code-block:: python

    alerce = Alerce()
    alerce.load_config_from_file("config.py")

Making Queries
################
There are two operations you can perform with stamps. Getting the stamps of an object and if you are on a jupyter notebook you can plot the stamps. A detailed explanation of each method and parameters can be found here: :ref:`code_documentation`

- get_stamps method will allow you to get stamps of the first detection of an object id. You can also specify a candid to retrieve stamps of a different detection.
- plot_stamp works the same as get_stamps but will plot the stamps using IPython HTML if you are in a notebook environment.

Examples
---------

.. code-block:: python

   from alerce.core import Alerce
   client = Alerce()

   # get stamps
   stamps = client.get_stamps("ZTF18abkifng")
   # plot stamps on jupyter notebook
   client.plot_stamps("ZTF18abkifng", candid=576161491515015015) 


.. _code_documentation:

Client Documentation
#####################
.. autoclass:: alerce.core.Alerce
    :members:
    :inherited-members:
