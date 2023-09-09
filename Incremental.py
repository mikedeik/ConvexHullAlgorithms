from UtilityFunctions import generatePoints
from polygon import Point, Polygon, Edge, doEdgesIntersect, plotPolygon, intersect, ccw
from collections import deque
import time 
import matplotlib.pyplot as plt 



# points = [Point(0,0), Point(5,2), Point(4,7), Point(8,10) , Point(3,2), Point(7,3), Point(1,10)]


class incrementalAlgorithm:

    def __init__(self, points) -> None:
        self.points = points
        self.convexHull = Polygon()

        # for i in range(3):
        #     self.convexHull.addPoint(self.points[i])

        # Calculate the area of the first triangle
        area = (
            (self.points[1]._x - self.points[0]._x) * (self.points[2]._y - self.points[0]._y) -
            (self.points[2]._x - self.points[0]._x) * (self.points[1]._y - self.points[0]._y)
        )

        # if not ccw(self.points[0], self.points[1], self.points[2]):
        if area > 0 :
            # Add the first three points
            self.convexHull.addPoint(self.points[0])
            self.convexHull.addPoint(self.points[1])
            self.convexHull.addPoint(self.points[2])
        else :
            # Add the first three points
            self.convexHull.addPoint(self.points[0])
            self.convexHull.addPoint(self.points[2])
            self.convexHull.addPoint(self.points[1])

        print(self.convexHull.getVertices())
        

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
            print(f"=========== Iteration {index - 2} =================")
            purple_start, purple_end = self.findRedEdges(self.points[index - 1], self.points[index])

            purple_start_index = self.convexHull.getVertices().index(purple_start)
            purple_end_index = self.convexHull.getVertices().index(purple_end)
            print(f'start index : {purple_start_index + 1} , end index : {purple_end_index}')
            
            if purple_end_index == 0:
                purple_end_index = len(self.convexHull.getVertices())

            print(f'new start index : {purple_start_index + 1} ,new end index : {purple_end_index}')
            for i in range(purple_start_index + 1, purple_end_index):
                print(f"removing point at position {i}")
                print(f"point to be removed {self.convexHull.getVertices()[purple_start_index + 1]}")
                self.convexHull.removeVertice(self.convexHull.getVertices()[purple_start_index + 1])


            if len(self.convexHull.getVertices()) == 2 and not ccw(self.convexHull.getVertices()[0], self.convexHull.getVertices()[1], self.points[index]):
                print("this is the case")
                self.convexHull.addPoint(self.points[index])
            else:
                self.convexHull.addPointAtIndex(self.points[index], purple_start_index + 1)

            print("==============================")
            print(self.convexHull.getVertices())
            self.plotPolygon(self.convexHull)
            plt.pause(0.01)  # Pause briefly to update the plot
            # plt.pause(2) 
            # if index == 4: 
            #     break
            
            
        plotPolygon(self.convexHull, self.points)
        



    def getConvexHull(self):
        return self.convexHull


if __name__ == '__main__':

    for i in range(20):
        points = generatePoints(100)
        points.sort()

        # points = []
        # items = [(-100,-35), (-99,37), (-98,10), (-95,74), (-93,-30), (-91,-69), (-89,48), (-88,-39), (-86,-15), (-84,68), (-83,-43), (-83,24), (-82,-50), (-81,-89), (-81,1), (-81,68), (-80,-87), (-80,10), (-80,61), (-80,62), (-80,95), (-79,-16), (-79,85), (-75,95), (-69,-55), (-67,-59), (-65,37), (-64,92), (-63,-80), (-61,34), (-54,-52), (-51,44), (-49,-19), (-48,44), (-43,-89), (-41,-57), (-41,-38), (-38,-4), (-31,71), (-27,84), (-26,7), (-21,-21), (-17,86), (-15,94), (-8,-86), (-8,-81), (-7,-23), (-3,40), (-1,8), (1,-83), (1,-46), (2,5), (4,36), (6,-84), (9,-87), (11,34), (12,82), (14,74), (15,88), (17,-29), (21,99), (22,-31), (24,100), (27,36), (35,59), (36,-68), (37,18), (38,-97), (38,-53), (39,-52), (40,-20), (43,-85), (49,-65), (49,-51), (49,92), (50,96), (57,-72), (57,-23), (59,73), (61,-33), (61,1), (64,99), (66,-20), (70,3), (70,14), (76,69), (77,0), (80,-67), (81,-10), (83,-86), (84,-47), (84,62), (85,94), (86,36), (87,5), (88,96), (94,-54), (95,85), (98,-36)]
        # for item in items:
        #     points.append(Point(item[0], item[1]))

        print(points)

        CH = incrementalAlgorithm(points)

        CH.createConvexHull()


        print(CH.getConvexHull())

# print(CH)