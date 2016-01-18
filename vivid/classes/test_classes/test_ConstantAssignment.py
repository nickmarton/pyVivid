"""ConstantAssignment unit tests."""

import pytest
from vivid.classes.attribute import Attribute
from vivid.classes.relation_symbol import RelationSymbol
from vivid.classes.attribute_structure import AttributeStructure
from vivid.classes.attribute_system import AttributeSystem
from vivid.classes.vocabulary import Vocabulary
from vivid.classes.constant_assignment import ConstantAssignment


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


def test_total_ordering():
    """Test overloaded < subset operator for ConstantAssignment."""
    vocabulary1 = Vocabulary(
        ['C1', 'C2', 'C3'], [RelationSymbol('R', 1)], ['V'])
    vocabulary2 = Vocabulary(['C\''], [RelationSymbol('R\'', 1)], ['V\''])

    a = Attribute("a", [])
    b = Attribute("b", [])
    astr1 = AttributeStructure(a, b)
    astr2 = AttributeStructure(b)
    objs1 = ['a', 'b', 'c']
    objs2 = ['a']
    attribute_system1 = AttributeSystem(astr1, objs1)
    attribute_system2 = AttributeSystem(astr2, objs2)

    mapping1 = {'C1': 'a'}
    mapping2 = {'C1': 'a', 'C2': 'b'}
    mapping3 = {'C1': 'a', 'C2': 'b', 'C3': 'c'}
    mapping4 = {'C\'': 'a'}
    mapping5 = {'C1': 'b'}

    CA1 = ConstantAssignment(vocabulary1, attribute_system1, mapping1)
    CA2 = ConstantAssignment(vocabulary1, attribute_system1, mapping2)
    CA3 = ConstantAssignment(vocabulary1, attribute_system1, mapping3)
    CA4 = ConstantAssignment(vocabulary2, attribute_system2, mapping4)
    CA5 = ConstantAssignment(vocabulary1, attribute_system1, mapping5)

    assert not CA1 < CA1
    assert CA1 <= CA1
    assert not CA1 > CA1
    assert CA1 >= CA1
    assert CA1 < CA2
    assert CA2 > CA1
    assert CA1 < CA2 < CA3
    assert CA3 > CA2 > CA1
    assert not CA1 < CA4
    assert not CA4 < CA1
    assert not CA5 < CA2


def test___le__():
    """Test overloaded <= subset operator for ConstantAssignment."""
    vocabulary1 = Vocabulary(
        ['C1', 'C2', 'C3'], [RelationSymbol('R', 1)], ['V'])
    vocabulary2 = Vocabulary(['C\''], [RelationSymbol('R\'', 1)], ['V\''])

    a = Attribute("a", [])
    b = Attribute("b", [])
    astr1 = AttributeStructure(a, b)
    astr2 = AttributeStructure(b)
    objs1 = ['a', 'b', 'c']
    objs2 = ['a']
    attribute_system1 = AttributeSystem(astr1, objs1)
    attribute_system2 = AttributeSystem(astr2, objs2)

    mapping1 = {'C1': 'a'}
    mapping2 = {'C1': 'a', 'C2': 'b'}
    mapping3 = {'C1': 'a', 'C2': 'b', 'C3': 'c'}
    mapping4 = {'C\'': 'a'}
    mapping5 = {'C1': 'b'}

    CA1 = ConstantAssignment(vocabulary1, attribute_system1, mapping1)
    CA2 = ConstantAssignment(vocabulary1, attribute_system1, mapping2)
    CA3 = ConstantAssignment(vocabulary1, attribute_system1, mapping3)
    CA4 = ConstantAssignment(vocabulary2, attribute_system2, mapping4)
    CA5 = ConstantAssignment(vocabulary1, attribute_system1, mapping5)

    assert CA1 <= CA1
    assert CA1 <= CA2
    assert CA1 <= CA2 <= CA3
    assert not CA1 <= CA4
    assert not CA4 <= CA1
    assert not CA5 <= CA2


def test___getitem__():
    """Test indexing for ConstantAssignment object."""
    def test_TypeError(constant_assignment, key):
        """Test constructor for TypeErrors with given params."""
        with pytest.raises(TypeError) as excinfo:
            constant_assignment[key]

    def test_KeyError(constant_assignment, key):
        """Test constructor for KeyErrors with given params."""
        with pytest.raises(KeyError) as excinfo:
            constant_assignment[key]

    vocabulary = Vocabulary(['C'], [RelationSymbol('R', 1)], ['V'])

    a = Attribute("a", [])
    b = Attribute("b", [])
    astr = AttributeStructure(a, b)
    objs = ['a', 'b', 'c']
    attribute_system = AttributeSystem(astr, objs)

    mapping = {'C': 'a'}

    CA = ConstantAssignment(vocabulary, attribute_system, mapping)

    test_TypeError(CA, 1)
    test_TypeError(CA, None)
    test_TypeError(CA, object)
    test_KeyError(CA, '')

    assert CA['C'] == 'a'


def test___deepcopy__():
    """Test copy.deepcopy for ConstantAssignment object."""
    from copy import deepcopy

    vocabulary = Vocabulary(['C'], [RelationSymbol('R', 1)], ['V'])

    a = Attribute("a", [])
    b = Attribute("b", [])
    astr = AttributeStructure(a, b)
    objs = ['a', 'b', 'c']
    attribute_system = AttributeSystem(astr, objs)

    mapping = {'C': 'a'}

    CA = ConstantAssignment(vocabulary, attribute_system, mapping)

    CA_copy = deepcopy(CA)
    assert CA == CA_copy
    assert CA is not CA_copy
    assert CA._vocabulary is CA_copy._vocabulary
    assert CA._attribute_system is not CA_copy._attribute_system
    assert CA._mapping is not CA_copy._mapping


def test_add_mapping():
    """Test add_mapping function for ConstantAssignment."""
    def test_TypeError(constant_assignment, constant_symbol, obj):
        """Test constructor for TypeErrors with given params."""
        with pytest.raises(TypeError) as excinfo:
            constant_assignment.add_mapping(constant_symbol, obj)

    def test_ValueError(constant_assignment, constant_symbol, obj):
        """Test constructor for ValueErrors with given params."""
        with pytest.raises(ValueError) as excinfo:
            constant_assignment.add_mapping(constant_symbol, obj)

    vocabulary = Vocabulary(['C1', 'C2'], [], [])

    a = Attribute("a", [])
    b = Attribute("b", [])
    astr = AttributeStructure(a, b)
    objs = ['a', 'b', 'c']
    attribute_system = AttributeSystem(astr, objs)

    C = ConstantAssignment(vocabulary, attribute_system, {'C2': 'b'})

    test_TypeError(C, None, 'a')
    test_TypeError(C, object, 'a')
    test_TypeError(C, 'C1', None)
    test_TypeError(C, 'C1', object)
    test_ValueError(C, 'bad_C', 'a')
    test_ValueError(C, 'C1', 'bad_obj')
    test_ValueError(C, 'C2', 'a')
    test_ValueError(C, 'C1', 'b')

    C.add_mapping('C1', 'a')
    C2 = ConstantAssignment(vocabulary, attribute_system,
                            {'C2': 'b', 'C1': 'a'})
    C3 = ConstantAssignment(vocabulary, attribute_system,
                            {'C1': 'a', 'C2': 'b'})
    assert C == C2
    assert C == C3


def test_remove_mapping():
    """Test remove_mapping function for ConstantAssignment."""
    def test_TypeError(constant_assignment, constant_symbol, obj):
        """Test constructor for TypeErrors with given params."""
        with pytest.raises(TypeError) as excinfo:
            constant_assignment.remove_mapping(constant_symbol, obj)

    def test_ValueError(constant_assignment, constant_symbol, obj):
        """Test constructor for ValueErrors with given params."""
        with pytest.raises(ValueError) as excinfo:
            constant_assignment.remove_mapping(constant_symbol, obj)

    vocabulary = Vocabulary(['C1', 'C2'], [], [])

    a = Attribute("a", [])
    b = Attribute("b", [])
    astr = AttributeStructure(a, b)
    objs = ['a', 'b', 'c']
    attribute_system = AttributeSystem(astr, objs)

    C = ConstantAssignment(vocabulary, attribute_system,
                           {'C1': 'a', 'C2': 'b'})

    test_TypeError(C, None, 'a')
    test_TypeError(C, object, 'a')
    test_TypeError(C, 'C1', None)
    test_TypeError(C, 'C1', object)
    test_ValueError(C, 'bad_C', 'a')
    test_ValueError(C, 'C1', 'bad_obj')
    test_ValueError(C, 'C2', 'a')
    test_ValueError(C, 'C1', 'b')

    C.remove_mapping('C1', 'a')
    C2 = ConstantAssignment(vocabulary, attribute_system,
                            {'C2': 'b'})
    assert C == C2


def test_is_total():
    """Test is_total function for ConstantAssignment object."""
    vocabulary = Vocabulary(['C', 'C\''], [RelationSymbol('R', 1)], ['V'])
    vocabulary_total = Vocabulary(
        ['C1', 'C2', 'C3'], [RelationSymbol('R', 1)], ['V'])

    a = Attribute("a", [])
    b = Attribute("b", [])
    astr = AttributeStructure(a, b)
    objs = ['a', 'b', 'c']
    attribute_system = AttributeSystem(astr, objs)

    mapping = {'C': 'a'}
    total_mapping = {'C1': 'a', 'C2': 'b', 'C3': 'c'}

    CA = ConstantAssignment(vocabulary, attribute_system, mapping)
    CA_total = ConstantAssignment(
        vocabulary_total, attribute_system, total_mapping)

    assert not CA.is_total()
    assert CA_total.is_total()


def test_get_domain():
    """Test get_domain function for ConstantAssignment object."""
    vocabulary = Vocabulary(['C', 'C\''], [RelationSymbol('R', 1)], ['V'])

    a = Attribute("a", [])
    b = Attribute("b", [])
    astr = AttributeStructure(a, b)
    objs = ['a', 'b', 'c']
    attribute_system = AttributeSystem(astr, objs)

    mapping = {'C': 'a'}
    mapping2 = {'C': 'a', 'C\'': 'b'}

    CA = ConstantAssignment(vocabulary, attribute_system, mapping)
    CA2 = ConstantAssignment(vocabulary, attribute_system, mapping2)

    assert CA.get_domain() == ['C']
    assert CA2.get_domain() == ['C', "C'"]


def test_in_conflict():
    """Test in_conflict function for ConstantAssignment object."""
    vocabulary = Vocabulary(['C', 'C\''], [RelationSymbol('R', 1)], ['V'])

    a = Attribute("a", [])
    b = Attribute("b", [])
    astr = AttributeStructure(a, b)
    objs = ['a', 'b', 'c']
    attribute_system = AttributeSystem(astr, objs)

    mapping = {'C': 'a'}
    mapping2 = {'C': 'a', 'C\'': 'b'}
    mapping3 = {'C': 'b'}

    CA = ConstantAssignment(vocabulary, attribute_system, mapping)
    CA2 = ConstantAssignment(vocabulary, attribute_system, mapping2)
    CA3 = ConstantAssignment(vocabulary, attribute_system, mapping3)

    assert not CA.in_conflict(CA)
    assert not CA.in_conflict(CA2)
    assert CA.in_conflict(CA3)


def test___str__():
    """Test str(ConstantAssignment)."""
    vocabulary = Vocabulary(['C', 'C\''], [RelationSymbol('R', 1)], ['V'])

    a = Attribute("a", [])
    b = Attribute("b", [])
    astr = AttributeStructure(a, b)
    objs = ['a', 'b', 'c']
    attribute_system = AttributeSystem(astr, objs)

    mapping = {'C': 'a'}
    mapping2 = {'C': 'a', 'C\'': 'b'}

    CA = ConstantAssignment(vocabulary, attribute_system, mapping)
    CA2 = ConstantAssignment(vocabulary, attribute_system, mapping2)

    assert CA.__str__() == "CA{'C': 'a'}"
    assert CA2.__str__() == "CA{'C': 'a', \"C\'\": 'b'}"


def test___repr__():
    """Test repr(ConstantAssignment)."""
    vocabulary = Vocabulary(['C', 'C\''], [RelationSymbol('R', 1)], ['V'])

    a = Attribute("a", [])
    b = Attribute("b", [])
    astr = AttributeStructure(a, b)
    objs = ['a', 'b', 'c']
    attribute_system = AttributeSystem(astr, objs)

    mapping = {'C': 'a'}
    mapping2 = {'C': 'a', 'C\'': 'b'}

    CA = ConstantAssignment(vocabulary, attribute_system, mapping)
    CA2 = ConstantAssignment(vocabulary, attribute_system, mapping2)

    assert CA.__repr__() == "CA{'C': 'a'}"
    assert CA2.__repr__() == "CA{'C': 'a', \"C\'\": 'b'}"
