# concave hull
from shapely.ops import cascaded_union, polygonize
from scipy.spatial import Delaunay
import numpy as np
from shapely import geometry
alpha = 0.7
coords = np.concatenate(tuple([np.array(x.exterior.coords) for x in poly.geoms])).astype(np.int32)
tri = Delaunay(coords)
triangles = coords[tri.vertices]
a = ((triangles[:,0,0] - triangles[:,1,0]) ** 2 + (triangles[:,0,1] - triangles[:,1,1]) ** 2) ** 0.5
b = ((triangles[:,1,0] - triangles[:,2,0]) ** 2 + (triangles[:,1,1] - triangles[:,2,1]) ** 2) ** 0.5
c = ((triangles[:,2,0] - triangles[:,0,0]) ** 2 + (triangles[:,2,1] - triangles[:,0,1]) ** 2) ** 0.5
s = ( a + b + c ) / 2.0
areas = (s*(s-a)*(s-b)*(s-c)) ** 0.5
circums = a * b * c / (4.0 * areas)
filtered = triangles[circums < (1.0 / alpha)]
edge1 = filtered[:,(0,1)]
edge2 = filtered[:,(1,2)]
edge3 = filtered[:,(2,0)]
edge_points = np.unique(np.concatenate((edge1,edge2,edge3)), axis = 0).tolist()
m = geometry.MultiLineString(edge_points)
triangles = list(polygonize(m))
cascaded_union(triangles)
