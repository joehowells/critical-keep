from copy import deepcopy
from math import hypot

from helper_functions import line_iter
from multiarray import MultiArray


class Map:
    def __init__(self, floor: MultiArray, rooms, endpoints):
        self.width = 64
        self.height = 28
        self.walkable = deepcopy(floor)
        self.transparent = deepcopy(floor)
        self.fov = MultiArray((64, 28))
        self.fov[:] = False
        self.explored = MultiArray((64, 28))
        self.explored[:] = False

        self.rooms = rooms
        self.endpoints = endpoints

    def compute_fov(
            self,
            x: int,
            y: int,
            radius: int = 0,
    ) -> None:
        self.fov[:] = False
        self.fov[x, y] = True

        for xd in range(x-radius, x+radius+1):
            yd = max(y-radius, 0)

            for xi, yi in line_iter(x, y, xd, yd):
                self.fov[xi, yi] = True
                if not self.transparent[xi, yi] or hypot(xi-x, yi-y) > radius:
                    break

            yd = min(y+radius, self.fov.shape[1]-1)

            for xi, yi in line_iter(x, y, xd, yd):
                self.fov[xi, yi] = True
                if not self.transparent[xi, yi] or hypot(xi-x, yi-y) > radius:
                    break

        for yd in range(y-radius+1, y+radius):
            xd = max(x-radius, 0)

            for xi, yi in line_iter(x, y, xd, yd):
                self.fov[xi, yi] = True
                if not self.transparent[xi, yi] or hypot(xi-x, yi-y) > radius:
                    break

            xd = min(x+radius, self.fov.shape[0]-1)

            for xi, yi in line_iter(x, y, xd, yd):
                self.fov[xi, yi] = True
                if not self.transparent[xi, yi] or hypot(xi-x, yi-y) > radius:
                    break
