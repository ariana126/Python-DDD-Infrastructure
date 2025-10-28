from ddd.domain import ValueObject


class Identity(ValueObject):
    def __init__(self, id_: str):
        self.__id = id_

    @classmethod
    def from_string(cls, id_: str) -> 'Identity':
        return Identity(id_)

    def as_string(self) -> str:
        return self.__id

    def __str__(self):
        return self.__id

    def __repr__(self):
        return f"Identity({self.__id})"