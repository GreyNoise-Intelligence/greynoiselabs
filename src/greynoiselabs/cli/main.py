#!/usr/bin/env python3

import asyncio
import importlib.metadata
import json
import os

import httpx
import jsonlines
import typer
from platformdirs import PlatformDirs
from typing_extensions import Annotated

from greynoiselabs.api.client import Client
from greynoiselabs.api.exceptions import GraphQLClientGraphQLMultiError
from greynoiselabs.cli.auth import authenticate, login

AUTH0_DOMAIN = os.getenv("AUTH0_DOMAIN", default="greynoise2.auth0.com")
AUTH0_CLIENT_ID = os.getenv(
    "AUTH0_CLIENT_ID", default="IM8Old6x7WCr2wqVI0Cz3I0c4JPSR1gn"
)
ALGORITHMS = ["RS256"]

NOT_READY_MSG = "not available"

current_user = None
token_data = None
client = None


def get_version():
    try:
        version = importlib.metadata.version("greynoiselabs")
    except importlib.metadata.PackageNotFoundError:
        version = None
    return version


config_dir = typer.Option(
    "--config",
    "-c",
    help="Output directory for CLI config.",
    show_default=True,
    default_factory=PlatformDirs(
        "greynoiselabs", "greynoise", version=get_version()
    ).user_config_dir,
)
token = typer.Option(
    "--token", "-t", envvar="GNL_TOKEN", help="HTTP JWT auth bearer token."
)
output = typer.Option(
    "--output",
    "-o",
    help="JSON lines output file location.",
    show_default=False,
    default_factory=lambda: "",
)
ip = typer.Argument(
    help="Specify the IP to retrieve.", show_default=False, default_factory=lambda: ""
)
input: typer.Argument(
    help="Specify the input text to translate.",
    show_default=False,
    default_factory=lambda: "",
)
app = typer.Typer(no_args_is_help=True, pretty_exceptions_enable=False)


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
        dirs = PlatformDirs("greynoiselabs", "greynoise", version=get_version())
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


def out(obj: any, outfile_writer: jsonlines.Writer):
    """
    Output the object as JSON
    """
    if isinstance(obj, str):
        try:
            if outfile_writer:
                outfile_writer.write(obj)
            else:
                print(obj)
        except Exception as ex:
            print(f"unable to dump object {ex}")
            typer.Abort()
    else:
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
    print(get_version())


@app.command()
def init(
    config_dir: Annotated[str, config_dir],
):
    """
    Initialize the client by authenticating with Auth0 and saving the token to a file.
    """
    global current_user, token_data, client
    init_conf_dir(config_dir)
    token_data, current_user = authenticate(config_dir)
    if token_data is None or current_user is None:
        run_init = typer.confirm(
            "You are not authenticated, would you like to do this now?"
        )
        if run_init:
            token_data, current_user = login(config_dir)
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
def c2s(output: Annotated[str, output], config_dir: Annotated[str, config_dir]):
    """
    Return the top 10% of C2s ranked by pervasiveness.
    This data may be up to 4 hours old but covers the previous day.
    """
    init(config_dir)
    writer = initOutfile(output)
    try:
        response = asyncio.run(client.get_c2s())
        if len(response.top_c2s.c2s) == 0:
            print("no results found.")
        for c2 in response.top_c2s.c2s:
            out(c2, writer)
    except GraphQLClientGraphQLMultiError as ex:
        if NOT_READY_MSG in str(ex):
            print(
                "Labs API data refresh in progress, please try again in a few minutes."
            )
            raise typer.Abort()
        else:
            print(f"unable to get C2s: {ex}")
            raise typer.Abort()
    except Exception as ex:
        print(f"unable to get C2s: {ex}")
        raise typer.Abort()
    if writer:
        writer.close()


@app.command()
def http_requests(
    output: Annotated[str, output],
    config_dir: Annotated[str, config_dir],
    ips: Annotated[bool, typer.Option("--ips", help="Show the source IPs.")] = False,
):
    """
    Return the top 1% of HTTP requests ranked by pervasiveness.
    This is for requestsover the last 7 days.
    This data may be up to 4 hours old.
    The '/' path has been removed.
    """
    init(config_dir)
    writer = initOutfile(output)
    try:
        response = asyncio.run(client.get_requests())
        if len(response.top_h_t_t_p_requests.http_requests) == 0:
            print("no results found.")
        for request in response.top_h_t_t_p_requests.http_requests:
            if not ips:
                delattr(request, "source_ips")
            out(request, writer)
    except GraphQLClientGraphQLMultiError as ex:
        if NOT_READY_MSG in str(ex):
            print(
                "Labs API data refresh in progress, please try again in a few minutes."
            )
            raise typer.Abort()
        else:
            print(f"unable to get HTTP requests: {ex}")
            raise typer.Abort()
    except Exception as ex:
        print(f"unable to get HTTP requests: {ex}")
        raise typer.Abort()
    if writer:
        writer.close()


@app.command()
def payloads(
    output: Annotated[str, output],
    config_dir: Annotated[str, config_dir],
    ips: Annotated[bool, typer.Option("--ips", help="Show the source IPs.")] = False,
):
    """
    Return the top 1% of observed payloads ranked by pervasiveness
    This is for payloads over the last 7 days.
    This data may be up to 4 hours old.
    """
    init(config_dir)
    writer = initOutfile(output)
    try:
        response = asyncio.run(client.get_payloads())
        if len(response.top_payloads.payloads) == 0:
            print("no results found.")
        for payload in response.top_payloads.payloads:
            if not ips:
                delattr(payload, "source_ips")
            out(payload, writer)
    except GraphQLClientGraphQLMultiError as ex:
        if NOT_READY_MSG in str(ex):
            print(
                "Labs API data refresh in progress, please try again in a few minutes."
            )
            raise typer.Abort()
        else:
            print(f"unable to get payloads: {ex}")
            raise typer.Abort()
    except Exception as ex:
        print(f"unable to get payloads: {ex}")
        raise typer.Abort()
    if writer:
        writer.close()


@app.command()
def knocks(
    ip: Annotated[str, ip],
    output: Annotated[str, output],
    config_dir: Annotated[str, config_dir],
):
    """
    Return the top 1% of Knock results by most recently seen.
    A Knock represents an IP observed by GreyNoise that we have scanned back.
    This data may be up to 12 hours old.
    This endpoint supports filtering by a single IP.
    """
    init(config_dir)
    writer = initOutfile(output)
    try:
        response = asyncio.run(client.get_knocks(ip))
        if len(response.top_knocks.knock) == 0:
            print("no results found.")
        for knock in response.top_knocks.knock:
            out(knock, writer)
    except GraphQLClientGraphQLMultiError as ex:
        if NOT_READY_MSG in str(ex):
            print(
                "Labs API data refresh in progress, please try again in a few minutes."
            )
            raise typer.Abort()
        else:
            print(f"unable to get knocks: {ex}")
            raise typer.Abort()
    except Exception as ex:
        print(f"unable to get knocks: {ex}")
        raise typer.Abort()
    if writer:
        writer.close()


@app.command()
def popular_ips(output: Annotated[str, output], config_dir: Annotated[str, config_dir]):
    """
    Return the top 1% of IPs searched in GreyNoise.
    These results are ordered by the number of users observed over the last 7 days.
    This data may be up to 24 hours old.
    This also returns the user and request counts.
    This also returns a boolean if this IP was observed by GreyNoise sensors.
    """
    init(config_dir)
    writer = initOutfile(output)
    try:
        response = asyncio.run(client.get_i_ps())
        if len(response.top_popular_i_ps.popular_i_ps) == 0:
            print("no results found.")
        for ip in response.top_popular_i_ps.popular_i_ps:
            out(ip, writer)
    except GraphQLClientGraphQLMultiError as ex:
        if NOT_READY_MSG in str(ex):
            print(
                "Labs API data refresh in progress, please try again in a few minutes."
            )
            raise typer.Abort()
        else:
            print(f"unable to get IPs: {ex}")
            raise typer.Abort()
    except Exception as ex:
        print(f"unable to get IPs: {ex}")
        raise typer.Abort()
    if writer:
        writer.close()


@app.command()
def noise_rank(
    ip: Annotated[str, ip],
    output: Annotated[str, output],
    config_dir: Annotated[str, config_dir],
):
    """
    Return the top 1% of ranked IPs by noise score over the previous 7 days of traffic.
    This also returns the pervasiveness and diversity scores.
    This endpoint supports filtering by a single IP.
    """
    init(config_dir)
    writer = initOutfile(output)
    try:
        response = asyncio.run(client.get_noise_ranks(ip))
        if len(response.noise_rank.ips) == 0:
            print("no results found.")
        for ip in response.noise_rank.ips:
            out(ip, writer)
    except GraphQLClientGraphQLMultiError as ex:
        if NOT_READY_MSG in str(ex):
            print(
                "Labs API data refresh in progress, please try again in a few minutes."
            )
            raise typer.Abort()
        else:
            print(f"unable to get noise rank: {ex}")
            raise typer.Abort()
    except Exception as ex:
        print(f"unable to get noise rank: {ex}")
        raise typer.Abort()
    if writer:
        writer.close()


@app.command()
def gengnql(
    input: Annotated[str, input],
    output: Annotated[str, output],
    config_dir: Annotated[str, config_dir],
):
    """
    Translate text into usable GreyNoise GNQL queries.
    """
    init(config_dir)
    writer = initOutfile(output)
    try:
        response = asyncio.run(client.generate_g_n_q_l(input))
        if len(response.generate_g_n_q_l.queries) == 0:
            print("no results found.")
        for query in response.generate_g_n_q_l.queries:
            out(query, writer)
    except Exception:
        print(
            """unable to generate GNQL, please try again.
an error occured while processing your request.
"""
        )
        raise typer.Abort()
    if writer:
        writer.close()


if __name__ == "__main__":
    app()
