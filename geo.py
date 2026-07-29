"""
#
#
# Gabut Tracer v0.6.9
# Written by Prima Agus Setiawan 
# a.k.a joeheartless / joefryme@gmail.com
"""

from __future__ import annotations

import ipaddress
from pathlib import Path

import maxminddb


class GeoIP:

    def __init__(self, database=None):

        if database is None:
            database = (
                Path(__file__).parent
                / "data"
                / "GeoLite2-City.mmdb"
            )

        self.database = Path(database)

        self.reader = None

        self.cache = {}

        self._open()

    # -----------------------------------------------------

    def _open(self):

        if not self.database.exists():
            return

        self.reader = maxminddb.open_database(
            str(self.database)
        )

    # -----------------------------------------------------

    @staticmethod
    def is_private(ip):

        try:
            return ipaddress.ip_address(ip).is_private
        except Exception:
            return True

    # -----------------------------------------------------

    def lookup(self, ip):

        if self.is_private(ip):

            return {

                "ip": ip,

                "private": True

            }

        if ip in self.cache:
            return self.cache[ip]

        if self.reader is None:

            return {

                "ip": ip,

                "error": "Geo database not found"

            }

        raw = self.reader.get(ip)

        if raw is None:

            return {

                "ip": ip,

                "error": "Not Found"

            }

        result = {

            "ip": ip,

            "private": False,

            "country":
                raw.get("country", {})
                   .get("names", {})
                   .get("en"),

            "country_code":
                raw.get("country", {})
                   .get("iso_code"),

            "city":
                raw.get("city", {})
                   .get("names", {})
                   .get("en"),

            "region":
                (
                    raw.get("subdivisions", [{}])[0]
                    .get("names", {})
                    .get("en")
                ),

            "postal":
                raw.get("postal", {})
                   .get("code"),

            "timezone":
                raw.get("location", {})
                   .get("time_zone"),

            "latitude":
                raw.get("location", {})
                   .get("latitude"),

            "longitude":
                raw.get("location", {})
                   .get("longitude"),

            "accuracy_radius":
                raw.get("location", {})
                   .get("accuracy_radius")

        }

        self.cache[ip] = result

        return result

    # -----------------------------------------------------

    def close(self):

        if self.reader:

            self.reader.close()


geo = GeoIP()