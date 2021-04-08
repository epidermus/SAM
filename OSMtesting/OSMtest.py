from OSMPythonTools.api import Api
from OSMPythonTools.overpass import Overpass
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
    if(element.lon() and element.lat()):
        print(element.lon())
        print(element.lat())
        count += 1
        print(count)

print(result)
