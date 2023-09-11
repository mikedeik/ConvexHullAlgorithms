

# from .ConvexHullAlgorithms.DivideAndConquer import divide_and_conquer_convex_hull
from Incremental import incrementalAlgorithm
from QuickHull import QuickHull, plotQuickHull
from GiftWrapping import GiftWrap
from UtilityFunctions import generatePoints
import argparse
import time
import numpy as np


def main():

    parser = argparse.ArgumentParser(description="Usage: python3 -a [algorithm] [-v] (otpional)")
    
    parser.add_argument('-a', '--algorithm', type=str, required=True, help='Name of the Algorithm (valid options: incremental, giftwrap, quickhull, divide, all)')
    parser.add_argument('-v', '--visualize', action='store_true', help='Enable visualization')

    args = parser.parse_args()

    algortihm = args.algorithm
    visualize = args.visualize

    points = generatePoints(50)

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
    # TODO add visualize
    elif algortihm == 'quickhull':
        quickhull = QuickHull(points=points)
        if visualize:
            plotQuickHull(points, quickhull)
    elif algortihm == 'devide':
        return

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
        points = np.random.randint(-100, 101, size=(50, 2))

        start_time = time.time()
        quickhull = QuickHull(points=points)
        end_time = time.time()
        execution_times['quickhull'] = end_time - start_time

        print(execution_times)












if __name__ == '__main__':

    main()
