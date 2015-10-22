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

    #test standard invalid params
    test_TypeError('', '')
    test_TypeError(None, None)
    test_TypeError(object, object)
    #test type mismatch
    test_TypeError(1, 1.0)
    test_TypeError(1.0, 1)
    test_TypeError(1.0, 1L)
    test_TypeError(1L, 1.0)
    test_TypeError(1L, 1)
    test_TypeError(1, 1L)
    #test inf >= sup
    test_ValueError(10, 5)
    test_ValueError(5, 5)

def test___lt__():
    """Test < operator for Interval; [i, s](i' s')."""
    #test standard less than
    assert Interval(-1, 0) < Interval(1, 2)
    assert Interval(-1.0, 0.0) < Interval(1.0, 2.0)
    assert Interval(-1L, 0L) < Interval(1L, 2L)
    #test strictly less than
    assert not Interval(-1, 0) < Interval(0, 1)
    assert not Interval(-1.0, 0.0) < Interval(0.0, 1.0)
    assert not Interval(-1L, 0L) < Interval(0L, 1L)
    #test not less than
    assert not Interval(8, 9) < Interval(0, 1)
    assert not Interval(8.0, 9.0) < Interval(0.0, 1.0)
    assert not Interval(8L, 9L) < Interval(0L, 1L)

def test___le__():
    """."""
    pass

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
    """
    Implement overloaded >= operator for Interval; (i',[i, s'), s]
    Return True when other Interval's infimum is strictly less than this
    Interval's infimum, other Interval supremum is less than this Interval's supremum
    """
    #c_inf = other._infimum < self._infimum
    #c_sup = self._infimum <= other._supremum < self._supremum
    #return c_inf and c_sup

    #test standard greater than or equal to
    assert Interval(3, 8) >= Interval(0, 5)
    assert Interval(3.0, 8.0) >= Interval(0.0, 5.0)
    assert Interval(3L, 8L) >= Interval(0L, 5L)
    #test [i s](i' s')
    assert not Interval(-5, -3) >= Interval(0, 5)
    assert not Interval(-5.0, -3.0) >= Interval(0.0, 5.0)
    assert not Interval(-5L, -3L) >= Interval(0L, 5L)
    #test (i' s')[i s]
    assert not Interval(90, 100) >= Interval(8, 9)
    assert not Interval(90.0, 100.0) >= Interval(8.0, 9.0)
    assert not Interval(90L, 100L) >= Interval(8L, 9L)
    #test [i (i' s] s')
    assert not Interval(-2, 3) >= Interval(0, 5)
    assert not Interval(-2.0, 3.0) >= Interval(0.0, 5.0)
    assert not Interval(-2L, 3L) >= Interval(0L, 5L)
    #test [i (i' s') s]
    assert not Interval(-5, 10) >= Interval(0, 5)
    assert not Interval(-5.0, 10.0) >= Interval(0.0, 5.0)
    assert not Interval(-5L, 10L) >= Interval(0L, 5L)
    #test [i' (i s) s']
    assert not Interval(-5, 10) >= Interval(-10, 15)
    assert not Interval(-5.0, 10.0) >= Interval(-10.0, 15.0)
    assert not Interval(-5L, 10L) >= Interval(-10L, 15L)
    #test ([i'i ss'])
    assert not Interval(-10, 15) >= Interval(-10, 15)
    assert not Interval(-10.0, 15.0) >= Interval(-10.0, 15.0)
    assert not Interval(-10L, 15L) >= Interval(-10L, 15L)


def test___gt__():
    """Test > operator for Interval; (i' s')[i, s]."""
    #test standard less than
    assert Interval(1, 2) > Interval(-1, 0)
    assert Interval(1.0, 2.0) > Interval(-1.0, 0.0)
    assert Interval(1L, 2L) > Interval(-1L, 0L)
    #test strictly greater than
    assert not Interval(0, 1) > Interval(-1, 0)
    assert not Interval(0.0, 1.0) > Interval(-1.0, 0.0)
    assert not Interval(0L, 1L) > Interval(-1L, 0L)
    #test not greater than
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

def test___add__():
    """."""
    pass

def test___iadd__():
    """."""
    pass

def test___contains__():
    """."""
    pass

def test___getitem__():
    """."""
    pass

def test___deepcopy__():
    """."""
    pass

def test__key():
    """."""
    pass

def test___hash__():
    """."""
    pass

def test_discretize():
    """."""
    pass

def test___str__():
    """."""
    pass

def test___repr__():
    """."""
    pass


def test_collapse_intervals():
    """."""
    pass
