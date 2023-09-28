import random
import pygame
from pygame.locals import *
from polygon import Point
from KDTree import KDTree
import numpy as np

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


def generate_random_enemy():
    return Point(random.uniform(0, 500), random.uniform(0, 500))

def generateEnemies(num):
    points = np.random.randint(0, 500, size=(num, 2))
    points = [tuple(point) for point in points]
    return points

def draw_minimap(location, enemies, screen, screen_center):
    minimap_rect = pygame.Rect(
        location._x - MINIMAP_SIZE // 2,
        location._y - MINIMAP_SIZE // 2,
        MINIMAP_SIZE,
        MINIMAP_SIZE,
    )
    pygame.draw.rect(screen, (0, 0, 0), minimap_rect, 2)

    for enemy in enemies:
        x = int( enemy._x)
        y = int( enemy._y)
        

        # Check if the enemy is inside the minimap
        pygame.draw.circle(screen, (255, 0, 0), (x, y), ENEMY_RADIUS)  # Red if inside minimap
        


def main():
    
    minimap_center = Point(screen_center[0],screen_center[1])
    enemies = generateEnemies(100)
    kd_tree = KDTree(enemies)
    # kd_tree.build()

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == QUIT:
                running = False

        # Handle key presses
        keys = pygame.key.get_pressed()
        if keys[K_w]:
            minimap_center._y -= 0.1
            print(minimap_center)
            # draw_minimap(minimap_center, enemies, screen, screen_center)
        if keys[K_s]:
            minimap_center._y += 0.1
            # draw_minimap(minimap_center, enemies, screen, screen_center)
        if keys[K_a]:
            minimap_center._x -= 0.1
            # draw_minimap(minimap_center, enemies, screen, screen_center)
        if keys[K_d]:
            minimap_center._x += 0.1
            # draw_minimap(minimap_center, enemies, screen, screen_center)

        screen.fill((255, 255, 255))
        
        # new_enemy = generate_random_enemy()
        # kd_tree.insert(new_enemy)
        enemies_inside = [Point(point[0], point[1]) for point in kd_tree.points_inside_rectangle((minimap_center._x - MINIMAP_SIZE / 2, minimap_center._y - MINIMAP_SIZE / 2),
                                 (minimap_center._x + MINIMAP_SIZE / 2, minimap_center._y + MINIMAP_SIZE / 2))]
        
        draw_minimap(minimap_center, enemies_inside, screen, screen_center)

        pygame.display.flip()

    pygame.quit()

if __name__ == '__main__':
    main()
