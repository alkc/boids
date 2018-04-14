from collections import namedtuple, defaultdict
from util import Color
import random
import numpy as np
Chromatid = namedtuple("Chromatid", ["coh", "sep", "ali", "R", "G", "B"])
Phenotype = namedtuple("Phenotype", ["behavior", "color"])
Egg = namedtuple("Egg", ["genome", "phenotype"])


def is_chromatid(namedtuple):
    return type(namedtuple).__name__ == "Chromatid"


def is_phenotype(namedtuple):
    return type(namedtuple).__name__ == "Phenotype"


def get_crossover_gametes(gametes):
    return gametes


def get_mutated_gametes(gametes):
    return gametes


def get_phenotype(boid_genome):
    chromatid_a, chromatid_b = boid_genome
    behavior = get_boid_weights(chromatid_a, chromatid_b)
    color = get_boid_color(chromatid_a, chromatid_b)
    return Phenotype(behavior, color)


def get_baby_boid(mate_1, mate_2):
    gametes = [random.choice(mate_1), random.choice(mate_2)]
    gametes = get_mutated_gametes(gametes)
    gametes = get_crossover_gametes(gametes)
    boid_genome = gametes
    phenotype = get_phenotype(boid_genome)

    return Egg(boid_genome, phenotype)


def get_next_generation(individual_genomes, nbr_boids_in_next_gen):

    # TODO: Fix>
    individuals = individual_genomes
    next_generation_eggs = list()

    for i in range(nbr_boids_in_next_gen):

        mate_1 = random.choice(individuals)
        mate_2 = random.choice(individuals)

        while mate_1 is mate_2:
            mate_2 = random.choice(individuals)

        new_boid = get_baby_boid(mate_1, mate_2)
        next_generation_eggs.append(new_boid)

    return hatch_flock(next_generation_eggs)


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


def get_weight_genes(chromatid):

    genes = dict()
    # TODO: Break out to func parameter
    weight_genes = ['coh', 'ali', 'sep']

    for gene in weight_genes:
        genes[gene] = chromatid._asdict()[gene]

    return genes


def get_boid_weights(chromatid_a, chromatid_b):

    weights = dict()

    genes_a = get_weight_genes(chromatid_a)
    genes_b = get_weight_genes(chromatid_b)

    def get_weight_mean(a, b):
        return (a+b)/2

    for gene in genes_a.keys():
        a, b = (genes_a[gene], genes_b[gene])
        weights[gene] = get_weight_mean(a, b)

    return weights


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


def hatch_flock(eggs):

    colors = list()
    genomes = list()
    weights_dict = defaultdict(list)

    for egg in eggs:
        colors.append(egg.phenotype.color)
        genomes.append(egg.genome)
        for weight in egg.phenotype.behavior.keys():
            # TODO: it aint an array
            weight_array = egg.phenotype.behavior[weight]
            weights_dict[weight].append(weight_array)

    for weight_list in weights_dict.keys():
        weights_dict[weight_list] = np.array(weights_dict[weight_list])
    # print(weights_dict)
    # print(genomes)
    # print(colors)
    return colors, genomes, weights_dict


def get_random_flock(nbr_boids):

    eggs = list()

    for i in range(nbr_boids):
        genome = (generate_random_chromatid(True, True),
                  generate_random_chromatid(True, True))
        phenotype = get_phenotype(genome)

        eggs.append(Egg(genome, phenotype))

    return hatch_flock(eggs)
