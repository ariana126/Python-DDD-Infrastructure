from abc import ABC
from ddd.domain import DomainEvent
from ddd.domain import Entity
from ddd.domain.value import Identity


class AggregateRoot(Entity, ABC):
    def __init__(self, id_: Identity):
        self.__events: list[DomainEvent] = []
        super().__init__(id_)

    def release_events(self)->list[DomainEvent]:
        events: list[DomainEvent] = self.__events
        self.__events = []
        return events

    def _record_that(self, event: DomainEvent) -> None:
        self.__events.append(event)

