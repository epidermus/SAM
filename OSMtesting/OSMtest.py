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
result = overpass.query('area[name="Salt Lake City"];way(area)[foot]; out;')
count = 0
for element in result.elements():
    print(element)
    count += 1
    print(count)

print(result)
