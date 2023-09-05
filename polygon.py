import matplotlib.pyplot as plt

class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __str__(self) -> str:
        return f'({self.x},{self.y})'
    
    def __repr__(self):
        return str(self)
    
    def __eq__(self, __value: object) -> bool:
        if isinstance(__value, Point):
            return self.x == __value.x and self.y == __value.y
        return False
    
    def __hash__(self) -> int:
        return hash((self.x, self.y))
    
    def __lt__(self, __value: object) -> bool:

        if isinstance(__value, Point):
            if self.x == __value.x : 
                return self.y < __value.y 
            else : 
                return self.x < __value.x
        raise Exception(f"Can't compare {type(self)} and {type(__value)}")

class Edge:
    def __init__(self, start, end):
        self.start = start
        self.end = end
    
    def __str__(self) -> str:
        return f'{self.start} -> {self.end}'
    
    def __repr__(self):
        return str(self)
    
    def __eq__(self, __value: object) -> bool:
        if isinstance(__value, Edge):
            return self.start == __value.start and self.end == __value.end
        return False
    

def plotEdges(edge1, edge2):
    # Create a figure and axis for the plot
    fig, ax = plt.subplots()

    # Extract the x and y coordinates of the edges
    x_coords1 = [edge1.start.x, edge1.end.x]
    y_coords1 = [edge1.start.y, edge1.end.y]
    x_coords2 = [edge2.start.x, edge2.end.x]
    y_coords2 = [edge2.start.y, edge2.end.y]

    # Plot the edges
    ax.plot(x_coords1, y_coords1, label='Edge 1', marker='o')
    ax.plot(x_coords2, y_coords2, label='Edge 2', marker='o')

    # Set labels and legend
    ax.set_xlabel('X')
    ax.set_ylabel('Y')
    ax.legend()

    # Show the plot
    plt.show()


def doEdgesIntersect(edge1, edge2):
    # Calculate the slopes of the edges
    slope1 = (edge1.end.y - edge1.start.y) / (edge1.end.x - edge1.start.x) if edge1.end.x != edge1.start.x else float('inf')
    slope2 = (edge2.end.y - edge2.start.y) / (edge2.end.x - edge2.start.x) if edge2.end.x != edge2.start.x else float('inf')

    # Check if the slopes are equal (parallel lines)
    if slope1 == slope2:
        return False

    # Calculate the intersection point
    intersection_x = (
        (edge2.start.y - edge1.start.y) + (slope1 * edge1.start.x - slope2 * edge2.start.x)
    ) / (slope1 - slope2)

    intersection_y = slope1 * (intersection_x - edge1.start.x) + edge1.start.y

    # Check if the intersection point lies within both line segments
    def isBetween(a, b, c):
        return a <= b <= c or c <= b <= a

    if (
        isBetween(edge1.start.x, intersection_x, edge1.end.x)
        and isBetween(edge1.start.y, intersection_y, edge1.end.y)
        and isBetween(edge2.start.x, intersection_x, edge2.end.x)
        and isBetween(edge2.start.y, intersection_y, edge2.end.y)
        and not (intersection_x == edge1.start.x and intersection_y == edge1.start.y)
        and not (intersection_x == edge1.end.x and intersection_y == edge1.end.y)
        and not (intersection_x == edge2.start.x and intersection_y == edge2.start.y)
        and not (intersection_x == edge2.end.x and intersection_y == edge2.end.y)
    ):
        return True
    return False


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

        # Add an edge from the new point back to the starting point
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
            

    def __str__(self):
        vertices_str = ', '.join([f"({point.x}, {point.y})" for point in self.vertices])
        edges_str = ', '.join([f"({edge.start.x}, {edge.start.y}) -> ({edge.end.x}, {edge.end.y})" for edge in self.edges])
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


    print(doEdgesIntersect(edge1, edge2))
    plotEdges(edge1, edge2)

    print(polygon)

    polygon.removeVertice(Point(3.0,3.0))
    print(polygon)
