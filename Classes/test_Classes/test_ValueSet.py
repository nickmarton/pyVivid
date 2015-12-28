"""ValueSet class unit tests."""

import pytest
from vivid.Classes.ValueSet import ValueSet
from vivid.Classes.Interval import Interval
from vivid.Classes.Point import Point


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

    # test value_set errors
    test_TypeError(1)
    test_TypeError(1.0)
    test_TypeError("")
    test_TypeError(object)
    test_TypeError(Interval(0, 10))
    test_TypeError(Point(0.0))


def test___eq__():
    """Test == operator."""
    VS1, VS2 = ValueSet([]), ValueSet([])
    assert VS1 == VS2
    VS1, VS2 = ValueSet([1]), ValueSet([1])
    assert VS1 == VS2
    # Test out of order
    VS1, VS2 = ValueSet([1, 3, 5]), ValueSet([5, 3, 1])
    assert VS1 == VS2
    VS1 = ValueSet([1, 'b', 3, 'c', 'a', 5])
    VS2 = ValueSet([5, 3, 1, 'a', 'b', 'c'])
    assert VS1 == VS2
    VS1 = ValueSet([1, 'b', 3, 'c', 'a', 5, Interval(1, 10), Point(1.0)])
    VS2 = ValueSet([Interval(1, 10), 5, 3, 1, Point(1.0), 'a', 'b', 'c'])
    assert VS1 == VS2
    VS1 = ValueSet([Point(1.0, 1.0)])
    VS2 = ValueSet([Point(1.0)])
    assert not VS1 == VS2
    # test type mismatch for Interval
    VS1, VS2 = ValueSet([Interval(1, 10)]), ValueSet([Interval(1.0, 10.0)])
    assert VS1 != VS2


def test___le__():
    """
    Test <, <=, >, >= total ordering operators for subset-superset relations.
    """
    VS0 = ValueSet([])
    VS1 = ValueSet([Interval(20, 100),
                    True, 1, 'b', 3, 'c', 'a', 5,
                    Interval(1, 10),
                    Point(0.0)])
    VS2 = ValueSet([Interval(1, 10),
                    5, 3, 1, 'a',
                    Interval(20, 100),
                    'b', True, 'c',
                    Point(0.0)])
    VS3 = ValueSet([Interval(1, 10),
                    5, 3, 1, 'a',
                    Interval(20, 100),
                    'b', True, 'c', False,
                    Point(0.0),
                    Point(0.0, 0.0)])
    VS4 = ValueSet([5, 3, 1, 17L, 2.67854, 'b', True, Point(0.0, 0.0)])
    VS5 = ValueSet([Interval(1, 10),
                    Interval(1.0, 10.0),
                    Interval(10L, 100L),
                    'b', True,
                    Point(0.0, 0.0)])

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

    # Test ints, floats, and longs being subsumed by Intervals during comp
    assert VS4 < VS5
    assert VS4 <= VS5
    assert VS5 > VS4
    assert VS5 >= VS4


def test___ne__():
    """Test != operator."""
    VS1, VS2 = ValueSet([]), ValueSet([])
    assert not VS1 != VS2
    VS1, VS2 = ValueSet(['1']), ValueSet([1])
    assert VS1 != VS2
    # Test out of order
    VS1, VS2 = ValueSet([1, 3, 5]), ValueSet([5, 3, 1])
    assert not VS1 != VS2
    VS1 = ValueSet([1, 'b', 3, 'c', 'a', 5])
    VS2 = ValueSet([5, 3, 1, 'a', 'b', 'c'])
    assert not VS1 != VS2
    VS1 = ValueSet([Point(1.0, 1.0)])
    VS2 = ValueSet([Point(1.0)])
    assert VS1 != VS2
    VS1 = ValueSet([Point(1.0)])
    VS2 = ValueSet([Point(2.0)])
    assert VS1 != VS2
    # test type mismatch for Interval
    VS1, VS2 = ValueSet([Interval(1, 10)]), ValueSet([Interval(1.0, 10.0)])
    assert VS1 != VS2
    VS1, VS2 = ValueSet([Interval(1L, 10L)]), ValueSet([Interval(1, 10)])
    assert VS1 != VS2


def test___add__():
    """Test + operator for ValueSet."""
    def test_TypeError(valueset, object_type):
        """Test TypeError raising in add_object_type."""
        with pytest.raises(TypeError) as excinfo:
            valueset + object_type

    VSA = ValueSet([
        -5,
        15L,
        167.4,
        'c',
        True,
        Interval(1, 10),
        Interval(10.0, 75.4)])

    VSB = ValueSet([
        -2,
        33L,
        555.679,
        'e',
        False,
        Point(1.0, 1.0),
        Interval(2L, 5L)])

    VSC = VSA + VSB
    assert VSC == ValueSet([-5, -2, 15L, 33L, 167.4, 555.679, 'c', 'e',
                           True, False, Interval(1, 10), Interval(10.0, 75.4),
                           Interval(2L, 5L), Point(1.0, 1.0)])
    assert VSA == VSA + VSA

    VSD = ValueSet([
        -5, -100,
        15L,
        167.4,
        'c',
        True,
        Interval(1, 10),
        Interval(10.0, 75.4)])

    assert VSD == VSA + -100
    assert VSD == VSA + [-5, -100]

    from vivid.Classes.Attribute import Attribute
    test_TypeError(VSA, Attribute("l", ['s']))


def test___sub__():
    """Test - operator for set theoretic difference."""
    VSA = ValueSet([
        -1, -3, -5,
        15L, 32L,
        167.4, 555.678,
        'a', 'b', 'c',
        True, False,
        Interval(1, 10), Interval(20, 100),
        Interval(10.0, 75.4), Interval(2L, 5L)])

    VSB = ValueSet([
        -1, -3, -5,
        15L, 32L,
        167.4, 555.678,
        'a', 'b', 'c',
        True, False,
        Interval(1, 10), Interval(20, 100),
        Interval(10.0, 75.4), Interval(2L, 5L)])

    VSC = ValueSet([
        -1, -3,
        32L,
        167.4,
        'c',
        False,
        Interval(1, 10), Interval(2L, 5L),
        Point(0.0)])

    VSD = ValueSet([
        -1, -3,
        32L,
        555.678,
        'b', 'c',
        False,
        Interval(1, 10), Interval(10.0, 75.4), Interval(2L, 5L),
        Point(1.0, 1.0)])

    VSE = ValueSet([
        -1, -5,
        15L,
        167.4,
        'a',
        True,
        Interval(1, 10), Interval(20, 100),
        Point(3.4)])

    assert VSA - VSA == ValueSet([])
    assert VSA - VSB == ValueSet([])
    assert VSA - VSC == ValueSet([-5, 15L, 555.678, 'a', 'b', True,
                                  Interval(20, 100), Interval(10.0, 75.4)])
    assert VSC - VSA == ValueSet([Point(0.0)])
    assert VSD - VSE == ValueSet([-3, 32L, 555.678, 'b', 'c', False,
                                  Interval(10.0, 75.4), Interval(2L, 5L),
                                  Point(1.0, 1.0)])
    assert VSE - VSD == ValueSet([-5, 15L, 167.4, 'a', True,
                                  Interval(20, 100),
                                  Point(3.4)])

    VSF = ValueSet([Interval(1, 10)])
    VSG = ValueSet([1, 5, 10])
    assert VSF - VSG == ValueSet([Interval(2, 4), Interval(6, 9)])
    VSH = ValueSet([2, 9])
    assert VSF - VSH == ValueSet([1, 10, Interval(3, 8)])
    VSI = ValueSet([2, 4, 6])
    assert VSF - VSI == ValueSet([1, 3, 5, Interval(7, 10)])

    VSJ = ValueSet([Interval(1L, 10L)])
    VSK = ValueSet([1L, 5L, 10L])
    assert VSJ - VSK == ValueSet([Interval(2L, 4L), Interval(6L, 9L)])
    VSL = ValueSet([2L, 9L])
    assert VSJ - VSL == ValueSet([1L, 10L, Interval(3L, 8L)])
    VSM = ValueSet([2L, 4L, 6L])
    assert VSJ - VSM == ValueSet([1L, 3L, 5L, Interval(7L, 10L)])

    VSN = ValueSet([Interval(1.0, 10.0)])
    VSO = ValueSet([1.0, 5.0, 10.0])
    assert VSN - VSO == ValueSet([Interval(1.00000000001, 4.99999999999),
                                  Interval(5.00000000001, 9.99999999999)])
    VSP = ValueSet([2.0, 9.0])
    assert VSN - VSP == ValueSet([Interval(1.0, 1.99999999999),
                                  Interval(2.00000000001, 8.99999999999),
                                  Interval(9.00000000001, 10.0)])
    VSQ = ValueSet([2.0, 4.0, 6.0])
    assert VSN - VSQ == ValueSet([Interval(1.0, 1.99999999999),
                                  Interval(2.00000000001, 3.99999999999),
                                  Interval(4.00000000001, 5.99999999999),
                                  Interval(6.00000000001, 10.0)])
    VSR = ValueSet([1.00000000001])
    assert VSN - VSR == ValueSet([1.0, Interval(1.00000000002, 10.0)])

    VSS = VSF + VSJ + VSN
    VST = VSG + VSK + VSO
    VSU = VSH + VSL + VSP
    VSV = VSI + VSM + VSQ

    assert VSS - VST == ValueSet([Interval(2, 4),
                                  Interval(6, 9),
                                  Interval(1.00000000001, 4.99999999999),
                                  Interval(5.00000000001, 9.99999999999),
                                  Interval(2L, 4L),
                                  Interval(6L, 9L)])

    assert VSS - VSU == ValueSet([1, 10, Interval(3, 8),
                                  1L, 10L, Interval(3L, 8L),
                                  Interval(1.0, 1.99999999999),
                                  Interval(2.00000000001, 8.99999999999),
                                  Interval(9.00000000001, 10.0)])

    assert VSS - VSV == ValueSet([1, 3, 5, Interval(7, 10),
                                  1L, 3L, 5L, Interval(7L, 10L),
                                  Interval(1.0, 1.99999999999),
                                  Interval(2.00000000001, 3.99999999999),
                                  Interval(4.00000000001, 5.99999999999),
                                  Interval(6.00000000001, 10.0)])

    # assert False


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

    v = ValueSet([1, 2, 'a', 'b', False, True,
                  Interval(100, 1000),
                  Point(1.0)])
    test_TypeError(v, '')
    test_IndexError(v, 8)
    assert v[0] == 1
    assert v[0] is v._values[0]
    assert v[1] == 2
    assert v[1] is v._values[1]
    assert v[2] == 'a'
    assert v[2] is v._values[2]
    assert v[3] == 'b'
    assert v[3] is v._values[3]
    assert v[4] is False
    assert v[4] is v._values[4]
    assert v[5] is True
    assert v[5] is v._values[5]
    assert v[6] == Interval(100, 1000)
    assert v[6] is v._values[6]
    assert v[7] == Point(1.0)
    assert v[7] is v._values[7]


def test___contains__():
    """Test in operator for ValueSet object."""
    v = ValueSet([1, 2, 'a', 'b', False, True,
                  Interval(100, 1000),
                  Point(1.0)])
    assert 1 in v
    assert 2 in v
    assert 'a' in v
    assert 'b' in v
    assert False in v
    assert True in v
    assert Interval(100, 1000) in v
    assert Point(1.0) in v
    assert not Interval(400, 500) in v
    assert not Interval(100.0, 1000.0) in v
    assert not Interval(100L, 1000L) in v
    assert not Point('x') in v


def test___len__():
    """Test len() function for ValueSet object."""
    v = ValueSet([Interval(100, 105), 5, 3, 1, 'a',
                  Interval(2.0, 10.0),
                  'b', True, 'c', False,
                  Point(1.0)])
    v2 = ValueSet([])
    assert len(v) == 11
    assert len(v2) == 0


def test___iter__():
    """Test iterator for ValueSet object."""
    v = ValueSet([Interval(100, 105),
                  5, 3, 1, 'a',
                  Interval(2.0, 10.0),
                  'b', True, 'c', False,
                  Point(1.0)])
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

    v = ValueSet([1, 3, 5, 'a', 'b', 'c', False, True,
                  Interval(100, 105),
                  Interval(2.0, 10.0),
                  Point(1.0)])

    v[0] = 1000
    assert v[0] == 1000
    # test invalid key types
    test_TypeError(v, '', 1)
    test_TypeError(v, object, 1)
    test_TypeError(v, None, 1)
    test_TypeError(v, 1.0, 1)
    test_TypeError(v, 1L, 1)
    # test duplicate value catching
    test_ValueError(v, 1, 1)
    test_IndexError(v, 11, -37)


def test___nonzero__():
    """Test boolean behavior for ValueSet."""
    v = ValueSet([Interval(100, 105),
                  5, 3, 1, 'a',
                  Interval(2.0, 10.0),
                  'b', True, 'c', False,
                  Point(1.0)])
    assert v
    v2 = ValueSet([])
    assert not v2


def test___deepcopy__():
    """Test copy.deepcopy for ValueSet object."""
    import copy
    v = ValueSet([1, 3, 5, 'a', 'b', 'c', False, True,
                  Interval(100, 105), Interval(2.0, 10.0),
                  Point(1.0)])
    v_copy = copy.deepcopy(v)
    assert v == v_copy
    assert v is not v_copy
    assert v[8] is not v_copy[8]
    assert v[9] is not v_copy[9]
    assert v[10] is not v_copy[10]


def test___str__():
    """Test str() for ValueSet object."""
    v1 = ValueSet([1, 3, 5, 'a', 'b', 'c', False, True,
                  Interval(100, 105), Interval(2.0, 10.0),
                  Point(1.0)])
    v2 = ValueSet([Interval(100, 105),
                  5, 3, 1,
                  Point(1.0),
                  'a',
                   Interval(2.0, 10.0),
                   'b', True, 'c', False])
    v3 = ValueSet([])
    assert v1.__str__() == "V(1, 3, 5, a, b, c, False, True, I(100, 105), I(2.0, 10.0), P(1.0))"
    # test out of order
    assert v2.__str__() == "V(1, 3, 5, a, b, c, False, True, I(100, 105), I(2.0, 10.0), P(1.0))"
    # test empty
    assert v3.__str__() == "V()"


def test___repr__():
    """Test repr() for ValueSet object."""
    v1 = ValueSet([1, 3, 5, 'a', 'b', 'c', False, True,
                  Interval(100, 105), Interval(2.0, 10.0),
                  Point(1.0)])
    v2 = ValueSet([Interval(100, 105),
                  5, 3, 1,
                  Point(1.0),
                  'a',
                   Interval(2.0, 10.0),
                   'b', True, 'c', False])
    v3 = ValueSet([])
    assert v1.__repr__() == "V(1, 3, 5, a, b, c, False, True, I(100, 105), I(2.0, 10.0), P(1.0))"
    # test out of order
    assert v2.__repr__() == "V(1, 3, 5, a, b, c, False, True, I(100, 105), I(2.0, 10.0), P(1.0))"
    # test empty
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

    # test error raising
    i = Interval(1, 10)
    i._is_different_object = True
    ValueSet.add_object_type("_is_different_object")
    test_AttributeError([i])
    test_TypeError([object])

    # test output
    types = ValueSet._split_by_types(
        [1, 2, 1.0, 1.5, 1L, 2L, 'a', 'b', True, False,
         Interval(0, 10), Interval(0.0, 10.0), Interval(0L, 10L),
         Point(1.0), Point(1.0, 1.0), Point('x')])

    d = {
        int: [1, 2], float: [1.0, 1.5], long: [1L, 2L],
        str: ['a', 'b'], bool: [True, False],
        "_is_Interval": [Interval(0, 10), Interval(0.0, 10.0), Interval(0L, 10L)],
        "_is_Point": [Point(1.0), Point(1.0, 1.0), Point('x')]}

    empty = ValueSet._split_by_types([])
    assert empty == {}
    assert d == types


def test__parse():
    """Test _parse function for ValueSet."""
    def test_TypeError(values):
        """Test TypeError raising in split_by_types."""
        with pytest.raises(TypeError) as excinfo:
            ValueSet._parse(values)

    # test standard type parsing
    standard_types = ValueSet._parse(
        [-1, -2, -1.0, -1.5, -1L, -2L, 'a', 'b', True, False,
         Interval(0, 10), Interval(0.0, 10.0), Interval(0L, 10L), Point(1.0)])

    assert standard_types == [-2, -1, -1.5, -1.0, -2L, -1L, 'a', 'b',
                              False, True, Interval(0, 10),
                              Interval(0.0, 10.0), Interval(0L, 10L),
                              Point(1.0)]

    # test single numbers being filtered by intervals
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

    point_duplicates = ValueSet._parse([Point(1.0), Point(1.0), Point('x')])

    assert point_duplicates == [Point(1.0), Point('x')]
