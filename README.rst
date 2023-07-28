==========================================
Python GreyNoise Labs GraphQL Client & SDK
==========================================

.. image:: https://img.shields.io/badge/License-MIT-yellow.svg
    :target: https://opensource.org/licenses/MIT

This is an abstract python client and SDK library generated from the `GreyNoise Labs API`_ service.

.. _GreyNoise Labs API: https://api.labs.greynoise.io/

Documentation
=============
Documentation is available here: `Documentation`_

.. _Documentation: https://api.labs.greynoise.io/1/docs/

CLI Quick Start
===============
**Install the CLI**:

``python3 -m pip install greynoiselabs``




SDK Quick Start
===============
**Install the library**:

``python3 -m pip install greynoiselabs`` or ``make install`` when in the root directory of the repository.

Example SDK Code

You can authenticate to the Labs API and obtain a copy of your token there 
or with the CLI after running `greynoiselabs init`

..  code-block:: python

    import os
    import asyncio
    from greynoiselabs.client import Client

    client = Client("https://api.labs.greynoise.io/1/query",
                    {"Authorization": f"Bearer {os.environ['AUTH_TOKEN']}"})

    response = asyncio.run(client.top_knocks(ip="221.144.229.187"))
    print(response)
