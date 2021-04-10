from OSMPythonTools.api import Api
from OSMPythonTools.overpass import Overpass
import geojson
import webbrowser
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


list = []
count = 0
for element in result.elements():
    linestring = element.geometry()
    list = []
    for x in linestring["coordinates"]:
        list.append(x)

url = ""
count = 0
for item in list:
    url += str(item[1])[0:7] + "," + str(item[0])[0:7] + "/"
    count += 1
print(url)
print(count)
webbrowser.open("https://www.google.com/maps/dir/" + url)
