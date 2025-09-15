import pytest
from assertpy.assertpy import assert_that
from ddd.domain import ValueObject


class StubValueObject(ValueObject):
    def __init__(self, value: str) -> None:
        self.__value = value

def test_two_value_objects_are_equals_based_on_their_values() -> None:
    # arrange
    dummy_value: str = 'dummy-value'
    sut: StubValueObject = StubValueObject(dummy_value)
    other_value: StubValueObject = StubValueObject(dummy_value)

    # act

    # assert
    assert_that(sut.equals(other_value)).is_true()
    assert_that(sut == other_value).is_true()
    assert_that(sut != other_value).is_false()
    assert_that(sut).is_equal_to(other_value)

def test_two_value_objects_with_the_same_values_have_the_same_hash() -> None:
    # arrange
    dummy_value: str = 'dummy-value'
    sut: StubValueObject = StubValueObject(dummy_value)
    other_value: StubValueObject = StubValueObject(dummy_value)

    # act

    # assert
    assert_that(hash(sut)).is_equal_to(hash(other_value))

def test_an_attribute_of_a_value_object_can_not_be_modified_after_initiation() -> None:
    # arrange
    sut: StubValueObject = StubValueObject('dummy-value')

    # act

    # assert
    with pytest.raises(BaseException):
        sut.value = 'some-other-value'

def test_an_attribute_of_a_value_object_can_not_be_deleted_after_initiation() -> None:
    # arrange
    sut: StubValueObject = StubValueObject('dummy-value')

    # act

    # assert
    with pytest.raises(BaseException):
        del sut.value

def test_a_new_attribute_can_not_be_added_to_a_value_object_that_has_been_initiated() -> None:
    # arrange
    sut: StubValueObject = StubValueObject('dummy-value')

    # act

    # assert
    with pytest.raises(BaseException):
        sut.new_attribute = ''

def test_a_value_object_private_attribute_can_not_be_seen_out_side_the_object()-> None:
    # arrange
    sut: StubValueObject = StubValueObject('dummy-value')

    # act

    # assert
    with pytest.raises(BaseException):
        x = sut.__value

def test_a_value_object_private_method_can_not_be_called_out_side_the_object()-> None:
    # arrange
    sut: StubValueObject = StubValueObject('dummy-value')

    # act

    # assert
    with pytest.raises(BaseException):
        x = sut.__attributes()