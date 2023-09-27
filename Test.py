import random
import pygame
from pygame.locals import *

# Constants for the display
WIDTH, HEIGHT = 800, 600
MINIMAP_SIZE = 200
ENEMY_RADIUS = 5

# Initialize pygame
pygame.init()

# Create the display window
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Minimap with Enemies")

class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y

class KDNode:
    def __init__(self, point, left=None, right=None):
        self.point = point
        self.left = left
        self.right = right

class KDTree:
    def __init__(self):
        self.root = None

    def insert(self, point, depth=0, node=None):
        if self.root is None:
            self.root = KDNode(point)
        else:
            if node is None:
                node = self.root
            axis = depth % 2  # Assuming 2D space, change for 3D
            if point.x < node.point.x:
                if node.left is None:
                    node.left = KDNode(point)
                else:
                    self.insert(point, depth + 1, node.left)
            else:
                if node.right is None:
                    node.right = KDNode(point)
                else:
                    self.insert(point, depth + 1, node.right)

    def search(self, rect_min, rect_max):
        points = []
        stack = [(self.root, 0)]  # Initialize stack with root node and depth

        while stack:
            node, depth = stack.pop()
            if node is None:
                continue

            axis = depth % 2  # Assuming 2D space, change for 3D

            if (
                rect_min.x <= node.point.x <= rect_max.x
                and rect_min.y <= node.point.y <= rect_max.y
            ):
                points.append(node.point)

            if rect_min.x <= node.point.x:
                stack.append((node.left, depth + 1))
            if rect_max.x >= node.point.x:
                stack.append((node.right, depth + 1))

        return points

def generate_random_enemy():
    return Point(random.uniform(-100, 100), random.uniform(-100, 100))

def draw_minimap(center, enemies, screen):
    minimap_rect = pygame.Rect(WIDTH - MINIMAP_SIZE - 10, 10, MINIMAP_SIZE, MINIMAP_SIZE)
    pygame.draw.rect(screen, (0, 0, 0), minimap_rect, 2)

    for enemy in enemies:
        x = int(center.x + enemy.x * MINIMAP_SIZE / 200)
        y = int(center.y + enemy.y * MINIMAP_SIZE / 200)
        pygame.draw.circle(screen, (255, 0, 0), (x, y), ENEMY_RADIUS)

def main():
    kd_tree = KDTree()
    minimap_center = Point(WIDTH - MINIMAP_SIZE / 2 - 10, MINIMAP_SIZE / 2 + 10)
    enemies = [Point(100,20),Point(50,50),Point(85,100),Point(200,200),Point(150,300),Point(500,210),Point(400,20)]

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == QUIT:
                running = False

        # Handle key presses
        keys = pygame.key.get_pressed()
        if keys[K_w]:
            print(f'key {keys[K_w] } pressed')
            minimap_center.y -= 1
            draw_minimap(minimap_center, enemies, screen)
        if keys[K_s]:
            minimap_center.y += 1
            draw_minimap(minimap_center, enemies, screen)
        if keys[K_a]:
            minimap_center.x -= 1
            draw_minimap(minimap_center, enemies, screen)
        if keys[K_d]:
            minimap_center.x += 1
            draw_minimap(minimap_center, enemies, screen)

        screen.fill((255, 255, 255))
        
        new_enemy = generate_random_enemy()
        kd_tree.insert(new_enemy)
        enemies = kd_tree.search(Point(minimap_center.x - MINIMAP_SIZE / 2, minimap_center.y - MINIMAP_SIZE / 2),
                                 Point(minimap_center.x + MINIMAP_SIZE / 2, minimap_center.y + MINIMAP_SIZE / 2))
        
        draw_minimap(minimap_center, enemies, screen)

        pygame.display.flip()

    pygame.quit()

if __name__ == '__main__':
    main()
