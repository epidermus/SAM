from OSMPythonTools.api import Api
from OSMPythonTools.overpass import Overpass
import json
# from OSMPythonTools.overpass import overpassQueryBuilder
# from OSMPythonTools.nominatim import Nominatim
# nominatim = Nominatim()

api = Api()
overpass = Overpass()

# below line pulls all roads in an area
# test comment

# query = overpassQueryBuilder(area=nominatim.query('Salt Lake County'), elementType='way', selector = 'foot', out='body', includeGeometry=True)
# overpass.query(query,timeout=50)

result = overpass.query('''area[name="Salt Lake County"];
way(area)[foot];
out body geom;

''', timeout=50)



count = 0
for element in result.elements():
    print(element.geometry())
    for geometry in element.geometry():
        print(geometry)
        # if(geometry.lon() and geometry.lat()):
        #     print(geometry.lon())
        #     print(geometry.lat())
        #     count += 1
        #     print(count)

print(result)
