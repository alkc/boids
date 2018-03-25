#!/usr/bin/env python3

import numpy as np
import pygame
import sys

from util import *
from rules import *
from graphics import *

habitat_size = (500, 500)
nbr_boids = 25
min_distance_to_other_boids = 10
cohesion_weight = 0.01
align_weight = 0.125
separation_weight = 1.00
max_speed = 5

# Intialize pygame display:

pygame.init()
screen = pygame.display.set_mode(habitat_size)
bg_color = (0, 0, 0)
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

    velocities += cohesion_rule(positions, cohesion_weight)
    velocities += align_rule(velocities, align_weight)
    velocities += separation_rule(positions,
                                  min_distance_to_other_boids, separation_weight)
    velocities = limit_speed(velocities, max_speed)

    positions = positions + velocities
    positions = keep_in_confines(positions, habitat_size)

    screen.fill(bg_color)
    draw_boids(positions, screen)
    pygame.display.update()
    clock.tick(30)


pygame.quit()
output_thing.close()
sys.exit()
