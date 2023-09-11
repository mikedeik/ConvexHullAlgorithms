from polygon import Point, Polygon, Edge, plotPolygon, ccw
from UtilityFunctions import generatePoints, generate_unique_points

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

    bottomEdge = Edge(left_max, right_min)
        
    

    # Find the lower tangent of the two convex hulls
    while True:
        changed = False
        while True:
            next_left = left_hull.getNextPoint(left_max)
            if not next_left:
                break
            for left_ch_point in left_hull.getVertices():

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
        
    topEdge = Edge(left_max, right_min)
    print(topEdge)
    print(bottomEdge)

    # Merge the two convex hulls using the upper and lower tangents
    merged_hull = Polygon()

    left_stop_index = left_hull.getVertices().index(bottomEdge.start())
    left_start_index = left_hull.getVertices().index(topEdge.start())

    right_start_index = right_hull.getVertices().index(bottomEdge.end())
    right_stop_index = right_hull.getVertices().index(topEdge.end())

    for point in left_hull.getVertices()[:left_stop_index+1]:
        merged_hull.addPoint(point)
    
    for point in right_hull.getVertices()[right_start_index: right_stop_index + 1]:
        merged_hull.addPoint(point)

    for point in left_hull.getVertices()[left_start_index:]:
        merged_hull.addPoint(point)

    # for left_point in left_hull.getVertices():
        
    #     merged_hull.addPoint(left_point)
    #     if left_point == bottomEdge.start():
    #         for right_point in right_hull.getVertices():
    #             if right_point != bottomEdge.end():
    #                 continue
    #             merged_hull.addPoint(right_point)

    #             if right_point == topEdge.end():
    #                 break
        
    #     if left_point != topEdge.start():
    #         continue
    #     merged_hull.addPoint(left_point)
  
    # plotPolygon(merged_hull, points)
    # merged_hull.addEdge(Edge(left_max, right_min))
    # merged_hull.addEdge(Edge(right_min, left_max))

    return merged_hull

if __name__ == '__main__':
    # Example usage:
    points = generate_unique_points(20, -100, 100, -100, 100)

    convex_hull = divide_and_conquer_convex_hull(points)
    print("Convex Hull:")
    print(convex_hull)
    plotPolygon(convex_hull, points)
