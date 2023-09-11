import numpy as np
from scipy.spatial import ConvexHull
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

# Generate some random 3D points
np.random.seed(0)
points = np.random.rand(20, 3)  # 100 random 3D points

# Compute the convex hull
hull = ConvexHull(points)

# Print the vertices (corners) of the convex hull
print("Vertices (Corners) of Convex Hull:")
for vertex in hull.vertices:
    print(points[vertex])

# Visualize the convex hull in 3D
fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')

# Plot the convex hull vertices
hull_points = points[hull.vertices]
# ax.plot(hull_points[:, 0], hull_points[:, 1], hull_points[:, 2], 'ro', label='Hull Vertices')

# Plot the convex hull edges
for simplex in hull.simplices:
    simplex_points = points[simplex]
    simplex_points = np.append(simplex_points, [simplex_points[0]], axis=0)  # Close the loop
    ax.plot(simplex_points[:, 0], simplex_points[:, 1], simplex_points[:, 2], 'b-', label='Hull Edges')

# Plot all points for reference
ax.scatter(points[:, 0], points[:, 1], points[:, 2], c='r', marker='o', label='All Points')

ax.set_xlabel('X')
ax.set_ylabel('Y')
ax.set_zlabel('Z')
ax.set_title('3D Convex Hull')
# ax.legend()

plt.show()
