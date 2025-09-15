from abc import ABC
from underpy import Encapsulated, Immutable


class Command(Encapsulated, Immutable, ABC):
    pass