import attr

import numpy as np


@attr.s
class Item:
    type = attr.ib()
    transform = attr.ib()
    color = attr.ib()
