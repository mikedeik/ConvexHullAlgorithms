import matplotlib.pyplot as plt

class Point:
    def __init__(self, x, y):
        self._x = x
        self._y = y

    def __str__(self) -> str:
        return f'({self._x},{self._y})'
    
    def __repr__(self):
        return str(self)
    
    def __eq__(self, __value: object) -> bool:
        if isinstance(__value, Point):
            return self._x == __value._x and self._y == __value._y
        return False
    
    def __hash__(self) -> int:
        return hash((self._x, self._y))
    
    def __lt__(self, __value: object) -> bool:

        if isinstance(__value, Point):
            if self._x == __value._x : 
                return self._y < __value._y 
            else : 
                return self._x < __value._x
        raise Exception(f"Can't compare {type(self)} and {type(__value)}")

class Edge:
    def __init__(self, _start: Point, _end: Point):
        self._start = _start
        self._end = _end
    
    def __str__(self) -> str:
        return f'{self._start} -> {self._end}'
    
    def __repr__(self):
        return str(self)
    
    def __eq__(self, __value: object) -> bool:
        if isinstance(__value, Edge):
            return self._start == __value._start and self._end == __value._end
        return False
    
    def start(self) -> Point:
        return self._start
    
    def end(self) -> Point:
        return self._end
    

def plotEdges(edge1, edge2):
    # Create a figure and axis for the plot
    fig, ax = plt.subplots()

    # Extract the x and y coordinates of the edges
    x_coords1 = [edge1._start._x, edge1._end._x]
    y_coords1 = [edge1._start._y, edge1._end._y]
    x_coords2 = [edge2._start._x, edge2._end._x]
    y_coords2 = [edge2._start._y, edge2._end._y]

    # Plot the edges
    ax.plot(x_coords1, y_coords1, label='Edge 1', marker='o')
    ax.plot(x_coords2, y_coords2, label='Edge 2', marker='o')

    # Set labels and leg_end
    ax.set_xlabel('X')
    ax.set_ylabel('Y')
    ax.legend()

    # Show the plot
    plt.show()


def plotPolygon(polygon, points):
    # Extract vertices and edges from the polygon
    vertices = polygon.getVertices()
    edges = polygon.getEdges()

    # Extract x and y coordinates of vertices
    x_coords = [point._x for point in points]
    y_coords = [point._y for point in points]

    # Plot all the points
    plt.scatter(x_coords, y_coords, color='red', label='Points')

    # Extract x and y coordinates of edges
    edge_x = []
    edge_y = []
    for edge in edges:
        edge_x.extend([edge._start._x, edge._end._x, None])
        edge_y.extend([edge._start._y, edge._end._y, None])

    # Plot the edges
    plt.plot(edge_x, edge_y, linestyle='-', color='blue', label='Polygon Edges')

    # Set labels and legend
    plt.xlabel('X')
    plt.ylabel('Y')
    plt.title('Polygon with Points and Edges')
    # plt.legend()
    plt.grid(True)

    # Show the plot
    plt.show()

def ccw(A: Point, B: Point, C: Point):
    return ((B._x * C._y - C._x * B._y) - (C._y * A._x - C._x * A._y) + (A._x * B._y - A._y * B._x)) > 0


# Return true if line segments edge1 and edge2 intersect
def intersect(edge1: Edge, edge2: Edge):
    start1, end1 = edge1.start(), edge1.end()
    start2, end2 = edge2.start(), edge2.end()

    # Check if one endpoint of one segment is equal to an endpoint of the other segment
    if start1 == start2 or start1 == end2 or end1 == start2 or end1 == end2:
        # Check if they are not extensions of each other
        if not (start1 == end2 and end1 == start2):
            return False

    return (
        ccw(start1, start2, end2) != ccw(end1, start2, end2) and
        ccw(start1, end1, start2) != ccw(start1, end1, end2)
    )


class Polygon:
    def __init__(self):
        self.vertices = []
        self.edges = []

    def getVertices(self):
        return self.vertices
    
    def getEdges(self):
        return [edge for edge in self.edges]


    def addPoint(self, point):
        if len(self.edges) >= 2:
            # Remove the edge between the previous last point and the first point
            self.edges.pop()
        if len(self.vertices) >= 1:
            # Add an edge between the previous point and the new point
            prev_point = self.vertices[-1]
            edge = Edge(prev_point, point)
            self.edges.append(edge)

        self.vertices.append(point)

        # Add an edge from the new point back to the _starting point
        if len(self.vertices) >= 2:
            edge = Edge(point, self.vertices[0])
            self.edges.append(edge)

    def addPointAtIndex(self, point, index):
        if index < 0 or index > len(self.vertices):
            raise ValueError("Invalid index")

        if index == len(self.vertices):
            # If index is equal to the length, add the point using the regular method
            self.addPoint(point)
        else:
            # Insert the point at the specified index
   
            # Update the edges array
            if index == 0:
                # If the point was inserted at the beginning, update edges accordingly
                edge1 = Edge(point, self.vertices[0])
                edge2 = Edge(self.vertices[-1], point)
            else:
                edge1 = Edge(point, self.vertices[index])
                edge2 = Edge(self.vertices[index - 1], point)
            self.vertices.insert(index, point)
            
            self.edges.insert(index, edge1)

            self.edges[index - 1] = edge2

    def removeVertice(self, point):
        if point not in self.vertices:
            return

        index = self.vertices.index(point)

        # Remove the point and corresponding edges
        self.vertices.pop(index)
        self.edges.pop(index)
        if index == 0:
            self.edges.pop()
        else:
            self.edges.pop(index - 1)

        # Reconnect the previous and next points with a new edge
        if len(self.vertices) >= 2:
            prev_index = (index - 1) % len(self.vertices)
            next_index = index % len(self.vertices)
            edge = Edge(self.vertices[prev_index], self.vertices[next_index])
            self.edges.insert(prev_index, edge)

    def getPreviousPoint(self, point: Point) -> Point:
        
        point_index = self.vertices.index(point)
        if point_index == 0:
            return None

        return self.vertices[point_index - 1]

    def getNextPoint(self, point: Point) -> Point:
        
        point_index = self.vertices.index(point)
        if point_index == len(self.vertices) - 1:
            return None
        return self.vertices[point_index + 1]            

    def __str__(self):
        vertices_str = ', '.join([f"({point._x}, {point._y})" for point in self.vertices])
        edges_str = ', '.join([f"({edge._start._x}, {edge._start._y}) -> ({edge._end._x}, {edge._end._y})" for edge in self.edges])
        return f"Vertices: [{vertices_str}]\nEdges: [{edges_str}]"

if __name__ == '__main__':
    # Example usage:
    polygon = Polygon()
    polygon.addPoint(Point(1.0, 1.0))
    polygon.addPoint(Point(2.0, 2.0))
    polygon.addPoint(Point(3.0, 3.0))

    polygon.addPointAtIndex(Point(1.5, 1.5), 1)
    print(polygon)
    polygon.addPointAtIndex(Point(4, 2), 0)
    
    edge1 = Edge(Point(2.0, 2.0) , Point(3.0,3.0))
    edge2 = Edge(Point(4.0, 1.5) , Point(3.0,3.0))
    edge3 = Edge(Point(4.0, 1.5) , Point(3.0,3.0))

    p = edge2.start()
    # print(doEdgesIntersect(edge1, edge2))
    plotEdges(edge1, edge2)

    print(polygon)

    polygon.removeVertice(Point(3.0,3.0))
    print(polygon)
