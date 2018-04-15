import random
import numpy as np
from collections import namedtuple


def get_weight_from_flock(flock, weight):

    return np.array([b[weight] for b in flock['weights']])


def get_colors_from_flock(flock):
    return [b["color"] for b in flock]


def remove_collided_boids(array_2d, kill_list, axis):
    return np.delete(array_2d, kill_list, axis=axis)


def get_collisions(distances, neighbor_lists, collision_radius):

    boids_that_have_collided = list()

    for i, distance_vector in enumerate(distances):
        if i in boids_that_have_collided:
            continue

        current_distances = distance_vector[neighbor_lists[i]]
        collided_boids = [i for x in current_distances if x < collision_radius]

        boids_that_have_collided = boids_that_have_collided + collided_boids

    return set(boids_that_have_collided)


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


def get_random_position(habitat_size):
    x = random.randrange(1, habitat_size[0] - 1)
    y = random.randrange(1, habitat_size[1] - 1)
    return np.array([x, y])


def get_random_velocity():
    return np.random.uniform(-2, 2, 2)


def remove_curr_boid(list_of_arrays, index):
    copy_list = list(list_of_arrays)
    del copy_list[index]
    return copy_list


def normalize(vector):
    norm = np.linalg.norm(vector)
    if norm == 0:
        return vector
    return vector / norm


def intialize_empty_vectors(nbr):
    return np.zeros([nbr, 2])


Color = namedtuple('Color', ['red', 'green', 'blue'])


def get_random_color():
    R, G, B = [random.randint(0, 255) for _ in range(3)]
    return Color(R, G, B)


def get_displacement_vectors(positions):

    displacement_vectors = list()

    for position in positions:
        displacement_vectors.append(positions - position)

    return displacement_vectors


def get_distances(displacement_vector_lists):

    distances = list()

    for d in displacement_vector_lists:
        distances.append(np.linalg.norm(d, axis=1))

    return distances


def get_neighbors(distance_vectors, neighbor_radius):

    neighbor_indices = list()

    for i, distance_vector in enumerate(distance_vectors):
        neighbors = [j for j in range(len(distance_vector))
                     if distance_vector[j] < neighbor_radius and i != j]
        neighbor_indices.append(neighbors)

    return neighbor_indices
