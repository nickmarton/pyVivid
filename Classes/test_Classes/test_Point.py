"""Point unit tests."""

import pytest
from vivid.Classes.Point import Point


def test___init__():
    """Test Point constructor."""
    def test_TypeError(*dimension_values):
        """Test constructor for TypeErrors with given params."""
        with pytest.raises(TypeError) as excinfo:
            Point(*dimension_values)

    def test_ValueError(*dimension_values):
        """Test constructor for ValueErrors with given params."""
        with pytest.raises(ValueError) as excinfo:
            Point(*dimension_values)

    test_ValueError()
    test_TypeError(1)
    test_TypeError('')
    test_TypeError(None)
    test_TypeError(object)

    coords = (1.0, 2.0, 3.0)
    p = Point(*coords)

    assert p._coordinate is not coords


def test___eq__():
    """Test == operator for Point object."""
    p1 = Point(1.0)
    p2 = Point(1.0)
    p3 = Point(1.0, 2.0, 3.0)
    p4 = Point(1.0, 2.0, 3.0)
    p5 = Point('x')
    p6 = Point('x')
    p7 = Point('x', 'x', 'x')
    p8 = Point('x', 'x', 'x')

    assert p1 == p2
    assert p3 == p4
    assert p5 == p6
    assert p7 == p8


def test___ne__():
    """Test != operator for Point object."""
    p1 = Point(1.0)
    p2 = Point(1.0)
    p3 = Point(1.0, 2.0, 3.0)
    p4 = Point(1.0, 2.0, 3.0)
    p5 = Point('x')
    p6 = Point('x')
    p7 = Point('x', 'x', 'x')
    p8 = Point('x', 'x', 'x')

    assert not p1 != p2
    assert not p3 != p4
    assert not p5 != p6
    assert not p7 != p8

    p1 = Point(1.0)
    p2 = Point(2.0)
    p3 = Point(1.0, 2.0, 3.0)
    p4 = Point(3.0, 4.0, 5.0)
    p5 = Point(1.0, 2.0)
    p6 = Point(2.0, 1.0)

    assert p1 != p2
    assert p3 != p4
    assert p5 != p6


def test___deepcopy__():
    """Test copy.deepcopy for Point object."""
    from copy import deepcopy

    p1 = Point(1.0)
    p2 = Point(1.0, 2.0)

    p1_copy = deepcopy(p1)
    p2_copy = deepcopy(p2)

    assert p1 == p1_copy
    assert p1 is not p1_copy
    assert p2 == p2_copy
    assert p2 is not p2_copy


def test__key():
    """Test key of Point used for hashing."""
    coords = (1.0, 2.0, 3.0)
    p = Point(*coords)
    assert p._key() == coords


def test___hash__():
    """Test hash of Point."""
    coords = (1.0, 2.0, 3.0)
    p = Point(*coords)
    assert hash(p) == 2528502973977326415


def test___str__():
    """Test str(Point)."""
    assert Point(1.0, 2.0, 3.0).__str__() == "P(1.0,2.0,3.0)"
    assert Point('x', 'x', 'x').__str__() == "P(x,x,x)"


def test___repr__():
    """Test repr(Point)."""
    assert Point(1.0, 2.0, 3.0).__repr__() == "P(1.0,2.0,3.0)"
    assert Point('x', 'x', 'x').__repr__() == "P(x,x,x)"
