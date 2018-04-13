from collections import namedtuple
from util import Color
import random

Chromatid = namedtuple("Chromatid", ["coh", "sep", "ali", "R", "G", "B"])


def mutate_weight():
    pass


def generate_random_chromatid(random_weights, random_colors, default_colors=(0, 0, 0)):

    coh, sep, ali = (0.0, 0.0, 0.0)
    R, G, B = default_colors

    if random_weights:
        coh, sep, ali = [random.uniform(-1, 1) for _ in range(3)]

    if random_colors:
        R, G, B = [random.randint(0, 255) for _ in range(3)]

    return Chromatid(coh=coh, sep=sep, ali=ali, R=R, G=G, B=B)


def get_color_genes(boid_chromatid):
    return (boid_chromatid.R, boid_chromatid.G, boid_chromatid.B)


def get_weights(boid_chromatid):
    pass


def get_boid_color(chromatid_a, chromatid_b):

    colors_1 = get_color_genes(chromatid_a)
    colors_2 = get_color_genes(chromatid_b)

    def average_color(a, b):
        final_color = int((a + b)/2)
        if final_color > 255:
            final_color = 255
        if final_color < 0:
            final_color = 0
        return final_color

    R, G, B = [average_color(colors_1[i], colors_2[i]) for i in range(3)]

    return Color(R, G, B)
