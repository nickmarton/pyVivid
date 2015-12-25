"""VariableAssignment unit tests."""

import pytest
from vivid.Classes.Attribute import Attribute
from vivid.Classes.RelationSymbol import RelationSymbol
from vivid.Classes.AttributeStructure import AttributeStructure
from vivid.Classes.AttributeSystem import AttributeSystem
from vivid.Classes.Vocabulary import Vocabulary
from vivid.Classes.VariableAssignment import VariableAssignment


def test___init__():
    """Test VariableAssignment constructor."""
    def test_TypeError(vocabulary, attribute_system, mapping):
        """Test constructor for TypeErrors with given params."""
        with pytest.raises(TypeError) as excinfo:
            VariableAssignment(vocabulary, attribute_system, mapping)

    def test_ValueError(vocabulary, attribute_system, mapping):
        """Test constructor for ValueErrors with given params."""
        with pytest.raises(ValueError) as excinfo:
            VariableAssignment(vocabulary, attribute_system, mapping)

    vocabulary = Vocabulary(['C'], [RelationSymbol('R', 1)], ['V'])

    a = Attribute("a", [])
    b = Attribute("b", [])
    astr = AttributeStructure(a, b)
    objs = ['a', 'b', 'c']
    attribute_system = AttributeSystem(astr, objs)

    test_TypeError(vocabulary, attribute_system, {'V': 1})
    test_TypeError(vocabulary, attribute_system, {1: 'a'})
    test_ValueError(vocabulary, attribute_system, {'V': 'bad'})
    test_ValueError(vocabulary, attribute_system, {'bad': 'a'})

    VA = VariableAssignment(vocabulary, attribute_system, {'V': 'a'})


def test___eq__():
    """Test == operator for VariableAssignment object."""
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

    mapping1 = {'V': 'a'}
    mapping2 = {'V': 'b'}

    A1 = VariableAssignment(vocabulary1, attribute_system1, mapping1)
    A2 = VariableAssignment(vocabulary1, attribute_system1, mapping1)
    A3 = VariableAssignment(vocabulary1, attribute_system1, mapping2)

    assert A1 == A1
    assert A1 == A2
    assert not A1 == A3


def test___ne__():
    """Test != operator for VariableAssignment object."""
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

    mapping1 = {'V': 'a'}
    mapping2 = {'V': 'b'}

    A1 = VariableAssignment(vocabulary1, attribute_system1, mapping1)
    A2 = VariableAssignment(vocabulary1, attribute_system1, mapping1)
    A3 = VariableAssignment(vocabulary1, attribute_system1, mapping2)

    assert not A1 != A1
    assert not A1 != A2
    assert A1 != A3


def test___getitem__():
    """Test indexing for VariableAssignment object."""
    def test_TypeError(variable_assignment, key):
        """Test constructor for TypeErrors with given params."""
        with pytest.raises(TypeError) as excinfo:
            variable_assignment[key]

    def test_KeyError(variable_assignment, key):
        """Test constructor for KeyErrors with given params."""
        with pytest.raises(KeyError) as excinfo:
            variable_assignment[key]

    vocabulary = Vocabulary(['C'], [RelationSymbol('R', 1)], ['V'])

    a = Attribute("a", [])
    b = Attribute("b", [])
    astr = AttributeStructure(a, b)
    objs = ['a', 'b', 'c']
    attribute_system = AttributeSystem(astr, objs)

    mapping = {'V': 'a'}

    VA = VariableAssignment(vocabulary, attribute_system, mapping)

    test_TypeError(VA, 1)
    test_TypeError(VA, None)
    test_TypeError(VA, object)
    test_KeyError(VA, '')

    assert VA['V'] == 'a'


def test___deepcopy__():
    """Test copy.deepcopy for VariableAssignment object."""
    from copy import deepcopy

    vocabulary = Vocabulary(['C'], [RelationSymbol('R', 1)], ['V'])

    a = Attribute("a", [])
    b = Attribute("b", [])
    astr = AttributeStructure(a, b)
    objs = ['a', 'b', 'c']
    attribute_system = AttributeSystem(astr, objs)

    mapping = {'V': 'a'}

    VA = VariableAssignment(vocabulary, attribute_system, mapping)

    VA_copy = deepcopy(VA)
    assert VA == VA_copy
    assert VA is not VA_copy
    assert VA._vocabulary is not VA_copy._vocabulary
    assert VA._attribute_system is not VA_copy._attribute_system
    assert VA._mapping is not VA_copy._mapping


def test___str__():
    """Test str(VariableAssignment)."""
    vocabulary = Vocabulary(['C', 'C\''], [RelationSymbol('R', 1)], ['V'])

    a = Attribute("a", [])
    b = Attribute("b", [])
    astr = AttributeStructure(a, b)
    objs = ['a', 'b', 'c']
    attribute_system = AttributeSystem(astr, objs)

    mapping = {'V': 'a'}

    VA = VariableAssignment(vocabulary, attribute_system, mapping)

    assert VA.__str__() == "VA{'V': 'a'}"


def test___repr__():
    """Test repr(VariableAssignment)."""
    vocabulary = Vocabulary(['C', 'C\''], [RelationSymbol('R', 1)], ['V'])

    a = Attribute("a", [])
    b = Attribute("b", [])
    astr = AttributeStructure(a, b)
    objs = ['a', 'b', 'c']
    attribute_system = AttributeSystem(astr, objs)

    mapping = {'V': 'a'}

    VA = VariableAssignment(vocabulary, attribute_system, mapping)

    assert VA.__repr__() == "VA{'V': 'a'}"
