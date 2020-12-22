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
    num_inputs = rng.choice(10 * num_vars) + 1
    variables = {f"${i}" for i in range(num_vars)}
    sampler = InputSampler(
        PCFGSampler(rng, weights=WEIGHTS), num_inputs=num_inputs, image_size=25
    )
    program, inputs, _ = sampler.sample(variables)
    return program, inputs


def generate_dataset(path, n, **kwargs):
    with shelve.open(path, "c") as shelf:
        for i in tqdm.trange(n):
            if str(i) in shelf:
                continue
            shelf[str(i)] = sample_program(i)


def main():
    fire.Fire(generate_dataset)
