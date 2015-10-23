"""ValueSet class unit tests."""

import pytest
from vivid.Classes.ValueSet import ValueSet
from vivid.Classes.Interval import Interval

def test_add_object_type():
    """."""
    pass

def test___init__():
    """Test ValueSet Constructor"""
    def test_TypeError(valueset):
        """Test an individual ValueSet construction."""
        with pytest.raises(TypeError) as excinfo:
            ValueSet(valueset)

    #test value_set errors
    test_TypeError(1)
    test_TypeError(1.0)
    test_TypeError("")
    test_TypeError(set([]))
    test_TypeError(object)
    test_TypeError(Interval(0,10))

def test___eq__():
    """Test == operator."""
    VS1, VS2 = ValueSet([]), ValueSet([])
    assert VS1 == VS2
    VS1, VS2 = ValueSet([1]), ValueSet([1])
    assert VS1 == VS2
    #Test out of order
    VS1, VS2 = ValueSet([1,3,5]), ValueSet([5,3,1])
    assert VS1 == VS2
    VS1, VS2 = ValueSet([1,'b', 3,'c','a', 5]), ValueSet([5,3,1, 'a', 'b', 'c'])
    assert VS1 == VS2
    VS1, VS2 = ValueSet([1,'b', 3,'c','a', 5, Interval(1,10)]), ValueSet([Interval(1,10), 5, 3, 1, 'a', 'b', 'c'])
    assert VS1 == VS2
    #test type mismatch for Interval
    VS1, VS2 = ValueSet([Interval(1,10)]), ValueSet([Interval(1.0,10.0)])
    assert VS1 != VS2

def test___ne__():
    """Test != operator."""
    VS1, VS2 = ValueSet([]), ValueSet([])
    assert not VS1 != VS2
    VS1, VS2 = ValueSet(['1']), ValueSet([1])
    assert VS1 != VS2
    #Test out of order
    VS1, VS2 = ValueSet([1,3,5]), ValueSet([5,3,1])
    assert not VS1 != VS2
    VS1, VS2 = ValueSet([1,'b', 3,'c','a', 5]), ValueSet([5,3,1, 'a', 'b', 'c'])
    assert not VS1 != VS2
    #test type mismatch for Interval
    VS1, VS2 = ValueSet([Interval(1,10)]), ValueSet([Interval(1.0,10.0)])
    assert VS1 != VS2
    VS1, VS2 = ValueSet([Interval(1L,10L)]), ValueSet([Interval(1,10)])
    assert VS1 != VS2

def test___le__():
    """
    Test <, <=, >, >= total ordering operators for subset-superset relations.
    """
    VS0 = ValueSet([])
    VS1 = ValueSet([Interval(20, 100), True, 1,'b', 3,'c','a', 5, Interval(1,10)])
    VS2 = ValueSet([Interval(1,10), 5, 3, 1, 'a', Interval(20, 100), 'b', True, 'c'])
    VS3 = ValueSet([Interval(1,10), 5, 3, 1, 'a', Interval(20, 100), 'b', True, 'c', False])

    assert not VS0 < VS0
    assert not VS1 < VS2
    assert VS0 < VS1
    assert VS1 < VS3
    assert VS0 <= VS0
    assert VS0 <= VS1
    assert VS1 <= VS2
    assert VS1 <= VS3
    assert not VS2 > VS3
    assert not VS3 > VS3
    assert not VS0 > VS0
    assert VS3 > VS2
    assert VS3 > VS1
    assert VS3 > VS0
    assert VS3 >= VS3
    assert VS3 >= VS1
    assert not VS2 >= VS3
    assert VS0 >= VS0

def test___sub__():
    """Test - operator for set theoretic difference."""
    VSA = ValueSet([
        -1, -3, -5,
        15L, 32L,
        167.4, 555.678,
        'a', 'b', 'c', 
        True, False, 
        Interval(1,10), Interval(20, 100), Interval(10.0, 75.4), Interval(2L, 5L)])

    VSB = ValueSet([
        -1, -3, -5,
        15L, 32L,
        167.4, 555.678,
        'a', 'b', 'c', 
        True, False, 
        Interval(1,10), Interval(20, 100), Interval(10.0, 75.4), Interval(2L, 5L)])

    VSC = ValueSet([
        -1, -3,
        32L,
        167.4,
        'c', 
        False, 
        Interval(1,10), Interval(2L, 5L)])

    VSD = ValueSet([
        -1, -3,
        32L,
        555.678,
        'b', 'c', 
        False, 
        Interval(1,10), Interval(10.0, 75.4), Interval(2L, 5L)])

    VSE = ValueSet([
        -1, -5,
        15L,
        167.4,
        'a', 
        True, 
        Interval(1,10), Interval(20, 100)])


    assert VSA - VSA == ValueSet([])
    assert VSA - VSB == ValueSet([])
    assert VSA - VSC == ValueSet([-5, 15L, 555.678, 'a', 'b', True, Interval(20, 100), Interval(10.0, 75.4)])
    assert VSC - VSA == ValueSet([])
    assert VSD - VSE == ValueSet([-3, 32L, 555.678, 'b', 'c', False, Interval(10.0, 75.4), Interval(2L, 5L)])
    assert VSE - VSD == ValueSet([-5, 15L, 167.4, 'a', True, Interval(20, 100)])

def test___getitem__():
    """Test indexing for ValueSet object."""
    def test_TypeError(valueset, index):
        "test TypeError raising for indexing."
        with pytest.raises(TypeError):
            valueset._values[index]

    def test_IndexError(valueset, index):
        "test IndexError raising for indexing."
        with pytest.raises(IndexError):
            valueset._values[index]

    v = ValueSet([1, 2, 'a', 'b', False, True, Interval(100, 1000)])
    test_TypeError(v, '')
    test_IndexError(v, 7)
    assert v[0] == 1
    assert v[0] is v._values[0]
    assert v[1] == 2
    assert v[1] is v._values[1]
    assert v[2] == 'a'
    assert v[2] is v._values[2]
    assert v[3] == 'b'
    assert v[3] is v._values[3]
    assert v[4] == False
    assert v[4] is v._values[4]
    assert v[5] == True
    assert v[5] is v._values[5]
    assert v[6] == Interval(100, 1000)
    assert v[6] is v._values[6]

def test___contains__():
    """."""
    pass

def test___len__():
    """."""
    pass

def test___iter__():
    """."""
    pass

def test___nonzero__():
    """."""
    pass

def test___deepcopy__():
    """."""
    pass

def test___str__():
    """."""
    pass

def test___repr__():
    """."""
    pass

def test__split_by_types():
    """."""
    pass

def test__parse():
    """."""
    pass
