Developer Guide
###############

Configure API for other environment
===================================

The ALeRCE client can be modified to request other APIs (for example local or develop APIs). To change the default behavior we have two ways,
as initialization parameters or calling a method to change the routes.

As initialization parameters
------------------------------
You can pass parameters to the `Alerce` class constructor to set the parameters for API connection.

.. code-block:: python

    alerce = Alerce(ZTF_API_URL="https://ztf.alerce.online")


From a dictionary object
----------------------
You can pass parameters to the `Alerce` class from a dictionary object.

.. code-block:: python

    my_config = {
        "ZTF_API_URL": "https://ztf.alerce.online"
    }
    alerce = Alerce()
    alerce.load_config_from_object(my_config)

Routes that can be modified
----------------------------

The examples changes the default ZTF api, but there are other API and routes that can be modified, all the routes are the following

.. list-table:: Routes
   :widths: 20 25 55
   :header-rows: 1

   * - Variable
     - Default
     - Description
   * - ZTF_API_URL
     - http://dev.api.alerce.online/
     - ALeRCE ZTF API route.
   * - ZTF_ROUTES
     - {
        'objects':'/objects',
        'single_object':'/objects/%s',
        'detections':'/objects/%s/detections',
        'non_detections':'/objects/%s/non_detections',
        'lightcurve':'/objects/%s/lightcurve',
        'magstats':'/objects/%s/magstats',
        'probabilities': '/objects/%s/probabilities'
       }
     - Dictionary with query type and route, with %s as wildcard for object id
   * - CATSHTM_API_URL
     - http://catshtm.alerce.online
     - ALeRCE catsHTM API base url.
   * - CATSHTM_ROUTES
     - {
        "conesearch": "/conesearch",
        "conesearch_all": "/conesearch_all",
        "crossmatch": "/crossmatch",
        "crossmatch_all": "/crossmatch_all"
       }
     - ALeRCE catsHTM routes.

   * - AVRO_URL
     - http://avro.alerce.online
     - ZTF AVRO/Stamps API
   * - AVRO_ROUTES
     - {
         "get_stamp": "/get_stamp",
       }
     - ZTF AVRO/Stamps API Routes

How to contribute
=================

We are open to contributions in new features or fixing issues.

To send a contribution add the #IssueNumber in the Pull Request (PR) for Issue tracker, the PR then will be assigned to the team to be reviewed.

Steps to create a Pull Request
------------------------------

1. Fork the repository
2. Create a branch if necessary
3. Fix the issue or add new feature
4. Push changed to personal repository
5. `Create a PR <https://github.com/alercebroker/alerce_client_new/pulls>` to the *alercebroker* repository

For a detailed guide check `this link <https://docs.github.com/en/github/collaborating-with-issues-and-pull-requests/creating-a-pull-request-from-a-fork>`_
