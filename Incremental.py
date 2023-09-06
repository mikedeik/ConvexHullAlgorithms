from UtilityFunctions import generatePoints
from polygon import Point, Polygon, Edge, doEdgesIntersect, plotPolygon
from collections import deque
import time 

points = generatePoints(10)


class incrementalAlgorithm:

    def __init__(self, points) -> None:
        self.points = points
        self.convexHull = Polygon()

        for i in range(3):
            self.convexHull.addPoint(self.points[i])

        plotPolygon(self.convexHull, self.points)

    def findRedEdges(self, prev_poimt, new_point):

        purple_start: Point = None
        purple_end: Point = None
        
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
                
                if edge == left_edge or edge == right_edge or edge == edge_to_check:
                    continue

                if doEdgesIntersect(edge, left_edge) or doEdgesIntersect(edge, right_edge):
                    intersection = True
                    break
            
            if not intersection:
                redEdges.append(current_index)
            
            # print(redEdges)

            # time.sleep(3)

            # Find neighbors (adjacent elements) and visit them
            for neighbor_index in [current_index - 1, current_index + 1]:
                if 0 <= neighbor_index < len(self.convexHull.getVertices()) and not visited[neighbor_index]:
                    queue.append(neighbor_index)
                    visited[neighbor_index] = True

        
        purple_start = self.convexHull.getEdges()[min(redEdges)].start()
        purple_end = self.convexHull.getEdges()[max(redEdges)].end()

        return purple_start, purple_end
        # return redEdges


    
    def createConvexHull(self):

        for index in range(3, len(self.points)):

            purple_start, purple_end = self.findRedEdges(self.points[index - 1], self.points[index])

            purple_start_index = self.convexHull.getVertices().index(purple_start)
            purple_end_index = self.convexHull.getVertices().index(purple_end)
            print(f'start index : {purple_start_index + 1} , end index : {purple_end_index - 1}')
            for i in range(purple_start_index + 1, purple_end_index):
                self.convexHull.removeVertice(self.convexHull.getVertices()[i])

            self.convexHull.addPointAtIndex(self.points[index], purple_end_index)

            plotPolygon(self.convexHull, self.points)
        



    def getConvexHull(self):
        return self.convexHull




sorted_points = points.sort()
print(points)

CH = incrementalAlgorithm(points)

CH.createConvexHull()


print(CH.getConvexHull())

# print(CH)