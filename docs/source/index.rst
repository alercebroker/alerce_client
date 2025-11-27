.. ALeRCE Python Client documentation master file, created by
   sphinx-quickstart on Fri Jul  3 10:37:29 2020.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

.. _ALERCE ZTF API: https://api.alerce.online/ztf/v1

ALeRCE Client
================================================
`ALeRCE <http://alerce.science>`_ client is a Python library to interact with ALeRCE services and databases.

In this documentation you will find the basic usage of the ALeRCE Client, how to install, a short tutorial for each
service and the guidelines to contribute to the project.

Installing ALeRCE Client
########################

The ALeRCE client can be installed through pip with

.. code-block:: bash

    pip install alerce

Or clone the repository and install from there

.. code-block:: bash

    git clone https://github.com/alercebroker/alerce_client.git
    cd alerce_client
    python setup.py install

Tutorials
###########

The ALeRCE client is divided according to the requested API,
depending on your usecase check the following tutorials:

.. toctree::
   :maxdepth: 2
   :glob:
   
   tutorials/multisurvey_api.rst
   tutorials/ztf_api.rst
   tutorials/multisurvey_stamps_api.rst
   tutorials/xmatch_api.rst

Migration Guide
###############

.. toctree::
   :maxdepth: 2

   migration_guide


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
