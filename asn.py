"""
#
#
# Gabut Tracer v0.6.9
# Written by Prima Agus Setiawan 
# a.k.a joeheartless / joefryme@gmail.com
"""

from __future__ import annotations

from pathlib import Path
import ipaddress

import maxminddb


class ASNLookup:

    def __init__(self, database=None):

        if database is None:

            database = (
                Path(__file__).parent
                / "data"
                / "GeoLite2-ASN.mmdb"
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

                "private": True,

                "asn": None,

                "organization": "Private Network"

            }

        if ip in self.cache:
            return self.cache[ip]

        if self.reader is None:

            return {

                "ip": ip,

                "error": "ASN database not found"

            }

        raw = self.reader.get(ip)

        if raw is None:

            return {

                "ip": ip,

                "error": "ASN not found"

            }

        result = {

            "ip": ip,

            "private": False,

            "asn":
                raw.get("autonomous_system_number"),

            "organization":
                raw.get("autonomous_system_organization")

        }

        self.cache[ip] = result

        return result

    # -----------------------------------------------------

    def close(self):

        if self.reader:
            self.reader.close()


asn = ASNLookup()