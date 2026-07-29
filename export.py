"""
#
#
# Gabut Tracer v0.6.9
# Written by Prima Agus Setiawan 
# a.k.a joeheartless / joefryme@gmail.com
"""

from __future__ import annotations

import csv
import json
from pathlib import Path
from datetime import datetime

from jinja2 import Template


class Exporter:

    def __init__(self, output_dir="reports"):

        self.output_dir = Path(output_dir)

        self.output_dir.mkdir(
            parents=True,
            exist_ok=True
        )

    # -----------------------------------------------------

    def timestamp(self):

        return datetime.now().strftime(
            "%Y%m%d_%H%M%S"
        )

    # -----------------------------------------------------

    def filename(self, prefix, ext):

        return self.output_dir / (
            f"{prefix}_{self.timestamp()}.{ext}"
        )

    # -----------------------------------------------------

    def export_csv(
        self,
        results,
        prefix="trace"
    ):

        file = self.filename(prefix, "csv")

        with open(
            file,
            "w",
            newline="",
            encoding="utf-8"
        ) as f:

            writer = csv.DictWriter(
                f,
                fieldnames=results[0].keys()
            )

            writer.writeheader()

            writer.writerows(results)

        return file

    # -----------------------------------------------------

    def export_json(
        self,
        results,
        prefix="trace"
    ):

        file = self.filename(prefix, "json")

        with open(
            file,
            "w",
            encoding="utf-8"
        ) as f:

            json.dump(
                results,
                f,
                indent=4,
                ensure_ascii=False
            )

        return file

    # -----------------------------------------------------

    def export_txt(
        self,
        results,
        prefix="trace"
    ):

        file = self.filename(prefix, "txt")

        with open(
            file,
            "w",
            encoding="utf-8"
        ) as f:

            f.write(
                "NetTraceX Report\n"
            )

            f.write("=" * 70)

            f.write("\n\n")

            for hop in results:

                f.write(
                    f'Hop {hop["ttl"]:>2} '
                    f'{hop["ip"]:<16} '
                    f'{hop["avg"]:.2f} ms '
                    f'Loss {hop["loss"]:.1f}%\n'
                )

        return file

    # -----------------------------------------------------

    def export_markdown(
        self,
        results,
        prefix="trace"
    ):

        file = self.filename(prefix, "md")

        with open(
            file,
            "w",
            encoding="utf-8"
        ) as f:

            f.write("# NetTraceX Report\n\n")

            f.write(
                "|Hop|Host|IP|Loss|Avg|Min|Max|Jitter|\n"
            )

            f.write(
                "|---|---|---|---|---|---|---|---|\n"
            )

            for hop in results:

                f.write(

                    f'|{hop["ttl"]}'
                    f'|{hop["host"]}'
                    f'|{hop["ip"]}'
                    f'|{hop["loss"]:.1f}%'
                    f'|{hop["avg"]:.2f}'
                    f'|{hop["min"]:.2f}'
                    f'|{hop["max"]:.2f}'
                    f'|{hop["jitter"]:.2f}|\n'

                )

        return file

    # -----------------------------------------------------

    def export_html(
        self,
        results,
        prefix="trace"
    ):

        file = self.filename(prefix, "html")

        template = Template("""

<!DOCTYPE html>

<html>

<head>

<meta charset="utf-8">

<title>NetTraceX Report</title>

<style>

body{

font-family:Arial;

margin:40px;

background:#f5f5f5;

}

table{

border-collapse:collapse;

width:100%;

background:white;

}

th,td{

border:1px solid #ddd;

padding:8px;

}

th{

background:#333;

color:white;

}

tr:nth-child(even){

background:#eee;

}

</style>

</head>

<body>

<h1>NetTraceX Report</h1>

<p>Generated :
{{ date }}</p>

<table>

<tr>

<th>Hop</th>
<th>Host</th>
<th>IP</th>
<th>Loss</th>
<th>Avg</th>
<th>Min</th>
<th>Max</th>
<th>Jitter</th>

</tr>

{% for hop in hops %}

<tr>

<td>{{hop.ttl}}</td>

<td>{{hop.host}}</td>

<td>{{hop.ip}}</td>

<td>{{"%.1f"|format(hop.loss)}}%</td>

<td>{{"%.2f"|format(hop.avg)}} ms</td>

<td>{{"%.2f"|format(hop.min)}} ms</td>

<td>{{"%.2f"|format(hop.max)}} ms</td>

<td>{{"%.2f"|format(hop.jitter)}} ms</td>

</tr>

{% endfor %}

</table>

</body>

</html>

""")

        html = template.render(

            date=datetime.now(),

            hops=results

        )

        with open(
            file,
            "w",
            encoding="utf-8"
        ) as f:

            f.write(html)

        return file

    # -----------------------------------------------------

    def export_all(
        self,
        results,
        prefix="trace"
    ):

        return {

            "csv":
                self.export_csv(
                    results,
                    prefix
                ),

            "json":
                self.export_json(
                    results,
                    prefix
                ),

            "txt":
                self.export_txt(
                    results,
                    prefix
                ),

            "markdown":
                self.export_markdown(
                    results,
                    prefix
                ),

            "html":
                self.export_html(
                    results,
                    prefix
                )

        }


exporter = Exporter()