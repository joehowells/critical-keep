import random


class RandomNumberComponent:
    def __init__(self):
        self.number: int = random.randint(0, 99)
