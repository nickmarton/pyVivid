"""Relation class unit tests."""

import pytest
from ..Relation import Relation

def test___init__():
    """Test Relation object construction."""

    def test_type_params(definition, D_of_r, subscript):
        """Test constructor for TypeErrors with given params."""
        with pytest.raises(TypeError) as excinfo:
            Relation(definition, D_of_r, subscript)

    def test_value_params(definition, D_of_r, subscript):
        """Test constructor for TypeErrors with given params."""
        with pytest.raises(ValueError) as excinfo:
            Relation(definition, D_of_r, subscript)

    #ignore valid definition errors as handled in test_is_valid_definition
    #definition is a string test
    test_type_params([], [], 0)
    #D(R) is a list test
    test_type_params("R1(a,b,c) <=> ", "not list", 0)
    #D(R) only strings test
    test_type_params("R1(a,b,c) <=> ", [1,2,3], 0)
    test_type_params("R1(o) <=> ", [object], 0)
    #subscript is an int test
    test_type_params("R1(a,b,c) <=> ", ["a", "b", "c"], "not int")
    test_type_params("R1(a,b,c) <=> ", ["a", "b", "c"], object)
    #parameter cardinality mismatch test
    test_value_params("R1(a,b,c) <=> ", ["a", "b"], 0)
    test_value_params("R1(a,b) <=> ", ["a", "b", "c"], 0)

def test___eq__():
    """Test == operator."""
    r1 = Relation("R1(a) <=> ", ["a"], 0)
    r2 = Relation("R1(a) <=> ", ["a"], 0)
    #only the same Relation is equal to itself
    assert r1 == r1
    assert r1 == r2

def test___ne__():
    """Test != operator."""
    r1 = Relation("R1(a) <=> ", ["a"], 0)
    #different definitions test
    r2 = Relation("R2(a) <=> ", ["a"], 0)
    #different D(R)'s test
    r3 = Relation("R1(a) <=> ", ["b"], 0)
    #different subscripts test
    r4 = Relation("R1(a) <=> ", ["a"], 1)
    
    assert r1 != r2
    assert r1 != r3
    assert r1 != r4

def test___add__():
    """Test + operator."""
    from ..Attribute import Attribute
    from ..AttributeStructure import AttributeStructure

    a1 = Attribute("a1", [])
    r1 = Relation("R1(a) <=> ", ["a1"], 0)
    astr_a1 = AttributeStructure(a1)
    astr_a1_r1 = AttributeStructure(a1, r1)

    assert astr_a1_r1 == r1 + a1
    assert astr_a1_r1 == a1 + r1
    assert astr_a1_r1 == r1 + astr_a1
    assert astr_a1_r1 == astr_a1 + r1

def test___iadd__():
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

def test_set_definition():
    """Test set_definition function."""
    r = Relation("R1(a) <=> ", ["a"], 0)

    def test_type_params(definition):
        """Test constructor for TypeErrors with given params."""
        with pytest.raises(TypeError) as excinfo:
            r.set_definition(definition)

    def test_value_params(definition):
        """Test constructor for TypeErrors with given params."""
        with pytest.raises(ValueError) as excinfo:
            r.set_definition(definition)

    #non-string test
    test_type_params(None)
    #invalid definition test
    test_value_params("invalid definition")

def test_get_DR():
    """."""
    pass

def test_set_DR():
    """Test set_DR function."""
    r = Relation("R1(a) <=> ", ["a"], 0)

    def test_type_params(DR):
        """Test TypeErrors in set_DR function."""
        with pytest.raises(TypeError) as excinfo:
            r.set_DR(DR)

    def test_value_params(DR):
        """Test TypeErrors in set_DR function."""
        with pytest.raises(ValueError) as excinfo:
            r.set_DR(DR)

    #not a list test
    test_type_params(1)
    #empty list test
    test_type_params([])
    #list with non string elements test
    test_type_params([1])
    #cardinality mismatch test
    test_value_params(["a", "b"])

def test_get_arity():
    """."""
    pass

def test_is_valid_definition():
    """Test is_valid_definition function."""
    
    #correct definition form test
    assert Relation.is_valid_definition("R1(a,b,c) <=>")
    #whitespace correction test
    assert Relation.is_valid_definition("    R 1(  a, b ,  c  ) <   = > ")
