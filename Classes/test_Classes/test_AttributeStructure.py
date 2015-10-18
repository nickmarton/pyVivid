"""Attribute Structure unit tests."""

import pytest
from ..Attribute import Attribute
from ..Relation import Relation
from ..AttributeStructure import AttributeStructure

def test___init__():
    """Test AttributeStructure construction."""
    def test_type_params(*ops):
        """Test constructor for TypeErrors with given params."""
        with pytest.raises(TypeError) as excinfo:
            AttributeStructure(*ops)

    def test_value_params(*ops):
        """Test constructor for TypeErrors with given params."""
        with pytest.raises(ValueError) as excinfo:
            AttributeStructure(*ops)

    #Test bad optional param
    test_type_params("a")
    test_type_params(object)

    a = Attribute("a", [])
    b = Attribute("b", [])
    R1 = Relation("R1(a) <=> ", ["a1"], 1)
    R2 = Relation("R2(a) <=> ", ["b"], 2)
    R3 = Relation("R3(a) <=> ", ["a"], 3)

    #Test no duplicate labels
    test_value_params(a, a)
    #Test no duplicate subscripts
    test_value_params(R1, R1)
    #Test D(R) subset of labels
    test_value_params(a, R1)
    #Test out of order construction
    AttributeStructure(R2, R3, b, a)

def test___eq__():
    """Test == operator for AttributeStructure."""
    a1 = Attribute("a1", [])
    a2 = Attribute("a2", [])
    R1 = Relation("R1(a) <=> ", ["a1"], 1)
    R2 = Relation("R2(a) <=> ", ["a1"], 2)

    astr1 = AttributeStructure(a1, a2, R1, R2)
    astr2 = AttributeStructure(a1, a2, R1, R2)
    astr3 = AttributeStructure(R2, R1, a2, a1)
    astr4 = AttributeStructure()
    astr5 = AttributeStructure()

    #Test identity
    assert astr1 == astr1
    #Test regular equality
    assert astr1 == astr2
    #Test out of order constuctions
    assert astr1 == astr3
    #Test empty equality
    assert astr4 ==astr5

def test___ne__():
    """!= operator for AttributeStructure."""
    a1 = Attribute("a1", [])
    a2 = Attribute("a2", [])
    R1 = Relation("R1(a) <=> ", ["a1"], 1)
    R2 = Relation("R2(a) <=> ", ["a1"], 2)

    astr1 = AttributeStructure(a1, a2, R1, R2)
    astr2 = AttributeStructure(a1, R2)
    astr3 =AttributeStructure()
    
    #strict subset-superset tests
    assert astr1 != astr2
    assert astr2 != astr1
    #empty comparison test
    assert astr1 != astr3
    assert astr3 != astr1

def test___add__():
    """Test + operator for AttributeStructure."""
    a = Attribute("a", [])
    b = Attribute("b", [])
    R1 = Relation("R1(a) <=> ", ["a"], 1)
    R2 = Relation("R2(a) <=> ", ["b"], 2)
    astr_empty = AttributeStructure()
    astr_a = AttributeStructure(a)
    astr_a_R1 = AttributeStructure(a, R1)
    astr_a_b_R1_R2 = AttributeStructure(a, b, R1, R2)

    #test empty addition and identities after
    assert astr_a == astr_empty + a
    assert astr_a is not astr_empty
    #test simplest chained addition
    assert astr_a_R1 == astr_empty + a + R1
    assert astr_a_R1 is not astr_empty
    assert astr_a_R1 is not R1
    #test chained addition
    assert astr_a_b_R1_R2 == astr_empty + a + b + R1 + R2
    assert astr_a_b_R1_R2 == astr_empty + b + a + R1 + R2
    assert astr_a_b_R1_R2 == astr_empty + a + b + R2 + R1
    assert astr_a_b_R1_R2 == a + astr_empty + b + R1 + R2
    assert astr_a_b_R1_R2 == a + b + astr_empty + R1 + R2
    assert astr_a_b_R1_R2 == a + b + R1 + astr_empty + R2
    assert astr_a_b_R1_R2 == a + b + R1 + R2 + astr_empty
    assert astr_a_b_R1_R2 is not astr_empty
    assert astr_a_b_R1_R2 is not a
    assert astr_a_b_R1_R2 is not b
    assert astr_a_b_R1_R2 is not R1
    assert astr_a_b_R1_R2 is not R2

def test___sub__():
    """Test - uperator for AttributeStructure."""
    def test_ValueError(astr, sub):
        """Test constructor for TypeErrors with given params."""
        with pytest.raises(ValueError) as excinfo:
            astr - sub

    def test_KeyError(astr, sub):
        """Test constructor for TypeErrors with given params."""
        with pytest.raises(KeyError) as excinfo:
            astr - sub

    def test_TypeError(astr, sub):
        """Test constructor for TypeErrors with given params."""
        with pytest.raises(TypeError) as excinfo:
            astr - sub

    a = Attribute("a", [])
    b = Attribute("b", [])
    R1 = Relation("R1(a) <=> ", ["a"], 1)
    R2 = Relation("R2(a) <=> ", ["b"], 2)
    astr_empty = AttributeStructure()
    astr_a = AttributeStructure(a)
    astr_a_R1 = AttributeStructure(a, R1)
    astr_a_b_R1_R2 = AttributeStructure(a, b, R1, R2)

    #Test invalid subtraction error catching
    test_ValueError(astr_empty, a)
    test_KeyError(astr_empty, R1)
    test_TypeError(astr_empty, None)
    test_TypeError(astr_empty, "")
    test_TypeError(astr_empty, object)
    test_ValueError(astr_empty, astr_a)
    test_ValueError(astr_empty, astr_a_R1)
    
    astr_a_copy = AttributeStructure(a)
    test_ValueError(astr_a, astr_a_R1)
    assert astr_a_copy == astr_a

    #Test attribute removal
    assert astr_empty == astr_a - a
    assert astr_a == astr_a_R1 - R1
    assert astr_empty == astr_a_R1 - R1 - a
    #tTest invalid remaining Relation's D(R)s
    with pytest.raises(ValueError) as excinfo:
        astr_a_R1 - a
    
    #Test chained subtraction
    assert astr_empty == astr_a_b_R1_R2 - R1 - R2 - a - b


def test___iadd__():
    """."""
    pass
def test___isub__():
    """."""
    pass
def test___deepcopy__():
    """."""
    pass
def test_set_attributes():
    """."""
    pass
def test_set_relations():
    """."""
    pass
def test_get_labels():
    """."""
    pass
def test_get_attribute():
    """."""
    pass
def test_get_relation():
    """."""
    pass
def test_get_subscripts():
    """."""
    pass
def test_get_cardinality():
    """."""
    pass
def test___str__():
    """."""
    pass
def test___repr__():
    """."""
    pass