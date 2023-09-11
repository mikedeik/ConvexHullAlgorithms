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
    points = generatePoints(20)

    GF = GiftWrap(points, True)
    convex_hull = GF.getConvexHull()

    print("Convex Hull:")
    print(convex_hull)
    # plotPolygon(convex_hull, points)
