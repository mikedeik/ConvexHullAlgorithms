from UtilityFunctions import generatePoints
from polygon import Point, Polygon, Edge, doEdgesIntersect, plotPolygon, intersect, ccw
from collections import deque
import time 
import matplotlib.pyplot as plt 

points = generatePoints(100)

# points = [Point(0,0), Point(5,2), Point(4,7), Point(8,10) , Point(3,2), Point(7,3), Point(1,10)]


class incrementalAlgorithm:

    def __init__(self, points) -> None:
        self.points = points
        self.convexHull = Polygon()

        # for i in range(3):
        #     self.convexHull.addPoint(self.points[i])

        if not ccw(self.points[0], self.points[1], self.points[2]):
            # Add the first three points
            self.convexHull.addPoint(self.points[0])
            self.convexHull.addPoint(self.points[1])
            self.convexHull.addPoint(self.points[2])
        else :
            # Add the first three points
            self.convexHull.addPoint(self.points[0])
            self.convexHull.addPoint(self.points[2])
            self.convexHull.addPoint(self.points[1])

        self.figure, self.ax = plt.subplots()
        self.plotPoints(self.points)
        self.plotPolygon(self.convexHull)
        plt.show(block=False)  # Show the plot without blocking

    def plotPoints(self, points):
        x = [point._x for point in points]
        y = [point._y for point in points]
        self.ax.plot(x, y, marker='o', color='r', linestyle='')

    def plotPolygon(self, polygon):
        x = [point._x for point in polygon.getVertices()]
        y = [point._y for point in polygon.getVertices()]
        x.append(x[0])  # Close the polygon
        y.append(y[0])
        self.ax.clear()
        self.plotPoints(self.points)  # Plot points continuously
        self.ax.plot(x, y, marker='o', linestyle='-', color='b')
        self.ax.set_aspect('equal', adjustable='datalim')
        self.figure.canvas.flush_events()  # Update the plot

    def findRedEdges(self, prev_poimt, new_point):

        purple_start: Point = None
        purple_end: Point = None
        # change user
        # index of the previous point
        index = self.convexHull.getVertices().index(prev_poimt)
        
        # perform a bfs sarting from previous point
        visited = [False] * len(self.convexHull.getEdges())
        redEdges = []
        queue = deque()

        queue.append(index)
        visited[index] = True

        while queue:
            current_index = queue.popleft()
            edge_to_check: Edge = self.convexHull.getEdges()[current_index]

            left_edge = Edge(edge_to_check.start(), new_point)
            right_edge = Edge(new_point, edge_to_check.end())

            

            intersection = False
            for edge in self.convexHull.getEdges():
                
                if edge == edge_to_check:
                    continue

                if new_point == Point(-27,27):
                    print(f'checking edge {edge} with edge {left_edge} : {doEdgesIntersect(edge, left_edge)}')
                    print(f'checking edge {edge} with edge {right_edge} : {doEdgesIntersect(edge, right_edge)}')
                    print("+++++++")
                
                if intersect(edge, left_edge) or intersect(edge, right_edge):
                    intersection = True
                    break
            
            if not intersection:
                if new_point == Point(-27,27):
                    print(f'adding edge with index {current_index}')
                redEdges.append(current_index)
            
            # print(f'current red edges {redEdges})

            # time.sleep(3)

            # Find neighbors (adjacent elements) and visit them
            for neighbor_index in [current_index - 1, current_index + 1]:
                if 0 <= neighbor_index < len(self.convexHull.getVertices()) and not visited[neighbor_index]:
                    queue.append(neighbor_index)
                    visited[neighbor_index] = True

        print(redEdges)
        print(self.convexHull.getEdges())

        if len(redEdges) == len(self.convexHull.getEdges()):
            return self.convexHull.getVertices()[0] , self.convexHull.getVertices()[-1]
        purple_start = self.convexHull.getEdges()[min(redEdges)].start()
        purple_end = self.convexHull.getEdges()[max(redEdges)].end()

        print(f'{purple_start} ==== {purple_end}')
        return purple_start, purple_end
        # return redEdges


    
    def createConvexHull(self):

        for index in range(3, len(self.points)):
            print(f"=========== Iteration {index} =================")
            purple_start, purple_end = self.findRedEdges(self.points[index - 1], self.points[index])

            purple_start_index = self.convexHull.getVertices().index(purple_start)
            purple_end_index = self.convexHull.getVertices().index(purple_end)
            print(f'start index : {purple_start_index + 1} , end index : {purple_end_index}')
            
            if purple_end_index == 0:
                purple_end_index = len(self.convexHull.getVertices())

            print(f'new start index : {purple_start_index + 1} ,new end index : {purple_end_index}')
            for i in range(purple_start_index + 1, purple_end_index):
                print(f"removing point at position {i}")
                self.convexHull.removeVertice(self.convexHull.getVertices()[purple_start_index + 1])

            # plotPolygon(self.convexHull, self.points)
            # before adding 
            print(self.convexHull.getVertices())
            print(self.convexHull.getEdges())

            self.convexHull.addPointAtIndex(self.points[index], purple_start_index + 1)

            # after adding 
            print(self.convexHull.getVertices())
            print(self.convexHull.getEdges())
            print("==============================")
            # if index == 4 :
            #     break

            self.plotPolygon(self.convexHull)
            plt.pause(0.05)  # Pause briefly to update the plot
            
            
        plotPolygon(self.convexHull, self.points)
        



    def getConvexHull(self):
        return self.convexHull




points.sort()

# points = []
# items = [(-99,-29), (-97,-42), (-96,-31), (-94,-96), (-78,-76), (-77,-22), (-77,96), (-74,-7), (-73,47), (-73,71), (-71,-10), (-70,93), (-67,66), (-63,-65), (-50,54), (-43,32), (-38,-72), (-28,61), (-26,60), (-25,-9), (-13,-9), (-12,-45), (-12,66), (-5,96), (-1,-88), (2,-50), (4,70), (11,54), (16,-78), (21,-67), (23,-84), (30,9), (34,12), (48,-48), (50,-62), (50,-45), (53,-76), (56,-48), (56,-26), (62,56), (65,40), (66,99), (68,-96), (70,-5), (71,-72), (74,-89), (76,-65), (87,77), (87,87), (96,-65)]
# for item in items:
#     points.append(Point(item[0], item[1]))

print(points)

CH = incrementalAlgorithm(points)

CH.createConvexHull()


print(CH.getConvexHull())

# print(CH)