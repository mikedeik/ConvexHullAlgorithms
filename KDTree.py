import numpy as np
from UtilityFunctions import generatePoints
import matplotlib.pyplot as plt

class KDNode:
    def __init__(self, point, left=None, right=None):
        self.point = point
        self.left = left
        self.right = right

class KDTree:
    def __init__(self, points, visualize=False):
        self.points = points
        self.k = len(points[0]) # Number of dimensions
        self.root = self.build(points)
        self.visualize = visualize

    def build(self, points, depth=0):
        if not len(points):
            return None

        # Alternate between dimensions
        axis = depth % self.k

        # Sort points and choose median as pivot element
        points.sort(key=lambda x: x[axis])
        median = len(points) // 2

        # Create node and construct subtrees
        return KDNode(
            point=points[median],
            left=self.build(points[:median], depth + 1),
            right=self.build(points[median + 1:], depth + 1)
        )
    # starting at root we do a reursive search into the tree
    def points_inside_rectangle(self, rect_min, rect_max):
        inside_points = []

        def recursive_search(node, depth=0):
            if node is None:
                return

            axis = depth % self.k
            
            if rect_min[axis] <= node.point[axis] <= rect_max[axis]:
                if all(rect_min[i] <= node.point[i] <= rect_max[i] for i in range(self.k)):
                    inside_points.append(node.point)

            if rect_min[axis] <= node.point[axis]:
                recursive_search(node.left, depth + 1)
            if rect_max[axis] >= node.point[axis]:
                recursive_search(node.right, depth + 1)

        recursive_search(self.root)
        if self.visualize:
            self.plot_kd_tree_and_rectangle(inside_points, rect_min, rect_max)

        return inside_points
    
    def plot_kd_tree_and_rectangle(self, inside_points, rect_min, rect_max):
    
        

        # Plot KD tree points in blue
        kd_tree_points_x, kd_tree_points_y = zip(*self.points)
        plt.scatter(kd_tree_points_x, kd_tree_points_y, c='blue', label='KD Tree Points')
    
        # Plot points inside the rectangle in red
        inside_points_x, inside_points_y = zip(*inside_points)
        plt.scatter(inside_points_x, inside_points_y, c='red', label='Inside Rectangle')


        # Plot the rectangle in green lines
        plt.gca().add_patch(plt.Rectangle(rect_min, rect_max[0] - rect_min[0], rect_max[1] - rect_min[1], fill=False, color='green', linewidth=2, label='Rectangle'))

        plt.xlabel('X-axis')
        plt.ylabel('Y-axis')
        plt.legend()
        plt.title('KD Tree Points and Rectangle')
        plt.grid(True)
        plt.show()
    



if __name__ == '__main__':

    np.random.seed(0)
    points = np.random.randint(-100, 101, size=(50, 2))
    points = [tuple(point) for point in points]
    kdtree = KDTree(points)
    rect_min = (3, 2)
    rect_max = (8, 5)
    inside_points = kdtree.points_inside_rectangle(rect_min, rect_max)
    print("Points inside the rectangle:", inside_points)
