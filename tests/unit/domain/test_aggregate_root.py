from assertpy import assert_that
from ddd.domain import AggregateRoot
from ddd.domain import DomainEvent
from ddd.domain.value import Identity


class DummyDomainEvent(DomainEvent):
    pass

class StubAggregateRoot(AggregateRoot):
    def capture_event(self, event: DomainEvent) -> None:
        self._record_that(event)

def test_domain_events_will_be_released_only_once_from_a_aggregate_root() -> None:
    # arrange
    sut: AggregateRoot = StubAggregateRoot(Identity.from_string('dummy-id'))
    sut.capture_event(DummyDomainEvent())

    # act
    events: list[DomainEvent] = sut.release_events()

    # assert
    assert_that(sut.release_events()).is_empty()
    assert_that(events).is_not_empty()