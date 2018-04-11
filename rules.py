import numpy as np

from util import *


def cohesion_rule(positions):
    nbr_boids = len(positions)
    output = list()
    for i in range(nbr_boids):
        curr_boid = positions[i]
        other_boids = remove_curr_boid(positions, i)
        output_vector = sum(other_boids) / (nbr_boids - 1)
        output.append(output_vector - curr_boid)
    return output * np.array([1])


def steer(velocities, old_velocities):
    return velocities - old_velocities


def get_displacement_vector(boid_position, other_boids_positions, min_distance_to_other_boids):
    displacement_vectors = other_boids_positions - boid_position
    output = np.array([0.0, 0.0])
    for displacement_vector in displacement_vectors:
        distance_to_other_boid = np.linalg.norm(displacement_vector)
        if distance_to_other_boid < min_distance_to_other_boids:
            difference = displacement_vector.copy()
            difference = normalize(difference)
            # difference = difference/distance_to_other_boid
            output = output - (difference)
            # print(boid_position, output, difference)

    return output


def separation_rule(positions, min_distance_to_other_boids):
    weight = 1
    nbr_boids = len(positions)
    output = list()

    for i in range(nbr_boids):
        curr_boid = positions[i]
        other_boids = remove_curr_boid(positions, i)

        output.append(
            get_displacement_vector(curr_boid, other_boids,
                                    min_distance_to_other_boids))
    return output * np.array([weight])


def align_rule(velocities):
    weight = 1
    nbr_boids = len(velocities)
    output = list()

    for i in range(nbr_boids):
        curr_boid = velocities[i]
        other_boids = sum(remove_curr_boid(velocities, i)) / (nbr_boids - 1)
        output.append(other_boids - curr_boid)

    return output * np.array(weight)


def set_speed(velocities, min_speed, max_speed):

    output = list()

    for velocity in velocities:
        speed = np.linalg.norm(velocity)
        new_velocity = velocity
        if speed > max_speed:
            new_velocity = (velocity / speed) * max_speed
        elif speed < min_speed:
            new_velocity = (velocity / speed) * min_speed

        output.append(new_velocity)

    return np.array(output)


# TODO: Iterate over boids, create subsets based on min distance to other boids
def move_them_boids(positions, velocities):
    nbr_boids = len(positions)

    for i in range(nbr_boids):
        pass


def keep_in_confines(positions, habitat_size):

    output = list()

    max_x, max_y = habitat_size

    for boid in positions:
        x = boid[0]
        y = boid[1]

        if x > max_x:
            # print("foo")
            x = x - max_x
        if x < 0:
            # print("foo")
            x = max_x + x

        if y > max_y:
            # print("foo")
            y = y - max_y
        if y < 0:
            # print("foo")
            y = max_y + y

        output.append(np.array([x, y]))

    return output * np.array(1)
