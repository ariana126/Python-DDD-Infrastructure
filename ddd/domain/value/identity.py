import uuid

from ddd.domain import ValueObject


class Identity(ValueObject):
    def __init__(self, id_: str):
        self.__id = id_

    @staticmethod
    def new() -> 'Identity':
        return Identity(str(uuid.uuid4()))

    @classmethod
    def from_string(cls, id_: str) -> 'Identity':
        return Identity(id_)

    @property
    def as_string(self) -> str:
        return self.__id

    def __str__(self):
        return self.__id