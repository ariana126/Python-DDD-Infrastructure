import pytest

from ddd.framework.mutability import Immutable

class DummyImmutableClass(Immutable):
    def __init__(self):
        self.dummy_attribute = 'dummy-value'

def test_an_attribute_of_an_immutable_object_can_not_be_modified()->None:
    # arrange
    sut = DummyImmutableClass()

    # act

    # assert
    with pytest.raises(AttributeError):
        sut.dummy_attribute = 'another-value'

def test_an_attribute_of_an_immutable_object_can_be_deleted()->None:
    # arrange
    sut = DummyImmutableClass()

    # act

    # assert
    with pytest.raises(AttributeError):
        del sut.dummy_attribute

def test_a_new_attribute_can_not_be_added_to_an_immutable_object()->None:
    # arrange
    sut = DummyImmutableClass()

    # act

    # assert
    with pytest.raises(AttributeError):
        sut.new_attribute = 'dummy-value'