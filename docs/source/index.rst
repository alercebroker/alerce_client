.. ALeRCE Python Client documentation master file, created by
   sphinx-quickstart on Fri Jul  3 10:37:29 2020.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

ALeRCE Client
================================================
`ALeRCE <http://alerce.science>`_ client is a Python library to interact with ALeRCE services and databases.

In this documentation you will find the basic usage of the ALeRCE Client, how to install, a short tutorial for each
service and the guidelines to contribute to the project.

Installing ALeRCE Client
########################

The ALeRCE client can be installed through pip with

.. code-block:: bash

    pip install git+https://git@github.com/alercebroker/alerce_client_new#egg=alerce

Or clone the repository and install from there

.. code-block:: bash

    git clone https://github.com/alercebroker/alerce_client_new.git
    cd alerce_client_new
    python setup.py install

Tutorials
###########

The ALeRCE client is divided according to the requested API,
depending on your usecase check the following tutorials:

.. toctree::
   :maxdepth: 2
   :glob:

   tutorials/ztf_api.rst
   tutorials/stamps_api.rst
   tutorials/xmatch_api.rst


API Reference
#############
.. toctree::
  :maxdepth: 2
  :glob:

  apis
  models


Developer and Support documentation
####################################

.. toctree::
  :maxdepth: 2

  support_dev/support
  support_dev/dev
