"""
#
#
# Gabut Tracer v0.6.9
# Written by Prima Agus Setiawan 
# a.k.a joeheartless / joefryme@gmail.com
"""

from __future__ import annotations

import socket
import ipaddress
import time
import functools
from datetime import datetime

from rich import print


# ==========================================================
# IP Utilities
# ==========================================================

def is_ipv4(address: str) -> bool:

    try:
        return isinstance(
            ipaddress.ip_address(address),
            ipaddress.IPv4Address
        )

    except ValueError:
        return False


def is_ipv6(address: str) -> bool:

    try:
        return isinstance(
            ipaddress.ip_address(address),
            ipaddress.IPv6Address
        )

    except ValueError:
        return False


def validate_ip(address: str) -> bool:

    try:

        ipaddress.ip_address(address)

        return True

    except ValueError:

        return False


def resolve_host(host: str) -> str:

    return socket.gethostbyname(host)


# ==========================================================
# Formatting
# ==========================================================

def format_rtt(value):

    if value is None:
        return "--"

    return f"{value:.2f} ms"


def format_loss(loss):

    return f"{loss:.1f}%"


def format_ttl(ttl):

    return str(ttl)


def format_bytes(size):

    size = float(size)

    units = [
        "B",
        "KB",
        "MB",
        "GB",
        "TB"
    ]

    index = 0

    while size >= 1024 and index < len(units)-1:

        size /= 1024

        index += 1

    return f"{size:.2f} {units[index]}"


def format_duration(seconds):

    if seconds < 1:

        return f"{seconds*1000:.0f} ms"

    if seconds < 60:

        return f"{seconds:.2f} sec"

    minute = int(seconds // 60)

    second = seconds % 60

    return f"{minute}m {second:.0f}s"


# ==========================================================
# Safe Math
# ==========================================================

def safe_divide(a, b, default=0):

    try:

        return a / b

    except ZeroDivisionError:

        return default


# ==========================================================
# Time
# ==========================================================

def timestamp():

    return datetime.now().strftime(
        "%Y-%m-%d %H:%M:%S"
    )


class Timer:

    def __init__(self):

        self.start_time = None

    def start(self):

        self.start_time = time.perf_counter()

    def stop(self):

        return (
            time.perf_counter()
            -
            self.start_time
        )


# ==========================================================
# Retry Decorator
# ==========================================================

def retry(times=3, delay=0.5):

    def decorator(func):

        @functools.wraps(func)

        def wrapper(*args, **kwargs):

            last = None

            for _ in range(times):

                try:

                    return func(
                        *args,
                        **kwargs
                    )

                except Exception as e:

                    last = e

                    time.sleep(delay)

            raise last

        return wrapper

    return decorator


# ==========================================================
# Terminal Colors
# ==========================================================

def color_latency(ms):

    if ms is None:
        return "[red]Timeout[/red]"

    if ms < 20:
        return f"[green]{ms:.2f}[/green]"

    if ms < 80:
        return f"[yellow]{ms:.2f}[/yellow]"

    return f"[red]{ms:.2f}[/red]"


def color_loss(loss):

    if loss == 0:
        return "[green]0%[/green]"

    if loss < 5:
        return f"[yellow]{loss:.1f}%[/yellow]"

    return f"[red]{loss:.1f}%[/red]"


def color_hop(ttl):

    return f"[cyan]{ttl}[/cyan]"