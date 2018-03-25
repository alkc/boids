#!/usr/bin/env python3

import random
import numpy as np
import pygame
import sys

habitat_size = (500, 500)


def get_random_position(habitat_size):
    x = random.randrange(1, habitat_size[0] - 1)
    y = random.randrange(1, habitat_size[1] - 1)
    return np.array([x, y])


def get_random_velocity():
    return np.array([0.0, 0.0])


nbr_boids = 25
min_distance_to_other_boids = 10
cohesion_weight = 0.01
align_weight = 0.125
separation_weight = 1.00
max_speed = 5


def remove_curr_boid(list_of_arrays, index):
    copy_list = list(list_of_arrays)
    del copy_list[index]
    return copy_list


def cohesion_rule(positions, weight):
    nbr_boids = len(positions)
    output = list()
    for i in range(nbr_boids):
        curr_boid = positions[i]
        other_boids = remove_curr_boid(positions, i)
        output_vector = sum(other_boids) / (nbr_boids - 1)
        output.append(output_vector - curr_boid)
    return output * np.array(weight)


def get_distances(boid, other_boids, min_distance_to_other_boids):
    displacement_vectors = list(other_boids - boid)
    output = np.array([0.0, 0.0])
    for vector in displacement_vectors:
        distance_to_other_boid = np.linalg.norm(vector)
        if distance_to_other_boid < min_distance_to_other_boids:
            output = output - vector

    return output


def separation_rule(positions, min_distance_to_other_boids, weight):
    nbr_boids = len(positions)
    output = list()

    for i in range(nbr_boids):
        curr_boid = positions[i]
        other_boids = remove_curr_boid(positions, i)
        output.append(
            get_distances(curr_boid, other_boids,
                          min_distance_to_other_boids))

    return output * np.array([weight])


def align_rule(velocities, weight):
    nbr_boids = len(velocities)
    output = list()

    for i in range(nbr_boids):
        curr_boid = velocities[i]
        other_boids = sum(remove_curr_boid(velocities, i)) / (nbr_boids - 1)
        output.append(other_boids - curr_boid)

    return output * np.array(weight)


def limit_speed(velocities, max_speed):

    output = list()

    for velocity in velocities:
        speed = np.linalg.norm(velocity)
        new_velocity = velocity
        if speed > max_speed:
            new_velocity = (velocity / speed) * max_speed
        output.append(new_velocity)

    return np.array(output)


def keep_in_confines(positions, habitat_size):

    output = list()

    max_x, max_y = habitat_size

    for boid in positions:
        x = boid[0]
        y = boid[1]

        if x > max_x:
            print("foo")
            x = x - max_x
        if x < 0:
            print("foo")
            x = max_x + x

        if y > max_y:
            print("foo")
            y = y - max_y
        if y < 0:
            print("foo")
            y = max_y + y

        output.append(np.array([x, y]))

    return output * np.array(1)


positions = [get_random_position(habitat_size) for x in range(nbr_boids)]
velocities = [get_random_velocity() for x in range(nbr_boids)]


# Quick function and some overhead  to log positions to output:
# output_thing = open("positions_over_time.txt", "w")
header = ['boid', 't', 'x', 'y']
header = "\t".join(header)
print(header, file=output_thing)


def draw_boids(positions, screen):
    for boid in positions:
        x, y = boid.astype("int")
        pygame.draw.circle(screen, (255, 255, 255), (x, y), 2, 0)


# def write_to_table(output_handle, positions, t):
#     for i, position in enumerate(positions):

#         x = str(int(position[0]))
#         y = str(int(position[1]))

#         row = [str(i + 1), str(t), x, y]
#         row = "\t".join(row)
#         print(row, file=output_handle)


pygame.init()
screen = pygame.display.set_mode(habitat_size)
bg_color = (0, 0, 0)
clock = pygame.time.Clock()

# Ticker:
i = 1
simulation = True

while simulation:

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            simulation = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                simulation = False

    # print(i)
    # print(len(positions))
    velocities += cohesion_rule(positions, cohesion_weight)
    velocities += align_rule(velocities, align_weight)
    velocities += separation_rule(positions,
                                  min_distance_to_other_boids, separation_weight)
    velocities = limit_speed(velocities, max_speed)

    positions = positions + velocities
    positions = keep_in_confines(positions, habitat_size)

    # if i % 10 == 0:
    #     write_to_table(output_thing, positions, i)
    # if i % 10000 == 0 and i > 0:
    #     simulation = False

    screen.fill(bg_color)
    draw_boids(positions, screen)
    pygame.display.update()
    clock.tick(30)
    i += 1

pygame.quit()
output_thing.close()
sys.exit()
