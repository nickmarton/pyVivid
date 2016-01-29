"""LineSegment unit tests."""

import pytest
from vivid.classes.point import Point
from vivid.classes.line_segment import LineSegment


def test___init__():
    """Test LineSegment constructor."""
    def test_ValueError(start_point, end_point):
        """Test constructor for ValueErrors with given params."""
        with pytest.raises(ValueError) as excinfo:
            LineSegment(start_point, end_point)

    test_ValueError(None, None)
    test_ValueError(None, object)
    test_ValueError(object, object)
    test_ValueError(Point(1.0), None)
    test_ValueError(Point(1.0), Point('x'))
    test_ValueError(Point(1.0), Point(1.0, 1.0))


def test___eq__():
    """Test == operator."""
    assert LineSegment(Point(1.0), Point(1.0)) == LineSegment(Point(1.0), Point(1.0))
    assert not LineSegment(Point(1.0), Point(1.0)) == LineSegment(Point('x'), Point('x'))
    assert not LineSegment(Point(1.0), Point(1.0)) == LineSegment(Point(1.0, 1.0), Point(1.0, 1.0))


def test___ne__():
    """Test != operator."""
    assert not LineSegment(Point(1.0), Point(1.0)) != LineSegment(Point(1.0), Point(1.0))
    assert LineSegment(Point(1.0), Point(1.0)) != LineSegment(Point('x'), Point('x'))
    assert LineSegment(Point(1.0), Point(1.0)) != LineSegment(Point(1.0, 1.0), Point(1.0, 1.0))


def test_total_ordering():
    """Test ."""
    a = LineSegment(Point(1.0), Point(2.0))
    b = LineSegment(Point(0.0), Point(2.0))
    c = LineSegment(Point(1.0), Point(3.0))
    d = LineSegment(Point(0.0), Point(3.0))
    e = LineSegment(Point('x'), Point('x'))

    assert a <= a
    assert not a < a
    assert a >= a
    assert not a > a
    assert a <= b
    assert a < b
    assert a <= c
    assert a < c
    assert a <= d
    assert a < d
    assert a <= e
    assert a < e
    assert b >= a
    assert b > a
    assert c >= a
    assert c > a
    assert d >= a
    assert d > a
    assert e >= a
    assert e > a
    assert a < b < d < e

    a = LineSegment(Point(1.0, 1.0, 1.0, 1.0), Point(2.0, 2.0, 2.0, 2.0))
    b = LineSegment(Point(0.0, 0.0, 0.0, 0.0), Point(2.0, 2.0, 2.0, 2.0))
    c = LineSegment(Point(1.0, 1.0, 1.0, 1.0), Point(3.0, 3.0, 3.0, 3.0))
    d = LineSegment(Point(0.0, 0.0, 0.0, 0.0), Point(3.0, 3.0, 3.0, 3.0))
    e = LineSegment(Point('x', 'x', 'x', 'x'), Point('x', 'x', 'x', 'x'))

    assert a <= a
    assert not a < a
    assert a >= a
    assert not a > a
    assert a <= b
    assert a < b
    assert a <= c
    assert a < c
    assert a <= d
    assert a < d
    assert a <= e
    assert a < e
    assert b >= a
    assert b > a
    assert c >= a
    assert c > a
    assert d >= a
    assert d > a
    assert e >= a
    assert e > a
    assert a < b < d < e

    a = LineSegment(Point(1.0, 1.0), Point(2.0, 2.0))
    b = LineSegment(Point(0.0, 1.0), Point(2.0, 2.0))

    assert not a < b
    assert not a > b
    assert not a <= b
    assert not a >= b


def test___contains__():
    """Test in operator."""
    def test_AttributeError(member, segment):
        """Test constructor for AttributeErrors with given params."""
        with pytest.raises(AttributeError) as excinfo:
            member in segment

    a = LineSegment(Point(1.0), Point(2.0))
    b = LineSegment(Point(0.0), Point(2.0))
    c = LineSegment(Point(1.0), Point(3.0))
    d = LineSegment(Point(0.0), Point(3.0))
    e = LineSegment(Point('x'), Point('x'))
    p = Point(1.5)

    test_AttributeError('', a)
    test_AttributeError(None, a)
    test_AttributeError(object, a)

    assert a in a
    assert a in b
    assert b not in c
    assert a in c
    assert a in d
    assert a in e
    assert p in a
    assert p in b
    assert p in c
    assert p in d
    assert p in e

    a = LineSegment(Point(1.0, 1.0, 1.0), Point(2.0, 2.0, 2.0))
    b = LineSegment(Point(0.0, 0.0, 0.0), Point(2.0, 2.0, 2.0))
    c = LineSegment(Point(1.0, 1.0, 1.0), Point(3.0, 3.0, 3.0))
    d = LineSegment(Point(0.0, 0.0, 0.0), Point(3.0, 3.0, 3.0))
    e = LineSegment(Point('x', 'x', 'x'), Point('x', 'x', 'x'))
    p = Point(1.5, 1.5, 1.5)

    assert a in a
    assert a in b
    assert b not in c
    assert a in c
    assert a in d
    assert a in e
    assert p in a
    assert p in b
    assert p in c
    assert p in d
    assert p in e


def test___deepcopy__():
    """Test copy.deepcopy."""
    from copy import deepcopy
    a = LineSegment(Point(1.0), Point(2.0))
    b = deepcopy(a)

    assert a == b
    assert a is not b
    assert a[0] is not b[0]
    assert a[1] is not b[1]


def test___getitem__():
    """Test indexing."""
    def test_TypeError(index, segment):
        """Test constructor for TypeErrors with given params."""
        with pytest.raises(TypeError) as excinfo:
            segment[index]

    def test_IndexError(index, segment):
        """Test constructor for IndexErrors with given params."""
        with pytest.raises(IndexError) as excinfo:
            segment[index]

    p1, p2 = Point(1.0), Point(2.0)
    a = LineSegment(p1, p2)
    assert a[0] == p1
    assert a[1] == p2

    test_TypeError(a, a)
    test_TypeError('', a)
    test_TypeError(None, a)
    test_TypeError(object, a)
    test_IndexError(-1, a)
    test_IndexError(2, a)


def test___hash__():
    """Test hash(LineSegment)."""
    p1, p2 = Point(1.0), Point(2.0)
    a = LineSegment(p1, p2)
    assert hash(a) == 2847735836036288514


def test___str__():
    """Test str(LineSegment)."""
    p1, p2 = Point(1.0), Point(2.0)
    p3, p4 = Point(1.0, 1.0, 1.0), Point(2.0, 2.0, 2.0)
    a = LineSegment(p1, p2)
    b = LineSegment(p3, p4)
    assert str(a) == "L(P(1.0),P(2.0))"
    assert str(b) == "L(P(1.0,1.0,1.0),P(2.0,2.0,2.0))"


def test___repr__():
    """Test repr(LineSegment)."""
    p1, p2 = Point(1.0), Point(2.0)
    p3, p4 = Point(1.0, 1.0, 1.0), Point(2.0, 2.0, 2.0)
    a = LineSegment(p1, p2)
    b = LineSegment(p3, p4)
    assert repr(a) == "L(P(1.0),P(2.0))"
    assert repr(b) == "L(P(1.0,1.0,1.0),P(2.0,2.0,2.0))"


def test__key():
    """Test key used in hashing."""
    a = LineSegment(Point(1.0), Point(2.0))
    assert a._key() == (Point(1.0), Point(2.0))


def test_meets():
    """Test meets wrapper for Point function."""
    a = LineSegment(Point(0.0, 0.0), Point(5.0, 5.0))
    b = LineSegment(Point(0.0, 0.0), Point(5.0, 5.0))
    p1 = Point(0.0, 0.0)
    p2 = Point(1.0, 1.0)
    p3 = Point(5.0, 5.0)
    assert LineSegment.meets(p1, a, b)
    assert LineSegment.meets(p2, a, b)
    assert LineSegment.meets(p3, a, b)
    c = LineSegment(Point(5.0, 0.0), Point(0.0, 5.0))
    p4 = Point(2.5, 2.5)
    assert not LineSegment.meets(p1, a, c)
    assert not LineSegment.meets(p2, a, c)
    assert not LineSegment.meets(p3, a, c)
    assert LineSegment.meets(p4, a, c)


def test_unstringify():
    """Test unstringify function for LineSegment."""
    p1, p2 = Point(1.0), Point(2.0)
    p3, p4 = Point(1.0, 1.0, 1.0), Point(2.0, 2.0, 2.0)
    a = LineSegment(p1, p2)
    b = LineSegment(p3, p4)
    assert a == LineSegment.unstringify("L(P(1.0),P(2.0))")
    assert b == LineSegment.unstringify("L(P(1.0,1.0,1.0),P(2.0,2.0,2.0))")
