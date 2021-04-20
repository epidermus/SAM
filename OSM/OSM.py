from OSMPythonTools.overpass import Overpass, overpassQueryBuilder


def obtain_map(city):
	overpass = Overpass()
	result = overpass.query(('''area[name="{}"];
	way(area)[highway=motorway];
	out body geom;

	''').format(city), timeout=500)
	return result


def obtain_square_portion(corner1, corner3, corner2, corner4):
	overpass = Overpass()
	query = overpassQueryBuilder(bbox=[corner1, corner2, corner3, corner4], elementType='way',
								 selector='"highway"', out="body geom")
	result = overpass.query(query)
	road_coords = []
	for element in result.elements():
		linestring = element.geometry()
		for x in linestring["coordinates"]:
			road_coords.append(x)
	return road_coords




# api = Api()
# overpass = Overpass()

# below line pulls all roads in an area
# test comment

# query = overpassQueryBuilder(area=nominatim.query('Salt Lake County'), elementType='way', selector = 'foot', out='body', includeGeometry=True)
# overpass.query(query,timeout=50)

# result = overpass.query(#'''area[name="Salt Lake County"];
# way(area)[highway=motorway];
# out body geom;

# ''', timeout=500)


# list = []
# count = 0
# counter = 0
# for element in result.elements():
#    linestring = element.geometry()
#    for x in linestring["coordinates"]:
#        counter += 1
#        if counter == 150:
#            list.append(x)
#            counter = 0
#
# coords = ""
# count = 0
# for item in list:
#    coords += str(item[1])[0:7] + "," + str(item[0])[0:7] + "/"
#    count += 1

# print('SLC coords: ' + str(coords))
# print('Number of SLC coords loaded: ' + str(count) + '\n')
#
# image = ip.load_shape('apple-1.json')
# print('\nPoints of image before being converted to lat/long: ' + str(image))
## testing the conversion of image points to lat long points
## our ranges for Salt Lake... lat: 40.5928 - 40.7187 / long: -112.06 - -111.97
## playing around with the ranges creates drastically different routes
# geo_image = ip.points_to_lat_long(image, 40.5928, 40.7, -112, -111.9)
# print('Points of image after being converted to lat/long: ' + str(geo_image))
#
##construct coords to be placed into URL
# url_end = ''
# for point in geo_image:
#    url_end += str(point[0]) + ',' + str(point[1]) + '/'
#
## showing route that will look like an apple in Google maps...
# webbrowser.open('https://www.google.com/maps/dir/' + url_end)
