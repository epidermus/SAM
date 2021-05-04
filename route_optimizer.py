from scipy.spatial.distance import directed_hausdorff
from ShapesStructure import image_processing as ip
import copy


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
	roads = []
	# preprocessing roads from OSM
	for list in city_coords:
		for road in list:
			if len(road) is 2:
				roads.append(road)

	best_image = copy.deepcopy(image)
	best_hausdorff = float('inf')

	rotation_degrees = 10
	for i in range(19):
		rotated_image = ip.rotate_image(image, rotation_degrees * i)
		lat = 0.0001
		# trying 25 different scaled versions of the rotated image each at 25 different vertical adjustments on map
		for j in range(25):
			scale_factor = 0.15
			temp_image = ip.scale_image(rotated_image, scale_factor * j)
			for k in range(25):
				temp_image = ip.translate_image(temp_image, lat, 0)
				current_hausdorff = max(directed_hausdorff(temp_image, roads)[0],
										directed_hausdorff(roads, temp_image)[0])
				if current_hausdorff < best_hausdorff:
					best_hausdorff = current_hausdorff
					best_image = copy.deepcopy(temp_image)


		long = 0.0001
		# trying 25 different scaled versions of the rotated image each at 25 different horizontal adjustments on map
		for j in range(25):
			scale_factor = 0.15
			temp_image = ip.scale_image(rotated_image, scale_factor * j)
			for k in range(25):
				temp_image = ip.translate_image(temp_image, 0, long)
				current_hausdorff = max(directed_hausdorff(temp_image, roads)[0],
										directed_hausdorff(roads, temp_image)[0])
				if current_hausdorff < best_hausdorff:
					best_hausdorff = current_hausdorff
					best_image = copy.deepcopy(temp_image)
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
