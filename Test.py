import random
import pygame
from pygame.locals import *

# Constants for the display
WIDTH, HEIGHT = 500, 500
MINIMAP_SIZE = 100
ENEMY_RADIUS = 5

# Initialize pygame
pygame.init()

# Create the display window
screen = pygame.display.set_mode((WIDTH, HEIGHT))
screen_center = (WIDTH // 2, HEIGHT // 2)  # Center of the screen
pygame.display.set_caption("Minimap with Enemies")

class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __str__(self) -> str:
        return f'({self.x},{self.y})'

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
    return Point(random.uniform(-200, 200), random.uniform(-200, 200))

def generateEnemies(num):
    enemies = []
    for i in range(num):
        enemies.append(generate_random_enemy())
    return enemies

def draw_minimap(location, enemies, screen, screen_center):
    minimap_rect = pygame.Rect(
        screen_center[0] - MINIMAP_SIZE // 2,
        screen_center[1] - MINIMAP_SIZE // 2,
        MINIMAP_SIZE,
        MINIMAP_SIZE,
    )
    pygame.draw.rect(screen, (0, 0, 0), minimap_rect, 2)

    for enemy in enemies:
        x = int(screen_center[0] + enemy.x)
        y = int(screen_center[1] + enemy.y)

        # Check if the enemy is inside the minimap
        if (
            screen_center[0] - MINIMAP_SIZE // 2 <= x <= screen_center[0] + MINIMAP_SIZE // 2
            and screen_center[1] - MINIMAP_SIZE // 2 <= y <= screen_center[1] + MINIMAP_SIZE // 2
        ):
            pygame.draw.circle(screen, (255, 0, 0), (x, y), ENEMY_RADIUS)  # Red if inside minimap
        else:
            pygame.draw.circle(screen, (0, 0, 255), (x, y), ENEMY_RADIUS)  # Blue if outside minimap


def main():
    kd_tree = KDTree()
    minimap_center = Point(0,-200)
    enemies = generateEnemies(100)
    
    for enemy in enemies:
        kd_tree.insert(enemy)

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == QUIT:
                running = False

        # Handle key presses
        keys = pygame.key.get_pressed()
        if keys[K_w]:
            minimap_center.y += 0.1
            print(minimap_center)
            draw_minimap(minimap_center, enemies, screen, screen_center)
        if keys[K_s]:
            minimap_center.y -= 0.1
            draw_minimap(minimap_center, enemies, screen, screen_center)
        if keys[K_a]:
            minimap_center.x -= 0.1
            draw_minimap(minimap_center, enemies, screen, screen_center)
        if keys[K_d]:
            minimap_center.x += 0.1
            draw_minimap(minimap_center, enemies, screen, screen_center)

        screen.fill((255, 255, 255))
        
        # new_enemy = generate_random_enemy()
        # kd_tree.insert(new_enemy)
        enemies = kd_tree.search(Point(minimap_center.x - MINIMAP_SIZE / 2, minimap_center.y - MINIMAP_SIZE / 2),
                                 Point(minimap_center.x + MINIMAP_SIZE / 2, minimap_center.y + MINIMAP_SIZE / 2))
        
        draw_minimap(minimap_center, enemies, screen, screen_center)

        pygame.display.flip()

    pygame.quit()

if __name__ == '__main__':
    main()
