import json
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


# testing points with directed_hausdorff from scipy
frog = load_shape('frog-1.json')
fork = load_shape('fork-1.json')

# directed hausdorff from fork to frog
directed_hdorff = directed_hausdorff(fork, frog)[0]
print('Directed Hausdorff between frog and fork image: {}'.format(directed_hdorff))

# symmetric hausdorff
symmetric_hdorff = max(directed_hausdorff(frog, fork)[0], directed_hausdorff(fork, frog)[0])
print('Symmetric Hausdorff between frog and fork image: {}'.format(symmetric_hdorff))
