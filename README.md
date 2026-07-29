# Gabut-Tracer v0.6.9

A lightweight Python-based network traceroute utility with support for:

- ICMP Traceroute (IPv4 & IPv6)
- Reverse DNS Lookup
- GeoLite2 City Lookup
- GeoLite2 ASN Lookup
- Live Rich Terminal UI

---

## Dependencies

### Python Version

- Python 3.10+

### Third-Party Libraries

```bash
pip install scapy rich geoip2 maxminddb jinja2 asn
```

## GeoLite2 Database

Gabut-Tracer uses the **MaxMind GeoLite2 City** and **GeoLite2 ASN** databases to provide IP geolocation and Autonomous System Number (ASN) information.

These database files are **not included** in this repository.

Please download the following databases from the official MaxMind website:

- **GeoLite2-City.mmdb**
- **GeoLite2-ASN.mmdb**

https://dev.maxmind.com/geoip/geolite2-free-geolocation-data/

After downloading, place both files in the `data/` directory:

```text
data/
├── GeoLite2-City.mmdb
└── GeoLite2-ASN.mmdb
```

> **Note**
>
> A free MaxMind account is required to download the GeoLite2 databases.

## Project Structure

```
Gabut-Tracer/
│
├── main.py
├── tracer.py
├── dns.py
├── geo.py
├── asn.py
├── stats.py
├── export.py
├── ui.py
├── utils.py
│
├── data/
│   ├── GeoLite2-City.mmdb
│   └── GeoLite2-ASN.mmdb
│
├── reports/
│
└── README.md
```
