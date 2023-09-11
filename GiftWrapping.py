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
    # items = [(167,-965), (143,-887), (-630,381), (-155,-40), (-15,-287), (714,788),(-1000,-400),(-1000,400), (-1000,989), (-931,324), (332,488), (810,-269), (457,-114), (-438,-533), (-982,-729), (191,-112), (543,-664), (277,51),(1000,347), (-581,978), (-342,308), (-325,720), (358,-227), (-940,807), (-910,462), (-875,-147), (-757,477), (519,-8), (860,916), (-995,-50), (451,512), (-509,-559), (382,-263), (807,96), (740,823), (-757,958), (-747,-450), (112,-972), (795,275), (-946,-829), (-256,-733), (239,-582), (64,211), (-896,727), (-715,673), (-84,987), (15,-363), (-53,-85), (-838,278), (619,-840), (-140,-923), (924,-697), (329,-630), (-516,756), (43,16), (185,483), (-158,-877), (-475,-823), (182,-151), (-521,583), (132,-896), (22,872), (379,-369), (109,-152), (264,-448), (-807,-851), (-353,-588), (-956,48), (-827,521), (-978,703), (425,980), (-45,770), (-832,414), (-88,-138), (388,-364), (305,-761), (507,-541), (773,-368), (-573,-19), (969,-968), (819,-707), (653,-483), (498,822), (-299,156), (445,-654), (-723,107), (759,-97), (171,-86), (-580,-999), (-302,856), (-442,868), (49,-690), (791,-223), (-903,518), (-462,-915), (81,816), (-618,-269), (-837,814), (617,-823), (343,145), (1000,-50), (1000,978),(-926,-459), (886,554), (-448,52), (774,-603)]
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
