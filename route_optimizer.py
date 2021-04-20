from scipy.spatial.distance import directed_hausdorff
from OSMPythonTools.api import Api
from OSMPythonTools.overpass import Overpass
from ShapesStructure import image_processing as ip
from OSMPythonTools.overpass import overpassQueryBuilder
import webbrowser
import numpy as np


def optimize_route(image, city_coords):
	"""
	utilizes scaling and rotation functions from image_processing.py to position an image from the 2DShapesStructure
	dataset onto the roads of a city such that the roads closely resemble the original image. Hausdorff distance is used
	as fitness metric of any single fitting.
	:param image: the image to fit to a route
	:param city_coords: the geographic coordinates of the streets of the city we are fitting an image to
	:return:
	"""
	pass


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
