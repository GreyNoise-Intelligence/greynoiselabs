#!/usr/bin/env python3

import json
import asyncio
from greynoiselabs.client import Client
from auth import login
from auth0.authentication.token_verifier import TokenVerifier, AsymmetricSignatureVerifier
import typer

AUTH0_DOMAIN = 'greynoise2.auth0.com'
AUTH0_CLIENT_ID = 'IM8Old6x7WCr2wqVI0Cz3I0c4JPSR1gn'
ALGORITHMS = ['RS256']
TOKEN_FILE = '~/.greynoiselabs/token.json'


app = typer.Typer()

current_user = None
token_data = None
client = None
authenticated = False

def output(obj):
    """
    Output the object as JSON
    """
    try:
        jobject = json.dumps(obj.__dict__) 
        print(jobject)
    except Exception as ex:
        print(f"unable to dump object {ex}")

def new_client(id_token):
    return Client("https://api.labs.greynoise.io/1/query",
                {"Authorization": f"Bearer {id_token}"})   
@app.command()
def authenticate():
    global current_user, token_data, authenticated, client
    token_data, current_user = login(TOKEN_FILE)
    if token_data != None and current_user != None:
        authenticated = True
        client = new_client(token_data['id_token'])
    else: 
        print("Authentication failed")

@app.command()
def c2s():
    if not authenticated:
        authenticate()
    response = asyncio.run(client.get_c2s())
    for c2 in response.top_c2s.c2s:
        output(c2)

@app.command()
def knocks():
    if not authenticated:
        authenticate()
    response = asyncio.run(client.get_knocks())
    for knock in response.top_knocks.knocks:
        output(knock)

@app.command()
def popular_ips():
    if not authenticated:
        authenticate()
    response = asyncio.run(client.get_i_ps())
    for ip in response.top_popular_i_ps.popular_i_ps:
        output(ip)

if __name__ == "__main__":
    app()