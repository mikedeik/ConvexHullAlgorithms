from polygon import Point, Polygon, Edge, plotPolygon, ccw

def divide_and_conquer_convex_hull(points):
    if len(points) <= 3:
        # For a small number of points, return the convex hull directly
        hull = Polygon()
        for point in points:
            hull.addPoint(point)
        return hull

    # Sort the points by x-coordinate
    points.sort()

    # Divide the points into two halves
    mid = len(points) // 2
    left_half = points[:mid]
    right_half = points[mid:]

    # Recursively compute the convex hulls of the two halves
    left_hull = divide_and_conquer_convex_hull(left_half)
    right_hull = divide_and_conquer_convex_hull(right_half)

    # Merge the two convex hulls
    return merge_convex_hulls(left_hull, right_hull)

def merge_convex_hulls(left_hull: Polygon, right_hull: Polygon):
    # Find the rightmost point in the left convex hull and the leftmost point in the right convex hull
    left_max = max(left_hull.getVertices())
    right_min = min(right_hull.getVertices())

    while True:
        changed = False
        # Find the upper tangent of the two convex hulls
        while True:
            prev_left = left_hull.getPreviousPoint(left_max)
            if not prev_left:
                break
            if not ccw(prev_left, left_max, right_min):
                left_max = prev_left
                changed = True
            else:
                break
            
        while True:
            next_right = right_hull.getNextPoint(right_min)
            if not next_right:
                break
            if not ccw(left_max, right_min, next_right):
                right_min = next_right
                changed = True
            else:
                break
        
        if not changed:
            break

    topEdge = (left_max, right_min)
        
    

    # Find the lower tangent of the two convex hulls
    while True:
        changed = False
        while True:
            next_left = left_hull.getNextPoint(left_max)
            if not next_left:
                break
            if ccw(left_max, right_min, next_left):
                left_max = next_left
                changed = True
            else:
                break
        while True:
            prev_right = right_hull.getPreviousPoint(right_min)
            if not prev_right:
                break
            if ccw(prev_right, right_min, left_max):
                right_min = prev_right
                changed = True
            else:
                break
        
        if not changed:
            break
        
    bottomEdge = (left_max, right_min)
    print(topEdge)
    print(bottomEdge)

    # Merge the two convex hulls using the upper and lower tangents
    merged_hull = Polygon()
    merged_hull.vertices = left_hull.vertices + right_hull.vertices
    merged_hull.edges = left_hull.edges + right_hull.edges

    # merged_hull.addEdge(Edge(left_max, right_min))
    # merged_hull.addEdge(Edge(right_min, left_max))

    return merged_hull

if __name__ == '__main__':
    # Example usage:
    points = [
        Point(1, 1),
        Point(2, 5),
        Point(3, 3),
        Point(0, 2),
        Point(8, 0),
        Point(4, 1),
    ]

    convex_hull = divide_and_conquer_convex_hull(points)
    print("Convex Hull:")
    print(convex_hull)
    plotPolygon(convex_hull, points)
