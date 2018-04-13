import numpy as np

from util import *


def cohesion_rule(positions, neighbor_indices):

    nbr_boids = len(positions)
    cohesion_vectors = list()

    # TODO: Investigate if needed:
    positions = positions * np.array(1)

    for i in range(nbr_boids):
        curr_boid_position = positions[i]
        other_boid_positions = positions[[neighbor_indices[i]]]
        other_boid_nbr = len(other_boid_positions)

        if other_boid_nbr < 1:
            cohesion_vectors.append(np.zeros(2))
            continue

        flock_center = sum(other_boid_positions) / (other_boid_nbr)
        cohesion_vector = flock_center - curr_boid_position
        cohesion_vector = normalize(cohesion_vector)

        cohesion_vectors.append(cohesion_vector)

    return cohesion_vectors * np.array([1])


def separation_rule(positions, neighbor_indices, displacement_vectors, distances, min_distance_to_other_boids):

    weight = 1
    nbr_boids = len(positions)
    output = list()

    for i in range(nbr_boids):

        displacement_vector = np.zeros(2)
        other_boids = neighbor_indices[i]

        other_boids = [b for b in other_boids if distances[i]
                       [b] < min_distance_to_other_boids]

        nbr_other_boids = len(other_boids)

        # If no nearby boids then append empty vector.
        if nbr_other_boids < 1:
            output.append(displacement_vector)
            continue

        d = displacement_vectors[i][other_boids]
        d = normalize(d)
        # d = d/distances[i][other_boids][:, None]
        displacement_vector = sum(displacement_vector - d)

        output.append(displacement_vector)

    return output * np.array([weight])


def align_rule(velocities, neighbor_indices):
    weight = 1
    nbr_boids = len(velocities)
    alignment_vectors = list()

    for i in range(nbr_boids):
        curr_boid_velocity = velocities[i]
        other_boid_velocities = velocities[neighbor_indices[i]]

        other_boid_nbr = len(other_boid_velocities)
        if other_boid_nbr < 1:
            alignment_vectors.append(np.zeros(2))
            continue

        other_boid_velocities = sum(other_boid_velocities)/other_boid_nbr
        alignment_vector = other_boid_velocities - curr_boid_velocity
        alignment_vector = normalize(alignment_vector)
        alignment_vectors.append(alignment_vector)

    return alignment_vectors * np.array(weight)


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


def keep_in_confines(positions, habitat_size):

    output = list()

    max_x, max_y = habitat_size

    for boid in positions:
        x = boid[0]
        y = boid[1]

        if x > max_x:
            x = x - max_x
        if x < 0:
            x = max_x + x
        if y > max_y:
            y = y - max_y
        if y < 0:
            y = max_y + y

        output.append(np.array([x, y]))

    return output * np.array(1)
