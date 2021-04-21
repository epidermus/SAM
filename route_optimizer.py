from scipy.spatial.distance import directed_hausdorff
from ShapesStructure import image_processing as ip
import numpy as np


def optimize_route(image, city_coords):
	"""
	utilizes scaling and rotation functions from image_processing.py to position an image from the 2DShapesStructure
	dataset onto the roads of a city such that the roads closely resemble the original image. Hausdorff distance is used
	as fitness metric of any single fitting.
	:param image: the image to fit to a route
	:param city_coords: the geographic coordinates of the streets of the city we are fitting an image to (from OSM)
	:return: the image coordinates optimized to a road in the provided city bounds
	"""
	# 1) filter out coords that are greater than a certain Hausdorff dist
	# 2) rotate, scale, and translate until a threshold is met for Hausdorff
	closest_roads = []
	# trimming roads that are over a Hausdorff distance threshold
	for road in city_coords:
		# check that num of columns in road is same as image
		if len(road[0]) is 2 and max(directed_hausdorff(road, image)[0], directed_hausdorff(image, road)[0]) < 215.79:
			closest_roads.append(road)

	best_image = image
	best_hausdorff = float('inf')
	for road in closest_roads:
		temp_image = best_image
		lat = 0.0001
		# trying 25 different vertical adjustments on map
		for i in range(25):
			temp_image = ip.translate_image(temp_image, lat, 0)
			current_hausdorff = max(directed_hausdorff(temp_image, road)[0], directed_hausdorff(road, temp_image)[0])
			if current_hausdorff < best_hausdorff:
				best_hausdorff = current_hausdorff
				best_image = temp_image

	for road in closest_roads:
		temp_image = best_image
		long = 0.0001
		# trying 25 different horizontal adjustments on map
		for i in range(25):
			temp_image = ip.translate_image(temp_image, 0, long)
			current_hausdorff = max(directed_hausdorff(temp_image, road)[0], directed_hausdorff(road, temp_image)[0])
			if current_hausdorff < best_hausdorff:
				best_hausdorff = current_hausdorff
				best_image = temp_image

	return best_image



# A = np.array([(1.0, 0.0),
#              (0.0, 1.0),
#              (-1.0, 0.0),
#              (0.0, -1.0)])

# B = np.array([(2.0, 0.0),
#              (0.0, 2.0),
#              (-2.0, 0.0),
#             (0.0, -4.0)])

'''
directed_hausdorff returns a 3-tuple where the first element is the directed hausdorff distance from A to B, and the
second and third elements are the indexes of the points in A and B in their respective array representations that
generated that distance
'''
# print(directed_hausdorff(A, B))

'''
note that scipy uses a "directed" hausdorff, meaning that, given sets of points A and B,
directed_hausdorff(A, B) is not always equal to directed_hausdorff(B, A) (not symmetric). For a general (symmetric)
Hausdorff distance, use the max() function:
'''
# print(max(directed_hausdorff(A, B)[0], directed_hausdorff(B, A)[0]))
