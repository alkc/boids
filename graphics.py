import pygame


def draw_boids(boid_positions, screen, boid_colors):
    for boid_position, boid_color in zip(boid_positions, boid_colors):
        x, y = boid_position.astype("int")
        pygame.draw.circle(screen, boid_color, (x, y), 4, 0)
