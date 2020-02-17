from dataclasses import dataclass, replace
from functools import reduce
from itertools import product
from operator import mul, or_
from typing import Any, List, Tuple, Union


def key_to_range(key: Union[int, slice], dim: int) -> range:
    if isinstance(key, int):
        key = slice(key, key + 1, 1)

    start, stop, step = key.indices(dim)
    return range(start, stop, step)


@dataclass
class MultiArray:
    shape: Tuple[int, ...]
    data: List[Any] = None

    @property
    def size(self):
        return reduce(mul, self.shape, 1)

    @property
    def strides(self):
        return tuple(reduce(mul, self.shape[:dim], 1) for dim, _ in enumerate(self.shape))

    def __post_init__(self):
        if self.data is None:
            self.data = [None for _ in range(self.size)]

    def __getitem__(self, key):
        if isinstance(key, int):
            return self.data[key]

        elif isinstance(key, slice):
            for i in key_to_range(key, self.size):
                return self.data[i]

        else:
            raw_index = sum(map(mul, key, self.strides))
            return self.data[raw_index]

    def __setitem__(self, key, value):
        if isinstance(key, int):
            self.data[key] = value

        elif isinstance(key, slice):
            for i in key_to_range(key, self.size):
                self.data[i] = value

        else:
            ranges = (key_to_range(k, d) for k, d in zip(key, self.shape))

            for indices in product(*ranges):
                raw_index = sum(map(mul, indices, self.strides))
                self.data[raw_index] = value

    def __or__(self, other):
        return replace(self, data=list(map(or_, self.data, other.data)))
