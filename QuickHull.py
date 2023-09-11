from scipy.spatial import ConvexHull
import numpy as np
import time

def QuickHull(points):
    
    # Compute the convex hull
    hull = ConvexHull(points)

    # Print the vertices (corners) of the convex hull
    print("Vertices (Corners) of Convex Hull:")
    for vertex in hull.vertices:
        print(f"({points[vertex][0]}, {points[vertex][1]})")

    # Print the edges of the convex hull (optional)
    print("\nEdges of Convex Hull:")
    for simplex in hull.simplices:
        print(f"({points[simplex[0]][0]}, {points[simplex[0]][1]}) -> ({points[simplex[1]][0]}, {points[simplex[1]][1]})")

    return hull

# Visualize the convex hull (optional)
def plotQuickHull(points, hull):
    
    import matplotlib.pyplot as plt
    
    plt.figure(figsize=(8, 6))
    
    
    # Plot the edges of the convex hull in blue
    for simplex in hull.simplices:
        plt.plot(points[simplex, 0], points[simplex, 1], 'b-')
    
    # Plot the vertices (corners) in red
    plt.plot(points[:,0], points[:,1], 'ro', label='Vertices')
    
    plt.title('Quickhull Convex Hull')
    plt.xlabel('X')
    plt.ylabel('Y')
    plt.legend()
    plt.grid(True)
    
    # Show the plot
    plt.show()

if __name__ == '__main__':

    # Generate random integer points between -100 and 100
    np.random.seed(0)
    points = np.random.randint(-100, 101, size=(100, 2))
    
    hull = QuickHull(points)

    plotQuickHull(points, hull)