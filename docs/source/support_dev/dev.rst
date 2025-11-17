Developer Guide
###############

Configure API for other environment
===================================

The ALeRCE client can be configured to request different API endpoints (for
example local or development instances). The recommended and current way to
override the default configuration is to create a JSON file with the desired
settings and point the library to that file using the `ALERCE_CONFIG_PATH`
environment variable.

Why use an external JSON config
-------------------------------

- Keeps environment-specific configuration out of source code.
- Works cleanly in containerized and CI environments.
- Matches the library's `load_config` behavior which checks
  `ALERCE_CONFIG_PATH` before falling back to the built-in defaults.

Create a custom config file
---------------------------

Create a JSON file (for example `my_alerce_config.json`) that replaces the
default configuration file `default_config.json` packaged with the library.

Point the client to your config
-------------------------------

Set the `ALERCE_CONFIG_PATH` environment variable to the absolute path of
your JSON file before importing or initializing the client. For example in a
bash shell:

.. code-block:: bash

    export ALERCE_CONFIG_PATH=/path/to/my_alerce_config.json
    python -c "from alerce.core import Alerce; client=Alerce(); print('configured')"

Notes on usage
--------------

- If `ALERCE_CONFIG_PATH` is not set the client uses the built-in
  `default_config.json` packaged with the library.
- The JSON file should be valid JSON. Invalid JSON will raise a `FileNotFoundError`
  or a JSON decode error when the client attempts to load it.


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
5. Create a PR `<https://github.com/alercebroker/alerce_client/pulls>`_ to the *alerce_client* repository

For a detailed guide check `this link <https://docs.github.com/en/github/collaborating-with-issues-and-pull-requests/creating-a-pull-request-from-a-fork>`_
