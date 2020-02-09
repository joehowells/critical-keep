from math import hypot

import numpy

from helper_functions import line_iter


class Map:
    def __init__(self, floor: numpy.ndarray, rooms, endpoints):
        self.width, self.height = floor.shape
        self.walkable = numpy.array(floor, dtype=numpy.bool)
        self.transparent = numpy.array(floor, dtype=numpy.bool)
        self.fov = numpy.empty(shape=(64, 28), dtype=numpy.bool)
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
            xd = max(y-radius, 0)

            for xi, yi in line_iter(x, y, xd, yd):
                self.fov[xi, yi] = True
                if not self.transparent[xi, yi] or hypot(xi-x, yi-y) > radius:
                    break

            xd = min(x+radius, self.fov.shape[0]-1)

            for xi, yi in line_iter(x, y, xd, yd):
                self.fov[xi, yi] = True
                if not self.transparent[xi, yi] or hypot(xi-x, yi-y) > radius:
                    break
