"""Attribute System unit tests."""

import pytest
from ..AttributeSystem import AttributeSystem
from ..AttributeSystem import AttributeStructure
from ..AttributeSystem import Attribute, Relation

def test___init__():
    """."""
    def test_TypeError(A, objs):
        """Test constructor for TypeErrors with given params."""
        with pytest.raises(TypeError) as excinfo:
            AttributeSystem(A, objs)

    def test_ValueError(A, objs):
        """Test constructor for ValueErrors with given params."""
        with pytest.raises(ValueError) as excinfo:
            AttributeSystem(A, objs)

    a = Attribute("a", [])
    b = Attribute("b", [])
    R1 = Relation("R1(a) <=> ", ["a1"], 1)
    R2 = Relation("R2(a) <=> ", ["b"], 2)
    R3 = Relation("R3(a) <=> ", ["a"], 3)
    astr = AttributeStructure()
    objs = ['a', 'b', 'c']
    bad_objs = ['c', 'c']
    bad_objs2 = ['c', 1]
    bad_objs3 = [object]
    bad_objs4 = [None]

    #Test invalid paramters
    test_TypeError(object, objs)
    test_TypeError(None, objs)
    test_TypeError(astr, object)
    test_TypeError(astr, None)
    test_TypeError(object, object)
    test_TypeError(None, None)
    #Test duplicate objects
    test_ValueError(astr, bad_objs)
    #Test not all objects are strings
    test_ValueError(astr, bad_objs2)
    test_ValueError(astr, bad_objs3)
    test_ValueError(astr, bad_objs4)

def test___eq__():
    """Test == operator for AttributeSystem."""
    a = Attribute("a", [])
    b = Attribute("b", [])
    R1 = Relation("R1(a) <=> ", ["a"], 1)
    R2 = Relation("R2(a) <=> ", ["b"], 2)
    
    astr_empty = AttributeStructure()
    astr_a_b = AttributeStructure(a, b)
    astr_a_b_R1_R2 = AttributeStructure(a, b, R1, R2)
    
    objs_empty = []
    objs = ['a', 'b', 'c']
    
    asys = AttributeSystem(astr_empty, objs_empty)
    asys_o = AttributeSystem(astr_empty, objs)
    asys_o_copy = AttributeSystem(astr_empty, objs)
    
    asys_a_b = AttributeSystem(astr_a_b, objs_empty)
    asys_a_b_copy = AttributeSystem(astr_a_b, objs_empty)
    
    asys_a_b_R1_R2 = AttributeSystem(astr_a_b_R1_R2, objs_empty)
    asys_a_b_R1_R2_copy = AttributeSystem(astr_a_b_R1_R2, objs_empty)
    
    asys_a_b_R1_R2_o = AttributeSystem(astr_a_b_R1_R2, objs)
    asys_a_b_R1_R2_o_copy = AttributeSystem(astr_a_b_R1_R2, objs)

    #test identity
    assert asys == asys
    #components tests
    assert asys_o == asys_o_copy
    assert asys_a_b == asys_a_b_copy
    assert asys_a_b_R1_R2 == asys_a_b_R1_R2_copy
    assert asys_a_b_R1_R2_o == asys_a_b_R1_R2_o_copy

def test___le__():
    """Implement <= for AttributeSystem."""
    a = Attribute("a", [])
    b = Attribute("b", [])
    R1 = Relation("R1(a) <=> ", ["a"], 1)
    R2 = Relation("R2(a) <=> ", ["b"], 2)
    
    astr_empty = AttributeStructure()
    astr_a_b = AttributeStructure(a, b)
    astr_a_b_R1_R2 = AttributeStructure(a, b, R1, R2)
    
    objs_empty = []
    objs = ['a', 'b', 'c']
    
    asys_empty = AttributeSystem(astr_empty, objs_empty)
    asys_o = AttributeSystem(astr_empty, objs)
    asys_o_copy = AttributeSystem(astr_empty, objs)
    
    asys_a_b = AttributeSystem(astr_a_b, objs_empty)
    asys_a_b_copy = AttributeSystem(astr_a_b, objs_empty)
    
    asys_a_b_R1_R2 = AttributeSystem(astr_a_b_R1_R2, objs_empty)
    asys_a_b_R1_R2_copy = AttributeSystem(astr_a_b_R1_R2, objs_empty)
    
    asys_a_b_R1_R2_o = AttributeSystem(astr_a_b_R1_R2, objs)
    asys_a_b_R1_R2_o_copy = AttributeSystem(astr_a_b_R1_R2, objs)

    #test identity
    assert not asys_empty < asys_empty
    assert asys_empty <= asys_empty
    assert not asys_empty > asys_empty
    assert asys_empty >= asys_empty
    #components tests
    assert not asys_o > asys_o_copy
    assert asys_o >= asys_o_copy
    assert not asys_o < asys_o_copy
    assert asys_o <= asys_o_copy

    assert not asys_a_b > asys_a_b_copy
    assert asys_a_b >= asys_a_b_copy
    assert not asys_a_b < asys_a_b_copy
    assert asys_a_b <= asys_a_b_copy

    assert not asys_a_b_R1_R2 > asys_a_b_R1_R2_copy
    assert asys_a_b_R1_R2 >= asys_a_b_R1_R2_copy
    assert not asys_a_b_R1_R2 < asys_a_b_R1_R2_copy
    assert asys_a_b_R1_R2 <= asys_a_b_R1_R2_copy

    assert not asys_a_b_R1_R2_o > asys_a_b_R1_R2_o_copy
    assert asys_a_b_R1_R2_o >= asys_a_b_R1_R2_o_copy
    assert not asys_a_b_R1_R2_o < asys_a_b_R1_R2_o_copy
    assert asys_a_b_R1_R2_o <= asys_a_b_R1_R2_o_copy

    assert asys_empty < asys_a_b_R1_R2_o
    assert asys_a_b < asys_a_b_R1_R2_o
    assert asys_a_b_R1_R2 < asys_a_b_R1_R2_o
    assert not asys_a_b_R1_R2_o < asys_a_b_R1_R2_o
    assert not asys_a_b_R1_R2_o > asys_a_b_R1_R2_o
    assert asys_a_b_R1_R2_o > asys_a_b_R1_R2
    assert asys_a_b_R1_R2_o > asys_a_b
    assert asys_a_b_R1_R2_o > asys_empty

def test___ne__():
    """Test != operator for AttributeSystem."""
    a = Attribute("a", [])
    b = Attribute("b", [])
    R1 = Relation("R1(a) <=> ", ["a"], 1)
    R2 = Relation("R2(a) <=> ", ["b"], 2)
    
    astr_empty = AttributeStructure()
    astr_a_b = AttributeStructure(a, b)
    astr_a_b_R1_R2 = AttributeStructure(a, b, R1, R2)
    
    objs_empty = []
    objs = ['a', 'b', 'c']
    
    asys = AttributeSystem(astr_empty, objs_empty)
    asys_o = AttributeSystem(astr_empty, objs)
    asys_o_copy = AttributeSystem(astr_empty, objs)
    
    asys_a_b = AttributeSystem(astr_a_b, objs_empty)
    asys_a_b_copy = AttributeSystem(astr_a_b, objs_empty)
    
    asys_a_b_R1_R2 = AttributeSystem(astr_a_b_R1_R2, objs_empty)
    asys_a_b_R1_R2_copy = AttributeSystem(astr_a_b_R1_R2, objs_empty)
    
    asys_a_b_R1_R2_o = AttributeSystem(astr_a_b_R1_R2, objs)
    asys_a_b_R1_R2_o_copy = AttributeSystem(astr_a_b_R1_R2, objs)

    #test identity
    assert not asys != asys
    #components tests
    assert not asys_o != asys_o_copy
    assert not asys_a_b != asys_a_b_copy
    assert not asys_a_b_R1_R2 != asys_a_b_R1_R2_copy
    assert not asys_a_b_R1_R2_o != asys_a_b_R1_R2_o_copy

    assert asys != asys_o
    assert asys != asys_a_b
    assert asys != asys_a_b_R1_R2
    assert asys != asys_a_b_R1_R2_o
    assert asys_a_b != asys
    assert asys_a_b != asys_a_b_R1_R2
    assert asys_a_b != asys_a_b_R1_R2_o
    assert asys_a_b_R1_R2 != asys
    assert asys_a_b_R1_R2 != asys_a_b
    assert asys_a_b_R1_R2 != asys_a_b_R1_R2_o
    assert asys_a_b_R1_R2_o != asys_a_b_R1_R2
    assert asys_a_b_R1_R2_o != asys_a_b
    assert asys_a_b_R1_R2_o != asys

def test___add__():
    """Test + operator for AttributeSystem."""
    a = Attribute("a", [])
    b = Attribute("b", [])
    R1 = Relation("R1(a) <=> ", ["a"], 1)
    R2 = Relation("R2(a) <=> ", ["b"], 2)
    
    astr_empty = AttributeStructure()
    astr_a = AttributeStructure(a)
    astr_a_b = AttributeStructure(a, b)
    astr_a_R1 = AttributeStructure(a, R1)
    astr_a_b_R1 = AttributeStructure(a, b, R1)
    astr_a_b_R1_R2 = AttributeStructure(a, b, R1, R2)

    objs = ['a', 'b', 'c']
    
    asys = AttributeSystem(astr_empty, [])
    asys_a = AttributeSystem(astr_a, [])
    asys_a_b = AttributeSystem(astr_a_b, [])
    asys_a_R1 = AttributeSystem(astr_a_R1, [])
    asys_a_b_R1 = AttributeSystem(astr_a_b_R1, [])
    asys_a_b_R1_R2 = AttributeSystem(astr_a_b_R1_R2, [])

    assert asys_a == asys + a
    #ensure no implicit type conversion happens
    assert not asys_a == asys
    with pytest.raises(AttributeError) as excinfo:
        asys_a == a
    
    assert asys_a_b == asys + a + b
    assert asys_a_b == a + asys + b
    assert asys_a_b == a + b + asys
    assert asys_a_b_R1_R2 == a + b + asys + R1 + R2
    assert asys_a_R1 == R1 + asys_a
    assert asys_a_b_R1 == R1 + asys_a + b
    assert asys_a_b_R1 == asys + astr_a_b_R1
    assert asys_a_b_R1_R2 == asys + astr_a_b_R1 + R2
    assert asys_a_b_R1_R2 == asys + astr_a_b + R1 + R2
    assert asys_a_b_R1_R2 == asys + astr_a + b + R1 + R2
    assert asys_a_b_R1_R2 == asys + b + astr_a + R1 + R2

def test___sub__():
    """Test - operator for AttributeSystem."""
    a = Attribute("a", [])
    b = Attribute("b", [])
    R1 = Relation("R1(a) <=> ", ["a"], 1)
    R2 = Relation("R2(a) <=> ", ["b"], 2)
    
    astr_empty = AttributeStructure()
    astr_a = AttributeStructure(a)
    astr_a_b = AttributeStructure(a, b)
    astr_a_R1 = AttributeStructure(a, R1)
    astr_a_b_R1 = AttributeStructure(a, b, R1)
    astr_a_b_R1_R2 = AttributeStructure(a, b, R1, R2)

    objs = ['a', 'b', 'c']
    
    asys = AttributeSystem(astr_empty, [])
    asys_a = AttributeSystem(astr_a, [])
    asys_a_b = AttributeSystem(astr_a_b, [])
    asys_a_R1 = AttributeSystem(astr_a_R1, [])
    asys_a_b_R1 = AttributeSystem(astr_a_b_R1, [])
    asys_a_b_R1_R2 = AttributeSystem(astr_a_b_R1_R2, [])

    assert asys_a == asys + a
    #ensure no implicit type conversion happens
    assert not asys_a == asys
    with pytest.raises(AttributeError) as excinfo:
        asys_a == a
    
    assert asys == asys_a_b - a - b
    #Test D(R) remains in AttributeStructure
    with pytest.raises(ValueError) as excinfo:
        asys_a_b_R1_R2 - a
    assert asys_a == asys_a_R1 - R1
    assert asys == asys_a_b_R1_R2 - R1 - R2 - a - b
    assert asys == asys_a_b_R1_R2 - astr_a_b_R1_R2 
    assert asys == asys_a_b_R1_R2 - R1 - R2 - astr_a_b
    assert asys == asys_a_b_R1_R2 - R1 - R2 - astr_a - b

def test___iadd__():
    """Test += operator for AttributeSystem."""
    a = Attribute("a", [])
    b = Attribute("b", [])
    R1 = Relation("R1(a) <=> ", ["a"], 1)
    R2 = Relation("R2(a) <=> ", ["b"], 2)
    
    astr_empty = AttributeStructure()
    astr_a = AttributeStructure(a)
    astr_a_b = AttributeStructure(a, b)
    astr_a_R1 = AttributeStructure(a, R1)
    astr_a_b_R1 = AttributeStructure(a, b, R1)
    astr_a_b_R1_R2 = AttributeStructure(a, b, R1, R2)

    objs = ['a', 'b', 'c']
    
    asys = AttributeSystem(astr_empty, [])
    asys_a = AttributeSystem(astr_a, [])
    asys_a_b = AttributeSystem(astr_a_b, [])
    asys_a_R1 = AttributeSystem(astr_a_R1, [])
    asys_a_b_R1 = AttributeSystem(astr_a_b_R1, [])
    asys_a_b_R1_R2 = AttributeSystem(astr_a_b_R1_R2, [])

    asys += a
    assert asys == asys_a
    assert asys is not asys_a
    asys += b
    assert asys == asys_a_b
    assert asys is not asys_a_b
    asys += R1
    assert asys == asys_a_b_R1
    assert asys is not asys_a_b_R1
    asys += R2
    assert asys == asys_a_b_R1_R2
    assert asys is not asys_a_b_R1_R2

def test___isub__():
    """Test -= operator for AttributeSystem."""
    a = Attribute("a", [])
    b = Attribute("b", [])
    R1 = Relation("R1(a) <=> ", ["a"], 1)
    R2 = Relation("R2(a) <=> ", ["b"], 2)
    
    astr_empty = AttributeStructure()
    astr_a = AttributeStructure(a)
    astr_a_b = AttributeStructure(a, b)
    astr_a_R1 = AttributeStructure(a, R1)
    astr_a_b_R1 = AttributeStructure(a, b, R1)
    astr_a_b_R1_R2 = AttributeStructure(a, b, R1, R2)

    objs = ['a', 'b', 'c']
    
    asys = AttributeSystem(astr_empty, [])
    asys_a = AttributeSystem(astr_a, [])
    asys_a_b = AttributeSystem(astr_a_b, [])
    asys_a_R1 = AttributeSystem(astr_a_R1, [])
    asys_a_b_R1 = AttributeSystem(astr_a_b_R1, [])
    asys_a_b_R1_R2 = AttributeSystem(astr_a_b_R1_R2, [])

    asys_a_b_R1_R2 -= R2
    assert asys_a_b_R1_R2 == asys_a_b_R1
    assert asys_a_b_R1_R2 is not asys_a_b_R1
    asys_a_b_R1_R2 -= R1
    assert asys_a_b_R1_R2 == asys_a_b
    assert asys_a_b_R1_R2 is not asys_a_b
    asys_a_b_R1_R2 -= b
    assert asys_a_b_R1_R2 == asys_a
    assert asys_a_b_R1_R2 is not asys_a
    asys_a_b_R1_R2 -= a
    assert asys_a_b_R1_R2 == asys
    assert asys_a_b_R1_R2 is not asys

def test___getitem__():
    """Test indexing of AttributeSystem."""
    a = Attribute("a", [])
    b = Attribute("b", [])
    R1 = Relation("R1(a) <=> ", ["a"], 1)
    R2 = Relation("R2(a) <=> ", ["b"], 2)

    astr_a_b_R1_R2 = AttributeStructure(a, b, R1, R2)
    objs = ['a', 'b', 'c']
    
    asys_a_b_R1_R2_o = AttributeSystem(astr_a_b_R1_R2, objs)

    ia = asys_a_b_R1_R2_o[a]
    assert ia == a
    assert ia is a
    iR1 = asys_a_b_R1_R2_o[R1]
    assert iR1 == R1
    assert iR1 is R1
    #Test object retrieval with string. Note, strings may not index
    #AttributeStructure members within this AttributeSystem, only objects.
    #To index objects in AttributeStructure in AttributeSystem, use index
    #with asys.astr[index]
    iobj = asys_a_b_R1_R2_o['a']
    assert iobj == objs[0]
    assert iobj is objs[0]

    #Test retrieval by string for AttributeStructure members
    ias = asys_a_b_R1_R2_o._attribute_structure['a']
    assert ias == a
    assert ias is a
    iR1s = asys_a_b_R1_R2_o._attribute_structure['R1']
    assert iR1s == R1
    assert iR1s is R1

def test___contains__():
    """Test "in" operator for AttributeSystem."""
    a = Attribute("a", [])
    b = Attribute("b", [])
    R1 = Relation("R1(a) <=> ", ["a"], 1)
    R2 = Relation("R2(a) <=> ", ["b"], 2)
    
    astr_a_b_R1_R2 = AttributeStructure(a, b, R1, R2)
    objs = ['a', 'b', 'c']

    asys_a_b_R1_R2 = AttributeSystem(astr_a_b_R1_R2, [])
    asys_a_b_R1_R2_o = AttributeSystem(astr_a_b_R1_R2, objs)

    assert a in asys_a_b_R1_R2_o
    assert R1 in asys_a_b_R1_R2_o
    assert astr_a_b_R1_R2 in asys_a_b_R1_R2
    assert astr_a_b_R1_R2 in asys_a_b_R1_R2_o
    with pytest.raises(TypeError) as excinfo:
        asys_a_b_R1_R2 in asys_a_b_R1_R2_o
    #Test strings only checked against objects
    assert 'a' not in asys_a_b_R1_R2
    assert 'a' in asys_a_b_R1_R2._attribute_structure
    assert 'a' in asys_a_b_R1_R2_o

def test___deepcopy__():
    """Test copy.deepcopy for AttributeSystem."""
    a = Attribute("a", [])
    b = Attribute("b", [])
    c = Attribute("c", ['a'])
    R1 = Relation("R1(a) <=> ", ["a"], 1)
    R2 = Relation("R2(a) <=> ", ["b"], 2)
    
    objs = ['a', 'b', 'c']
    astr_a_b_R1_R2 = AttributeStructure(a, b, R1, R2)
    asys_a_b_R1_R2_o = AttributeSystem(astr_a_b_R1_R2, objs)

    import copy
    asys_copy = copy.deepcopy(asys_a_b_R1_R2_o)
    assert asys_copy == asys_a_b_R1_R2_o
    assert asys_copy is not asys_a_b_R1_R2_o
    assert asys_copy._attribute_structure is not asys_a_b_R1_R2_o._attribute_structure
    assert asys_copy._objects is not asys_a_b_R1_R2_o._objects

def test_get_power():
    """Test get_power(); power = n * |A|."""
    a = Attribute("a", [])
    b = Attribute("b", [])
    R1 = Relation("R1(a) <=> ", ["a"], 1)
    R2 = Relation("R2(a) <=> ", ["b"], 2)
    
    astr_a_b = AttributeStructure(a, b)
    astr_a_b_R1_R2 = AttributeStructure(a, b, R1, R2)
    objs = ['a', 'b', 'c']
    
    asys_a_b_o = AttributeSystem(astr_a_b, objs)
    asys_a_b_R1_R2_o = AttributeSystem(astr_a_b_R1_R2, objs)
    #Test when power = 0
    assert AttributeSystem(AttributeStructure(), []).get_power() == 0
    assert AttributeSystem(AttributeStructure(a), []).get_power() == 0
    assert AttributeSystem(AttributeStructure(), ['o1']).get_power() == 0
    #test normal power calculation
    assert asys_a_b_o.get_power() == 6
    assert asys_a_b_R1_R2_o.get_power() == 6

def test___str__():
    """Test str()."""
    a = Attribute("a", [])
    b = Attribute("b", [])
    R1 = Relation("R1(a) <=> ", ["a"], 1)
    R2 = Relation("R2(a) <=> ", ["b"], 2)
    
    astr_a_b_R1_R2 = AttributeStructure(a, b, R1, R2)
    objs = ['a', 'b', 'c']
    
    asys_a_b_R1_R2_o = AttributeSystem(astr_a_b_R1_R2, objs)
    assert str(asys_a_b_R1_R2_o) == "({a, b, c} ; (a: {}, b: {} ; R1,R2))"
    assert str(AttributeSystem(AttributeStructure(), [])) == "({} ; ( ; ))"

def test___repr__():
    """Test repr()."""
    a = Attribute("a", [])
    b = Attribute("b", [])
    R1 = Relation("R1(a) <=> ", ["a"], 1)
    R2 = Relation("R2(a) <=> ", ["b"], 2)
    
    astr_a_b_R1_R2 = AttributeStructure(a, b, R1, R2)
    objs = ['a', 'b', 'c']
    
    asys_a_b_R1_R2_o = AttributeSystem(astr_a_b_R1_R2, objs)
    assert repr(asys_a_b_R1_R2_o) == "({a, b, c} ; (a: {}, b: {} ; R1,R2))"
    assert repr(AttributeSystem(AttributeStructure(), [])) == "({} ; ( ; ))"

def test_is_automorphic():
    """Test if system is automorphic."""
    a = Attribute("a", [])
    b = Attribute("b", [])
    c = Attribute("c", ['a'])
    R1 = Relation("R1(a) <=> ", ["a"], 1)
    R2 = Relation("R2(a) <=> ", ["b"], 2)
    
    astr_c = AttributeStructure(c)
    astr_a_b_R1_R2 = AttributeStructure(a, b, R1, R2)
    objs = ['a', 'b', 'c']
    
    asys_a_b_R1_R2_o = AttributeSystem(astr_a_b_R1_R2, objs)
    asys_auto = AttributeSystem(astr_c, objs)

    assert asys_auto.is_automorphic()
    assert not asys_a_b_R1_R2_o.is_automorphic()    
