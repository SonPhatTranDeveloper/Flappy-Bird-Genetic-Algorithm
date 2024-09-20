from objects.bird import Bird
import numpy as np


def mutate(weights, mutation_prob=0.5):
    """
    Mutate a weight based on a random factor
    :param mutation_prob: probability of mutation
    :param weights: the weights
    :return: mutated weights
    """
    # Generate a mask
    mask = (np.random.rand(*weights.shape) < mutation_prob).astype(int)

    # Generate mutation
    mutation = (np.random.choice([-1, 1], size=weights.shape)
                * np.random.randint(0, 30) * 0.0005)

    # Calculate the mutated weights
    return weights + mask * mutation


def clone_brain(bird):
    """
    Clone a bird and perform mutation on the gene
    :param bird: a bird to clone
    :return: new bird
    """
    # Create a new bird
    new_bird = bird.clone()

    # Mutate
    new_bird.brain.receive_genes(
        W1=mutate(bird.brain.W1),
        b1=mutate(bird.brain.b1),
        W2=mutate(bird.brain.W2),
        b2=mutate(bird.brain.b2),
    )

    return new_bird


def combine_brain(bird_mom: Bird, bird_dad: Bird):
    """
    Combine the brains of bird mom and bird dad to make new bird
    :param bird_mom: mom of the new generation
    :param bird_dad: dad of the new generation
    :return: a new bird
    """
    # Create a new bird
    bird = Bird()

    # Combine the brain
    mom_score = bird_mom.score
    dad_score = bird_dad.score

    # Calculate the ratio
    mom_ratio = 0.5
    dad_ratio = 0.5

    # Combine the parameter
    child_W1 = mom_ratio * bird_mom.brain.W1 + dad_ratio * bird_dad.brain.W1
    child_W2 = mom_ratio * bird_mom.brain.W2 + dad_ratio * bird_dad.brain.W2
    child_b1 = mom_ratio * bird_mom.brain.b1 + dad_ratio * bird_dad.brain.b1
    child_b2 = mom_ratio * bird_mom.brain.b2 + dad_ratio * bird_dad.brain.b2

    # Receive gene
    bird.brain.receive_genes(
        W1=mutate(child_W1),
        b1=mutate(child_b1),
        W2=mutate(child_W2),
        b2=mutate(child_b2)
    )

    return bird


def breed_bird(bird_mom: Bird, bird_dad: Bird, num_children: int):
    """
    Combine the brain of the two birds
    :param bird_mom: mom of the new generation
    :param bird_dad: dad of the new generation
    :param num_children: the number of children to produce
    :return: list of new bird children
    """
    return [combine_brain(bird_mom, bird_dad) for _ in range(num_children)]


def clone_bird(bird: Bird, num_children: int):
    """
    Clone bird into multiple children
    :param bird: bird to clone
    :return: list of cloned bird
    """
    return [clone_brain(bird) for _ in range(num_children)]