import webbrowser
from OSM import OSM
from ShapesStructure import image_processing as ip
from definitions import *
import route_optimizer as ro
import time



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
			# ranges for middle chunk of Salt Lake roughly... lat: 40.5928 - 40.68 / long: -112 - -111.9
			geo_image = ip.points_to_lat_long(image, 40.5928, 40.68, -112, -111.9)

	# TODO: still need to optimize which points are cut from each image (in ip.trim_points)
	if len(geo_image) > 25:
		print('Trimming image down to 25 points...')
		ip.trim_points(geo_image)

	SLC = OSM.obtain_map('Salt Lake City')
	Portland = OSM.obtain_map('Portland')
	SLC_square = OSM.obtain_square_portion(40.5928, 40.7, -112, -111.9)

	print('\nSAM is creating the route for you! This might take a minute or two...')

	start_time = time.time()

	# TODO: implement route optimization techniques (in route_optimizer.py) through rotation, scaling, and comparing to road coords from OSM using Hausdorff
	geo_image = ro.optimize_route(geo_image, SLC_square)

	end_time = time.time()
	print('Time taken to create route: ' + str(round(end_time - start_time, 2)) + ' seconds')

	# construct coords to be placed into URL
	url_end = ''
	for point in geo_image:
		url_end += str(point[0]) + ',' + str(point[1]) + '/'

	print('\nOpening SAM\'s sketch in Google Maps...')
	# showing route that will look like an apple in Google maps...
	webbrowser.open('https://www.google.com/maps/dir/' + url_end)


if __name__ == '__main__':
	main()
