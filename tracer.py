"""
#
#
# Gabut Tracer v0.6.9
# Written by Prima Agus Setiawan 
# a.k.a joeheartless / joefryme@gmail.com
"""
import socket
import statistics
import time

from rich.console import Console
from rich.progress import (
    Progress,
    SpinnerColumn,
    TextColumn,
    BarColumn,
    TimeElapsedColumn,
)
from rich.table import Table
from rich.live import Live
from rich.console import Group
from rich.spinner import Spinner

from scapy.all import IP, ICMP, IPv6, ICMPv6EchoRequest, sr1

from geo import geo
from asn import asn

console = Console()


class TraceRoute:

    def __init__(
        self,
        target,
        ip,
        probes=10,
        timeout=2,
        max_hops=30,
        ipv6=False,
    ):

        self.target = target
        self.ip = ip
        self.probes = probes
        self.timeout = timeout
        self.max_hops = max_hops
        self.ipv6 = ipv6

        self.results = []

        self.geo_cache = {}
        self.asn_cache = {}

    def ping_probe(self, ttl):

        rtts = []
        responder = None

        for _ in range(self.probes):

            if self.ipv6:

                pkt = IPv6(
                    dst=self.ip,
                    hlim=ttl
                ) / ICMPv6EchoRequest()

            else:

                pkt = IP(
                    dst=self.ip,
                    ttl=ttl
                ) / ICMP()

            start = time.perf_counter()

            reply = sr1(
                pkt,
                timeout=self.timeout,
                verbose=0
            )

            stop = time.perf_counter()

            if reply:

                responder = reply.src

                rtt = (stop - start) * 1000

                rtts.append(rtt)

        return responder, rtts

    def calc_loss(self, received):

        return (
            (self.probes - received)
            / self.probes
        ) * 100


    def calc_jitter(self, values):

        if len(values) < 2:
            return 0

        delta = []

        for i in range(1, len(values)):

            delta.append(
                abs(values[i] - values[i - 1])
            )

        return statistics.mean(delta)
    
    def get_geo(self, ip):

        if ip in self.geo_cache:
            return self.geo_cache[ip]

        try:

            result = geo.lookup(ip)

        except Exception:

            result = {
            "country": "-",
            "city": "-"
        }

        self.geo_cache[ip] = result

        return result


    def get_asn(self, ip):

        if ip in self.asn_cache:
            return self.asn_cache[ip]

        try:

            result = asn.lookup(ip)

        except Exception:

            result = {
            "asn": None,
            "organization": "-"
        }

        self.asn_cache[ip] = result

        return result
    

    def hop(self, ttl):

        responder, rtts = self.ping_probe(ttl)
        
        if responder is None:

            return {

            "ttl": ttl,
            "host": "*",
            "ip": "*",

            "country": "-",
            "city": "-",

            "asn": "-",
            "org": "-",

            "sent": self.probes,
            "recv": 0,
            "loss": 100,
            "avg": 0,
            "min": 0,
            "max": 0,
            "jitter": 0,
            "reached": False
        }

        try:
            hostname = socket.gethostbyaddr(responder)[0]

        except Exception:
            hostname = responder

        geo_info = self.get_geo(responder)

        asn_info = self.get_asn(responder)

        reached = responder == self.ip

        return {

        "ttl": ttl,

        "host": hostname,

        "ip": responder,

        "country": geo_info.get("country", "-"),
        "city": geo_info.get("city", "-"),

        "asn": (
            f"AS{asn_info['asn']}"
            if asn_info.get("asn")
            else "-"
        ),

        "org": asn_info.get(
            "organization",
            "-"
        ),

        "sent": self.probes,

        "recv": len(rtts),

        "loss": self.calc_loss(len(rtts)),

        "avg": statistics.mean(rtts),

        "min": min(rtts),

        "max": max(rtts),

        "jitter": self.calc_jitter(rtts),

        "reached": reached
        
    }


    def build_table(self):

        table = Table(show_lines=False)
        
        def color_rtt(rtt):

            if rtt == 0:
                return "[grey50]Timeout[/grey50]"

            if rtt < 10:
                return f"[green]{rtt:.2f} ms[/green]"

            if rtt < 30:
                return f"[cyan]{rtt:.2f} ms[/cyan]"

            if rtt < 60:
                return f"[yellow]{rtt:.2f} ms[/yellow]"

            return f"[red]{rtt:.2f} ms[/red]"

        table.add_column("Hop", justify="right")
        table.add_column("Hostname", style="cyan")
        table.add_column("IP", style="green")
        table.add_column("ASN", style="magenta")
        table.add_column("Organization", style="yellow")
        table.add_column("Country")
        table.add_column("City")
        table.add_column("Loss")
        table.add_column("Avg")
        table.add_column("Min")
        table.add_column("Max")
        table.add_column("Jitter")

        for row in self.results:

            table.add_row(

            str(row.get("ttl", "-")),

            row.get("host", "-"),

            row.get("ip", "-"),

            row.get("asn", "-"),

            row.get("org", "-"),

            row.get("country", "-"),

            row.get("city", "-"),
            
            f'{row.get("loss",0):.1f}%',

            color_rtt(row.get("avg", 0)),
           
            color_rtt(row.get("min", 0)),
            
            color_rtt(row.get("max", 0)),
            
            color_rtt(row.get("jitter", 0))
        )

        return table


    def summary(self):

        if not self.results:
            return

        final = self.results[-1]

        console.print()

        console.print(
            "[bold green]Summary[/bold green]"
        )

        console.print(
            f"Destination : {self.target}"
        )

        console.print(
            f"IP          : {self.ip}"
        )

        console.print(
            f"Total Hops  : {len(self.results)}"
        )

        console.print(
            f"Last Hop    : {final['host']}"
        )


    def run(self):

        spinner = Spinner("dots", text="[cyan]Tracing route...[/cyan]")

        with Live(
        Group(
                spinner,
                self.build_table()
            ),
        refresh_per_second=10
        ) as live:

            for ttl in range(1, self.max_hops + 1):

                hop = self.hop(ttl)

                self.results.append(hop)

                live.update(
                    Group(
                        spinner,
                        self.build_table()
                    )
                )

                if hop["reached"]:
                    break

        console.print()
        self.summary()