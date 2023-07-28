#!/usr/bin/env python3

import json
import os
import time

import jwt
import requests
import typer
from auth0.authentication.token_verifier import (
    AsymmetricSignatureVerifier,
    TokenVerifier,
)
from requests_oauthlib import OAuth2Session

AUTH0_DOMAIN = "greynoise2.auth0.com"
AUTH0_CLIENT_ID = "IM8Old6x7WCr2wqVI0Cz3I0c4JPSR1gn"
TOKEN_URL = f"https://{AUTH0_DOMAIN}/oauth/token"
JWKS_URL = f"https://{AUTH0_DOMAIN}/.well-known/jwks.json"
ISSUER_URL = f"https://{AUTH0_DOMAIN}/"
ALGORITHMS = ["RS256"]


def get_token_from_file(token_filename: str):
    """
    Gets the token from a file
    """
    try:
        fp = os.path.expanduser(token_filename)
        with open(fp, "r") as f:
            token_data = json.load(f)
            return token_data
    except Exception as ex:
        print(f"Unable to load token from {token_filename}, {ex}")
        return None


def token_saver(token_filename: str, token_data: any):
    """
    Saves the token to a file
    """
    try:
        fp = os.path.expanduser(token_filename)
        os.makedirs(os.path.dirname(fp), exist_ok=True)
        with open(fp, "w+") as f:
            json.dump(token_data, f)
        print(f"Token saved to {token_filename}.")
    except Exception as ex:
        print(f"Unable to save token to {token_filename}, {ex}")
        raise typer.Abort()


def token_refresh(token_filename: str, token_data_in: any):
    """
    Refreshes the token
    """
    extra = {
        "client_id": AUTH0_CLIENT_ID,
    }
    try:
        client = OAuth2Session(AUTH0_CLIENT_ID, token=token_data_in)
        token_data = client.refresh_token(TOKEN_URL, **extra)
        token_saver(token_filename, token_data)
        return token_data
    except Exception as ex:
        print(f"Unable to refresh token {ex}.")
        return None


def validate_token(id_token: any):
    """
    Verify the token and its precedence

    :param id_token:
    """
    sv = AsymmetricSignatureVerifier(JWKS_URL)
    tv = TokenVerifier(
        signature_verifier=sv, issuer=ISSUER_URL, audience=AUTH0_CLIENT_ID
    )
    try:
        tv.verify(id_token)
        return True
    except Exception:
        return False


def init_device_flow():
    """
    Initiate Oauth 2.0 Device Authorization Flow with Auth0
    """
    authenticated = False
    device_code_payload = {
        "client_id": AUTH0_CLIENT_ID,
        "scope": "openid profile offline_access",
    }
    device_code_response = requests.post(
        "https://{}/oauth/device/code".format(AUTH0_DOMAIN), data=device_code_payload
    )

    if device_code_response.status_code != 200:
        print("Error generating the device code")
        raise typer.Exit(code=1)

    print("Device code successful")
    device_code_data = device_code_response.json()
    print("1. Please browse to: ", device_code_data["verification_uri_complete"])
    print("2. Verify the code matches: ", device_code_data["user_code"])

    token_payload = {
        "grant_type": "urn:ietf:params:oauth:grant-type:device_code",
        "device_code": device_code_data["device_code"],
        "client_id": AUTH0_CLIENT_ID,
    }
    while not authenticated:
        print("Please click the link above and follow the instructions...")
        token_response = requests.post(TOKEN_URL, data=token_payload)
        token_data = token_response.json()
        if token_response.status_code == 200:
            # print('- Id Token: {}...'.format(token_data['id_token'][:10]))
            current_user = jwt.decode(
                token_data["id_token"],
                algorithms=ALGORITHMS,
                options={"verify_signature": False},
            )
            authenticated = True
        elif token_data["error"] not in ("authorization_pending", "slow_down"):
            print(token_data["error_description"])
            raise typer.Exit(code=1)
        else:
            time.sleep(device_code_data["interval"])
    return token_data, current_user


def authenticate(config_dir: str):
    """
    Checks for local token and validates it, if invalid, attempts to refresh it.
    """
    global token_data
    global current_user
    validated = False
    token_filename = os.path.join(config_dir, "token.json")

    token_data = get_token_from_file(token_filename)
    if token_data:
        validated = validate_token(token_data["id_token"])
        if validated:
            current_user = jwt.decode(
                token_data["id_token"],
                algorithms=ALGORITHMS,
                options={"verify_signature": False},
            )
            return token_data, current_user
        else:
            # Attempt to refresh the token when possible
            # the one we have in the file is not valid.
            token_data = token_refresh(token_filename, token_data)
            validated = validate_token(token_data["id_token"])
            if validated:
                current_user = jwt.decode(
                    token_data["id_token"],
                    algorithms=ALGORITHMS,
                    options={"verify_signature": False},
                )
                return token_data, current_user
    else:
        return None, None


def login(config_dir: str):
    """
    Runs the device authorization flow and stores the user object in memory
    """

    global token_data
    global current_user
    validated = False
    token_filename = os.path.join(config_dir, "token.json")

    token_data, current_user = init_device_flow()
    token_saver(token_filename, token_data)
    validated = validate_token(token_data["id_token"])
    if validated:
        current_user = jwt.decode(
            token_data["id_token"],
            algorithms=ALGORITHMS,
            options={"verify_signature": False},
        )
        return token_data, current_user
    else:
        print("Unable to obtain a valid token, please contact labs@greynoise.io.")
        typer.Abort()
