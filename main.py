from OSM import OSM
from ShapesStructure import image_processing as ip
from definitions import *
from route_optimizer import obtainMap
from route_optimizer import obtainSquarePortion
import webbrowser


def main():
	images_dir = ROOT_DIR + '\\ShapesStructure\\Shapes_JSON'
	image_files = [f for f in os.listdir(images_dir) if os.path.isfile(os.path.join(images_dir, f))]

	for image in image_files:
		print(image.split('.')[0])

	image_name = ''
	while image_name + '.json' not in image_files:
		image_name = input('\nEnter an image name from above for SAM to sketch on a map of SLC: ')
		if image_name + '.json' not in image_files:
			print('Sorry, there is no image with the name \'' + image_name + '\' in the dataset. Please enter a valid name.')
		else:
			image = ip.load_shape(image_name + '.json')
			# ranges for Salt Lake roughly... lat: 40.5928 - 40.7187 / long: -112.06 - -111.97
			geo_image = ip.points_to_lat_long(image, 40.5928, 40.7, -112, -111.9)

	# TODO: still need to optimize which points are cut from each image
	i = 1
	while len(geo_image) > 24:
		# remove every third point until total points in image is <= 25
		if i % 7 == 0:
			geo_image.pop(i)
		i += 1
	geo_image.append(geo_image[0])
	# construct coords to be placed into URL
	# TODO: implement route optimization techniques through rotation, scaling, and comparing to road coords from OSM using Hausdorff
	url_end = ''
	for point in geo_image:
		url_end += str(point[0]) + ',' + str(point[1]) + '/'

	print('\nOpening SAM\'s sketch in Google Maps...')
	# showing route that will look like an apple in Google maps...
	webbrowser.open('https://www.google.com/maps/dir/' + url_end)
	obtainMap("Salt Lake City")
	obtainMap("Portland")
	obtainSquarePortion(40.5928, 40.7, -112, -111.9)


if __name__ == "__main__":
	main()
