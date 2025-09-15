from abc import ABC
from typing import Any
from ddd.domain.value import Identity
from underpy import Encapsulated


class Entity(Encapsulated, ABC):
    def __init__(self, id_: Identity):
        self._id = id_

    def id(self) -> Identity:
        return self._id

    def equals(self, other: Any) -> bool:
        if not isinstance(other, self.__class__):
            return False
        return self._id.equals(other.id())

    def __eq__(self, other: Any) -> bool:
        return self.equals(other)
    def __ne__(self, other: Any) -> bool:
        return not self.equals(other)