import pytest
from assertpy import assert_that
from ddd.framework.encapsulation import Encapsulated

# TODO: Write test for delete and set.

class Parent(Encapsulated):
    def __init__(self):
        self.public_attribute = 'public'
        self._protected_attribute = 'protected'
        self.__private_attribute = 'private'

    def public_method(self) -> str:
        return self.public_attribute
    def _protected_method(self) -> str:
        return self._protected_attribute
    def __private_method(self) -> str:
        return self.__private_attribute

class Child(Parent):
    def get_public_attribute(self) -> str:
        return self.public_attribute
    def get_protected_attribute(self) -> str:
        return self._protected_attribute
    def get_private_attribute(self) -> str:
        return self.__private_attribute

    def call_public_method(self) -> str:
        return self.public_method()
    def call_protected_method(self) -> str:
        return self._protected_method()
    def call_private_method(self) -> str:
        return self.__private_method()

def test_public_attribute_can_be_accessed_out_side_the_object() -> None:
    # arrange
    sut: Child = Child()

    # act
    public_value = sut.public_attribute

    # assert
    assert_that(public_value).is_equal_to('public')

def test_public_attribute_can_be_accessed_in_the_child_class() -> None:
    # arrange
    sut: Child = Child()

    # act
    public_value = sut.get_public_attribute()

    # assert
    assert_that(public_value).is_equal_to('public')

def test_protected_attribute_can_not_be_accessed_out_side_the_object() -> None:
    # arrange
    sut: Child = Child()

    # act

    # assert
    with pytest.raises(AttributeError):
        x = sut._protected_attribute

def test_protected_attribute_can_be_accessed_in_the_child_class() -> None:
    # arrange
    sut: Child = Child()

    # act
    protected_value = sut.get_protected_attribute()

    # assert
    assert_that(protected_value).is_equal_to('protected')

def test_private_attribute_can_not_be_accessed_out_side_the_object() -> None:
    # arrange
    sut: Child = Child()

    # act

    # assert
    with pytest.raises(AttributeError):
        sut.get_private_attribute()

def test_public_method_can_be_accessed_out_side_the_object() -> None:
    # arrange
    sut: Child = Child()

    # act
    public_value = sut.public_method()

    # assert
    assert_that(public_value).is_equal_to('public')

def test_public_method_can_be_accessed_in_the_child_class() -> None:
    # arrange
    sut: Child = Child()

    # act
    public_value = sut.call_public_method()

    # assert
    assert_that(public_value).is_equal_to('public')

def test_protected_method_can_not_be_accessed_out_side_the_object() -> None:
    # arrange
    sut: Child = Child()

    # act

    # assert
    with pytest.raises(AttributeError):
        sut._protected_method()

def test_protected_method_can_be_accessed_in_child_class() -> None:
    # arrange
    sut: Child = Child()

    # act
    protected_value = sut.call_protected_method()

    # assert
    assert_that(protected_value).is_equal_to('protected')

def test_private_method_can_not_be_accessed_out_side_the_object() -> None:
    # arrange
    sut: Child = Child()

    # act

    # assert
    with pytest.raises(AttributeError):
        sut.__private_method()

def test_private_method_can_not_be_accessed_in_the_child_class() -> None:
    # arrange
    sut: Child = Child()

    # act

    # assert
    with pytest.raises(AttributeError):
        sut.call_private_method()