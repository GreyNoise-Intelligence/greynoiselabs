#!/usr/bin/env python3

import asyncio
import json
import os
from dataclasses import dataclass

import httpx
import jsonlines
import typer
from platformdirs import PlatformDirs
from typing_extensions import Annotated

from greynoiselabs.__version__ import __version__
from greynoiselabs.api.client import Client
from greynoiselabs.cli.auth import authenticate, login

AUTH0_DOMAIN = os.getenv("AUTH0_DOMAIN", default="greynoise2.auth0.com")
AUTH0_CLIENT_ID = os.getenv(
    "AUTH0_CLIENT_ID", default="IM8Old6x7WCr2wqVI0Cz3I0c4JPSR1gn"
)
ALGORITHMS = ["RS256"]

current_user = None
token_data = None
client = None
print = print


@dataclass
class Common:
    config_dir: str
    token: str
    output: str
    nocolor: bool


app = typer.Typer(no_args_is_help=True, pretty_exceptions_enable=False)


@app.callback()
def callback(
    ctx: typer.Context,
    config_dir: Annotated[
        str, typer.Option("--config", "-c", help="Output directory for CLI config.")
    ] = "~/.greynoiselabs",
    token: Annotated[
        str,
        typer.Option(
            "--token", "-t", envvar="GNL_TOKEN", help="HTTP JWT auth bearer token."
        ),
    ] = "",
    output: Annotated[
        str, typer.Option("--output", "-o", help="JSON lines output file location.")
    ] = "",
    nocolor: Annotated[
        str, typer.Option("--nocolor", "-n", help="Disable color output.")
    ] = False,
):
    ctx.obj = Common(config_dir, token, output, nocolor)


def initOutfile(outfile: str):
    if outfile != "":
        try:
            writer = jsonlines.open(outfile, mode="w")
            return writer
        except Exception as ex:
            print(f"unable to open {outfile} for writing: {ex}")
            raise typer.Abort()
    else:
        return None


def init_conf_dir(config_dir: str):
    try:
        dirs = PlatformDirs("greynoiselabs", "greynoise", version=__version__)
        if config_dir != "":
            config_dir = os.path.expanduser(config_dir)
            os.makedirs(config_dir, exist_ok=True)
        else:
            config_dir = dirs.user_config_dir
            os.makedirs(config_dir, exist_ok=True)
        return config_dir
    except Exception as ex:
        print(f"unable to create config directory {config_dir}: {ex}")
        raise typer.Abort()


def out(ctx: typer.Context, obj: any, outfile_writer: jsonlines.Writer):
    """
    Output the object as JSON
    """
    try:
        if outfile_writer:
            outfile_writer.write(obj.__dict__)
        else:
            print(json.dumps(obj.__dict__))
    except Exception as ex:
        print(f"unable to dump object {ex}")
        typer.Abort()


def new_client(id_token: any):
    transport = httpx.AsyncHTTPTransport(retries=1)
    return Client(
        "https://api.labs.greynoise.io/1/query",
        {"Authorization": f"Bearer {id_token}"},
        httpx.AsyncClient(
            headers={"Authorization": f"Bearer {id_token}"},
            transport=transport,
            timeout=90.0,
        ),
    )


@app.command()
def version():
    """
    Return the version of the GreyNoise Labs CLI.
    """
    print(__version__)


@app.command()
def init(ctx: typer.Context):
    """
    Initialize the client by authenticating with Auth0 and saving the token to a file.
    """
    global current_user, token_data, client
    init_conf_dir(ctx.obj.config_dir)
    token_data, current_user = authenticate(ctx.obj.config_dir)
    if token_data is None or current_user is None:
        run_init = typer.confirm(
            "You are not authenticated, would you like to do this now?"
        )
        if run_init:
            token_data, current_user = login(ctx.obj.config_dir)
            print("Authentication successful")
            raise typer.Abort()
        else:
            print("You must authenticate to use this CLI")
            raise typer.Abort()
    if token_data is not None and current_user is not None:
        try:
            client = new_client(token_data["id_token"])
        except Exception as ex:
            print(f"Unable to create client {ex}")
            raise typer.Abort()
    else:
        print("Authentication failed, please try again or contact labs@greynoise.io.")
        raise typer.Abort()


@app.command()
def c2s(ctx: typer.Context):
    """
    Return the top 1% of C2s ranked by pervasiveness.
    This data may be up to 4.5 hours old but covers the previous 24 hours.
    """
    init(ctx)
    writer = initOutfile(ctx.obj.output)
    response = asyncio.run(client.get_c2s())
    for c2 in response.top_c2s.c2s:
        out(c2, writer)
    if writer:
        writer.close()


@app.command()
def knocks(
    ctx: typer.Context,
    ip: Annotated[str, typer.Argument(help="Specify the IP to retrieve.")] = "",
):
    """
    Return the top 1% of Knock results by most recently seen.
    A Knock represents an IP observed by GreyNoise that we have scanned back.
    This data may be up to 12 hours old.
    This endpoint supports filtering by a single IP.
    """
    init(ctx)
    writer = initOutfile(ctx.obj.output)
    response = asyncio.run(client.get_knocks(ip))
    for knock in response.top_knocks.knock:
        out(knock, writer)
    if writer:
        writer.close()


@app.command()
def popular_ips(ctx: typer.Context):
    """
    Return the top 1% of IPs searched in GreyNoise.
    These results are ordered by the number of users observed over the last 7 days.
    This data may be up to 24 hours old.
    This also returns the user and request counts.
    This also returns a boolean if this IP was observed by GreyNoise sensors.
    """
    init(ctx)
    writer = initOutfile(ctx.obj.output)
    response = asyncio.run(client.get_i_ps())
    for ip in response.top_popular_i_ps.popular_i_ps:
        out(ip, writer)
    if writer:
        writer.close()


@app.command()
def noise_rank(
    ctx: typer.Context,
    ip: Annotated[str, typer.Argument(help="Specify the IP to retrieve.")] = "",
):
    """
    Return the top 1% of ranked IPs by noise score over the previous 7 days of traffic.
    This also returns the pervasiveness and diversity scores.
    This endpoint supports filtering by a single IP.
    """
    init(ctx)
    writer = initOutfile(ctx.obj.output)
    response = asyncio.run(client.get_noise_ranks(ip))
    for ip in response.noise_rank.ips:
        out(ip, writer)
    if writer:
        writer.close()


@app.command()
def gengnql(
    ctx: typer.Context,
    input: Annotated[str, typer.Argument(help="Specify the IP to retrieve.")] = "",
):
    """
    Translate text into usable GreyNoise GNQL queries.
    """
    init(ctx)
    writer = initOutfile(ctx.obj.output)
    response = asyncio.run(client.generate_g_n_q_l(input))
    for query in response.generate_g_n_q_l.queries:
        out(query, writer)
    if writer:
        writer.close()
