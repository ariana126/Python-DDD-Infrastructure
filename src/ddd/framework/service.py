from abc import ABC
from ddd.framework.encapsulation import Encapsulated
from ddd.framework.mutability import Immutable


class ServiceClass(Encapsulated, Immutable, ABC):
    pass