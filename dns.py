"""
#
#
# Gabut Tracer v0.6.9
# Written by Prima Agus Setiawan 
# a.k.a joeheartless / joefryme@gmail.com
"""

from __future__ import annotations

import ipaddress
import re
import socket
from functools import lru_cache


class DNSResolver:

    def __init__(self):

        self.forward_cache = {}
        self.reverse_cache = {}

    # --------------------------------------------------

    def resolve(self, hostname: str):

        if hostname in self.forward_cache:
            return self.forward_cache[hostname]

        try:

            ip = socket.gethostbyname(hostname)

        except Exception:

            ip = None

        self.forward_cache[hostname] = ip

        return ip

    # --------------------------------------------------

    def reverse(self, ip: str):

        if ip in self.reverse_cache:
            return self.reverse_cache[ip]

        try:

            host = socket.gethostbyaddr(ip)[0]

        except Exception:

            host = None

        self.reverse_cache[ip] = host

        return host

    # --------------------------------------------------

    @staticmethod
    def is_private(ip):

        try:

            return ipaddress.ip_address(ip).is_private

        except Exception:

            return False

    # --------------------------------------------------

    @staticmethod
    def is_ipv6(ip):

        try:

            return ipaddress.ip_address(ip).version == 6

        except Exception:

            return False

    # --------------------------------------------------

    @staticmethod
    def is_ipv4(ip):

        try:

            return ipaddress.ip_address(ip).version == 4

        except Exception:

            return False

    # --------------------------------------------------

    @staticmethod
    def hostname_parts(hostname):

        if hostname is None:
            return []

        hostname = hostname.lower()

        return re.findall(r"[a-z0-9]+", hostname)

    # --------------------------------------------------

    @staticmethod
    @lru_cache(maxsize=2048)
    def detect_location(hostname):

        """
        Parse hostname backbone
        """

        if hostname is None:
            return None

        host = hostname.lower()

        mapping = {

            "jkt": "Jakarta",
            "cgk": "Jakarta",

            "bdo": "Bandung",
            "sub": "Surabaya",
            "sby": "Surabaya",
            "dps": "Denpasar",
            "mdc": "Manado",
            "btm": "Batam",
            "plm": "Palembang",
            "pku": "Pekanbaru",
            "bpn": "Balikpapan",

            "sin": "Singapore",
            "sgp": "Singapore",

            "kul": "Kuala Lumpur",
            "hkg": "Hong Kong",
            "tpe": "Taipei",
            "tyo": "Tokyo",
            "nrt": "Tokyo",
            "hnd": "Tokyo",
            "icn": "Seoul",
            "sel": "Seoul",

            "lax": "Los Angeles",
            "sjc": "San Jose",
            "sfo": "San Francisco",
            "sea": "Seattle",
            "dfw": "Dallas",
            "ord": "Chicago",
            "mia": "Miami",
            "iad": "Washington",
            "nyc": "New York",

            "lon": "London",
            "lhr": "London",
            "fra": "Frankfurt",
            "ams": "Amsterdam",
            "par": "Paris",

            "syd": "Sydney",
            "mel": "Melbourne"

        }

        parts = DNSResolver.hostname_parts(host)

        for part in parts:

            if part in mapping:

                return mapping[part]

        return None

    # --------------------------------------------------

    @staticmethod
    def normalize(hostname):

        if hostname is None:
            return "-"

        hostname = hostname.rstrip(".")

        hostname = hostname.lower()

        return hostname

    # --------------------------------------------------

    def lookup(self, target):

        """
        Smart lookup

        input :
            google.com
            dns.google
            8.8.8.8

        output :

        {
            hostname
            ip
            location
            private
        }
        """

        if self.is_ipv4(target) or self.is_ipv6(target):

            ip = target

            hostname = self.reverse(ip)

        else:

            hostname = target

            ip = self.resolve(target)

        hostname = self.normalize(hostname)

        return {

            "hostname": hostname,

            "ip": ip,

            "private": self.is_private(ip) if ip else False,

            "location_hint": self.detect_location(hostname)

        }


resolver = DNSResolver()