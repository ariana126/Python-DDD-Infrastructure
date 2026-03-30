from assertpy import assert_that

from ddd import EntityRepository, AggregateRoot, Identity
from ddd.domain.service.repository import AggregateRootType


class SpyEntityRepository(EntityRepository):
    def __init__(self):
        self.__db: dict[str, AggregateRoot] = {}

    def find(self, _id: Identity) -> AggregateRootType | None:
        if _id.as_string not in self.__db:
            return None
        return self.__db[_id.as_string]

    def save(self, entity: AggregateRoot) -> None:
        self.__db[entity.id.as_string] = entity

    def assert_database_is_empty(self) -> None:
        assert_that(self.__db).is_empty()