from polygon import Point
import random


def generatePoints(__num: int ) -> list:

    points = []
    for i in range(__num):

        x = random.randint(-1000,1000)
        y = random.randint(-1000,1000)

        if Point(x,y) in points:
            __num = __num+1
            continue

        points.append(Point(x,y))

    return points
    

    