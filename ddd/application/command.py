from abc import ABC, abstractmethod
from typing import Any

from underpy import Encapsulated, Immutable, ServiceClass


class Command(Encapsulated, Immutable, ABC):
    pass


class CommandHandler(ServiceClass, ABC):
    @abstractmethod
    def handle(self, command: Command) -> Any:
        pass