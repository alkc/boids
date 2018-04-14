#!/usr/bin/env python3

import numpy as np
import pygame
import sys

from util import *
from genetics import *
from rules import *
from graphics import *

# Simulation settings:
habitat_size = (500, 500)
nbr_boids = 100
min_nbr_boids = 50

# Flocking rules weights:
cohesion_weight = 0.1
align_weight = 0.125
separation_weight = 1.0

# Boid params:
boid_max_speed = 8
boid_min_speed = 1
min_distance_to_other_boids = 10
boid_perception_radius = 50
boid_collision_radius = 3

# Graphics settings:
graphics_fps = 30
graphics_window_size = habitat_size

# Intialize pygame display:

pygame.init()
screen = pygame.display.set_mode(graphics_window_size)
bg_color = Color(130, 130, 200)
boid_colors = [get_random_color() for _ in range(nbr_boids)]
clock = pygame.time.Clock()

# Spawn random boids and get them moving
positions = [get_random_position(habitat_size) for x in range(nbr_boids)]
velocities = [get_random_velocity() for x in range(nbr_boids)]
velocities = set_speed(velocities, boid_min_speed, boid_min_speed + 1)

simulation = True

boid_colors, boid_genomes, weights = get_random_flock(nbr_boids)


def get_weight_from_flock(flock, weight):

    return np.array([b[weight] for b in flock['weights']])


def get_colors_from_flock(flock):
    return [b["color"] for b in flock]


cohesion_weight = weights['coh']
separation_weight = weights['sep']
align_weight = weights['ali']

mutable_lists = [boid_colors, boid_genomes,
                 cohesion_weight, align_weight, separation_weight]

curr_nbr_boids = nbr_boids

# print(separation_weight)
# print(np.shape(separation_weight))

# exit()


def filter_list_by_boid_killist(input_list, kill_list):
    return [input_list[i] for i in range(len(input_list)) if i not in kill_list]


while simulation:

    if curr_nbr_boids < min_nbr_boids:

        # TODO: Rewrite flock ffs
        # print(type(genomes))
        boid_colors, boid_genomes, weights = get_next_generation(
            boid_genomes, nbr_boids)
        # print(type(flock))
        cohesion_weight = weights['coh']
        separation_weight = weights['sep']
        align_weight = weights['ali']
        # print(np.shape(separation_weight))
        positions = [get_random_position(habitat_size)
                     for x in range(nbr_boids)]
        velocities = [get_random_velocity() for x in range(nbr_boids)]
        velocities = set_speed(velocities, boid_min_speed, boid_min_speed + 1)
        curr_nbr_boids = nbr_boids

    if len(positions) < 1:
        print("All boids are dead")
        simulation = False
        continue

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

    # Precalculate distances and neighboring boids based on perception radius
    displacement_vectors = get_displacement_vectors(positions)
    distances = get_distances(displacement_vectors)
    neighbor_lists = get_neighbors(distances, boid_perception_radius)

    # Figure out which boids have collided:
    collisions = get_collisions(
        distances, neighbor_lists, boid_collision_radius)

    if len(collisions) > 0:
        collisions = list(collisions)
        positions = remove_collided_boids(positions, collisions, axis=0)
        velocities = remove_collided_boids(velocities, collisions, axis=0)
        cohesion_weight = remove_collided_boids(
            cohesion_weight, collisions, axis=0)
        align_weight = remove_collided_boids(align_weight, collisions, axis=0)
        separation_weight = remove_collided_boids(
            separation_weight, collisions, 0)

        # TODO: Fix this :
        boid_colors = [boid_colors[i]
                       for i in range(len(boid_colors)) if i not in collisions]
        boid_genomes = [boid_genomes[i]
                        for i in range(len(boid_genomes)) if i not in collisions]
        curr_nbr_boids -= len(collisions)
        continue

    old_velocities = velocities.copy()

    # Apply rules
    # print(separation_weight)
    # print(separation_vector)

    separation_vector = separation_rule(positions, neighbor_lists,
                                        displacement_vectors, distances,
                                        min_distance_to_other_boids)

    alignment_vector = align_rule(old_velocities, neighbor_lists)

    cohesion_vector = cohesion_rule(positions, neighbor_lists)

    # Apply weights
    # print(separation_vector)

    separation_vector *= separation_weight[:, None]
    alignment_vector *= align_weight[:, None]
    cohesion_vector *= cohesion_weight[:, None]

    # Accelerate accordingly:
    velocities = old_velocities.copy()
    velocities += separation_vector
    velocities += alignment_vector
    velocities += cohesion_vector
    velocities = set_speed(velocities, boid_min_speed, boid_max_speed)

    # Update positions:
    positions = positions + velocities
    positions = keep_in_confines(positions, habitat_size)

    # Redraw screen:
    screen.fill(bg_color)
    draw_boids(positions, screen, boid_colors)
    pygame.display.update()
    clock.tick(graphics_fps)


pygame.quit()
