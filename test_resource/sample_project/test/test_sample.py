"""Sample Project"""


from source.sample import add


def test_add():  # pylint: disable=R0201
    """sample test"""
    expect_value = add(1, 2)
    assert expect_value == 3
