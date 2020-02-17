from dataclasses import dataclass, field, InitVar
from itertools import product
from typing import Any, List


@dataclass
class MultiArray:
    w: int
    h: int
    data: List[List[Any]] = field(init=False)
    value: InitVar[Any] = None

    @property
    def shape(self):
        return self.w, self.h

    def __post_init__(self, value):
        self.data = [value for _ in range(self.w*self.h)]

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
            start, stop, step = key.indices(self.w*self.h)
            for i in range(start, stop, step):
                return self.data[i]

        else:
            i, j = key

            return self.data[self.w * j + i]

    def __setitem__(self, key, value):
        if isinstance(key, int):
            self.data[key] = value

        elif isinstance(key, slice):
            start, stop, step = key.indices(self.w*self.h)
            for i in range(start, stop, step):
                self.data[i] = value

        else:
            x_key, y_key = key

            if isinstance(x_key, int):
                x_key = slice(x_key, x_key+1, 1)

            start, stop, step = x_key.indices(self.w)
            x_range = range(start, stop, step)

            if isinstance(y_key, int):
                y_key = slice(y_key, y_key+1, 1)

            start, stop, step = y_key.indices(self.h)
            y_range = range(start, stop, step)

            for i, j in product(x_range, y_range):
                self.data[self.w * j + i] = value

    def __or__(self, other):
        assert self.shape == other.shape

        result = MultiArray(self.w, self.h)

        for i in range(self.w*self.h):
            result[i] = self[i] or other[i]

        return result
