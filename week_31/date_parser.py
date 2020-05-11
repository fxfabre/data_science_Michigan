#!/usr/bin/env python3

import re
import numpy as np
import pandas as pd
from typing import Dict

months = [
    "Jan([ua]{2}ry)?",
    "Feb(ruary)?", "Mar(?:ch)?", "Apr(?:il)?",
    "May", "Jun(?:e)?", "July?", "Aug(ust)?",
    "Sep(?:tember)?", "Oct(?:ober)?", "Nov(?:eme?ber)?", "Dec(?:eme?ber)?"
]

regexs_str = [
    (r'(?P<month>[01]?\d)/(?P<day>[0123]?\d)/(?P<year>\d{4}|\d{2})', {}),
    (r'(?P<month>[01]?\d)-(?P<day>[0123]?\d)-(?P<year>\d{4}|\d{2})', {}),
    (r'(?P<month>[01]\d)(?P<day>[0123]\d)(?P<year>\d{4}|\d{2})', {}),
    (r'(?P<month>[01]?\d)/(?P<year>\d{4}|\d{2})', {"day": 1}),
] + [
    (f"(({month})\W? (?P<day>[0123]\d)\W? (?P<year>\d\d(\d\d)?))", {"month": month_num})
    for month_num, month in enumerate(months, 1)
] + [
    (f"(?P<day>[0123]?\d) ({month}) (?P<year>\d\d(\d\d)?)", {"month": month_num})
    for month_num, month in enumerate(months, 1)
] + [
    (f"({month})\W? (?P<year>\d\d(\d\d)?)", {"day": 1, "month": month_num})
    for month_num, month in enumerate(months, 1)
] + [
    ("(?P<year>\d{4})", {"day": 1, "month": 1})
]
regexs = [
    (re.compile(regex, re.IGNORECASE), date_default)
    for (regex, date_default) in regexs_str
]


def parse_date(s: str) -> Dict[str, int]:
    for regex, date_default in regexs:
        match = regex.search(s)
        if not match:
            continue

        date_infos = dict(date_default)
        date_infos.update(match.groupdict())
        date_infos = {
            k: int(date_infos.get(k, 1))
            for k in ["day", "month", "year"]
            if isinstance(date_infos.get(k, ""), int) or date_infos.get(k, "").isdigit()
        }
        if date_infos["year"] < 100:
            date_infos["year"] += 1900

        if (date_infos["day"] > 31) or (date_infos["month"] > 12):
            continue

        return date_infos

    return {'day': np.nan, 'month': np.nan, 'year': np.nan}


def parse_date_str_to_int(s: str) -> int:
    date_info = parse_date(s)
    return date_info["year"] * 10000 + date_info["month"] * 100 + date_info["day"]


def date_sorter(df: pd.Series):
    return df.map(parse_date_str_to_int).sort_values().reset_index()["index"]


if __name__ == '__main__':
    df = pd.Series([
        "03/25/93 Total time of visit (in minutes)",
        "6/18/85 Primary Care Doctor",
        "sshe plans to move as of 7/8/71 In-Home Servic",
        "7 on 9/27/75 Audit C Score Current"
    ])
    print(date_sorter(df))
