from assertpy import assert_that

from ddd import Identity


def test_two_new_ids_are_not_equal() -> None:
    identity1 = Identity.new()
    identity2 = Identity.new()

    assert_that(identity1).is_not_equal_to(identity2)