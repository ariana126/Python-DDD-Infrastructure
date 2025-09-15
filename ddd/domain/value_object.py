from abc import ABC
from typing import Any
from underpy import Immutable, Encapsulated


class ValueObject(Encapsulated, Immutable, ABC):
    def equals(self, other: Any) -> bool:
        if not isinstance(other, self.__class__):
            return False
        return self.__attributes() == other.__attributes()

    def __eq__(self, other: Any) -> bool:
        return self.equals(other)
    def __ne__(self, other: Any) -> bool:
        return not self.__eq__(other)
    def __hash__(self) -> int:
        return hash(self.__attributes())

    def __attributes(self) -> tuple:
        values = []
        for field in sorted(self.__dict__):
            value = getattr(self, field)
            # Handle nested ValueObjects
            if isinstance(value, ValueObject):
                values.append(value.__attributes())
            else:
                values.append(value)
        return tuple(values)