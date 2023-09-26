#!/usr/bin/env python3

import asyncio
import importlib.metadata
import json
import os
import subprocess
import time
from pathlib import Path

import httpx
import jsonlines
import pyperclip as pc
import typer
from platformdirs import PlatformDirs
from rich.progress import track
from typing_extensions import Annotated

from greynoiselabs.api.client import Client, Upload
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
protocol = typer.Option(
    "--protocol",
    "-p",
    help="Specify the IP protocol to filter on [TCP or UDP].",
    show_default=False,
    default_factory=lambda: "",
)
useragent = typer.Option(
    "--user-agent",
    "-u",
    help="Specify a string that the User-Agent contains. This is case sensitive.",
    show_default=False,
    default_factory=lambda: "",
)
input = typer.Argument(
    help="Specify the input text to translate.",
    show_default=False,
    default_factory=lambda: "",
)

reverse = typer.Option(
    "--reverse",
    "-r",
    help="PCAP extraction defaults to inbound, set to true to reverse the extraction.",
    show_default=True,
)

ignore_private = typer.Option(
    "--ignore-private",
    help="Don't parse packets which use an RFC1918 private IP as the \
        source OR destinaiton IP.",
    show_default=True,
)

ignore_flows = typer.Option(
    "--ignore-flows",
    help="Don't parse raw packet flows, only packets containing \
        useful metadata from HTTP, DNS, etc.",
    show_default=True,
)

show = typer.Option(
    "--show",
    help="Ouput data to STDOUT instead of the clipboard.",
    show_default=True,
)

pcap = typer.Argument(
    help="Specify the path to the PCAP file to be analyzed.",
)

pcap_app = typer.Typer(
    no_args_is_help=True,
    pretty_exceptions_enable=False,
    help="Commands for analyzing a PCAP/PCAPNG file.",
)

app = typer.Typer(no_args_is_help=True, pretty_exceptions_enable=False)
app.add_typer(pcap_app, name="pcap")


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
            # NOTE: This uses the default to json.dumps() by extracting all
            # nested objects that contain a __dict__ to prevent serialization errors.
            flattend_obj = json.loads(json.dumps(obj, default=lambda o: o.__dict__))
            if outfile_writer:
                outfile_writer.write(flattend_obj)
            else:
                print(json.dumps(flattend_obj))
        except Exception as ex:
            print(f"unable to dump object {ex}")
            typer.Abort()


def new_client(id_token: any):
    transport = httpx.AsyncHTTPTransport(retries=1)
    return Client(
        os.getenv("GN_API_URL", "https://api.labs.greynoise.io/1/query"),
        {"Authorization": f"Bearer {id_token}"},
        httpx.AsyncClient(
            headers={
                "Authorization": f"Bearer {id_token}",
                "User-Agent": f"GreyNoiseLabs/{get_version()}",
            },
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
    initialized_dir = init_conf_dir(config_dir)
    check_version(initialized_dir)
    token_data, current_user, email = authenticate(initialized_dir)
    if token_data is None or current_user is None or email is None:
        run_init = typer.confirm(
            "You are not authenticated, would you like to do this now?"
        )
        if run_init:
            token_data, current_user, email = login(initialized_dir)
            print(f"Authentication successful {email}")
            return initialized_dir
        else:
            print("You must authenticate to use this CLI")
            raise typer.Abort()
    if token_data is not None and current_user is not None:
        try:
            client = new_client(token_data["id_token"])
            return initialized_dir
        except Exception as ex:
            print(f"Unable to create client {ex}")
            raise typer.Abort()
    else:
        print("Authentication failed, please try again or contact labs@greynoise.io.")
        raise typer.Abort()


def check_version(config_dir, force=False):
    """Check the latest version of the CLI."""
    trigger_check = True
    updates_checked = f"{config_dir}/.updates_checked"
    disabled_path = f"{config_dir}/.updates_disabled"
    package_name = "greynoiselabs"
    if Path(disabled_path).exists():
        return
    if Path(updates_checked).exists():
        # Get the file's modification time as a Unix timestamp
        modification_time = os.path.getmtime(updates_checked)

        # Get the current time as a Unix timestamp
        current_time = time.time()

        # Calculate the time difference in seconds
        time_difference = current_time - modification_time
        # We only check automatically a maximum of once per hour
        if time_difference < 14400:
            trigger_check = False
    if trigger_check or force:
        response = httpx.get(f"https://pypi.org/pypi/{package_name}/json")
        for value in track(range(100), description="Checking for update..."):
            # Fake processing time
            time.sleep(0.01)
        latest_version = response.json()["info"]["version"]
        current_version = get_version()
        if latest_version == current_version:
            print(
                f"\n{current_version} is already the latest version, skipping update."
            )
            Path(updates_checked).touch()
            return
        else:
            update_confirmed = typer.confirm(
                f"A new version ({latest_version}) is available. Would you like \
                    to update?"
            )
            if update_confirmed:
                Path(updates_checked).touch()
                for value in track(range(100), description="Updating..."):
                    # Fake processing time
                    time.sleep(0.01)
                run_update(latest_version)
            else:
                disable_update = typer.confirm(
                    "Skipping this update, would you like to disable automatic \
                        update checks?"
                )
                if disable_update:
                    Path(disabled_path).touch()
                    print("Automatic update checks disabled.")


def run_update(latest_version):
    """Update the CLI to the latest version.
    This will re-enable automatic update checking."""
    subprocess.run(["pip", "install", "--upgrade", f"greynoiselabs=={latest_version}"])
    print(f"CLI updated successfully to {latest_version}.")


@app.command()
def update(config_dir: Annotated[str, config_dir]):
    """Update the CLI to the latest version.
    This will re-enable automatic update checking."""
    initialized_dir = init_conf_dir(config_dir)
    disabled_path = f"{initialized_dir}/.updates_disabled"
    # Remove the disabled path so automatic updates will be re-enabled
    if Path(disabled_path).exists():
        os.rmtree(disabled_path)
        print("Automatic updates re-enabled.")
    check_version(initialized_dir, force=True)


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
    useragent: Annotated[str, useragent],
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
        response = asyncio.run(client.get_requests(useragent))
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
    protocol: Annotated[str, protocol],
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
        response = asyncio.run(client.get_payloads(protocol))
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


@pcap_app.command()
def pivot(
    pcap: Annotated[str, pcap],
    output: Annotated[str, output],
    config_dir: Annotated[str, config_dir],
    reverse: Annotated[bool, reverse] = False,
    ignore_private: Annotated[bool, ignore_private] = False,
    ignore_flows: Annotated[bool, ignore_flows] = False,
):
    """
    Extracts interesting artifacts from a PCAP file by IP that can be used to
    pivot into GreyNoise or other enrichment sources.
    """
    init(config_dir)
    writer = initOutfile(output)
    try:
        with open(pcap, "rb") as f:
            response = asyncio.run(
                client.get_pivot(
                    pcap=Upload(
                        filename=pcap,
                        content=f,
                        content_type="application/vnd.tcpdump.pcap",
                    ),
                    reverse=reverse,
                    ignore_flows=ignore_flows,
                    ignore_private=ignore_private,
                    gnql=False,
                )
            )
        if len(response.pivot.ips) == 0:
            print("no results found.")
        for ip in response.pivot.ips:
            out(ip, writer)
    except GraphQLClientGraphQLMultiError as ex:
        if NOT_READY_MSG in str(ex):
            print(
                "Labs API data refresh in progress, please try again in a few minutes."
            )
            raise typer.Abort()
        else:
            print(f"unable to get pivot from PCAP: {ex}")
            raise typer.Abort()
    except Exception as ex:
        print(f"unable to get pivot from PCAP: {ex}")
        raise typer.Abort()
    if writer:
        writer.close()


@pcap_app.command()
def ips(
    pcap: Annotated[str, pcap],
    output: Annotated[str, output],
    config_dir: Annotated[str, config_dir],
    reverse: Annotated[bool, reverse] = False,
    ignore_private: Annotated[bool, ignore_private] = False,
    ignore_flows: Annotated[bool, ignore_flows] = False,
    show: Annotated[bool, show] = False,
):
    """
    Extract distinct IPs from a PCAP and copy to the clipboard for use in 3rd party
    analysis tools like https://viz.greynoise.io/analysis
    """
    init(config_dir)
    ips = []
    writer = initOutfile(output)
    try:
        with open(pcap, "rb") as f:
            response = asyncio.run(
                client.get_pivot(
                    pcap=Upload(
                        filename=pcap,
                        content=f,
                        content_type="application/vnd.tcpdump.pcap",
                    ),
                    reverse=reverse,
                    ignore_flows=ignore_flows,
                    ignore_private=ignore_private,
                    gnql=False,
                )
            )
        if len(response.pivot.ips) == 0:
            print("no results found.")
        for ip in response.pivot.ips:
            ips.append(ip.ip)
    except GraphQLClientGraphQLMultiError as ex:
        if NOT_READY_MSG in str(ex):
            print(
                "Labs API data refresh in progress, please try again in a few minutes."
            )
            raise typer.Abort()
        else:
            print(f"unable to get pivot from PCAP: {ex}")
            raise typer.Abort()
    except Exception as ex:
        print(f"unable to get pivot from PCAP: {ex}")
        raise typer.Abort()
    if show:
        for ip in ips:
            out(ip, writer)
    else:
        ipstr = "\n".join(ips)
        pc.copy(ipstr)
        print("The distinct IP addresses from the PCAP have been copied.")
        print("You can paste the copied IPs with Ctrl+V or Command+V.")
        print("For example navigate to: https://viz.greynoise.io/analysis.")
        print("--show will output the IPs to STDOUT and hide this message.")
    if writer:
        writer.close()


@pcap_app.command()
def gnql(
    pcap: Annotated[str, pcap],
    output: Annotated[str, output],
    config_dir: Annotated[str, config_dir],
    reverse: Annotated[bool, reverse] = False,
    ignore_private: Annotated[bool, ignore_private] = False,
    ignore_flows: Annotated[bool, ignore_flows] = False,
):
    """
    Extracts interesting artifacts from a PCAP file and converts these
    artifacts into compliant GNQL queries that you can evaluate in GreyNoise.
    """
    init(config_dir)
    writer = initOutfile(output)
    try:
        with open(pcap, "rb") as f:
            response = asyncio.run(
                client.get_pivot(
                    pcap=Upload(
                        filename=pcap,
                        content=f,
                        content_type="application/vnd.tcpdump.pcap",
                    ),
                    reverse=reverse,
                    ignore_private=ignore_private,
                    ignore_flows=ignore_flows,
                    gnql=True,
                )
            )
        if len(response.pivot.queries) == 0:
            print("no results found.")
        for queries in response.pivot.queries:
            out(queries, writer)
    except GraphQLClientGraphQLMultiError as ex:
        if NOT_READY_MSG in str(ex):
            print(
                "Labs API data refresh in progress, please try again in a few minutes."
            )
            raise typer.Abort()
        else:
            print(f"unable to get GNQL from PCAP: {ex}")
            raise typer.Abort()
    except Exception as ex:
        print(f"unable to get GNQL from PCAP: {ex}")
        raise typer.Abort()
    if writer:
        writer.close()


if __name__ == "__main__":
    app()
