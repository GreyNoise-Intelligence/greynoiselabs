================
Python GreyNoise Labs GraphQL Client
================

.. image:: https://img.shields.io/badge/License-MIT-yellow.svg
    :target: https://opensource.org/licenses/MIT

This is an abstract python library generated from the `GreyNoise Labs GraphQL API`_ service.

.. _GreyNoise Labs API: https://api.labs.greynoise.io/

Documentation
=============
Documentation is available here: `Documentation`_

.. _Documentation: https://api.labs.greynoise.io/1/docs/

Quick Start
===========
**Install the library**:

``pip install labs_graphql_client`` or ``python setup.py install``

**Example code**:

..  code-block:: python
    import os
    import asyncio
    from labs_graphql_client.client import Client

    client = Client("https://api.labs.greynoise.io/1/query",
                    {"Authorization": f"Bearer {os.environ['AUTH_TOKEN']}"})

    response = asyncio.run(client.top_knocks())
    print(response)