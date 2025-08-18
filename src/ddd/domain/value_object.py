from abc import ABC
from typing import Any


class ValueObject(ABC):
    def equals(self, other: Any) -> bool:
        pass