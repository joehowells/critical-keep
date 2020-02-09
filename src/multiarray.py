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

    def slice_to_range(self, sl, axis=None):
        if axis is None:
            default_stop = len(self.data)
        elif axis == 0:
            default_stop = self.w
        elif axis == 1:
            default_stop = self.h
        else:
            raise ValueError

        start = sl.start if sl.start is not None else 0
        stop = sl.stop if sl.stop is not None else default_stop
        step = sl.step if sl.step is not None else 1

        return range(start, stop, step)

    def __post_init__(self, value):
        self.data = [value for _ in range(self.w*self.h)]

    @classmethod
    def from_multiarray(cls, other, cast=None):
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
            for i in self.slice_to_range(key, None):
                return self.data[i]

        else:
            i, j = key

            return self.data[self.w * j + i]

    def __setitem__(self, key, value):
        if isinstance(key, int):
            self.data[key] = value

        elif isinstance(key, slice):
            for i in self.slice_to_range(key, None):
                self.data[i] = value

        else:
            xkey, ykey = key

            if isinstance(xkey, int):
                xkey = range(xkey, xkey+1, 1)
            else:
                xkey = self.slice_to_range(xkey)

            if isinstance(ykey, int):
                ykey = range(ykey, ykey+1, 1)
            else:
                ykey = self.slice_to_range(ykey)

            for i, j in product(xkey, ykey):
                self.data[self.w * j + i] = value

    def __or__(self, other):
        assert self.shape == other.shape

        result = MultiArray(self.w, self.h)

        for i in range(self.w*self.h):
            result[i] = self[i] or other[i]

        return result
