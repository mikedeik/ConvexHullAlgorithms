

# from .ConvexHullAlgorithms.DivideAndConquer import divide_and_conquer_convex_hull
from Incremental import incrementalAlgorithm
from QuickHull import QuickHull, plotQuickHull
from GiftWrapping import GiftWrap
from UtilityFunctions import generatePoints
from ConvexHull3D import quichHull3D
from KDTree import KDTree
import argparse
import time
import numpy as np


def main():

    parser = argparse.ArgumentParser(description="Usage: python3 -a [algorithm] -n [Num_of_Points] [-v] (otpional)")
    
    parser.add_argument('-a', '--algorithm', type=str, required=True, help='Name of the Algorithm (valid options: incremental, giftwrap, quickhull, divide, all)')
    parser.add_argument('-n', '--num_of_points', type=int, required=True, help='Number of Points')
    parser.add_argument('-v', '--visualize', action='store_true', help='Enable visualization')

    args = parser.parse_args()

    algortihm = args.algorithm
    visualize = args.visualize
    num_of_points = args.num_of_points

    points = generatePoints(num_of_points)

    execution_times = {
        'incremental': 0,
        'giftwrap': 0,
        'quickhull': 0,
        'devide': 0,
    }
    
    if algortihm == 'incremental':
        incremental = incrementalAlgorithm(points=points,visualize=visualize)
        incremental.createConvexHull()
        print(incremental.getConvexHull())
    elif algortihm == 'giftwrap':
        giftwrap = GiftWrap(points=points,visualize=visualize)
        giftwrap.createConvexHull()

    elif algortihm == 'quickhull':
        np.random.seed(0)
        points = np.random.randint(-100, 101, size=(num_of_points, 2))
        quickhull = QuickHull(points=points)
        if visualize:
            plotQuickHull(points, quickhull)
    elif algortihm == 'devide':
        return
    
    elif algortihm == 'kdtree':
        np.random.seed(0)
        points = np.random.randint(-100, 101, size=(num_of_points, 2))
        # need to change np array to tuples for KD Tree
        points = [tuple(point) for point in points]
        rect_min = (-50, -20)
        rect_max = (75, 25)
        kd = KDTree(points, visualize)
        inside_points = kd.points_inside_rectangle(rect_min, rect_max)
        print(inside_points)
    
    elif algortihm == 'quickhull3D':
        quichHull3D(num_of_points, visualize)

    elif algortihm == 'all':

        start_time = time.time()
        incremental = incrementalAlgorithm(points=points,visualize=False)
        incremental.createConvexHull()
        # print(incremental.getConvexHull())
        end_time = time.time()

        execution_times['incremental'] = end_time - start_time

        start_time = time.time()
        giftwrap = GiftWrap(points=points,visualize=False)
        end_time = time.time()

        execution_times['giftwrap'] = end_time - start_time

        np.random.seed(0)
        points = np.random.randint(-100, 101, size=(num_of_points, 2))

        start_time = time.time()
        quickhull = QuickHull(points=points)
        end_time = time.time()
        execution_times['quickhull'] = end_time - start_time

        print(execution_times)












if __name__ == '__main__':

    main()
