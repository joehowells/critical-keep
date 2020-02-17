import itertools
import random

from map import Map
from multiarray import MultiArray


class Room:
    def __init__(self, x1, x2, y1, y2):
        self.x1 = x1
        self.x2 = x2
        self.y1 = y1
        self.y2 = y2

        self.distance = None

    @property
    def w(self):
        return self.x2-self.x1

    @property
    def h(self):
        return self.y2-self.y1

    @property
    def cells(self):
        return [(x, y) for x in range(self.x1, self.x2) for y in range(self.y1, self.y2)]


def make_map():
    for _ in range(100):
        floor, rooms, endpoints = make_candidate()
        if len(endpoints) > 2:
            break

    return Map(floor, rooms, endpoints)


def make_candidate():
    rooms = {
        (m, n): Room(9*m+1, 9*m+9, 9*n+1, 9*n+9)
        for m, n in itertools.product(range(7), range(3))
    }
    links = []
    discovered = []

    def dfs(v):
        discovered.append(v)

        m, n = v

        neighbors = [(m - 1, n), (m + 1, n), (m, n - 1), (m, n + 1)]
        neighbors = [n for n in neighbors if n in rooms]
        random.shuffle(neighbors)

        for w in neighbors:
            if w not in discovered:
                if v < w:
                    links.append((v, w))
                else:
                    links.append((w, v))
                dfs(w)

    dfs((3, 1))

    # Construct horizontal links
    h_links = {
        ((m, n), (m+1, n)): Room(9*m+1, 9*m+18, 9*n+1, 9*n+9)
        for m, n in itertools.product(range(6), range(3))
    }

    # Construct vertical links
    v_links = {
        ((m, n), (m, n+1)): Room(9*m+1, 9*m+9, 9*n+1, 9*n+18)
        for m, n in itertools.product(range(7), range(2))
    }
    h_links = {key: value for key, value in h_links.items() if key in links or random.random() < 0.2}
    v_links = {key: value for key, value in v_links.items() if key in links or random.random() < 0.2}
    links = list(h_links.keys()) + list(v_links.keys())

    for link in h_links.values():
        link.y1 = random.randint(link.y1+1, link.y2-3)
        link.y2 = link.y1+2

    for link in v_links.values():
        link.x1 = random.randint(link.x1+1, link.x2-3)
        link.x2 = link.x1+2

    for u, room in rooms.items():
        m, n = u
        x1_base = 9*m+1
        x2_base = 9*m+9
        y1_base = 9*n+1
        y2_base = 9*n+9

        h_neighbors = [r for key, r in h_links.items() if u in key]
        v_neighbors = [r for key, r in v_links.items() if u in key]

        x1 = min((r.x1 for r in v_neighbors), default=x1_base+3)
        x2 = max((r.x2 for r in v_neighbors), default=x1_base+5)
        y1 = min((r.y1 for r in h_neighbors), default=y1_base+3)
        y2 = max((r.y2 for r in h_neighbors), default=y1_base+5)

        room.x1 = x1
        room.x2 = x2
        room.y1 = y1
        room.y2 = y2

        if not(min(room.w, room.h) == 2 and max(room.w, room.h) >= 4):
            room.x1 = random.randint(x1_base, x1-1)
            room.x2 = random.randint(x2+1, x2_base)
            room.y1 = random.randint(y1_base, y1-1)
            room.y2 = random.randint(y2+1, y2_base)

    for (m, n), link in h_links.items():
        link.x1 = min(rooms[m].x2, rooms[n].x2)
        link.x2 = max(rooms[m].x1, rooms[n].x1)

    for (m, n), link in v_links.items():
        link.y1 = min(rooms[m].y2, rooms[n].y2)
        link.y2 = max(rooms[m].y1, rooms[n].y1)

    floor = MultiArray((64, 28))
    floor[:] = False

    for i, room in enumerate(rooms.values()):
        floor[room.x1:room.x2, room.y1:room.y2] = True

    for room in h_links.values():
        floor[room.x1:room.x2, room.y1:room.y2] = True

    for room in v_links.values():
        floor[room.x1:room.x2, room.y1:room.y2] = True

    endpoints = [
        room for room_key, room in rooms.items()
        if len([link_key for link_key in links if room_key in link_key]) == 1
    ]
    rooms = list(rooms.values())

    return floor, rooms, endpoints
