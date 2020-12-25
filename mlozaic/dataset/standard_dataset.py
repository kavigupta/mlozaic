import os

import pickle
import shelve

import numpy as np
import tqdm as tqdm
import fire

from ..sampler import PCFGSampler, InputSampler
from ..ast.expression import Constant, Variable, Comparison
from ..ast.drawing import Primitive, If, IfE

WEIGHTS = {
    Constant: 3,
    Variable: 3,
    Primitive: 5,
    Comparison: 5,
    If: 0.5,
    IfE: 0.5,
    "null": 0,
}


def sample_program(seed):
    rng = np.random.RandomState(seed)
    num_vars = rng.choice(3) + 1
    num_inputs = rng.choice(10 * num_vars) + 2
    variables = {f"${i}" for i in range(num_vars)}
    sampler = InputSampler(
        PCFGSampler(rng, weights=WEIGHTS, max_depth=7),
        num_inputs=num_inputs,
        image_size=25,
    )
    program, inputs, _ = sampler.sample(variables)
    return program, inputs


def generate_dataset(path, n, **kwargs):
    try:
        os.makedirs(path)
    except FileExistsError:
        pass
    with shelve.open(path + "/data", "c") as shelf:
        for i in tqdm.trange(len(shelf), n):
            shelf[str(i)] = sample_program(i)


def main():
    fire.Fire(generate_dataset)
