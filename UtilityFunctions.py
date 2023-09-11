from polygon import Point
import random


def generatePoints(__num: int ) -> list:

    points = []
    for i in range(__num):

        x = random.randint(-100,100)
        y = random.randint(-100,100)

        if Point(x,y) in points:
            __num = __num+1
            continue

        points.append(Point(x,y))

    return points
    

def generate_unique_points(num_points, min_x, max_x, min_y, max_y):
    unique_x_values = set()
    points = []

    while len(points) < num_points:
        x = random.uniform(min_x, max_x)
        y = random.uniform(min_y, max_y)

        if x not in unique_x_values:
            unique_x_values.add(x)
            points.append(Point(x, y))

    return points
    