import pygame


def draw_boids(positions, screen, boid_color):
    for boid in positions:
        x, y = boid.astype("int")
        pygame.draw.circle(screen, boid_color, (x, y), 2, 0)
