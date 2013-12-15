# coding: utf-8
# TODO: Handle streams instead of strings.

import re


_line_endings = re.compile(r'\r?\n')
_backslash_and_something = re.compile(r'\\(.)')

def _filter_escape_sequences(s):
    if s == '\\N':
        return None
    else:
        t = s.replace('\\t', '\t').replace('\\n', '\n').replace('\\r', '\r')
        # Ignore all other backslashes.
        return _backslash_and_something.sub(r'\1', t)


def parse(text, framed=False):
    if framed:
        return parse_framed(text)
    else:
        return [ parse_line(line) for line
                                  in _line_endings.split(text) if line != '' ]


def parse_file(filename, framed=False):
    with open(filename) as fobj:
        return parse(fobj.read().decode('utf-8'), framed)


def parse_line(line):
    return map(_filter_escape_sequences, line.split('\t'))


def parse_framed(text, named=True):
    in_pragma = False
    fp = FramingParse()
    data = []
    for (num, line) in enumerate(_line_endings.split(text), 1):
        for tag, f in [('#:', fp.parse_types),  ('#.', fp.parse_columns),
                       ('#-', fp.parse_pragma), ('#=', fp.parse_pragma),
                       ('#*', fp.parse_version)]:
            if line.startswith(tag):
                f(line)
                continue
        if '#' == line[0:1] or '' == line: # Skip comments and empties.
            continue
        # If it doesn't begin with a '#', we're on a data line.
        if not fp.columns:
            raise ColumnNamesExpected()
        else:
            if named:
                data.append(dict(zip(fp.columns, parse_line(line))))
            else:
                data.append(parse_line(line))
    return (fp.framing(), data)


# State machine for handling framing lines.
class FramingParse(object):
    def __init__(self, columns=None, types=None, version=None, pragmas=[]):
        for name, value in locals().iteritems():
            setattr(self, name, value)
    def parse_columns(self, line):
        if not self.columns:
            self.columns = parse_line(line[2:].lstrip(' '))
    def parse_types(self, line):
        if not self.types:
            self.types = parse_line(line[2:].lstrip(' '))
    def parse_version(self, line):
        if not self.version:
            self.version = line[2:].strip()
    def parse_pragma(self, line):
        if line.startswith('#-'): pass
        if line.startswith('#='): pass
    def framing(self):
        if self.version is not None and self.columns is not None:
            return Framing(self.columns, self.types,
                           self.version, self.pragmas)

class Framing(object):
    def __init__(self, columns, types, version, pragmas=[]):
        for name, value in locals().iteritems():
            setattr(self, name, value)


class Error(Exception):
    pass

class ColumnNamesExpected(Error):
    pass

