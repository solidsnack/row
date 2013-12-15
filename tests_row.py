# coding: utf-8

import unittest

from textwrap import dedent

from row import parse, parse_file


class TestTab(unittest.TestCase):
    def test_normal_records(self):
        contents = dedent('''
        123\t456\t789\t0\t-1
        -1\t0\t789\t456\t123
        ''').strip()
        expected = [
            ['123', '456', '789', '0',   '-1'],
            ['-1',  '0',   '789', '456', '123'],
        ]
        result = parse(contents)
        self.assertEqual(result, expected)

    def test_empty_lines(self):
        contents = dedent('''
        123\t456\t789\t0\t-1


        -1\t0\t789\t456\t123
        ''').strip() + '\n'
        expected = [
            ['123', '456', '789', '0',   '-1'],
            ['-1',  '0',   '789', '456', '123'],
        ]
        result = parse(contents)
        self.assertEqual(result, expected)

    def test_escape_sequences(self):
        backslash = '\\\\'
        tab = '\\t'
        newline = '\\n'
        carriage_return = '\\r'
        null = '\\N'
        contents = dedent('''
        {}\t{}\t{}\t{}\t{}\tz
        \#a\tb\tc\td\te\tf
        '''.format(backslash, tab, newline, carriage_return, null)).strip()
        expected = [
            ['\\', '\t', '\n', '\r', None, 'z'],
            ['#a', 'b',  'c',  'd',  'e', 'f'],
        ]
        result = parse(contents)
        self.assertEqual(result, expected)

    def test_parse_unframed_file(self):
        cities = parse_file('brazilian-cities.tsv')
        self.assertEqual(len(cities), 5565)

        cities_rio = [city for city in cities if city[0] == u'RJ']
        self.assertEqual(len(cities_rio), 92)

        types_values = set([type(value) for city in cities for value in city])
        expected_types = set([unicode])
        self.assertEqual(types_values, expected_types)

    def test_parse_framed_file(self):
        (framing, cities) = parse_file('brazilian-cities.row', framed=True)
        self.assertIsNotNone(framing)
        self.assertEqual(len(cities), 5565)
        self.assertEqual(framing.columns,
                         ['state', 'city', 'inhabitants', 'area'])

        cities_rio = [city for city in cities if city['state'] == u'RJ']
        self.assertEqual(len(cities_rio), 92)

        types_values = set([type(value) for city in cities for value in city])
        expected_types = set([unicode])
        self.assertEqual(types_values, expected_types)
