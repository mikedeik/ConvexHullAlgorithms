import numpy as np
from UtilityFunctions import generatePoints

class KDNode:
    def __init__(self, point, left=None, right=None):
        self.point = point
        self.left = left
        self.right = right

class KDTree:
    def __init__(self, points):
        self.k = len(points[0])  # Number of dimensions
        self.root = self.build(points)

    def build(self, points, depth=0):
        if not points:
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
        return inside_points

if __name__ == '__main__':
    # Example usage:
    points = [(2, 3), (5, 4), (9, 6),(3.2, 4), (4, 7), (8, 1), (7, 2), (8,5), (10, 7)]
    kdtree = KDTree(points)
    rect_min = (3, 2)
    rect_max = (8, 5)
    inside_points = kdtree.points_inside_rectangle(rect_min, rect_max)
    print("Points inside the rectangle:", inside_points)
