import random
import numpy as np


def get_random_position(habitat_size):
    x = random.randrange(1, habitat_size[0] - 1)
    y = random.randrange(1, habitat_size[1] - 1)
    return np.array([x, y])


def get_random_velocity():
    return np.array([0.0, 0.0])


def remove_curr_boid(list_of_arrays, index):
    copy_list = list(list_of_arrays)
    del copy_list[index]
    return copy_list
