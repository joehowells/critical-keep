import numpy
import tcod.map


class Map(tcod.map.Map):
    def __init__(self, floor: numpy.ndarray, rooms, endpoints):
        super().__init__(width=64, height=28, order='F')
        self.walkable[:] = floor[:]
        self.transparent[:] = floor[:]
        self.explored = numpy.empty(shape=(64, 28), dtype=numpy.bool)
        self.explored[:] = False

        self.rooms = rooms
        self.endpoints = endpoints
