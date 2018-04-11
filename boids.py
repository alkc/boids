#!/usr/bin/env python3

import numpy as np
import pygame
import sys

from util import *
from rules import *
from graphics import *

habitat_size = (500, 500)
nbr_boids = 5
min_distance_to_other_boids = 50
boid_perception_radius = 100
cohesion_weight = 1.0
align_weight = 1.0
separation_weight = 1.00
boid_max_speed = 10
boid_min_speed = 1

# Intialize pygame display:

pygame.init()
screen = pygame.display.set_mode(habitat_size)
bg_color = Color(0, 0, 0)
clock = pygame.time.Clock()

# Spawn random boids
positions = [get_random_position(habitat_size) for x in range(nbr_boids)]

velocities = [get_random_velocity() for x in range(nbr_boids)]
velocities = set_speed(velocities, boid_min_speed, boid_max_speed)

print(velocities)

simulation = True


def intialize_empty_2d_vecs(nbr):
    return [np.array([0.0, 0.0]) for _ in range(nbr)]


while simulation:

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            simulation = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                simulation = False

    separation_vector = intialize_empty_2d_vecs(nbr_boids)
    alignment_vector = intialize_empty_2d_vecs(nbr_boids)
    cohesion_vector = intialize_empty_2d_vecs(nbr_boids)

    old_velocities = velocities.copy()
    separation_vector = separation_rule(positions,
                                        min_distance_to_other_boids) * separation_weight
    # separation_vector = steer(
    #     separation_vector, old_velocities)

    alignment_vector = align_rule(old_velocities) * align_weight
    # alignment_vector = steer(alignment_vector, old_velocities)

    cohesion_vector = cohesion_rule(positions) * cohesion_weight
    # cohesion_vector = steer(cohesion_vector, old_velocities)

    velocities = old_velocities + separation_vector + \
        alignment_vector + cohesion_vector
    velocities = set_speed(velocities, boid_min_speed, boid_max_speed)

    positions = positions + velocities
    positions = keep_in_confines(positions, habitat_size)

    screen.fill(bg_color)
    draw_boids(positions, screen)
    pygame.display.update()
    clock.tick(30)


pygame.quit()
sys.exit()
