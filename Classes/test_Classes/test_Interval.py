"""Interval class unit tests."""

import pytest
from vivid.Classes.Interval import Interval


def test___init__():
    """Test construction of Interval object."""
    def test_ValueError(inf, sup):
        """Test ValueError catching."""
        with pytest.raises(ValueError) as excinfo:
            Interval(inf, sup)

    def test_TypeError(inf, sup):
        """Test TypeError catching."""
        with pytest.raises(TypeError) as excinfo:
            Interval(inf, sup)

    # test standard invalid params
    test_TypeError('', '')
    test_TypeError(None, None)
    test_TypeError(object, object)
    # test type mismatch
    test_TypeError(1, 1.0)
    test_TypeError(1.0, 1)
    test_TypeError(1.0, 1L)
    test_TypeError(1L, 1.0)
    test_TypeError(1L, 1)
    test_TypeError(1, 1L)
    # test inf >= sup
    test_ValueError(10, 5)
    test_ValueError(5, 5)


def test___lt__():
    """Test < operator for Interval; [i, s](i' s')."""
    # test standard less than
    assert Interval(-1, 0) < Interval(1, 2)
    assert Interval(-1.0, 0.0) < Interval(1.0, 2.0)
    assert Interval(-1L, 0L) < Interval(1L, 2L)
    # test strictly less than
    assert not Interval(-1, 0) < Interval(0, 1)
    assert not Interval(-1.0, 0.0) < Interval(0.0, 1.0)
    assert not Interval(-1L, 0L) < Interval(0L, 1L)
    # test not less than
    assert not Interval(8, 9) < Interval(0, 1)
    assert not Interval(8.0, 9.0) < Interval(0.0, 1.0)
    assert not Interval(8L, 9L) < Interval(0L, 1L)


def test___le__():
    """Implement overloaded <= operator for Interval; (i',[i, s'), s]"""
    # test standard greater than or equal to
    assert Interval(0, 5) <= Interval(3, 8)
    assert Interval(0.0, 5.0) <= Interval(3.0, 8.0)
    assert Interval(0L, 5L) <= Interval(3L, 8L)
    # test (i' s')[i s]
    assert not Interval(0, 5) <= Interval(-5, -3)
    assert not Interval(0.0, 5.0) <= Interval(-5.0, -3.0)
    assert not Interval(0L, 5L) <= Interval(-5L, -3L)
    # test [i s](i' s')
    assert not Interval(8, 9) <= Interval(90, 100)
    assert not Interval(8.0, 9.0) <= Interval(90.0, 100.0)
    assert not Interval(8L, 9L) <= Interval(90L, 100L)
    # test [i' (i s'] s)
    assert not Interval(0, 5) <= Interval(-2, 3)
    assert not Interval(0.0, 5.0) <= Interval(-2.0, 3.0)
    assert not Interval(0L, 5L) <= Interval(-2L, 3L)
    # test [i' (i s) s']
    assert not Interval(0, 5) <= Interval(-5, 10)
    assert not Interval(0.0, 5.0) <= Interval(-5.0, 10.0)
    assert not Interval(0L, 5L) <= Interval(-5L, 10L)
    # test [i (i' s') s]
    assert not Interval(-10, 15) <= Interval(-5, 10)
    assert not Interval(-10.0, 15.0) <= Interval(-5.0, 10.0)
    assert not Interval(-10L, 15L) <= Interval(-5L, 10L)
    # test (i', s') == (i, s)
    assert not Interval(-10, 15) <= Interval(-10, 15)
    assert not Interval(-10.0, 15.0) <= Interval(-10.0, 15.0)
    assert not Interval(-10L, 15L) <= Interval(-10L, 15L)


def test___eq__():
    """Test == operator for Interval object."""
    assert Interval(0, 1) == Interval(0, 1)
    assert Interval(0.0, 1.0) == Interval(0.0, 1.0)
    assert Interval(0L, 1L) == Interval(0L, 1L)
    assert not Interval(0, 1) == Interval(0.0, 1.0)
    assert not Interval(0, 1) == Interval(0L, 1L)
    assert not Interval(0.0, 1.0) == Interval(0, 1)
    assert not Interval(0.0, 1.0) == Interval(0L, 1L)
    assert not Interval(0L, 1L) == Interval(0, 1)
    assert not Interval(0L, 1L) == Interval(0.0, 1.0)


def test___ge__():
    """Implement overloaded >= operator for Interval; (i',[i, s'), s]"""
    # test standard greater than or equal to
    assert Interval(3, 8) >= Interval(0, 5)
    assert Interval(3.0, 8.0) >= Interval(0.0, 5.0)
    assert Interval(3L, 8L) >= Interval(0L, 5L)
    # test [i s](i' s')
    assert not Interval(-5, -3) >= Interval(0, 5)
    assert not Interval(-5.0, -3.0) >= Interval(0.0, 5.0)
    assert not Interval(-5L, -3L) >= Interval(0L, 5L)
    # test (i' s')[i s]
    assert not Interval(90, 100) >= Interval(8, 9)
    assert not Interval(90.0, 100.0) >= Interval(8.0, 9.0)
    assert not Interval(90L, 100L) >= Interval(8L, 9L)
    # test [i (i' s] s')
    assert not Interval(-2, 3) >= Interval(0, 5)
    assert not Interval(-2.0, 3.0) >= Interval(0.0, 5.0)
    assert not Interval(-2L, 3L) >= Interval(0L, 5L)
    # test [i (i' s') s]
    assert not Interval(-5, 10) >= Interval(0, 5)
    assert not Interval(-5.0, 10.0) >= Interval(0.0, 5.0)
    assert not Interval(-5L, 10L) >= Interval(0L, 5L)
    # test [i' (i s) s']
    assert not Interval(-5, 10) >= Interval(-10, 15)
    assert not Interval(-5.0, 10.0) >= Interval(-10.0, 15.0)
    assert not Interval(-5L, 10L) >= Interval(-10L, 15L)
    # test (i', s') == (i, s)
    assert not Interval(-10, 15) >= Interval(-10, 15)
    assert not Interval(-10.0, 15.0) >= Interval(-10.0, 15.0)
    assert not Interval(-10L, 15L) >= Interval(-10L, 15L)


def test___gt__():
    """Test > operator for Interval; (i' s')[i, s]."""
    # test standard less than
    assert Interval(1, 2) > Interval(-1, 0)
    assert Interval(1.0, 2.0) > Interval(-1.0, 0.0)
    assert Interval(1L, 2L) > Interval(-1L, 0L)
    # test strictly greater than
    assert not Interval(0, 1) > Interval(-1, 0)
    assert not Interval(0.0, 1.0) > Interval(-1.0, 0.0)
    assert not Interval(0L, 1L) > Interval(-1L, 0L)
    # test not greater than
    assert not Interval(0, 1) > Interval(8, 9)
    assert not Interval(0.0, 1.0) > Interval(8.0, 9.0)
    assert not Interval(0L, 1L) > Interval(8L, 9L)


def test___ne__():
    """Test != operator for Interval object."""
    assert not Interval(0, 1) != Interval(0, 1)
    assert not Interval(0.0, 1.0) != Interval(0.0, 1.0)
    assert not Interval(0L, 1L) != Interval(0L, 1L)
    assert Interval(0, 1) != Interval(0.0, 1.0)
    assert Interval(0, 1) != Interval(0L, 1L)
    assert Interval(0.0, 1.0) != Interval(0, 1)
    assert Interval(0.0, 1.0) != Interval(0L, 1L)
    assert Interval(0L, 1L) != Interval(0, 1)
    assert Interval(0L, 1L) != Interval(0.0, 1.0)


def test___or__():
    """Test | operator for Interval."""
    def test_ValueError(i1, i2):
        """Test ValueError catching."""
        with pytest.raises(ValueError) as excinfo:
            i1 | i2

    i1, i2 = Interval(-200, 1000), Interval(50, 100)
    assert i1 | i2 == Interval(-200, 1000)
    i1, i2 = Interval(0, 10), Interval(50, 100)
    test_ValueError(i1, i2)
    i1, i2 = Interval(0, 55), Interval(50, 100)
    assert i1 | i2 == Interval(0, 100)
    i1, i2 = Interval(70, 80), Interval(50, 100)
    assert i1 | i2 == Interval(50, 100)
    i1, i2 = Interval(75, 125), Interval(50, 100)
    assert i1 | i2 == Interval(50, 125)
    i1, i2 = Interval(105, 125), Interval(50, 100)
    test_ValueError(i1, i2)


def test___and__():
    """Test & operator for Interval."""
    def test_ValueError(i1, i2):
        """Test ValueError catching."""
        with pytest.raises(ValueError) as excinfo:
            i1 & i2

    i1, i2 = Interval(-200, 1000), Interval(50, 100)
    assert i1 & i2 == Interval(50, 100)
    i1, i2 = Interval(0, 10), Interval(50, 100)
    test_ValueError(i1, i2)
    i1, i2 = Interval(0, 55), Interval(50, 100)
    assert i1 & i2 == Interval(50, 55)
    i1, i2 = Interval(70, 80), Interval(50, 100)
    assert i1 & i2 == Interval(70, 80)
    i1, i2 = Interval(75, 125), Interval(50, 100)
    assert i1 & i2 == Interval(75, 100)
    i1, i2 = Interval(105, 125), Interval(50, 100)
    test_ValueError(i1, i2)


def test___contains__():
    """Test in operator for Interval."""
    def test_TypeError(interval, key):
        """Test TypeError catching."""
        with pytest.raises(TypeError) as excinfo:
            key in interval
    # test standard greater than or equal to
    assert Interval(3, 8) not in Interval(0, 5)
    assert Interval(3.0, 8.0) not in Interval(0.0, 5.0)
    assert Interval(3L, 8L) not in Interval(0L, 5L)
    # test [i s](i' s')
    assert Interval(-5, -3) not in Interval(0, 5)
    assert Interval(-5.0, -3.0) not in Interval(0.0, 5.0)
    assert Interval(-5L, -3L) not in Interval(0L, 5L)
    # test (i' s')[i s]
    assert Interval(90, 100) not in Interval(8, 9)
    assert Interval(90.0, 100.0) not in Interval(8.0, 9.0)
    assert Interval(90L, 100L) not in Interval(8L, 9L)
    # test [i (i' s] s')
    assert Interval(-2, 3) not in Interval(0, 5)
    assert Interval(-2.0, 3.0) not in Interval(0.0, 5.0)
    assert Interval(-2L, 3L) not in Interval(0L, 5L)
    # test [i (i' s') s]
    assert Interval(-5, 10) not in Interval(0, 5)
    assert Interval(-5.0, 10.0) not in Interval(0.0, 5.0)
    assert Interval(-5L, 10L) not in Interval(0L, 5L)
    # test [i' (i s) s']
    assert Interval(-5, 10) in Interval(-10, 15)
    assert Interval(-5.0, 10.0) in Interval(-10.0, 15.0)
    assert Interval(-5L, 10L) in Interval(-10L, 15L)
    # test (i', s') == (i, s)
    assert Interval(-10, 15) in Interval(-10, 15)
    assert Interval(-10.0, 15.0) in Interval(-10.0, 15.0)
    assert Interval(-10L, 15L) in Interval(-10L, 15L)
    # test type mismatch
    test_TypeError(1.0, Interval(6, 7))
    test_TypeError(1L, Interval(6, 7))
    test_TypeError(1, Interval(6.0, 7.0))
    test_TypeError(1L, Interval(6.0, 7.0))
    test_TypeError(1.0, Interval(6L, 7L))
    test_TypeError(1, Interval(6L, 7L))


def test___getitem__():
    """Test indexing for Interval."""
    def test_IndexError(interval, index):
        """Test IndexError catching."""
        with pytest.raises(IndexError) as excinfo:
            interval[index]

    def test_TypeError(interval, index):
        """Test TypeError catching."""
        with pytest.raises(TypeError) as excinfo:
            Interval[index]

    test_TypeError(Interval(0, 1), "")
    test_IndexError(Interval(0, 1), -1)
    test_IndexError(Interval(0, 1), 2)


def test___deepcopy__():
    """Test copy.deepcopy for Interval object."""
    from copy import deepcopy
    # test ints
    i = Interval(0, 1)
    i_copy = deepcopy(i)
    assert i == i_copy
    assert i_copy is not deepcopy(i)
    # test floats
    i = Interval(0.0, 1.0)
    i_copy = deepcopy(i)
    assert i == i_copy
    assert i_copy is not deepcopy(i)
    # test longs
    i = Interval(0L, 1L)
    i_copy = deepcopy(i)
    assert i == i_copy
    assert i_copy is not deepcopy(i)


def test__key():
    """Test key used for hashing; just 2-tuple."""
    assert Interval(0, 1)._key() == (0, 1)
    assert Interval(0.0, 1.0)._key() == (0.0, 1.0)
    assert Interval(0L, 1L)._key() == (0L, 1L)


def test___hash__():
    """Test hash of Interval."""
    assert hash(Interval(0, 1)) == 3713080549409410656
    assert hash(Interval(0.0, 1.0)) == 3713080549409410656
    assert hash(Interval(0L, 1L)) == 3713080549409410656


def test_discretize():
    """Test Interval - discrete list conversion."""
    i = Interval(0, 10)
    assert i.discretize() == [v for v in range(i[0], i[1] + 1)]
    assert i.discretize(2) == [0, 2, 4, 6, 8, 10]
    assert i.discretize(3) == [0, 3, 6, 9]

    i = Interval(0.0, 2.0)
    assert i.discretize() == [0.0, 1.0, 2.0]
    assert i.discretize(.5) == [0.0, 0.50, 1.0, 1.5, 2.0]

    i = Interval(0L, 2L)
    assert i.discretize() == [0L, 1L, 2L]
    assert i.discretize(2L) == [0L, 2L]


def test___str__():
    """Test str() of Interval object."""
    assert str(Interval(0, 1)) == "I(0, 1)"
    assert str(Interval(0.0, 1.0)) == "I(0.0, 1.0)"
    assert str(Interval(0L, 1L)) == "I(0, 1)"


def test___repr__():
    """Test repr() of Interval object."""
    assert repr(Interval(0, 1)) == "I(0, 1)"
    assert repr(Interval(0.0, 1.0)) == "I(0.0, 1.0)"
    assert repr(Interval(0L, 1L)) == "I(0, 1)"


def test_collapse_intervals():
    """Test Interval collapsing."""
    intervals = [
        Interval(-10, 0), Interval(-1, 10), Interval(-4, 5), Interval(9, 13),
        Interval(11, 15), Interval(-4, 5), Interval(-100, -99),
        Interval(-10.0, 0.0), Interval(-1.0, 10.0), Interval(-4.0, 5.0),
        Interval(9.0, 13.0), Interval(11.0, 15.0), Interval(-4.0, 5.0),
        Interval(-100.0, -99.0), Interval(-10L, 0L), Interval(-1L, 10L),
        Interval(-4L, 5L), Interval(9L, 13L), Interval(11L, 15L),
        Interval(-4L, 5L), Interval(-100L, -99L)]

    out = [
        Interval(-100, -99), Interval(-10, 15), Interval(-100.0, -99.0),
        Interval(-10.0, 15.0), Interval(-100L, -99L), Interval(-10L, 15L)]

    assert Interval.collapse_intervals(intervals) == out
