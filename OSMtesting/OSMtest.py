from OSMPythonTools.api import Api
from OSMPythonTools.overpass import Overpass
import geojson
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
way(area)[highway=motorway];
out body geom;

''', timeout=500)


list = []
count = 0
counter = 0
for element in result.elements():
    linestring = element.geometry()
    for x in linestring["coordinates"]:
        counter += 1
        if(counter == 30):
            counter =0
            list.append(x)
    #for geometry in element.geometry():
    #    print(type(geometry["coordinates"]))
        # if(geometry.lon() and geometry.lat()):
        #     print(geometry.lon())
        #     print(geometry.lat())
        #     count += 1
        #     print(count)

url = ""
count = 0
for item in list:
    url += str(item[1])[0:7] + "," + str(item[0])[0:7] + "/"
    count += 1
print(url)
print(count)
