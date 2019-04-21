from ecs.components.consumables import Consumable
from ecs.components.criticals.abc import CriticalComponent


class Entity:
    def __init__(self, *components):
        self.components = {}

        for component in components:
            self.attach(component)

    def __getitem__(self, key):
        return self.components[key]

    def attach(self, component):
        if isinstance(component, Consumable):
            key = Consumable
        elif isinstance(component, CriticalComponent):
            key = CriticalComponent
        else:
            key = type(component)

        self.components[key] = component

    def remove(self, key):
        if key in self.components:
            del self.components[key]

    def __contains__(self, key):
        return key in self.components
