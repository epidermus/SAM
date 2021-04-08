import json
import os
import random
import math
import matplotlib.pyplot as plt
from scipy.spatial.distance import directed_hausdorff


def load_shape(shape_file_name):
	"""
	loads in the point of a shape from the 2DShapesStructure data set
	:param shape_file_name: a string of the exact name of the JSON file located within shapes_JSON
	:return: a list of tuples containing the x and y-coordinates of the shape
	"""
	with open('./Shapes_JSON/{}'.format(shape_file_name), 'r') as file:
		data = json.load(file)
		dict_points = data['points']
		points = []
		for dict in dict_points:
			points.append((dict['x'], dict['y']))
		return points


def load_random_shape():
	"""
	loads a random image from the 2DShapesStructure data set
	:return: a list of tuples containing the x and y-coordinates of the shapes
	"""
	path = './Shapes_JSON/'
	random_filename = random.choice([
		x for x in os.listdir(path)
		if os.path.isfile(os.path.join(path, x))
	])
	return load_shape(random_filename)


def rotate_image(points, angle):
	"""
	rotates an image (list of points) counterclockwise a specified number of degrees
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
	scales an image (list of points) by a specified scalar amount
	:param points: list of points representing an image
	:param scale_factor: the amount of scaling to apply to the image
	:return: the scaled image as a new list of points
	"""
	# no scaling done if scaling factor is 1
	if scale_factor == 1:
		return points
	scaled_points = []
	for point in points:
		scaled_x = scale_factor * point[0]
		scaled_y = scale_factor * point[1]
		# trying keep centroid of image in same position
		#	if scale_factor < 1:
		#		# image shrinks in this case
		#		scaled_x += (point[0] - scaled_x) / 2
		#		scaled_y += (point[1] - scaled_y) / 2
		#	else:
		# image grows in this case
		#		scaled_x -= (scaled_x - point[0]) / 2
		#		scaled_y -= (scaled_y - point[1]) / 2
		scaled_points.append((scaled_x, scaled_y))
	return scaled_points


def calculate_centroid(points):
	"""
	calculates the center of mass point given a set of cartesian coordinates
	:param points: the list of points
	:return: a tuple with the x and y coordinate values for the center of the image
	"""
	x = [p[0] for p in points]
	y = [p[1] for p in points]
	return (sum(x) / len(points), sum(y) / len(points))


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

# testing points with directed_hausdorff from scipy
frog = load_shape('frog-1.json')
fork = load_shape('fork-1.json')

# directed hausdorff from fork to frog
directed_hdorff = directed_hausdorff(fork, frog)[0]
print('Directed Hausdorff between frog and fork image: {}\n'.format(directed_hdorff))

# symmetric hausdorff
symmetric_hdorff = max(directed_hausdorff(frog, fork)[0], directed_hausdorff(fork, frog)[0])
print('Symmetric Hausdorff between frog and fork image: {}\n'.format(symmetric_hdorff))

# testing centroid
print('Centroid of frog image: ' + str(calculate_centroid(frog)) + '\n')


image = load_random_shape()

# testing rotation and scaling functions
draw_image(image, 'Random image before rotation')
image = rotate_image(image, 90)
draw_image(image, 'Random image rotated 90 degrees counterclockwise \n using image_processing.rotate_image function')
image = scale_image(image, 2)
draw_image(image, 'Random image rotated and scaled up by a factor of 2')
