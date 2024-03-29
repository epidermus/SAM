import json
import os
import random
import math
import matplotlib.pyplot as plt
from definitions import ROOT_DIR


def load_shape(shape_file_name):
	"""
	loads in the point of a shape from the ShapesStructure data set
	:param shape_file_name: a string of the exact name of the JSON file located within shapes_JSON
	:return: a list of tuples containing the x and y-coordinates of the shape
	"""
	with open(ROOT_DIR + '\\ShapesStructure\\Shapes_JSON\\{}'.format(shape_file_name), 'r') as file:
		data = json.load(file)
		dict_points = data['points']
		points = []
		count = 0
		for dict in dict_points:
			points.append((dict['x'], dict['y']))
			count += 1
		print('Number of points in loaded image: ' + str(count))
		return points


def load_random_shape():
	"""
	loads a random image from the ShapesStructure data set
	:return: a list of tuples containing the x and y-coordinates of the shapes
	"""
	path = ROOT_DIR + '\\ShapesStructure\\Shapes_JSON\\'
	random_filename = random.choice([
		x for x in os.listdir(path)
		if os.path.isfile(os.path.join(path, x))
	])
	print('Loaded image: ' + random_filename)
	return load_shape(random_filename)


def load_shape_from_mood(mood):
	"""
	Loads a random image from a directory that corresponds to the given mood
	:param mood: the mood of the image to randomly select
	:return: a list of tuples containing the x and y-coordinates of the shapes
	"""
	path = ROOT_DIR + '\\ShapesStructure\\Moods\\' + mood + "\\"
	random_filename = random.choice([
		x for x in os.listdir(path)
		if os.path.isfile(os.path.join(path, x))
	])
	print('Loaded image: ' + random_filename)
	return load_shape(random_filename)


def rotate_image(points, angle):
	"""
	rotates an image (list of points) counterclockwise a specified number of degrees (assuming (x,y) coordinate plane)
	NOTE: will rotate images clockwise if points are in (y,x) format, such as with geographic coordinates (lat, long)
	:param points: list of points representing an image
	:param angle: the amount of rotation to apply to the image in degrees
	:return: the rotated image as a new list of points
	"""
	centroid = calculate_centroid(points)
	rotated_points = []
	# convert angle to radians for calculations
	angle = math.radians(angle)
	o_x, o_y = centroid
	for point in points:
		p_x, p_y = point

		r_x = o_x + math.cos(angle) * (p_x - o_x) - math.sin(angle) * (p_y - o_y)
		r_y = o_y + math.sin(angle) * (p_x - o_x) + math.cos(angle) * (p_y - o_y)
		rotated_points.append((r_x, r_y))
	return rotated_points


def scale_image(points, scale_factor):
	"""
	scales an image (list of points) by a specified scalar amount, where center of resizing is the center of the image
	:param points: list of points representing an image
	:param scale_factor: the amount of scaling to apply to the image
	:return: the scaled image as a new list of points
	"""
	# no scaling done if scaling factor is 1
	centroid = calculate_centroid(points)
	if scale_factor == 1:
		return points
	scaled_points = []
	for point in points:
		scaled_x = centroid[0] + scale_factor * (point[0] - centroid[0])
		scaled_y = centroid[1] + scale_factor * (point[1] - centroid[1])
		scaled_points.append((scaled_x, scaled_y))
	return scaled_points


def translate_image(points, lat_direction, long_direction):
	"""
	moves an image to a different location
	:param points: list of points representing an image
	:param lat_direction: how many units the image will be translated in the north/south direction
	:param long_direction: how many units the image will be translated in the east/west direction
	:return: a new list of the translated points
	"""
	translated_points = []
	for point in points:
		translated_points.append((point[0] + lat_direction, point[1] + long_direction))
	return translated_points


def calculate_centroid(points):
	"""
	calculates the center of mass point given a set of cartesian coordinates
	:param points: the list of points
	:return: a tuple with the x and y coordinate values for the center of the image
	"""
	x = [p[0] for p in points]
	y = [p[1] for p in points]
	return (sum(x) / len(points), sum(y) / len(points))


# our ranges for Salt Lake are roughly... lat: 40.5928 - 40.7187 / long: -112.06 - -111.97
def points_to_lat_long(points, lat_s, lat_f, long_s, long_f):
	"""
	converts a set of points (assuming a range of [0, 1] for x and y coordinates) to a set of lat and long coordinates
	:param points: the points to be converted to geographical coordinates
	:param long_s: the minimum longitude value in the plane
	:param long_f: the maximum longitude value in the plane
	:param lat_s: the minimum latitude value in the plane
	:param lat_f: the maximum latitude value in the plane
	:return: a new list containing the geographic coordinates of the points representing an image
	"""
	old_range = 1
	new_range_long = long_f - long_s
	new_range_lat = lat_f - lat_s
	geo_points = []
	for point in points:
		lat = ((point[1] * new_range_lat) / old_range) + lat_s
		long = ((point[0] * new_range_long) / old_range) + long_s
		geo_points.append((lat, long))
	return geo_points


def trim_points(points):
	"""
	trims the number of points in an image to be <= 25 (Google Maps only accepts 25 coordinates in the URL)
	:param points: list of points representing an image
	:return: the original list having it total number of points trimmed to <= 25
	"""
	i = 1
	while len(points) > 24:
		# remove every third point until total points in image is <= 25
		if i >= len(points):
			i = 0
		if i % 2 == 0:
			points.pop(i)
		i += 1
	points.append(points[0])


def draw_image(points, title=''):
	"""
	draws an image from a set of points using matplotlib.pyplot
	:param points: the list of points of the image to draw
	:param title: (optional) set the title of the plotted image
	"""
	x_coords = []
	y_coords = []
	for point in points:
		x_coords.append(point[0])
		y_coords.append(point[1])
	plt.title(title)
	plt.xlim(-1, 2.5)
	plt.ylim(-1, 2.5)
	plt.plot(x_coords, y_coords)
	plt.show()


## testing points with directed_hausdorff from scipy
# frog = load_shape('frog-1.json')
# fork = load_shape('fork-1.json')
#
## directed hausdorff from fork to frog
# directed_hdorff = directed_hausdorff(fork, frog)[0]
# print('Directed Hausdorff between frog and fork image: {}\n'.format(directed_hdorff))
#
## symmetric hausdorff
# symmetric_hdorff = max(directed_hausdorff(frog, fork)[0], directed_hausdorff(fork, frog)[0])
# print('Symmetric Hausdorff between frog and fork image: {}\n'.format(symmetric_hdorff))
#
## testing centroid
# print('Centroid of frog image: ' + str(calculate_centroid(frog)) + '\n')
#
#
#image = load_random_shape()

# testing rotation and scaling functions
#draw_image(image, 'Random image before rotation')
#image = rotate_image(image, 90)
#draw_image(image, 'Random image rotated 90 degrees counterclockwise \n using image_processing.rotate_image function')
#image = scale_image(image, 2)
#draw_image(image, 'Random image rotated and scaled up by a factor of 2')
