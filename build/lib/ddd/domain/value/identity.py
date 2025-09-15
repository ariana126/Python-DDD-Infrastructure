from ddd.domain import ValueObject


class Identity(ValueObject):
    def __init__(self, id_: str):
        self.__id = id_

    @classmethod
    def from_string(cls, id_: str) -> 'Identity':
        return Identity(id_)

    def id(self) -> str:
        return self.__id