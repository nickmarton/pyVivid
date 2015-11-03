"""Assignment unit tests."""

import pytest
from vivid.Classes.Attribute import Attribute
from vivid.Classes.RelationSymbol import RelationSymbol
from vivid.Classes.AttributeStructure import AttributeStructure
from vivid.Classes.AttributeSystem import AttributeSystem
from vivid.Classes.RelationSymbol import RelationSymbol
from vivid.Classes.Vocabulary import Vocabulary
from vivid.Classes.Assignment import Assignment
from vivid.Classes.ConstantAssignment import ConstantAssignment

def test___init__():
    """Test ConstantAssignment constructor."""
    def test_TypeError(vocabulary, attribute_system, mapping):
        """Test constructor for TypeErrors with given params."""
        with pytest.raises(TypeError) as excinfo:
            ConstantAssignment(vocabulary, attribute_system, mapping)
    def test_ValueError(vocabulary, attribute_system, mapping):
        """Test constructor for ValueErrors with given params."""
        with pytest.raises(ValueError) as excinfo:
            ConstantAssignment(vocabulary, attribute_system, mapping)

    vocabulary = Vocabulary(['C'], [RelationSymbol('R', 1)], ['V'])

    a = Attribute("a", [])
    b = Attribute("b", [])
    astr = AttributeStructure(a, b)
    objs = ['a', 'b', 'c']
    attribute_system = AttributeSystem(astr, objs)

    test_TypeError(vocabulary, attribute_system, {'C': 1})
    test_TypeError(vocabulary, attribute_system, {1: 'a'})
    test_ValueError(vocabulary, attribute_system, {'C': 'bad'})
    test_ValueError(vocabulary, attribute_system, {'C': 'a', 'C2': 'a'})
    test_ValueError(vocabulary, attribute_system, {'bad': 'a'})

    C = ConstantAssignment(vocabulary, attribute_system, {'C': 'a'})

def test___eq__():
    """Test == operator for ConstantAssignment object."""
    vocabulary1 = Vocabulary(['C'], [RelationSymbol('R', 1)], ['V'])
    vocabulary2 = Vocabulary(['C\''], [RelationSymbol('R\'', 1)], ['V\''])

    a = Attribute("a", [])
    b = Attribute("b", [])
    astr1 = AttributeStructure(a, b)
    astr2 = AttributeStructure(b)
    objs1 = ['a', 'b', 'c']
    objs2 = ['a']
    attribute_system1 = AttributeSystem(astr1, objs1)
    attribute_system2 = AttributeSystem(astr2, objs2)

    mapping1 = {'C': 'a'}
    mapping2 = {'C': 'b'}

    A1 = ConstantAssignment(vocabulary1, attribute_system1, mapping1)
    A2 = ConstantAssignment(vocabulary1, attribute_system1, mapping1)
    A3 = ConstantAssignment(vocabulary2, attribute_system1, {})
    A4 = ConstantAssignment(vocabulary1, attribute_system2, {})
    A5 = ConstantAssignment(vocabulary1, attribute_system1, mapping2)

    assert A1 == A1
    assert A1 == A2
    assert not A1 == A3
    assert not A1 == A4
    assert not A1 == A5

def test___ne__():
    """Test != operator for ConstantAssignment object."""
    vocabulary1 = Vocabulary(['C'], [RelationSymbol('R', 1)], ['V'])
    vocabulary2 = Vocabulary(['C\''], [RelationSymbol('R\'', 1)], ['V\''])

    a = Attribute("a", [])
    b = Attribute("b", [])
    astr1 = AttributeStructure(a, b)
    astr2 = AttributeStructure(b)
    objs1 = ['a', 'b', 'c']
    objs2 = ['a']
    attribute_system1 = AttributeSystem(astr1, objs1)
    attribute_system2 = AttributeSystem(astr2, objs2)

    mapping1 = {'C': 'a'}
    mapping2 = {'C': 'b'}

    A1 = ConstantAssignment(vocabulary1, attribute_system1, mapping1)
    A2 = ConstantAssignment(vocabulary1, attribute_system1, mapping1)
    A3 = ConstantAssignment(vocabulary2, attribute_system1, {})
    A4 = ConstantAssignment(vocabulary1, attribute_system2, {})
    A5 = ConstantAssignment(vocabulary1, attribute_system1, mapping2)

    assert not A1 != A1
    assert not A1 != A2
    assert A1 != A3
    assert A1 != A4
    assert A1 != A5

def test___getitem__():
    """Test indexing for ConstantAssignment object."""
    pass

def test___deepcopy__():
    """Test copy.deepcopy for ConstantAssignment object."""
    pass

def test_is_total():
    """Test is_total function for ConstantAssignment object."""
    pass

def test_get_domain():
    """Test get_domain function for ConstantAssignment object."""
    pass

def test_in_conflict():
    """Test in_conflict function for ConstantAssignment object."""
    pass

def test___str__():
    """Test str(ConstantAssignment)."""
    pass

def test___repr__():
    """Test repr(ConstantAssignment)."""
    pass
