"""
#
#
# Gabut Tracer v0.6.9
# Written by Prima Agus Setiawan 
# a.k.a joeheartless / joefryme@gmail.com
"""

from __future__ import annotations

from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from rich.text import Text
from rich.progress import (
    Progress,
    SpinnerColumn,
    BarColumn,
    TimeElapsedColumn,
    TextColumn
)
from rich.live import Live
from rich import box

from utils import (
    color_latency,
    color_loss,
)

console = Console()


# ==========================================================
# Banner
# ==========================================================

def banner():

    console.print()

    console.print(
        Panel.fit(
            "[bold cyan]NetTraceX[/bold cyan]\n"
            "[white]Advanced Python Traceroute[/white]",
            border_style="cyan"
        )
    )

    console.print()


# ==========================================================
# Hop Table
# ==========================================================

def create_table():

    table = Table(

        title="Traceroute",

        box=box.ROUNDED,

        show_lines=False,

        expand=True

    )

    table.add_column(
        "Hop",
        justify="center",
        style="cyan",
        width=5
    )

    table.add_column(
        "Host",
        style="white",
        overflow="fold"
    )

    table.add_column(
        "RTT",
        justify="right"
    )

    table.add_column(
        "Loss",
        justify="right"
    )

    table.add_column(
        "ASN",
        style="green"
    )

    table.add_column(
        "Organization",
        style="yellow"
    )

    table.add_column(
        "Location",
        style="magenta"
    )

    return table


# ==========================================================
# Add Hop
# ==========================================================

def add_hop(

        table,

        hop,

        ip,

        rtt,

        loss,

        asn,

        org,

        city,

        country

):

    location = "-"

    if city or country:

        location = f"{city}, {country}"

    table.add_row(

        str(hop),

        ip,

        color_latency(rtt),

        color_loss(loss),

        str(asn),

        org,

        location

    )


# ==========================================================
# Summary Panel
# ==========================================================

def show_summary(stats):

    text = Text()

    text.append(
        f"Average RTT : {stats.average:.2f} ms\n"
    )

    text.append(
        f"Minimum RTT : {stats.minimum:.2f} ms\n"
    )

    text.append(
        f"Maximum RTT : {stats.maximum:.2f} ms\n"
    )

    text.append(
        f"Median RTT  : {stats.median:.2f} ms\n"
    )

    text.append(
        f"Std Dev     : {stats.stddev:.2f} ms\n"
    )

    text.append(
        f"Jitter      : {stats.jitter:.2f} ms\n"
    )

    text.append(
        f"RFC3550     : {stats.rfc3550_jitter:.2f} ms\n"
    )

    console.print(

        Panel(

            text,

            title="Statistics",

            border_style="green"

        )

    )


# ==========================================================
# Error
# ==========================================================

def error(message):

    console.print(

        Panel(

            f"[bold red]{message}[/bold red]",

            title="ERROR",

            border_style="red"

        )

    )


# ==========================================================
# Success
# ==========================================================

def success(message):

    console.print(

        Panel(

            f"[green]{message}[/green]",

            border_style="green"

        )

    )


# ==========================================================
# Info
# ==========================================================

def info(message):

    console.print(

        Panel(

            message,

            border_style="cyan"

        )

    )


# ==========================================================
# Progress
# ==========================================================

def progress():

    return Progress(

        SpinnerColumn(),

        TextColumn("[progress.description]{task.description}"),

        BarColumn(),

        TimeElapsedColumn()

    )


# ==========================================================
# Live View
# ==========================================================

def live():

    table = create_table()

    return Live(

        table,

        refresh_per_second=4,

        console=console

    )


# ==========================================================
# Print Table
# ==========================================================

def print_table(table):

    console.print(table)