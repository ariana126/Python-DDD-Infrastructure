from abc import ABC, abstractmethod
from typing import TypeVar

from ddd import Identity, AggregateRoot

AggregateRootType = TypeVar('AggregateRootType', bound='AggregateRoot')


class EntityNotFound(RuntimeError):
    @staticmethod
    def with_id(_id: Identity) -> 'EntityNotFound':
        return EntityNotFound(f'Entity with id {_id} not found.')


class EntityRepository(ABC):
    def get(self, _id: Identity) -> AggregateRootType:
        aggregate_root = self.find(_id)
        if aggregate_root is None:
            raise EntityNotFound.with_id(_id)
        return aggregate_root

    @abstractmethod
    def find(self, _id: Identity) -> AggregateRootType | None:
        pass

    @abstractmethod
    def save(self, entity: AggregateRoot) -> None:
        pass