"""Attribute Structure unit tests."""

import pytest
from ..Attribute import Attribute
from ..Relation import Relation
from ..AttributeStructure import AttributeStructure

def test___init__():
    """Test AttributeStructure construction."""
    def test_TypeError(*ops):
        """Test constructor for TypeErrors with given params."""
        with pytest.raises(TypeError) as excinfo:
            AttributeStructure(*ops)

    def test_ValueError(*ops):
        """Test constructor for TypeErrors with given params."""
        with pytest.raises(ValueError) as excinfo:
            AttributeStructure(*ops)

    #Test bad optional param
    test_TypeError("a")
    test_TypeError(object)

    a = Attribute("a", [])
    b = Attribute("b", [])
    R1 = Relation("R1(a) <=> ", ["a1"], 1)
    R2 = Relation("R2(a) <=> ", ["b"], 2)
    R3 = Relation("R3(a) <=> ", ["a"], 3)

    #Test no duplicate labels
    test_ValueError(a, a)
    #Test no duplicate subscripts
    test_ValueError(R1, R1)
    #Test D(R) subset of labels
    test_ValueError(a, R1)
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

def test___le__():
    """Test total ordering."""
    a = Attribute("a", [])
    b = Attribute("b", [])
    R1 = Relation("R1(a) <=> ", ["a"], 1)
    R2 = Relation("R2(a) <=> ", ["b"], 2)
    astr_empty = AttributeStructure()
    astr_a = AttributeStructure(a)
    astr_a_R1 = AttributeStructure(a, R1)
    astr_a_b_R1_R2 = AttributeStructure(a, b, R1, R2)

    #Test subsets and strict subsets
    assert not astr_empty < astr_empty
    assert astr_empty <= astr_empty
    assert astr_empty < astr_a_b_R1_R2
    assert astr_empty <= astr_a_b_R1_R2
    assert astr_a < astr_a_b_R1_R2
    assert astr_a <= astr_a_b_R1_R2
    assert astr_a_R1 < astr_a_b_R1_R2
    assert astr_a_R1 <= astr_a_b_R1_R2
    assert not astr_a_b_R1_R2 < astr_a_b_R1_R2
    assert astr_a_b_R1_R2 <= astr_a_b_R1_R2

    #Test supersets and strict supersets
    assert not astr_empty > astr_empty
    assert astr_empty >= astr_empty
    assert astr_a_b_R1_R2 > astr_empty
    assert astr_a_b_R1_R2 >= astr_empty
    assert astr_a_b_R1_R2 > astr_a
    assert astr_a_b_R1_R2 >= astr_a
    assert astr_a_b_R1_R2 > astr_a_R1
    assert astr_a_b_R1_R2 >= astr_a_R1
    assert not astr_a_b_R1_R2 > astr_a_b_R1_R2
    assert astr_a_b_R1_R2 >= astr_a_b_R1_R2

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
    """Test - operator for AttributeStructure."""
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
    #Test invalid remaining Relation's D(R)s
    with pytest.raises(ValueError) as excinfo:
        astr_a_R1 - a
    #Test chained subtraction
    assert astr_empty == astr_a_b_R1_R2 - R1 - R2 - a - b

def test___iadd__():
    """Test += operator for AttributeStructure."""
    a = Attribute("a", [])
    b = Attribute("b", [])
    R1 = Relation("R1(a) <=> ", ["a"], 1)
    R2 = Relation("R2(a) <=> ", ["b"], 2)
    astr_empty = AttributeStructure()
    astr_a = AttributeStructure(a)
    astr_a_b = AttributeStructure(a, b)
    astr_a_b_R1 = AttributeStructure(a, b, R1)
    astr_a_b_R1_R2 = AttributeStructure(a, b, R1, R2)

    astr_empty += a
    assert astr_a == astr_empty
    astr_empty += b
    assert astr_a_b == astr_empty
    astr_empty += R1
    assert astr_a_b_R1 == astr_empty
    astr_empty += R2
    assert astr_a_b_R1_R2 == astr_empty

def test___isub__():
    """Test -= operator for AttributeStructure."""
    def test_ValueError(astr, sub):
        """Test constructor for TypeErrors with given params."""
        with pytest.raises(ValueError) as excinfo:
            astr -= sub

    def test_KeyError(astr, sub):
        """Test constructor for TypeErrors with given params."""
        with pytest.raises(KeyError) as excinfo:
            astr -= sub

    def test_TypeError(astr, sub):
        """Test constructor for TypeErrors with given params."""
        with pytest.raises(TypeError) as excinfo:
            astr -= sub

    a = Attribute("a", [])
    b = Attribute("b", [])
    R1 = Relation("R1(a) <=> ", ["a"], 1)
    R2 = Relation("R2(a) <=> ", ["b"], 2)
    astr_empty = AttributeStructure()
    astr_a = AttributeStructure(a)
    astr_a_R1 = AttributeStructure(a, R1)
    astr_a_b = AttributeStructure(a, b)
    astr_a_b_R1 = AttributeStructure(a, b, R1)
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
    astr_a_b_R1_R2 -= R2
    assert astr_a_b_R1 == astr_a_b_R1_R2
    astr_a_b_R1_R2 -= R1
    assert astr_a_b == astr_a_b_R1_R2
    astr_a_b_R1_R2 -= b
    assert astr_a == astr_a_b_R1_R2
    astr_a_b_R1_R2 -= a
    assert astr_empty == astr_a_b_R1_R2

def test___getitem__():
    """."""
    pass

def test___contains__():
    """."""
    pass

def test___deepcopy__():
    """Test copy.deepcopy for AttributeStructure object."""
    import copy
    a = Attribute("a", [])
    b = Attribute("b", [])
    R1 = Relation("R1(a) <=> ", ["a"], 1)
    R2 = Relation("R2(a) <=> ", ["b"], 2)
    astr_a_b_R1_R2 = AttributeStructure(a, b, R1, R2)

    astr_copy = copy.deepcopy(astr_a_b_R1_R2)
    assert astr_copy == astr_a_b_R1_R2
    assert astr_copy._attributes is not astr_a_b_R1_R2._attributes
    assert astr_copy._relations is not astr_a_b_R1_R2._relations
    assert astr_copy is not astr_a_b_R1_R2

def test_get_labels():
    """Test get_labels function."""
    a = Attribute("a", [])
    b = Attribute("b", [])
    c = Attribute("c", [])

    astr = AttributeStructure(a, b, c)
    assert astr.get_labels() == ['a', 'b', 'c']

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