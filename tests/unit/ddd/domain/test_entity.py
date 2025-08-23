from assertpy import assert_that
from ddd.domain.entity import Entity
from ddd.domain.value.identity import Identity


class DummyEntity(Entity):
    def __init__(self, id_: Identity, property_: str) -> None:
        self.__property = property_
        super().__init__(id_)

def test_two_entities_are_equal_by_their_ids_even_with_different_properties()->None:
    # arrange
    id_: Identity = Identity.from_string('dummy-id')
    sut: Entity = DummyEntity(id_, 'dummy_property1')
    other: Entity = DummyEntity(id_, 'dummy_property2')

    # act

    # assert
    assert_that(sut.equals(other)).is_true()
    assert_that(sut == other).is_true()
    assert_that(sut != other).is_false()
    assert_that(sut).is_equal_to(other)

