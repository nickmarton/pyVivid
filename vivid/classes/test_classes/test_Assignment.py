"""Assignment unit tests."""

import pytest
from vivid.classes.attribute import Attribute
from vivid.classes.relation_symbol import RelationSymbol
from vivid.classes.attribute_structure import AttributeStructure
from vivid.classes.attribute_system import AttributeSystem
from vivid.classes.vocabulary import Vocabulary
from vivid.classes.assignment import Assignment


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

    # test type errors
    test_TypeError(None, attribute_system)
    test_TypeError('', attribute_system)
    test_TypeError(object, attribute_system)
    test_TypeError(vocabulary, None)
    test_TypeError(vocabulary, '')
    test_TypeError(vocabulary, object)

    # test reference keeping and breaking
    A = Assignment(vocabulary, attribute_system)
    assert vocabulary is A._vocabulary
    assert attribute_system is not A._attribute_system

    vocabulary.add_constant('cx')
    vocabulary.add_variable('vx')
    assert 'cx' in A._vocabulary._C
    assert 'vx' in A._vocabulary._V
    A._vocabulary.add_constant('cx2')
    A._vocabulary.add_variable('vx2')
    assert 'cx2' in vocabulary._C
    assert 'vx2' in vocabulary._V


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
    assert A1._vocabulary is A2._vocabulary
    assert A1._attribute_system is not A2._attribute_system
    assert not A1 == A3
    assert not A1 == A4

    A1._vocabulary.add_constant('cx')
    A1._vocabulary.add_variable('vx')
    assert 'cx' in A2._vocabulary._C
    assert 'vx' in A2._vocabulary._V
    A2._vocabulary.add_constant('cx2')
    A2._vocabulary.add_variable('vx2')
    assert 'cx2' in A1._vocabulary._C
    assert 'vx2' in A1._vocabulary._V


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
    assert A1._vocabulary is A2._vocabulary
    assert A1._attribute_system is not A2._attribute_system
    assert A1 != A3
    assert A1 != A4

    A1._vocabulary.add_constant('cx')
    A1._vocabulary.add_variable('vx')
    assert 'cx' in A2._vocabulary._C
    assert 'vx' in A2._vocabulary._V
    A2._vocabulary.add_constant('cx2')
    A2._vocabulary.add_variable('vx2')
    assert 'cx2' in A1._vocabulary._C
    assert 'vx2' in A1._vocabulary._V
