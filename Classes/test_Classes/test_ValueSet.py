"""ValueSet class unit tests."""

import pytest
from vivid.Classes.ValueSet import ValueSet
from vivid.Classes.Interval import Interval

def test_add_object_type():
    """Test add object types for ValueSet class."""
    def test_TypeError(object_type):
        """Test TypeError raising in add_object_type."""
        with pytest.raises(TypeError) as excinfo:
            ValueSet.add_object_type(object_type)
    def test_ValueError(object_type):
        """Test ValueError raising in add_object_type."""
        with pytest.raises(ValueError) as excinfo:
            ValueSet.add_object_type(object_type)

    test_TypeError(None)
    test_TypeError(object)
    test_ValueError('bad_string')
    test_ValueError('_bad_string')
    test_ValueError('_isbad_string')

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
    """Test in operator for ValueSet object."""
    v = ValueSet([1, 2, 'a', 'b', False, True, Interval(100, 1000)])
    assert 1 in v
    assert 2 in v
    assert 'a' in v
    assert 'b' in v
    assert False in v
    assert True in v
    assert Interval(100, 1000) in v
    assert not Interval(400, 500) in v
    assert not Interval(100.0, 1000.0) in v
    assert not Interval(100L, 1000L) in v

def test___len__():
    """Test len() function for ValueSet object."""
    v = ValueSet([Interval(100,105), 5, 3, 1, 'a', Interval(2.0, 10.0), 'b', True, 'c', False])
    v2 = ValueSet([])
    assert len(v) == 10
    assert len(v2) == 0

def test___iter__():
    """Test iterator for ValueSet object."""
    v = ValueSet([Interval(100,105), 5, 3, 1, 'a', Interval(2.0, 10.0), 'b', True, 'c', False])
    assert [i for i in v.__iter__()] == v._values

def test___setitem__():
    """Test ValueSet[key] = value assignment for ValueSet object."""
    def test_TypeError(valueset, key, value):
        """Test TypeError raising in index assignment."""
        with pytest.raises(TypeError) as excinfo:
            valueset[key] = value
    def test_ValueError(valueset, key, value):
        """Test ValueError raising in index assignment."""
        with pytest.raises(ValueError) as excinfo:
            valueset[key] = value
    def test_AttributeError(valueset, key, value):
        """Test AttributeError raising in index assignment."""
        with pytest.raises(AttributeError) as excinfo:
            valueset[key] = value
    def test_IndexError(valueset, key, value):
        """Test IndexError raising in index assignment."""
        with pytest.raises(IndexError) as excinfo:
            valueset[key] = value

    v = ValueSet([1, 3, 5, 'a', 'b', 'c', False, True, Interval(100, 105), Interval(2.0, 10.0)])

    v[0] = 1000
    assert v[0] == 1000
    #test invalid key types
    test_TypeError(v, '', 1)
    test_TypeError(v, object, 1)
    test_TypeError(v, None, 1)
    test_TypeError(v, 1.0, 1)
    test_TypeError(v, 1L, 1)
    #test duplicate value catching
    test_ValueError(v, 1, 1)
    test_IndexError(v, 10, -37)

def test___nonzero__():
    """Test boolean behavior for ValueSet."""
    v = ValueSet([Interval(100,105), 5, 3, 1, 'a', Interval(2.0, 10.0), 'b', True, 'c', False])
    assert v
    v2 = ValueSet([])
    assert not v2

def test___deepcopy__():
    """Test copy.deepcopy for ValueSet object."""
    import copy
    v = ValueSet([1, 3, 5, 'a', 'b', 'c', False, True, Interval(100, 105), Interval(2.0, 10.0)])
    v_copy = copy.deepcopy(v)
    assert v == v_copy
    assert v is not v_copy
    assert v[8] is not v_copy[8]
    assert v[9] is not v_copy[9]

def test___str__():
    """Test str() for ValueSet object."""
    v1 = ValueSet([1, 3, 5, 'a', 'b', 'c', False, True, Interval(100, 105), Interval(2.0, 10.0)])
    v2 = ValueSet([Interval(100,105), 5, 3, 1, 'a', Interval(2.0, 10.0), 'b', True, 'c', False])
    v3 = ValueSet([])
    assert str(v1) == "V(1, 3, 5, a, b, c, False, True, I(100, 105), I(2.0, 10.0))"
    assert v1.__str__() == "V(1, 3, 5, a, b, c, False, True, I(100, 105), I(2.0, 10.0))"
    #test out of order
    assert str(v2) == "V(1, 3, 5, a, b, c, False, True, I(100, 105), I(2.0, 10.0))"
    assert v2.__str__() == "V(1, 3, 5, a, b, c, False, True, I(100, 105), I(2.0, 10.0))"
    #test empty
    assert str(v3) == "V()"
    assert v3.__str__() == "V()"

def test___repr__():
    """Test repr() for ValueSet object."""
    v1 = ValueSet([1, 3, 5, 'a', 'b', 'c', False, True, Interval(100, 105), Interval(2.0, 10.0)])
    v2 = ValueSet([Interval(100,105), 5, 3, 1, 'a', Interval(2.0, 10.0), 'b', True, 'c', False])
    v3 = ValueSet([])
    assert repr(v1) == "V(1, 3, 5, a, b, c, False, True, I(100, 105), I(2.0, 10.0))"
    assert v1.__repr__() == "V(1, 3, 5, a, b, c, False, True, I(100, 105), I(2.0, 10.0))"
    #test out of order
    assert repr(v2) == "V(1, 3, 5, a, b, c, False, True, I(100, 105), I(2.0, 10.0))"
    assert v2.__repr__() == "V(1, 3, 5, a, b, c, False, True, I(100, 105), I(2.0, 10.0))"
    #test empty
    assert repr(v3) == "V()"
    assert v3.__repr__() == "V()"

def test__split_by_types():
    """Test split_by_types used in parsing."""
    def test_AttributeError(values):
        """Test AttributeError raising in split_by_types."""
        with pytest.raises(AttributeError) as excinfo:
            ValueSet._split_by_types(values)
    def test_TypeError(values):
        """Test TypeError raising in split_by_types."""
        with pytest.raises(TypeError) as excinfo:
            ValueSet._split_by_types(values)

    #test error raising
    i = Interval(1, 10)
    i._is_different_object = True
    ValueSet.add_object_type("_is_different_object")
    test_AttributeError([i])
    test_TypeError([object])

    #test output
    types = ValueSet._split_by_types(
        [1, 2, 1.0, 1.5, 1L, 2L, 'a', 'b', True, False, 
        Interval(0, 10), Interval(0.0, 10.0), Interval(0L, 10L)])
    
    d = {
        int: [1, 2], float: [1.0, 1.5], long: [1L, 2L],
        str: ['a', 'b'], bool: [True, False],
        "_is_Interval": [Interval(0, 10), Interval(0.0, 10.0), Interval(0L, 10L)]}
    
    empty = ValueSet._split_by_types([])
    assert empty == {}
    assert d == types

def test__parse():
    """Test _parse function for ValueSet."""
    def test_TypeError(values):
        """Test TypeError raising in split_by_types."""
        with pytest.raises(TypeError) as excinfo:
            ValueSet._parse(values)

    #test standard type parsing
    standard_types = ValueSet._parse(
        [-1, -2, -1.0, -1.5, -1L, -2L, 'a', 'b', True, False,
        Interval(0, 10), Interval(0.0, 10.0), Interval(0L, 10L)])
    
    assert standard_types == [-2, -1, -1.5, -1.0, -2L, -1L, 'a', 'b',
                                False, True, Interval(0, 10),
                                Interval(0.0, 10.0), Interval(0L, 10L)]
    
    #test single numbers being filtered by intervals
    number_filters = ValueSet._parse(
        [-2, 1, -1.5, 1.0, -2L, 1L, 
            Interval(0, 10), Interval(0.0, 10.0), Interval(0L, 10L)])

    assert number_filters == [-2, -1.5, -2L, Interval(0, 10),
                                Interval(0.0, 10.0), Interval(0L, 10L)]

    interval_collapsing = ValueSet._parse(
        [Interval(0, 10), Interval(5, 15), Interval(7, 11), Interval(15, 25),
        Interval(-10, 500), Interval(0.0, 10.4), Interval(5.56, 15.33),
        Interval(7.765, 11.001), Interval(15.32, 25.77),
        Interval(-10.2, 500.442), Interval(0L, 10L), Interval(5L, 15L),
        Interval(7L, 11L), Interval(15L, 25L), Interval(-10L, 500L)])

    assert interval_collapsing == [
            Interval(-10, 500), Interval(-10.2, 500.442), Interval(-10L, 500L)]
