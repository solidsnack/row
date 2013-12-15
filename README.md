row
===

It's a reference implementation of a new tabular file standard [discussed at
dataprotocols repository][issue76].

It is like [CSV](http://en.wikipedia.org/wiki/Comma-separated_values) but has
stronger rules, inspired by the default data interchange formats of widely
used relational databases, like [Postgres][pg_copy] and [MySQL][mysql_load].
This format is less ambiguous than CSV and allows for line-oriented processing
(see "Specification" below).

[pg_copy]: http://www.postgresql.org/docs/9.3/static/sql-copy.html
[mysql_load]: http://dev.mysql.com/doc/refman/5.7/en/load-data.html
[issue76]: https://github.com/dataprotocols/dataprotocols/issues/76

Specification
-------------

The format allows for unframed, tab-separated data (denoted with `.tsv`) and
framed data which includes headers, comments and additional metadata.

In the unframed format,

- Rows must be separated by character `0x0A` (new line, often represented as
  `\n`). **Any** `0x0A` in the file **are row separators** (no exceptions);
- Fields must be separated by `0x09` (tabular space, often represented as
  `\t`). **Any** `0x09` in the file **are field separators** (no exceptions);
- Field values must be encoded in UTF-8 without BOM (byte-order-marker).
  Binary data should be encoded as base64 or any other format that uses UTF-8
  (or a subset of it, like ASCII) as output;
- Escape sequences for use inside field data:
  - `\n` for new line (`0x0A`),
  - `\t` for tabular space (`0x09`),
  - `\r` for carriage returns (`0x0D`),
  - `\N` for unavailable data,
  - `\\` for back slash (`0x5C`).
- Any trailing carriage returns are stripped.
- Any sequences of a backslash and a hash sign (`\#`) are collapsed to `#`, to
  improve compatiblity with the framed format, where leading `#` indicates a
  comment.

The framed format is still under [discussion][issue76]. In the framed format,
lines beginning with `#` are comments or supply metadata like column types and
names, format version and schema information. One can take advantage of this
fact to strip framing, sort a dataset and then restore framing:

    sed '/^#/! d' < in.row > frame.row
    sed '/^#/ d' < in.row | LC_ALL=C sort > sorted_data.row
    cat frame.row sorted_data.row > sorted.row

    # Or without temporaries...
    ( sed '/^#/! d' < in.row &&
      sed '/^#/ d' < in.row | LC_ALL=C sort ) > sorted.row

Example of Usage
----------------

Given the file `brazilian-cities.tsv`, we can read it like this:

    # coding: utf-8

    import sys
    import codecs
    sys.stdout = codecs.getwriter('utf8')(sys.stdout)

    import row


    cities = row.parse_file('brazilian-cities.tsv')
    cities_rio = [city for city in cities if city[0] == u'RJ']
    for city_data in cities_rio:
        area = float(city_data[3])
        inhabitants = int(city_data[2])
        density = inhabitants / area
        print(u'{}:'.format(city_data[1]))
        print(u'  area        = {:8.2f} km²'.format(area))
        print(u'  inhabitants = {:8d} citizens'.format(inhabitants))
        print(u'  density     = {:8.2f} citizens/km²'.format(density))



Tests
-----

First be sure you installed all dependencies:

    pip install -r requirements-development.txt

Then, to run the tests, just execute:

    make test
