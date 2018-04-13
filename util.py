import random
import numpy as np
from collections import namedtuple


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
    return [np.array([0.0, 0.0]) for _ in range(nbr)]


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
