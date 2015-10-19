"""Attribute class unit tests."""

import pytest
from ..Attribute import Attribute

def test___init__():
    """Test Attribute constructor."""
    def test_TypeError(label, value_set):
        """Test an individual Attribute construction."""
        with pytest.raises(TypeError) as excinfo:
            Attribute(label, value_set)

    #test label errors
    test_TypeError(1, [])
    test_TypeError(1.0, [])
    test_TypeError([], [])
    test_TypeError(set([]), [])
    test_TypeError(object, [])
    #test value_set errors
    test_TypeError("", 1)
    test_TypeError("", 1.0)
    test_TypeError("", "")
    test_TypeError("", set([]))
    test_TypeError("", object)

def test___eq__():
    """Test == operator."""
    A1, A2 = Attribute("label", []), Attribute("label", [])
    assert A1 == A2

def test___ne__():
    """Test != operator."""
    A1, A2 = Attribute("lbl", []), Attribute("label", [])
    A3, A4 = Attribute("label", [1]), Attribute("label", [])
    assert A1 != A2
    assert A3 != A4

def test___add__():
    """Test + operator."""
    from ..Relation import Relation
    from ..AttributeStructure import AttributeStructure
    
    a1 = Attribute("a1", [])
    a2 = Attribute("a2", [])
    r1 = Relation("R1(a) <=> ", ["a1"], 1)
    astr = AttributeStructure()
    astr_a1 = AttributeStructure(a1)
    astr_a1_a2 = AttributeStructure(a1, a2)
    astr_a1_r1 = AttributeStructure(a1, r1)
    astr_a1_a2_r1 = AttributeStructure(a1, a2, r1)

    #add AttributeStructure and Attribute
    assert astr_a1 == astr + a1
    assert astr_a1 == a1 + astr
    #add Attribute and Attribute
    assert astr_a1_a2 == a1 + a2
    assert astr_a1_a2 == a2 + a1
    #add Attribute and Relation
    assert astr_a1_r1 == a1 + r1
    assert astr_a1_r1 == r1 + a1
    assert astr_a1_a2_r1 == a1 + a2 + r1
    assert astr_a1_a2_r1 == a2 + a1 + r1
    assert astr_a1_a2_r1 == r1 + a1 + a2
    #Test for when + fails, i.e. when Relation is added before attributes with
    #its D(R) labels.
    with pytest.raises(ValueError) as excinfo:
        r1 + a2 + a1

def test___iadd__():
    """Test += operator."""
    from ..Relation import Relation
    from ..AttributeStructure import AttributeStructure
    
    a1 = Attribute("a1", [])
    r1 = Relation("R1(a) <=> ", ["a1"], 1)
    astr = AttributeStructure()
    astr_a1 = AttributeStructure(a1)
    astr_a1_r1 = AttributeStructure(a1, r1)

    #add AttributeStructure and Relation
    astr_a1 += r1
    assert astr_a1_r1 == astr_a1
    #add Relation to Attribute implicitly converting a1 to AttributeStructure
    a1 += r1
    assert a1 == astr_a1
    assert not hasattr(a1, "_is_Attribute")
    assert hasattr(a1, "_is_AttributeStructure")

def test___deepcopy__():
    """Test copy.deepcopy functionality of Attribute object."""
    from copy import deepcopy
    a = Attribute("label", ["v1", "v2"])
    a_copy = deepcopy(a)

    assert a == a_copy
    assert a is not a_copy

def test___str__():
    """Test str()."""
    from ..Interval import Interval
    a = Attribute("label", ["1", Interval(40,50), True, 4.0, 6L])
    assert a.__str__() == "label: {4.0,6,1,True,I(40, 50)}"

def test___repr__():
    """ Test repr()."""
    from ..Interval import Interval
    a = Attribute("label", ["1", Interval(40,50), True, 4.0, 6L])
    print a.__repr__()
    assert a.__repr__() == "\"label: {4.0,6,1,True,I(40, 50)}\""

def test__key():
    """Test Attribute hash key."""
    A = Attribute("", [])
    A2 = Attribute("label", [1, 'string', True])
    assert A._key() == ("", '[]')
    assert A2._key() == ("label", "[1, 'string', True]")

def test___hash__():
    """test hash function for Attribute."""
    A = Attribute("label", [1, "string", True])
    B = Attribute("", [])
    assert hash(B._key()) == -7159864980619513463
    assert hash(A._key()) == 3112214484200701409
