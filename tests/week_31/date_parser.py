#!/usr/bin/env python3

from unittest import TestCase
from parameterized import parameterized
from week_31.date_parser import parse_date, regexs_str


class TestDateParser(TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        print('\n'.join(map(str, regexs_str)))

    @parameterized.expand([
        ("3/8/80", 8, 3, 1980),
        ("25 4-13-82 Ot", 13, 4, 1982),
        ("WEEKS on 24 Jan 2001.", 24, 1, 2001),
        ("194 April 11, 1990 CPT Code: 90791", 11, 4, 1990),
        ("school as of September 1985.", 1, 9, 1985),
        ("6/1998 Primary", 1, 6, 1998),
        ("lala 12 03121923 13 lala", 12, 3, 1923),
        ("lala 123 2020 13 lala", 1, 1, 2020),
    ])
    def test_parse_str(self, s: str, day: int, month: int, year: int):
        date = parse_date(s)
        self.assertEqual({"day": day, "month": month, "year": year}, date, date)
