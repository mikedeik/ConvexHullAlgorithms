from UtilityFunctions import generatePoints
from polygon import Point, Polygon, Edge


points = generatePoints(50)



def incrementalConvexHull(points):
    def isRed(edge, visible_edges):
        return edge in visible_edges

    def findVisibleEdges(new_point, previous_point, current_polygon):
        visible_edges = []
        for edge in current_polygon.edges:
            if (
                not isRed(edge, visible_edges)
                and edge.start != previous_point
                and edge.end != previous_point
            ):
                if isEdgeVisible(new_point, edge, current_polygon.vertices):
                    visible_edges.append(edge)
        return visible_edges

    def isEdgeVisible(new_point, edge, vertices):
        line_of_sight = Edge(new_point, edge.start)
        for vertex in vertices:
            if vertex != new_point and vertex != edge.start:
                if isPointLeft(line_of_sight, vertex):
                    return False
        return True

    def isPointLeft(line, point):
        return (
            (line.end.x - line.start.x) * (point.y - line.start.y)
            - (line.end.y - line.start.y) * (point.x - line.start.x)
        ) > 0

    def insertVisibleEdges(new_point, visible_edges, current_polygon):
        for edge in visible_edges:
            index = current_polygon.edges.index(edge)
            current_polygon.edges.pop(index)
            current_polygon.edges.insert(
                index, Edge(new_point, edge.start))
            current_polygon.edges.insert(
                index + 1, Edge(new_point, edge.end))

    # Step 1: Sort the points lexicographically by decreasing x-coordinate
    points.sort(key=lambda point: (-point.x, point.y))

    # Step 2: Initialize the current polygon with the first three points
    current_polygon = Polygon()
    current_polygon.addPoint(points[0])
    current_polygon.addPoint(points[1])
    current_polygon.addPoint(points[2])

    # Step 3: Incrementally add the remaining points
    for i in range(3, len(points)):
        new_point = points[i]
        previous_point = current_polygon.vertices[-1]

        # Find visible edges and vertices (red edges and blue edges)
        visible_edges = findVisibleEdges(new_point, previous_point, current_polygon)
        blue_edges = [
            edge for edge in current_polygon.edges if edge not in visible_edges
        ]
        purple_vertices = set()
        for blue_edge in blue_edges:
            if blue_edge.start not in purple_vertices:
                purple_vertices.add(blue_edge.start)
            else:
                purple_vertices.remove(blue_edge.start)
        for blue_edge in blue_edges:
            if blue_edge.end not in purple_vertices:
                purple_vertices.add(blue_edge.end)
            else:
                purple_vertices.remove(blue_edge.end)

        # Insert new edges with the new point (update red edges)
        insertVisibleEdges(new_point, visible_edges, current_polygon)

        # Remove any vertices that are not endpoints of a red edge
        vertices_to_remove = []
        for vertex in current_polygon.vertices:
            if vertex not in purple_vertices:
                vertices_to_remove.append(vertex)
        for vertex in vertices_to_remove:
            current_polygon.removeVertice(vertex)

    return current_polygon


sorted_points = points.sort()
print(points)

CH = incrementalConvexHull(points)

print(CH)