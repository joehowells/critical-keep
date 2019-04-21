from abc import ABC, abstractmethod
from typing import Any, Dict, List, Tuple, TYPE_CHECKING


if TYPE_CHECKING:
    from ecs.entity import Entity


class CriticalComponent(ABC):
    @abstractmethod
    def critical(self, attacker: 'Entity', defender: 'Entity') -> List[Tuple[str, Dict[str, Any]]]:
        ...

    @abstractmethod
    def damage(self, attacker: 'Entity', defender: 'Entity') -> int:
        ...
