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
    """."""
    pass

def test___add__():
    """."""
    pass

def test___sub__():
    """."""
    pass

def test___iadd__():
    """."""
    pass

def test___isub__():
    """."""
    pass

def test___getitem__():
    """."""
    pass

def test___contains__():
    """."""
    pass

def test___deepcopy__():
    """."""
    pass

def test_get_power():
    """."""
    pass

def test___str__():
    """."""
    pass

def test___repr__():
    """."""
    pass

def test_is_automorphic():
    """."""
    pass
