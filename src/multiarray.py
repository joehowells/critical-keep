from dataclasses import dataclass, field, InitVar
from itertools import product
from typing import Any, List, Union


def key_to_range(key: Union[int, slice], dim: int) -> range:
    if isinstance(key, int):
        key = slice(key, key + 1, 1)

    start, stop, step = key.indices(dim)
    return range(start, stop, step)


@dataclass
class MultiArray:
    w: int
    h: int
    data: List[Any] = field(init=False)
    value: InitVar[Any] = None

    @property
    def shape(self):
        return self.w, self.h

    @property
    def size(self):
        return self.w * self.h

    def __post_init__(self, value):
        self.data = [value for _ in range(self.size)]

    @classmethod
    def from_multi_array(cls, other, cast=None):
        result = cls(other.w, other.h)
        if cast:
            result.data = list(map(cast, other.data))
        else:
            result.data = other.data

        return result

    def __getitem__(self, key):
        if isinstance(key, int):
            return self.data[key]

        elif isinstance(key, slice):
            for i in key_to_range(key, self.size):
                return self.data[i]

        else:
            i, j = key

            raw_index = self.w * j + i
            return self.data[raw_index]

    def __setitem__(self, key, value):
        if isinstance(key, int):
            self.data[key] = value

        elif isinstance(key, slice):
            for i in key_to_range(key, self.size):
                self.data[i] = value

        else:
            x_key, y_key = key

            x_range = key_to_range(x_key, self.w)
            y_range = key_to_range(y_key, self.h)

            for i, j in product(x_range, y_range):
                raw_index = self.w * j + i
                self.data[raw_index] = value

    def __or__(self, other):
        assert self.shape == other.shape

        result = MultiArray(self.w, self.h)

        for i in range(self.size):
            result[i] = self[i] or other[i]

        return result
