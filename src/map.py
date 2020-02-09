from math import hypot

import numpy
import tcod.map

from helper_functions import line_iter


class Map(tcod.map.Map):
    def __init__(self, floor: numpy.ndarray, rooms, endpoints):
        super().__init__(width=64, height=28, order='F')
        self.walkable[:] = floor[:]
        self.transparent[:] = floor[:]
        self.explored = numpy.empty(shape=(64, 28), dtype=numpy.bool)
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

        for xd in range(0, self.fov.shape[0]):
            yd = 0

            for xi, yi in line_iter(x, y, xd, yd):
                self.fov[xi, yi] = True
                if not self.transparent[xi, yi] or hypot(xi-x, yi-y) > radius:
                    break

            yd = self.fov.shape[1]-1

            for xi, yi in line_iter(x, y, xd, yd):
                self.fov[xi, yi] = True
                if not self.transparent[xi, yi] or hypot(xi-x, yi-y) > radius:
                    break

        for yd in range(0, self.fov.shape[1]):
            xd = 0

            for xi, yi in line_iter(x, y, xd, yd):
                self.fov[xi, yi] = True
                if not self.transparent[xi, yi] or hypot(xi-x, yi-y) > radius:
                    break

            xd = self.fov.shape[0]-1

            for xi, yi in line_iter(x, y, xd, yd):
                self.fov[xi, yi] = True
                if not self.transparent[xi, yi] or hypot(xi-x, yi-y) > radius:
                    break
