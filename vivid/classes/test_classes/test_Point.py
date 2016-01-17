"""Point unit tests."""

import pytest
from vivid.classes.point import Point


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


def test_is_on():
    """Test is_on function used in LRB paper."""
    point = Point(1.0)
    start_point = Point(0.0)
    end_point = Point(3.0)
    assert point.is_on(start_point, end_point)
    assert point.is_on(end_point, start_point)

    point = Point(1.0, 1.0)
    start_point = Point(0.0, 0.0)
    end_point = Point(3.0, 3.0)
    assert point.is_on(start_point, end_point)
    assert point.is_on(end_point, start_point)

    point = Point(1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0)
    start_point = Point(0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0)
    end_point = Point(3.0, 3.0, 3.0, 3.0, 3.0, 3.0, 3.0, 3.0, 3.0, 3.0)
    assert point.is_on(start_point, end_point)
    assert point.is_on(end_point, start_point)

    point = Point(1.000000000000001)
    start_point = Point(0.000000000000001)
    end_point = Point(3.000000000000001)
    assert point.is_on(start_point, end_point)
    assert point.is_on(end_point, start_point)


def test_not_same_point():
    """Test not_same_point function used in LRB paper."""
    point_1 = Point(1.0)
    point_2 = Point(0.0)
    assert point_1.not_same_point(point_2)

    point_1 = Point(1.0, 1.0)
    point_2 = Point(0.0, 0.0)
    assert point_1.not_same_point(point_2)

    point_1 = Point(1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0)
    point_2 = Point(0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0)
    assert point_1.not_same_point(point_2)

    point_1 = Point(1.000000000000001)
    point_2 = Point(0.000000000000001)
    assert point_1.not_same_point(point_2)


def test_clocks_unequal():
    """Test clocks_unequal function used in LRB paper."""

    point_1 = Point(1.0, 1.0)
    point_2 = Point(0.0, 0.0)
    assert point_1.clocks_unequal(point_2)

    point_1 = Point(1.0, 1.0, 1.0, 1.0)
    point_2 = Point(0.0, 0.0, 0.0, 0.0)
    assert point_1.clocks_unequal(point_2)

    point_1 = Point(0.0, 1.000000000000001)
    point_2 = Point(0.0, 0.000000000000001)
    assert point_1.clocks_unequal(point_2)


def test_can_observe():
    """Test can_observe function used in LRB paper."""
    point = Point(1.0, 1.0, 1.0, 1.0)
    spacetime_loc = Point(0.0, 0.0, 0.0, 0.0)
    worldline_start = Point(-10.0, -10.0, -10.0, -10.0)
    worldline_end = Point(10.0, 10.0, 10.0, 10.0)
    assert point.can_observe(spacetime_loc, worldline_start, worldline_end)
    spacetime_loc = Point(1.0, 1.0, 1.0, 1.0)
    assert point.can_observe(spacetime_loc, worldline_start, worldline_end)


def test_meets():
    """Test meets function used in LRB paper."""
    spacetime_loc = Point(0.0, 0.0, 0.0, 0.0)
    worldline_1_start = Point(-10.0, -10.0, -10.0, -10.0)
    worldline_1_end = Point(10.0, 10.0, 10.0, 10.0)
    worldline_2_start = Point(10.0, 10.0, 10.0, 10.0)
    worldline_2_end = Point(-10.0, -10.0, -10.0, -10.0)
    assert spacetime_loc.meets(
        worldline_1_start, worldline_1_end, worldline_2_start, worldline_2_end)


def test_unstringify():
    """Test Point object reconstruction."""
    def test_ValueError(point_string):
        """Test constructor for ValueErrors with given params."""
        with pytest.raises(ValueError) as excinfo:
            Point.unstringify(point_string)

    test_ValueError('asdf')
    test_ValueError('P()')
    test_ValueError('P(xx)')
    test_ValueError('P(,2)')

    p1 = Point('x')
    p2 = Point('x', 'x')
    p3 = Point(1.0)
    p4 = Point(1.0, 1.0)
    assert Point.unstringify(str(p1)) == Point('x')
    assert Point.unstringify(str(p2)) == Point('x', 'x')
    assert Point.unstringify(str(p3)) == Point(1.0)
    assert Point.unstringify(str(p4)) == Point(1.0, 1.0)
