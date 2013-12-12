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
    print(city_data[1])
    print(u'  area        = {:8.2f} km²'.format(area))
    print(u'  inhabitants = {:8d} citizens'.format(inhabitants))
    print(u'  density     = {:8.2f} citizens/km²'.format(density))
