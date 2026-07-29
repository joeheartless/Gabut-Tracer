"""
#
#
# Gabut Tracer v0.6.9
# Written by Prima Agus Setiawan 
# a.k.a joeheartless / joefryme@gmail.com
"""

from __future__ import annotations

from dataclasses import dataclass
from statistics import mean, median
import math


@dataclass
class StatsResult:
    samples: int
    minimum: float
    maximum: float
    average: float
    median: float
    variance: float
    stddev: float
    jitter: float
    rfc3550_jitter: float


class NetworkStats:

    def __init__(self, values: list[float]):

        self.values = [
            float(v)
            for v in values
            if v is not None
        ]

    # ------------------------------------------

    @property
    def count(self):

        return len(self.values)

    # ------------------------------------------

    @property
    def minimum(self):

        if not self.values:
            return 0.0

        return min(self.values)

    # ------------------------------------------

    @property
    def maximum(self):

        if not self.values:
            return 0.0

        return max(self.values)

    # ------------------------------------------

    @property
    def average(self):

        if not self.values:
            return 0.0

        return mean(self.values)

    # ------------------------------------------

    @property
    def median(self):

        if not self.values:
            return 0.0

        return median(self.values)

    # ------------------------------------------

    @property
    def variance(self):

        n = len(self.values)

        if n < 2:
            return 0.0

        avg = self.average

        return sum(
            (x - avg) ** 2
            for x in self.values
        ) / (n - 1)

    # ------------------------------------------

    @property
    def stddev(self):

        return math.sqrt(self.variance)

    # ------------------------------------------

    @property
    def jitter(self):

        """
        Mean Absolute Difference
        """

        if len(self.values) < 2:
            return 0.0

        diff = []

        for i in range(1, len(self.values)):

            diff.append(
                abs(
                    self.values[i]
                    -
                    self.values[i - 1]
                )
            )

        return mean(diff)

    # ------------------------------------------

    @property
    def rfc3550_jitter(self):

        """
        RFC3550 estimator
        """

        if len(self.values) < 2:
            return 0.0

        j = 0.0

        previous = self.values[0]

        for current in self.values[1:]:

            d = abs(current - previous)

            j += (d - j) / 16

            previous = current

        return j

    # ------------------------------------------

    @staticmethod
    def packet_loss(sent, received):

        if sent <= 0:
            return 100.0

        return (
            (sent - received)
            / sent
        ) * 100

    # ------------------------------------------

    def summary(self):

        return StatsResult(

            samples=self.count,

            minimum=self.minimum,

            maximum=self.maximum,

            average=self.average,

            median=self.median,

            variance=self.variance,

            stddev=self.stddev,

            jitter=self.jitter,

            rfc3550_jitter=self.rfc3550_jitter
        )
    # ======================================================
# Advanced Statistics
# ======================================================

import bisect


class NetworkStats(NetworkStats):

    # ------------------------------------------

    def percentile(self, p: float):

        """
        Linear interpolation percentile.

        Example:
            percentile(95)
            percentile(99)
        """

        if not self.values:
            return 0.0

        if p <= 0:
            return self.minimum

        if p >= 100:
            return self.maximum

        data = sorted(self.values)

        k = (len(data) - 1) * (p / 100)

        f = int(k)

        c = min(f + 1, len(data) - 1)

        if f == c:
            return data[f]

        return data[f] + (data[c] - data[f]) * (k - f)

    # ------------------------------------------

    @property
    def p50(self):
        return self.percentile(50)

    @property
    def p90(self):
        return self.percentile(90)

    @property
    def p95(self):
        return self.percentile(95)

    @property
    def p99(self):
        return self.percentile(99)

    # ------------------------------------------

    def moving_average(self, window=5):

        """
        Simple Moving Average
        """

        if window <= 0:
            raise ValueError("window > 0")

        if len(self.values) < window:
            return []

        result = []

        for i in range(len(self.values) - window + 1):

            result.append(
                sum(self.values[i:i + window]) / window
            )

        return result

    # ------------------------------------------

    def ewma(self, alpha=0.25):

        """
        Exponential Weighted Moving Average
        """

        if not self.values:
            return []

        output = [self.values[0]]

        for value in self.values[1:]:

            output.append(
                alpha * value +
                (1 - alpha) * output[-1]
            )

        return output

    # ------------------------------------------

    def mad(self):

        """
        Median Absolute Deviation
        """

        if not self.values:
            return 0.0

        med = self.median

        dev = [
            abs(x - med)
            for x in self.values
        ]

        return median(dev)

    # ------------------------------------------

    def confidence95(self):

        """
        95% Confidence Interval
        """

        if self.count < 2:

            return (
                self.average,
                self.average
            )

        margin = (
            1.96 *
            self.stddev /
            math.sqrt(self.count)
        )

        return (

            self.average - margin,

            self.average + margin

        )

    # ------------------------------------------

    def trend(self):

        """
        Very simple latency trend
        """

        if self.count < 3:
            return "unknown"

        half = self.count // 2

        first = mean(self.values[:half])

        second = mean(self.values[half:])

        diff = second - first

        if diff > 2:
            return "increasing"

        if diff < -2:
            return "decreasing"

        return "stable"

    # ------------------------------------------

    def outlier_iqr(self):

        """
        IQR outlier detection
        """

        if self.count < 4:
            return []

        data = sorted(self.values)

        q1 = self.percentile(25)

        q3 = self.percentile(75)

        iqr = q3 - q1

        low = q1 - 1.5 * iqr

        high = q3 + 1.5 * iqr

        return [

            x

            for x in data

            if x < low or x > high

        ]

    # ------------------------------------------

    def insert_sample(self, value):

        """
        Keep sorted latency list.
        Useful for live monitor.
        """

        bisect.insort(self.values, float(value))

    # ------------------------------------------

    def summary_dict(self):

        ci_low, ci_high = self.confidence95()

        return {

            "count": self.count,

            "min": self.minimum,

            "max": self.maximum,

            "avg": self.average,

            "median": self.median,

            "stddev": self.stddev,

            "variance": self.variance,

            "jitter": self.jitter,

            "rfc3550_jitter": self.rfc3550_jitter,

            "p50": self.p50,

            "p90": self.p90,

            "p95": self.p95,

            "p99": self.p99,

            "mad": self.mad(),

            "trend": self.trend(),

            "confidence95": (

                ci_low,

                ci_high

            ),

            "outliers": self.outlier_iqr()

        }