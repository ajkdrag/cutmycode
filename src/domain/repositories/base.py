from abc import ABC, abstractmethod
from src.domain.entities import Entity


class CRUDRepository(ABC):
    """Base class for all repositories"""

    @abstractmethod
    def get(self, id: int) -> Entity: ...

    @abstractmethod
    def create(self, entity: Entity): ...

    @abstractmethod
    def update(self, entity: Entity): ...

    @abstractmethod
    def delete(self, id: int) -> bool: ...
