#!/usr/bin/env python3

import numpy as np
import pygame
import sys

from util import *
from rules import *
from graphics import *

habitat_size = (500, 500)
nbr_boids = 100
min_distance_to_other_boids = 5
boid_perception_radius = 50
cohesion_weight = 0.1
align_weight = 0.125
separation_weight = 1.0
boid_max_speed = 8
boid_min_speed = 1
graphics_fps = 30

# Intialize pygame display:

pygame.init()
screen = pygame.display.set_mode(habitat_size)
bg_color = Color(130, 130, 200)
boid_colors = [get_random_color() for _ in range(nbr_boids)]
clock = pygame.time.Clock()

# Spawn random boids
positions = [get_random_position(habitat_size) for x in range(nbr_boids)]

velocities = [get_random_velocity() for x in range(nbr_boids)]
velocities = set_speed(velocities, boid_min_speed, boid_min_speed + 1)

simulation = True


while simulation:

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            simulation = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                simulation = False
                continue

    separation_vector = intialize_empty_vectors(nbr_boids)
    alignment_vector = intialize_empty_vectors(nbr_boids)
    cohesion_vector = intialize_empty_vectors(nbr_boids)

    old_velocities = velocities.copy()

    displacement_vectors = get_displacement_vectors(positions)
    distances = get_distances(displacement_vectors)
    neighbor_lists = get_neighbors(distances, boid_perception_radius)

    separation_vector = separation_rule(positions, neighbor_lists,
                                        displacement_vectors, distances,
                                        min_distance_to_other_boids)

    separation_vector *= separation_weight

    alignment_vector = align_rule(old_velocities, neighbor_lists)
    alignment_vector *= align_weight

    cohesion_vector = cohesion_rule(positions, neighbor_lists)
    cohesion_vector *= cohesion_weight

    velocities = old_velocities.copy()
    velocities += separation_vector
    velocities += alignment_vector
    velocities += cohesion_vector
    velocities = set_speed(velocities, boid_min_speed, boid_max_speed)

    positions = positions + velocities
    positions = keep_in_confines(positions, habitat_size)

    screen.fill(bg_color)
    draw_boids(positions, screen, boid_colors)
    pygame.display.update()
    clock.tick(graphics_fps)


pygame.quit()
sys.exit()
