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
cohesion_weight = 0.01
align_weight = 0.125
separation_weight = 1.00
max_speed = 5

# Intialize pygame display:

pygame.init()
screen = pygame.display.set_mode(habitat_size)
bg_color = Color(0, 0, 0)
clock = pygame.time.Clock()

# Spawn random boids
positions = [get_random_position(habitat_size) for x in range(nbr_boids)]
velocities = [get_random_velocity() for x in range(nbr_boids)]

simulation = True

while simulation:

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            simulation = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                simulation = False

    old_velocities = velocities.copy()

    separation_vector = separation_rule(positions,
                                        min_distance_to_other_boids)
    separation_vector = steer(
        separation_vector, old_velocities) * separation_weight

    alignment_vector = align_rule(old_velocities)
    alignment_vector = steer(alignment_vector, old_velocities) * align_weight

    cohesion_vector = cohesion_rule(positions)
    cohesion_vector = steer(cohesion_vector, old_velocities) * cohesion_weight

    velocities = old_velocities + separation_vector + \
        alignment_vector + cohesion_vector
    velocities = limit_speed(velocities, max_speed)

    positions = positions + velocities
    positions = keep_in_confines(positions, habitat_size)

    screen.fill(bg_color)
    draw_boids(positions, screen)
    pygame.display.update()
    clock.tick(30)


pygame.quit()
sys.exit()
