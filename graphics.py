import pygame


def draw_boids(positions, screen):
    for boid in positions:
        x, y = boid.astype("int")
        pygame.draw.circle(screen, (255, 255, 255), (x, y), 2, 0)
