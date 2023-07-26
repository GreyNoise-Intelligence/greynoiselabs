import os
import json
import asyncio
from greynoiselabs.client import Client

client = Client("https://api.labs.greynoise.io/1/query",
                {"Authorization": f"Bearer {os.environ['AUTH_TOKEN']}"})   

response = asyncio.run(client.get_i_ps())
for ip in response.top_popular_i_ps.popular_i_ps:
    jobject = json.dumps(ip.__dict__, indent = 4) 
    print(jobject)
