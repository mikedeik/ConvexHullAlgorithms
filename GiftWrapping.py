from UtilityFunctions import generatePoints
from polygon import Point, Polygon, Edge, plotPolygon, ccw
import matplotlib.pyplot as plt

class GiftWrap:

    def __init__(self, points, visualize = False) -> None:
        self.points = points
        self.visualize = visualize
        self.convexHull = self.createConvexHull()

    def findFirstPoint(self):
        return min(self.points)

    def createConvexHull(self):
        if len(self.points) < 3:
            return None  # Convex hull is not possible with less than 3 points

        first_point = self.findFirstPoint()
        current_point = first_point
        convex_hull = Polygon()
        convex_hull.addPoint(first_point)
        
        if self.visualize:
            plt.figure(figsize=(8, 6))
            plt.ion()  # Turn on interactive mode

        for i in range(len(self.points)):
            next_point = None
            for point in self.points:
                if point == current_point:
                    continue
                if next_point is None or not ccw(current_point, next_point, point):
                    next_point = point

            if next_point == first_point:
                break
            else:
                convex_hull.addPoint(next_point)
                current_point = next_point
            if self.visualize:
                # Plot the current state
                plt.clf()
                plt.title('Convex Hull Incremental Construction')
                plotPolygon(convex_hull, self.points)
                plt.scatter(next_point._x, next_point._y, color='red', label='Current Point')
                plt.pause(0.5)  # Pause to visualize each step
        if self.visualize:
            plt.ioff()  # Turn off interactive mode when finished
            plt.show()  # Display the final plot

        return convex_hull
    
    def getConvexHull(self):
        return self.convexHull

if __name__ == '__main__':
    points = generatePoints(100)
    # points = []
    # items = [(-41,-20), (49,47), (9,-27), (31,-7), (26,-19), (39,-40), (-42,1), (30,44), (-24,29), (-6,19), (34,-49), (11,28), (32,-2), (22,-35), (35,0), (-25,38), (-18,-9), (45,-1), (12,14), (47,9), (-9,25), (24,-13), (49,23), (-12,30), (46,-6), (42,42), (-34,42), (3,28), (-30,-4), (12,-48), (-18,19), (-23,-26), (-40,45), (-9,-11), (5,-30), (12,-33), (8,-41), (11,49), (-37,47), (0,34), (23,-45), (13,-15), (-42,20), (44,-41), (42,32), (17,-3), (-28,-11), (26,-37), (-23,20), (-18,4), (8,38), (39,41), (26,-33), (26,-34), (-49,-18), (1,-32), (46,29), (-41,11), (17,-48), (49,-13), (-49,-48), (4,28), (-25,-46), (26,-12), (42,-34), (-40,41), (-30,-45), (-34,8), (17,-6), (-47,-9), (-17,-15), (35,18), (18,-17), (16,-5), (-35,22), (30,-44), (-14,-30), (-46,-11), (-48,10), (42,48), (32,25), (14,12), (12,21), (-7,-28), (7,-43), (47,1), (-19,4), (32,-36), (-25,6), (35,-40), (-8,-11), (-32,-48), (-36,17), (12,19), (-23,12), (-25,44), (49,9), (-42,15), (-48,-25), (-41,36)]
    # for point in items:
    #     points.append(Point(point[0],point[1]))
    
    # points.sort()
    # print(points)
    
    print(points)
    GF = GiftWrap(points, True)
    convex_hull = GF.getConvexHull()

    print("Convex Hull:")
    print(convex_hull)
    # plotPolygon(convex_hull, points)
