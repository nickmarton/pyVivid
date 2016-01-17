"""Relation class unit tests."""

import pytest
from vivid.classes.relation import Relation


def test___init__():
    """Test Relation object construction."""

    def test_TypeError(definition, D_of_r, subscript):
        """Test constructor for TypeErrors with given params."""
        with pytest.raises(TypeError) as excinfo:
            Relation(definition, D_of_r, subscript)

    def test_ValueError(definition, D_of_r, subscript):
        """Test constructor for TypeErrors with given params."""
        with pytest.raises(ValueError) as excinfo:
            Relation(definition, D_of_r, subscript)

    # ignore valid definition errors as handled in test_is_valid_definition
    # definition is a string test
    test_TypeError([], [], 0)
    # D(R) is a list test
    test_TypeError("R1(a,b,c) <=> ", "not list", 1)
    # D(R) only strings test
    test_TypeError("R1(a,b,c) <=> ", [1, 2, 3], 1)
    test_TypeError("R1(o) <=> ", [object], 1)
    # subscript is an int test
    test_TypeError("R1(a,b,c) <=> ", ["a", "b", "c"], "not int")
    test_TypeError("R1(a,b,c) <=> ", ["a", "b", "c"], object)
    # parameter cardinality mismatch test
    test_ValueError("R1(a,b,c) <=> ", ["a", "b"], 1)
    test_ValueError("R1(a,b) <=> ", ["a", "b", "c"], 1)
    # definition subscript, argument subscript mismatch test
    test_ValueError("R1(a,b) <=> ", ["a", "b", "c"], 2)


def test___eq__():
    """Test == operator."""
    r1 = Relation("R1(a) <=> ", ["a"], 1)
    r2 = Relation("R1(a) <=> ", ["a"], 1)
    # only the same Relation is equal to itself
    assert r1 == r1
    assert r1 == r2


def test___ne__():
    """Test != operator."""
    r1 = Relation("R1(a) <=> ", ["a"], 1)
    # different definitions test
    r2 = Relation("R2(a) <=> ", ["a"], 2)
    # different D(R)'s test
    r3 = Relation("R1(a) <=> ", ["b"], 1)

    assert r1 != r2
    assert r1 != r3


def test___add__():
    """Test + operator."""
    from vivid.classes.attribute import Attribute
    from vivid.classes.attribute_structure import AttributeStructure

    a1 = Attribute("a1", [])
    a2 = Attribute("a2", [])
    r1 = Relation("R1(a) <=> ", ["a1"], 1)
    astr = AttributeStructure()
    astr_a1 = AttributeStructure(a1)
    astr_a1_r1 = AttributeStructure(a1, r1)
    astr_a1_a2 = AttributeStructure(a1, a2)
    astr_r1_a1_a2 = AttributeStructure(a1, a2, r1)

    # test adding Relation to empty AttributeStructure fails
    with pytest.raises(ValueError) as excinfo:
        r1 + astr

    assert astr_a1_r1 == r1 + a1
    assert astr_a1_r1 == a1 + r1
    assert astr_a1_r1 == r1 + astr_a1
    assert astr_a1_r1 == astr_a1 + r1
    assert astr_r1_a1_a2 == astr_a1_a2 + r1
    assert astr_r1_a1_a2 == r1 + astr_a1_a2


def test___iadd__():
    """Test += operator."""
    from vivid.classes.attribute import Attribute
    from vivid.classes.attribute_structure import AttributeStructure

    a1 = Attribute("a1", [])
    r1 = Relation("R1(a) <=> ", ["a1"], 1)
    astr_a1 = AttributeStructure(a1)
    astr_a1_copy = AttributeStructure(a1)
    astr_a1_r1 = AttributeStructure(a1, r1)

    # test adding Relation to AttributeStructure
    astr_a1 += r1
    assert astr_a1_r1 == astr_a1
    assert hasattr(r1, "_is_Relation")
    # test implicit conversion of Relation into AttributeStructure
    r1 += astr_a1_copy
    assert astr_a1_r1 == r1
    assert not hasattr(r1, "_is_Relation")
    assert hasattr(r1, "_is_AttributeStructure")


def test___deepcopy__():
    """."""
    """Test copy.deepcopy functionality of Attribute object."""
    from copy import deepcopy
    r = Relation("R1(a) <=> ", ["a1"], 1)
    r_copy = deepcopy(r)

    assert r == r_copy
    assert r is not r_copy


def test___str__():
    """Test str(Relation)."""
    R1 = Relation(
        'R1(p1,l1) <=> p1 is_on_line l1', ['position', 'line_positions'], 1)
    R1_str = "R1 is a subset of position X line_positions, "
    R1_str += "defined as follows: R1(p1,l1) <=> p1 is_on_line l1"
    assert str(R1) == R1_str

    R2 = Relation("R2(a) <=> ", ["a1"], 2)
    assert str(R2) == "R2 is a subset of a1, defined as follows: R2(a) <=> "


def test___repr__():
    """Test str(Relation)."""
    R1 = Relation(
        'R1(p1,l1) <=> p1 is_on_line l1', ['position', 'line_positions'], 1)
    R2 = Relation("R2(a) <=> ", ["a1"], 2)

    assert R1.__repr__() == "R1"
    assert R2.__repr__() == "R2"


def test_set_definition():
    """Test set_definition function."""
    r = Relation("R1(a) <=> ", ["a"], 1)

    def test_TypeError(definition):
        """Test constructor for TypeErrors with given params."""
        with pytest.raises(TypeError) as excinfo:
            r.set_definition(definition)

    def test_ValueError(definition):
        """Test constructor for TypeErrors with given params."""
        with pytest.raises(ValueError) as excinfo:
            r.set_definition(definition)

    # non-string test
    test_TypeError(None)
    # invalid definition test
    test_ValueError("invalid definition")


def test_get_DR():
    """Test get_DR function."""
    r = Relation("R1(a,b,c) <=> ", ["a", 'b', 'c'], 1)
    assert r.get_DR() == ["a", 'b', 'c']
    assert r.get_DR(string=True) == "a X b X c"


def test_set_DR():
    """Test set_DR function."""
    r = Relation("R1(a) <=> ", ["a"], 1)

    def test_TypeError(DR):
        """Test TypeErrors in set_DR function."""
        with pytest.raises(TypeError) as excinfo:
            r.set_DR(DR)

    def test_ValueError(DR):
        """Test TypeErrors in set_DR function."""
        with pytest.raises(ValueError) as excinfo:
            r.set_DR(DR)

    # not a list test
    test_TypeError(1)
    # empty list test
    test_TypeError([])
    # list with non string elements test
    test_TypeError([1])
    # cardinality mismatch test
    test_ValueError(["a", "b"])


def test_get_arity():
    """Test get_arity function."""
    r = Relation("R1(a,b,c) <=> ", ["a", 'b', 'c'], 1)
    assert r.get_arity() == 3


def test_is_valid_definition():
    """Test is_valid_definition function."""
    # correct definition form test
    assert Relation.is_valid_definition("R1(a,b,c) <=>")
    # whitespace correction test
    assert Relation.is_valid_definition("    R 1(  a, b ,  c  ) <   = > ")
