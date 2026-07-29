#!/usr/bin/env python3
"""
#!/usr/bin/python
#
#
# Gabut Tracer v0.6.9
# Written by Prima Agus Setiawan 
# a.k.a joeheartless / joefryme@gmail.com
"""

import argparse
import socket
import sys
from rich.console import Console
from rich.panel import Panel

from tracer import TraceRoute

console = Console()


VERSION = "0.6.9"


def banner():

    console.print(
        Panel.fit(
            f"""
[bold cyan]
   ██████╗  █████╗ ██████╗ ██╗   ██╗████████╗
  ██╔════╝ ██╔══██╗██╔══██╗██║   ██║╚══██╔══╝
  ██║  ███╗███████║██████╔╝██║   ██║   ██║
  ██║   ██║██╔══██║██╔══██╗██║   ██║   ██║
  ╚██████╔╝██║  ██║██████╔╝╚██████╔╝   ██║
   ╚═════╝ ╚═╝  ╚═╝╚═════╝  ╚═════╝    ╚═╝

            ████████╗██████╗  █████╗  ██████╗███████╗██████╗
            ╚══██╔══╝██╔══██╗██╔══██╗██╔════╝██╔════╝██╔══██╗
               ██║   ██████╔╝███████║██║     █████╗  ██████╔╝
               ██║   ██╔══██╗██╔══██║██║     ██╔══╝  ██╔══██╗
               ██║   ██║  ██║██║  ██║╚██████╗███████╗██║  ██║
               ╚═╝   ╚═╝  ╚═╝╚═╝  ╚═╝ ╚═════╝╚══════╝╚═╝  ╚═╝
Version {VERSION}
Gegabutan Python Traceroute
By Prima Agus Setiawan
[/bold cyan]
"""
        )
    )


def resolve_target(target: str):
    """
    Resolve hostname menjadi IPv4.
    """

    try:
        ip = socket.gethostbyname(target)
        return ip

    except socket.gaierror:
        console.print(f"[red][-][/red] Unable to resolve host : {target}")
        sys.exit(1)


def build_parser():

    parser = argparse.ArgumentParser(
        prog="nettracex",
        description="Advanced Python Traceroute Utility"
    )

    parser.add_argument(
        "target",
        help="Hostname atau IPv4"
    )

    parser.add_argument(
        "-p",
        "--probe",
        default=10,
        type=int,
        help="Probe per hop (default 10)"
    )

    parser.add_argument(
        "-m",
        "--max-hop",
        default=30,
        type=int,
        help="Maximum hop"
    )

    parser.add_argument(
        "-t",
        "--timeout",
        default=2,
        type=float,
        help="Timeout (second)"
    )

    parser.add_argument(
        "--icmp",
        action="store_true",
        help="ICMP Traceroute (default)"
    )

    parser.add_argument(
        "--udp",
        action="store_true",
        help="UDP Traceroute"
    )

    parser.add_argument(
        "--tcp",
        action="store_true",
        help="TCP Traceroute"
    )

    parser.add_argument(
        "--json",
        action="store_true",
        help="Export JSON"
    )

    parser.add_argument(
        "--csv",
        action="store_true",
        help="Export CSV"
    )

    parser.add_argument(
        "--html",
        action="store_true",
        help="Export HTML"
    )

    parser.add_argument(
        "--live",
        action="store_true",
        help="Continuous Monitoring"
    )

    return parser


def main():

    banner()

    parser = build_parser()

    args = parser.parse_args()

    ip = resolve_target(args.target)

    console.print(f"[green][+][/green] Target   : {args.target}")
    console.print(f"[green][+][/green] IP       : {ip}")
    console.print(f"[green][+][/green] Max Hop  : {args.max_hop}")
    console.print(f"[green][+][/green] Probe    : {args.probe}")
    console.print(f"[green][+][/green] Timeout  : {args.timeout} sec")
    console.print()

    tracer = TraceRoute(
        target=args.target,
        ip=ip,
        probes=args.probe,
        timeout=args.timeout,
        max_hops=args.max_hop,
    )

    tracer.run()


if __name__ == "__main__":
    main()