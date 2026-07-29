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

### GeoLite2 Databases

Place the following databases inside the `data/` directory:

```
data/
├── GeoLite2-City.mmdb
└── GeoLite2-ASN.mmdb
```

These databases can be obtained from MaxMind.

---

## Project Structure

```
NetTraceX/
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
