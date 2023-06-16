import os
import asyncio
from greynoiselabs.client import Client

client = Client("https://api.labs.greynoise.io/1/query",
                {"Authorization": f"Bearer {os.environ['AUTH_TOKEN']}"})

response = asyncio.run(client.top_knocks(ip="221.144.229.187"))
print(response)