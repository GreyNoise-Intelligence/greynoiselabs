====================================
Python GreyNoise Labs GraphQL Client
====================================

.. image:: https://img.shields.io/badge/License-MIT-yellow.svg
    :target: https://opensource.org/licenses/MIT

This is an abstract python library generated from the `GreyNoise Labs API`_ service.

.. _GreyNoise Labs API: https://api.labs.greynoise.io/

Documentation
=============
Documentation is available here: `Documentation`_

.. _Documentation: https://api.labs.greynoise.io/1/docs/

Quick Start
===========
**Install the library**:

``pip install greynoiselabs`` or ``python setup.py install``

Example Code

..  code-block:: python

    import os
    import asyncio
    from greynoiselabs.client import Client

    client = Client("https://api.labs.greynoise.io/1/query",
                    {"Authorization": f"Bearer {os.environ['AUTH_TOKEN']}"})

    response = asyncio.run(client.top_knocks(ip="221.144.229.187"))
    print(response)
