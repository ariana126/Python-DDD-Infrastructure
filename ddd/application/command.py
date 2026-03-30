from abc import ABC, abstractmethod
from typing import Any

from underpy import Immutable


class Command(Immutable, ABC):
    pass


class CommandHandler(Immutable, ABC):
    @abstractmethod
    def handle(self, command: Command) -> Any:
        pass