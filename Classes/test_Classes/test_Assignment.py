"""Assignment unit tests."""

import pytest
from vivid.Classes.Attribute import Attribute
from vivid.Classes.RelationSymbol import RelationSymbol
from vivid.Classes.AttributeStructure import AttributeStructure
from vivid.Classes.AttributeSystem import AttributeSystem
from vivid.Classes.RelationSymbol import RelationSymbol
from vivid.Classes.Vocabulary import Vocabulary
from vivid.Classes.Assignment import Assignment

def test___init__():
    """Test Assignment constructor."""
    def test_TypeError(vocabulary, attribute_system):
        """Test constructor for TypeErrors with given params."""
        with pytest.raises(TypeError) as excinfo:
            Assignment(vocabulary, attribute_system)

    vocabulary = Vocabulary(['C'], [RelationSymbol('R', 1)], ['V'])

    a = Attribute("a", [])
    b = Attribute("b", [])
    astr = AttributeStructure(a, b)
    objs = ['a', 'b', 'c']
    attribute_system = AttributeSystem(astr, objs)

    #test type errors
    test_TypeError(None, attribute_system)
    test_TypeError('', attribute_system)
    test_TypeError(object, attribute_system)
    test_TypeError(vocabulary, None)
    test_TypeError(vocabulary, '')
    test_TypeError(vocabulary, object)

    #test reference breaking
    A = Assignment(vocabulary, attribute_system)
    assert vocabulary is not A._vocabulary
    assert attribute_system is not A._attribute_system

def test___eq__():
    """Test == operator for Assignment object."""
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

    A1 = Assignment(vocabulary1, attribute_system1)
    A2 = Assignment(vocabulary1, attribute_system1)
    A3 = Assignment(vocabulary1, attribute_system2)
    A4 = Assignment(vocabulary2, attribute_system1)

    assert A1 == A2
    assert A1._vocabulary is not A2._vocabulary
    assert A1._attribute_system is not A2._attribute_system
    assert not A1 == A3
    assert not A1 == A4

def test___ne__():
    """Test != operator for Assignment object."""
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

    A1 = Assignment(vocabulary1, attribute_system1)
    A2 = Assignment(vocabulary1, attribute_system1)
    A3 = Assignment(vocabulary1, attribute_system2)
    A4 = Assignment(vocabulary2, attribute_system1)

    assert not A1 != A2
    assert A1._vocabulary is not A2._vocabulary
    assert A1._attribute_system is not A2._attribute_system
    assert A1 != A3
    assert A1 != A4
