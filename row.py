# coding: utf-8

import re


_line_endings = re.compile(r'\r?\n')


def _filter_escape_sequences(value):
    if value == '\\N':
        return None
    else:
        return value.replace('\\t', '\t').replace('\\n', '\n')\
                    .replace('\\r', '\r').replace('\\\\', '\\')\
                    .replace('\\#', '#')


def parse(text, framed=False):
    if framed:
        raise ValueError('Framing is not implemented yet.')
    else:
        return [map(_filter_escape_sequences, line.split('\t'))
                for line in _line_endings.split(text) if line != '' ]


def parse_file(filename, framed=False):
    with open(filename) as fobj:
        return parse(fobj.read().decode('utf-8'), framed)
