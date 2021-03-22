from OSMPythonTools.api import Api
from OSMPythonTools.overpass import Overpass

api = Api()
overpass = Overpass()
way = api.query('way/5887599')
result = overpass.query('way["name"="Stephansdom"]; out body;')

print(way.tag('building'))
# 'castle'
print(way.tag('architect'))
# 'Johann Lucas von Hildebrandt'
print(way.tag('website'))
# 'http://www.belvedere.at'

print("Overpass Test")

stephansdom = result.elements()[0]

print(stephansdom.tag('name:en'))

# below line pulls all roads in an area
result = overpass.query('way[foot](53.2987342,-6.3870259,53.4105416,-6.1148829); out;')

pubs = result.elements()[0]
print(result)
