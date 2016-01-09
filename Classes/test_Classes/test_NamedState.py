"""NamedState unit tests."""

import pytest
from vivid.Classes.Context import Context
from vivid.Classes.AssumptionBase import AssumptionBase
from vivid.Classes.Formula import Formula
from vivid.Classes.AttributeInterpretation import AttributeInterpretation

from vivid.Classes.NamedState import NamedState

from vivid.Classes.ConstantAssignment import ConstantAssignment
from vivid.Classes.VariableAssignment import VariableAssignment

from vivid.Classes.RelationSymbol import RelationSymbol
from vivid.Classes.Vocabulary import Vocabulary

from vivid.Classes.State import State
from vivid.Classes.AttributeSystem import AttributeSystem
from vivid.Classes.AttributeStructure import AttributeStructure
from vivid.Classes.Attribute import Attribute
from vivid.Classes.Relation import Relation
from vivid.Classes.ValueSet import ValueSet
from vivid.Classes.Interval import Interval
from vivid.Classes.Point import Point


def test___init__():
    """Test NamedState constructor."""
    def test_TypeError(attribute_system, p, ascriptions={}):
        """Test constructor for TypeErrors with given params."""
        with pytest.raises(TypeError) as excinfo:
            NamedState(attribute_system, p, ascriptions)

    def test_ValueError(attribute_system, p, ascriptions={}):
        """Test constructor for ValueErrors with given params."""
        with pytest.raises(ValueError) as excinfo:
            NamedState(attribute_system, p, ascriptions)

    color = Attribute("color", ['R', 'G', 'B'])
    size = Attribute("size", ['S', 'M', 'L'])
    a = AttributeStructure(color, size)
    o = ['s1', 's2']
    attribute_system = AttributeSystem(a, o)
    attribute_system_bad = AttributeSystem(a, o[0:1])

    vocabulary = Vocabulary(['a', 'b', 'c', 'd', 'e', 'f', 'g'], [], [])
    p = ConstantAssignment(vocabulary, attribute_system, {'a': 's1'})
    p_bad = ConstantAssignment(vocabulary, attribute_system_bad, {'a': 's1'})

    # Test bad p types
    test_TypeError(attribute_system, [])
    test_TypeError(attribute_system, None)
    test_TypeError(attribute_system, object)
    # test mismatched AttributeSystem's
    test_ValueError(attribute_system_bad, p)
    test_ValueError(attribute_system, p_bad)

    s = NamedState(attribute_system, p)
    assert s._attribute_system == attribute_system
    assert s._attribute_system is not attribute_system
    assert s._p == p
    assert s._p is not p
    assert s._p._vocabulary is p._vocabulary

    s = NamedState(attribute_system, p, {
        ('color', 's1'): ['R'],
        ('color', 's2'): ['B', 'G'],
        ('size', 's1'): ['M'],
        ('size', 's2'): ['L', 'S']})

    assert s[(('color', 's1'))] == ValueSet(['R'])
    assert s[(('color', 's2'))] == ValueSet(['G', 'B'])
    assert s[(('size', 's1'))] == ValueSet(['M'])
    assert s[(('size', 's2'))] == ValueSet(['L', 'S'])


def test___eq__():
    """Test == operator for NamedState object."""
    def test_TypeError(self, other):
        """Test NamedState == operator for TypeErrors."""
        with pytest.raises(TypeError) as excinfo:
            self == other

    color = Attribute('color', ['R', 'G', 'B'])
    size = Attribute('size', ['S', 'M', 'L'])
    attribute_structure = AttributeStructure(color, size)
    objects = ['s1', 's2', 's3']
    attribute_system = AttributeSystem(attribute_structure, objects)
    vocabulary = Vocabulary(['a', 'b', 'c', 'd', 'e', 'f', 'g'], [], [])

    p = ConstantAssignment(vocabulary, attribute_system, {'a': 's1'})
    p_1 = ConstantAssignment(vocabulary,
                             attribute_system,
                             {'a': 's1', 'b': 's2'})

    ascr = {
        ('color', 's1'): ['R', 'B'], ('size', 's1'): ['S', 'M', 'L'],
        ('color', 's2'): ['R', 'B', 'G'], ('size', 's2'): ['M', 'L']}
    ascr_1 = {
        ('color', 's1'): ['B'], ('size', 's1'): ['S', 'M'],
        ('color', 's2'): ['B', 'G'], ('size', 's2'): ['M', 'L']}

    named_state = NamedState(attribute_system, p, ascr)
    named_state_copy = NamedState(attribute_system, p, ascr)
    named_state_1 = NamedState(attribute_system, p_1, ascr_1)
    named_state_2 = NamedState(attribute_system, p, ascr_1)

    test_TypeError(named_state, None)
    test_TypeError(named_state, object)
    test_TypeError(named_state, State(attribute_system))

    assert named_state == named_state
    assert named_state == named_state_copy
    assert not named_state == named_state_1
    assert not named_state == named_state_2
    named_state.set_ascription(('color', 's1'), ['B'])
    named_state.set_ascription(('size', 's1'), ['S', 'M'])
    named_state.set_ascription(('color', 's2'), ['B', 'G'])
    assert named_state == named_state_2


def test___ne__():
    """Test != operator for NamedState object."""
    def test_TypeError(self, other):
        """Test NamedState != operator for TypeErrors."""
        with pytest.raises(TypeError) as excinfo:
            self != other

    color = Attribute('color', ['R', 'G', 'B'])
    size = Attribute('size', ['S', 'M', 'L'])
    attribute_structure = AttributeStructure(color, size)
    objects = ['s1', 's2', 's3']
    attribute_system = AttributeSystem(attribute_structure, objects)
    vocabulary = Vocabulary(['a', 'b', 'c', 'd', 'e', 'f', 'g'], [], [])

    p = ConstantAssignment(vocabulary, attribute_system, {'a': 's1'})
    p_1 = ConstantAssignment(vocabulary,
                             attribute_system,
                             {'a': 's1', 'b': 's2'})

    ascr = {
        ('color', 's1'): ['R', 'B'], ('size', 's1'): ['S', 'M', 'L'],
        ('color', 's2'): ['R', 'B', 'G'], ('size', 's2'): ['M', 'L']}
    ascr_1 = {
        ('color', 's1'): ['B'], ('size', 's1'): ['S', 'M'],
        ('color', 's2'): ['B', 'G'], ('size', 's2'): ['M', 'L']}

    named_state = NamedState(attribute_system, p, ascr)
    named_state_copy = NamedState(attribute_system, p, ascr)
    named_state_1 = NamedState(attribute_system, p_1, ascr_1)
    named_state_2 = NamedState(attribute_system, p, ascr_1)

    test_TypeError(named_state, None)
    test_TypeError(named_state, object)
    test_TypeError(named_state, State(attribute_system))

    assert not named_state != named_state
    assert not named_state != named_state_copy
    assert named_state != named_state_1
    assert named_state != named_state_2
    named_state.set_ascription(('color', 's1'), ['B'])
    named_state.set_ascription(('size', 's1'), ['S', 'M'])
    named_state.set_ascription(('color', 's2'), ['B', 'G'])
    assert not named_state != named_state_2


def test___deepcopy__():
    """Test copy.deepcopy for NamedState object."""
    from copy import deepcopy

    color = Attribute('color', ['R', 'G', 'B'])
    size = Attribute('size', ['S', 'M', 'L'])
    attribute_structure = AttributeStructure(color, size)
    objects = ['s1', 's2', 's3']
    attribute_system = AttributeSystem(attribute_structure, objects)
    vocabulary = Vocabulary(['a', 'b', 'c', 'd', 'e', 'f', 'g'], [], [])

    p = ConstantAssignment(vocabulary, attribute_system, {'a': 's1'})
    p_1 = ConstantAssignment(vocabulary,
                             attribute_system,
                             {'a': 's1', 'b': 's2'})

    ascr = {
        ('color', 's1'): ['R', 'B'], ('size', 's1'): ['S', 'M', 'L'],
        ('color', 's2'): ['R', 'B', 'G'], ('size', 's2'): ['M', 'L']}

    named_state = NamedState(attribute_system, p, ascr)
    named_state_copy = deepcopy(named_state)
    assert named_state == named_state_copy
    assert named_state is not named_state_copy
    assert named_state._attribute_system == named_state_copy._attribute_system
    assert named_state._attribute_system is not named_state_copy._attribute_system
    assert named_state._p is not named_state_copy._p
    assert named_state._ascriptions is not named_state_copy._ascriptions


def test___lt__():
    """Test < operator for NamedState; overloaded for proper extension."""
    def test_TypeError(self, other):
        """Test NamedState < operator for TypeErrors."""
        with pytest.raises(TypeError) as excinfo:
            self < other

    color = Attribute('color', ['R', 'G', 'B'])
    size = Attribute('size', ['S', 'M', 'L'])
    attribute_structure = AttributeStructure(color, size)
    objects = ['s1', 's2', 's3']
    attribute_system = AttributeSystem(attribute_structure, objects)
    vocabulary = Vocabulary(['a', 'b', 'c', 'd', 'e', 'f', 'g'], [], [])

    p = ConstantAssignment(vocabulary, attribute_system, {'a': 's1'})
    p_1 = ConstantAssignment(vocabulary,
                             attribute_system,
                             {'a': 's1', 'b': 's2'})

    ascr = {
        ('color', 's1'): ['R', 'B'], ('size', 's1'): ['S', 'M', 'L'],
        ('color', 's2'): ['R', 'B', 'G'], ('size', 's2'): ['M', 'L']}
    ascr_1 = {
        ('color', 's1'): ['B'], ('size', 's1'): ['S', 'M'],
        ('color', 's2'): ['B', 'G'], ('size', 's2'): ['M', 'L']}
    ascr_2 = {
        ('color', 's1'): ['B'], ('size', 's1'): ['S'],
        ('color', 's2'): ['B'], ('size', 's2'): ['L']}

    named_state = NamedState(attribute_system, p, ascr)
    named_state_1 = NamedState(attribute_system, p_1, ascr)
    named_state_2 = NamedState(attribute_system, p, ascr_1)
    named_state_3 = NamedState(attribute_system, p_1, ascr_1)
    named_state_4 = NamedState(attribute_system, p_1, ascr_2)

    test_TypeError(named_state, State(attribute_system))
    test_TypeError(named_state, object)
    test_TypeError(named_state, None)

    assert not named_state < named_state
    # test superset p
    assert named_state_1 < named_state
    # test subset ascriptions
    assert named_state_2 < named_state
    # test both and chaining
    assert named_state_4 < named_state_3 < named_state_1 < named_state
    assert named_state_4 < named_state_3 < named_state_2 < named_state


def test___le__():
    """Test <= operator for NamedState; overloaded for proper extension."""
    def test_TypeError(self, other):
        """Test NamedState <= operator for TypeErrors."""
        with pytest.raises(TypeError) as excinfo:
            self < other

    color = Attribute('color', ['R', 'G', 'B'])
    size = Attribute('size', ['S', 'M', 'L'])
    attribute_structure = AttributeStructure(color, size)
    objects = ['s1', 's2', 's3']
    attribute_system = AttributeSystem(attribute_structure, objects)
    vocabulary = Vocabulary(['a', 'b', 'c', 'd', 'e', 'f', 'g'], [], [])

    p = ConstantAssignment(vocabulary, attribute_system, {'a': 's1'})
    p_1 = ConstantAssignment(vocabulary,
                             attribute_system,
                             {'a': 's1', 'b': 's2'})

    ascr = {
        ('color', 's1'): ['R', 'B'], ('size', 's1'): ['S', 'M', 'L'],
        ('color', 's2'): ['R', 'B', 'G'], ('size', 's2'): ['M', 'L']}
    ascr_1 = {
        ('color', 's1'): ['B'], ('size', 's1'): ['S', 'M'],
        ('color', 's2'): ['B', 'G'], ('size', 's2'): ['M', 'L']}
    ascr_2 = {
        ('color', 's1'): ['B'], ('size', 's1'): ['S'],
        ('color', 's2'): ['B'], ('size', 's2'): ['L']}

    named_state = NamedState(attribute_system, p, ascr)
    named_state_1 = NamedState(attribute_system, p_1, ascr)
    named_state_2 = NamedState(attribute_system, p, ascr_1)
    named_state_3 = NamedState(attribute_system, p_1, ascr_1)
    named_state_4 = NamedState(attribute_system, p_1, ascr_2)

    test_TypeError(named_state, State(attribute_system))
    test_TypeError(named_state, object)
    test_TypeError(named_state, None)

    assert named_state <= named_state
    # test superset p
    assert named_state_1 <= named_state
    # test subset ascriptions
    assert named_state_2 <= named_state
    # test both and chaining
    assert named_state_4 <= named_state_3 <= named_state_1 <= named_state
    assert named_state_4 <= named_state_3 <= named_state_2 <= named_state


def test_add_object():
    """Test add_object function for NamedState."""
    def test_TypeError(named_state, obj, ascriptions=None, constant=None):
        """Test constructor for TypeErrors with given params."""
        with pytest.raises(TypeError) as excinfo:
            named_state.add_object(obj, ascriptions, constant)

    def test_ValueError(named_state, obj, ascriptions=None, constant=None):
        """Test constructor for ValueErrors with given params."""
        with pytest.raises(ValueError) as excinfo:
            named_state.add_object(obj, ascriptions, constant)

    color = Attribute('color', ['R', 'G', 'B'])
    attribute_structure = AttributeStructure(color)
    objects = ['s1']
    attribute_system = AttributeSystem(attribute_structure, objects)
    vocabulary = Vocabulary(['a'], [], [])

    p = ConstantAssignment(vocabulary, attribute_system, {'a': 's1'})
    named_state = NamedState(attribute_system, p)

    test_TypeError(named_state, "a", None, 1)
    test_TypeError(named_state, "a", None, object)

    named_state.add_object("obj")
    ascr = {("color", "s1"): ValueSet(['R', 'G', 'B']),
            ("color", "obj"): ValueSet(['R', 'G', 'B'])}
    assert named_state._ascriptions == ascr

    named_state = NamedState(attribute_system, p)
    named_state.add_object("obj", {("color", "obj"): ['R']})
    ascr = {("color", "s1"): ValueSet(['R', 'G', 'B']),
            ("color", "obj"): ValueSet(['R'])}
    assert named_state._ascriptions == ascr

    named_state = NamedState(attribute_system, p)
    named_state.add_object("obj", constant_symbol="C")
    p = ConstantAssignment(vocabulary, named_state._attribute_system,
                           {'a': 's1', 'C': 'obj'})
    assert named_state._p == p
    assert 'C' in vocabulary._C


def test_is_world():
    """Test is_world() function for NamedState."""
    color = Attribute('color', ['R', 'G', 'B'])
    size = Attribute('size', ['S', 'M', 'L'])
    attribute_structure = AttributeStructure(color, size)
    objects = ['s1', 's2']
    attribute_system = AttributeSystem(attribute_structure, objects)
    vocabulary = Vocabulary(['a', 'b'], [], [])

    p = ConstantAssignment(vocabulary, attribute_system, {'a': 's1'})
    p_total = ConstantAssignment(vocabulary,
                                 attribute_system,
                                 {'a': 's1', 'b': 's2'})

    ascr = {
        ('color', 's1'): ['R', 'B'], ('size', 's1'): ['S', 'M', 'L'],
        ('color', 's2'): ['R', 'B', 'G'], ('size', 's2'): ['M', 'L']}
    validations = {
        ('color', 's1'): ['R'], ('size', 's1'): ['S'],
        ('color', 's2'): ['G'], ('size', 's2'): ['L']}

    named_state_1 = NamedState(attribute_system, p, ascr)
    named_state_2 = NamedState(attribute_system, p_total, ascr)
    named_state_3 = NamedState(attribute_system, p, validations)
    world = NamedState(attribute_system, p_total, validations)
    assert not named_state_1.is_world()
    assert not named_state_2.is_world()
    assert not named_state_3.is_world()
    assert world.is_world()


def test_get_worlds():
    """Test get_worlds() function for NamedState."""
    color = Attribute('color', ['R', 'G'])
    size = Attribute('size', ['S', 'L'])
    attribute_structure = AttributeStructure(color, size)
    objects = ['s1', 's2']
    attribute_system = AttributeSystem(attribute_structure, objects)
    vocabulary = Vocabulary(['a', 'b'], [], [])

    p = ConstantAssignment(vocabulary, attribute_system, {})
    p_1 = ConstantAssignment(vocabulary,
                             attribute_system,
                             {'a': 's1', 'b': 's2'})
    p_2 = ConstantAssignment(vocabulary,
                             attribute_system,
                             {'a': 's2', 'b': 's1'})

    ascr = {('color', 's1'): ['R']}

    ns = NamedState(attribute_system, p, ascr)
    worlds = [w for w in ns.get_worlds()]

    worlds_manual = [
        NamedState(attribute_system, p_1, {
                   ('color', 's1'): ['R'],
                   ('color', 's2'): ['G'],
                   ('size', 's1'): ['L'],
                   ('size', 's2'): ['L']}),
        NamedState(attribute_system, p_1, {
                   ('color', 's1'): ['R'],
                   ('color', 's2'): ['G'],
                   ('size', 's1'): ['L'],
                   ('size', 's2'): ['S']}),
        NamedState(attribute_system, p_1, {
                   ('color', 's1'): ['R'],
                   ('color', 's2'): ['G'],
                   ('size', 's1'): ['S'],
                   ('size', 's2'): ['L']}),
        NamedState(attribute_system, p_1, {
                   ('color', 's1'): ['R'],
                   ('color', 's2'): ['G'],
                   ('size', 's1'): ['S'],
                   ('size', 's2'): ['S']}),
        NamedState(attribute_system, p_1, {
                   ('color', 's1'): ['R'],
                   ('color', 's2'): ['R'],
                   ('size', 's1'): ['L'],
                   ('size', 's2'): ['L']}),
        NamedState(attribute_system, p_1, {
                   ('color', 's1'): ['R'],
                   ('color', 's2'): ['R'],
                   ('size', 's1'): ['L'],
                   ('size', 's2'): ['S']}),
        NamedState(attribute_system, p_1, {
                   ('color', 's1'): ['R'],
                   ('color', 's2'): ['R'],
                   ('size', 's1'): ['S'],
                   ('size', 's2'): ['L']}),
        NamedState(attribute_system, p_1, {
                   ('color', 's1'): ['R'],
                   ('color', 's2'): ['R'],
                   ('size', 's1'): ['S'],
                   ('size', 's2'): ['S']}),
        NamedState(attribute_system, p_2, {
                   ('color', 's1'): ['R'],
                   ('color', 's2'): ['G'],
                   ('size', 's1'): ['L'],
                   ('size', 's2'): ['L']}),
        NamedState(attribute_system, p_2, {
                   ('color', 's1'): ['R'],
                   ('color', 's2'): ['G'],
                   ('size', 's1'): ['L'],
                   ('size', 's2'): ['S']}),
        NamedState(attribute_system, p_2, {
                   ('color', 's1'): ['R'],
                   ('color', 's2'): ['G'],
                   ('size', 's1'): ['S'],
                   ('size', 's2'): ['L']}),
        NamedState(attribute_system, p_2, {
                   ('color', 's1'): ['R'],
                   ('color', 's2'): ['G'],
                   ('size', 's1'): ['S'],
                   ('size', 's2'): ['S']}),
        NamedState(attribute_system, p_2, {
                   ('color', 's1'): ['R'],
                   ('color', 's2'): ['R'],
                   ('size', 's1'): ['L'],
                   ('size', 's2'): ['L']}),
        NamedState(attribute_system, p_2, {
                   ('color', 's1'): ['R'],
                   ('color', 's2'): ['R'],
                   ('size', 's1'): ['L'],
                   ('size', 's2'): ['S']}),
        NamedState(attribute_system, p_2, {
                   ('color', 's1'): ['R'],
                   ('color', 's2'): ['R'],
                   ('size', 's1'): ['S'],
                   ('size', 's2'): ['L']}),
        NamedState(attribute_system, p_2, {
                   ('color', 's1'): ['R'],
                   ('color', 's2'): ['R'],
                   ('size', 's1'): ['S'],
                   ('size', 's2'): ['S']})]

    assert worlds == worlds_manual

    color = Attribute('color', ['R', 'G'])
    attribute_structure = AttributeStructure(color)
    objects = ['s1', 's2', 's3']
    attribute_system = AttributeSystem(attribute_structure, objects)
    vocabulary = Vocabulary(['a', 'b', 'c', 'd'], [], [])

    p = ConstantAssignment(vocabulary, attribute_system, {'a': 's1'})

    p_1 = ConstantAssignment(vocabulary, attribute_system,
                             {'a': 's1', 'c': 's3', 'b': 's2'})
    p_2 = ConstantAssignment(vocabulary, attribute_system,
                             {'a': 's1', 'b': 's2', 'd': 's3'})
    p_3 = ConstantAssignment(vocabulary, attribute_system,
                             {'a': 's1', 'c': 's2', 'b': 's3'})
    p_4 = ConstantAssignment(vocabulary, attribute_system,
                             {'a': 's1', 'c': 's2', 'd': 's3'})
    p_5 = ConstantAssignment(vocabulary, attribute_system,
                             {'a': 's1', 'b': 's3', 'd': 's2'})
    p_6 = ConstantAssignment(vocabulary, attribute_system,
                             {'a': 's1', 'c': 's3', 'd': 's2'})

    ascr = {('color', 's1'): ['R'], ('color', 's2'): ['R'],
            ('color', 's3'): ['R']}

    ns = NamedState(attribute_system, p, ascr)
    worlds = [w for w in ns.get_worlds()]

    worlds_manual = [
        NamedState(attribute_system, p_1, {
                   ('color', 's1'): ['R'],
                   ('color', 's2'): ['R'],
                   ('color', 's3'): ['R']}),
        NamedState(attribute_system, p_2, {
                   ('color', 's1'): ['R'],
                   ('color', 's2'): ['R'],
                   ('color', 's3'): ['R']}),
        NamedState(attribute_system, p_3, {
                   ('color', 's1'): ['R'],
                   ('color', 's2'): ['R'],
                   ('color', 's3'): ['R']}),
        NamedState(attribute_system, p_4, {
                   ('color', 's1'): ['R'],
                   ('color', 's2'): ['R'],
                   ('color', 's3'): ['R']}),
        NamedState(attribute_system, p_5, {
                   ('color', 's1'): ['R'],
                   ('color', 's2'): ['R'],
                   ('color', 's3'): ['R']}),
        NamedState(attribute_system, p_6, {
                   ('color', 's1'): ['R'],
                   ('color', 's2'): ['R'],
                   ('color', 's3'): ['R']})]

    assert worlds == worlds_manual

    color = Attribute('color', ['R', 'G'])
    attribute_structure = AttributeStructure(color)
    objects = ['s1', 's2', 's3', 's4']
    attribute_system = AttributeSystem(attribute_structure, objects)
    vocabulary = Vocabulary(['a', 'b', 'c'], [], [])

    p = ConstantAssignment(vocabulary, attribute_system, {'a': 's1'})

    p_1 = ConstantAssignment(vocabulary, attribute_system,
                             {'a': 's1', 'c': 's3', 'b': 's2'})
    p_2 = ConstantAssignment(vocabulary, attribute_system,
                             {'a': 's1', 'c': 's4', 'b': 's2'})
    p_3 = ConstantAssignment(vocabulary, attribute_system,
                             {'a': 's1', 'c': 's2', 'b': 's3'})
    p_4 = ConstantAssignment(vocabulary, attribute_system,
                             {'a': 's1', 'c': 's4', 'b': 's3'})
    p_5 = ConstantAssignment(vocabulary, attribute_system,
                             {'a': 's1', 'c': 's2', 'b': 's4'})
    p_6 = ConstantAssignment(vocabulary, attribute_system,
                             {'a': 's1', 'c': 's3', 'b': 's4'})

    ascr = {('color', 's1'): ['R'], ('color', 's2'): ['R'],
            ('color', 's3'): ['R'], ('color', 's4'): ['R']}

    ns = NamedState(attribute_system, p, ascr)
    worlds = [w for w in ns.get_worlds()]

    worlds_manual = [
        NamedState(attribute_system, p_1, {
                   ('color', 's1'): ['R'],
                   ('color', 's2'): ['R'],
                   ('color', 's3'): ['R'],
                   ('color', 's4'): ['R']}),
        NamedState(attribute_system, p_2, {
                   ('color', 's1'): ['R'],
                   ('color', 's2'): ['R'],
                   ('color', 's3'): ['R'],
                   ('color', 's4'): ['R']}),
        NamedState(attribute_system, p_3, {
                   ('color', 's1'): ['R'],
                   ('color', 's2'): ['R'],
                   ('color', 's3'): ['R'],
                   ('color', 's4'): ['R']}),
        NamedState(attribute_system, p_4, {
                   ('color', 's1'): ['R'],
                   ('color', 's2'): ['R'],
                   ('color', 's3'): ['R'],
                   ('color', 's4'): ['R']}),
        NamedState(attribute_system, p_5, {
                   ('color', 's1'): ['R'],
                   ('color', 's2'): ['R'],
                   ('color', 's3'): ['R'],
                   ('color', 's4'): ['R']}),
        NamedState(attribute_system, p_6, {
                   ('color', 's1'): ['R'],
                   ('color', 's2'): ['R'],
                   ('color', 's3'): ['R'],
                   ('color', 's4'): ['R']})]

    assert worlds == worlds_manual


def test_is_named_alternate_extension():
    """Test is_named_alternate_extension() function for NamedState."""
    def test_paper_example():
        """Test for the example provided in the paper."""
        color = Attribute("color", ['R', 'B', 'G'])
        size = Attribute("size", ['S', 'M', 'L'])
        objects = ['s1', 's2']
        attribute_system = AttributeSystem(
            AttributeStructure(color, size), objects)
        vocabulary = Vocabulary([], [], [])
        p = ConstantAssignment(vocabulary, attribute_system, {})

        state = NamedState(attribute_system, p, {
                           ("color", "s1"): ['R', 'B'],
                           ("size", "s2"): ['M', 'L']})

        state_1 = NamedState(attribute_system, p, {
                             ("color", "s1"): ['B'],
                             ("size", "s1"): ['S', 'M'],
                             ("color", "s2"): ['B', 'G'],
                             ("size", "s2"): ['M', 'L']})

        state_2 = NamedState(attribute_system, p, {
                             ("color", "s1"): ['R', 'B'],
                             ("size", "s1"): ['L'],
                             ("color", "s2"): ['R', 'B', 'G'],
                             ("size", "s2"): ['L']})

        state_3 = NamedState(attribute_system, p, {
                             ("color", "s1"): ['R'],
                             ("size", "s1"): ['S', 'M', 'L'],
                             ("color", "s2"): ['R', 'B', 'G'],
                             ("size", "s2"): ['M', 'L']})

        state_4 = NamedState(attribute_system, p, {
                             ("color", "s1"): ['B'],
                             ("size", "s1"): ['L'],
                             ("color", "s2"): ['R', 'B', 'G'],
                             ("size", "s2"): ['M']})

        state_5 = NamedState(attribute_system, p, {
                             ("color", "s1"): ['B'],
                             ("size", "s1"): ['S', 'M'],
                             ("color", "s2"): ['R'],
                             ("size", "s2"): ['M', 'L']})

        state_6 = NamedState(attribute_system, p, {
                             ("color", "s1"): ['B'],
                             ("size", "s1"): ['S', 'M', 'L'],
                             ("color", "s2"): ['R'],
                             ("size", "s2"): ['M']})

        extensions = [state_1, state_2, state_3]

        assert state.is_named_alternate_extension(state_4, *extensions)
        assert state.is_named_alternate_extension(state_5, *extensions)
        assert state.is_named_alternate_extension(state_6, *extensions)

    def test_objects_simple():
        """Do a test using Point and Interval object."""
        attr_1 = Attribute("attr_1", [Point(1.0), Interval(1, 4)])
        attr_2 = Attribute("attr_2", [10L, 65.4, True, False])
        objects = ['s1']
        attribute_system = AttributeSystem(
            AttributeStructure(attr_1, attr_2), objects)
        vocabulary = Vocabulary([], [], [])
        p = ConstantAssignment(vocabulary, attribute_system, {})

        state = NamedState(attribute_system, p, {})

        state_1 = NamedState(attribute_system, p, {
                             ("attr_1", "s1"): [Point(1.0), 1],
                             ("attr_2", "s1"): [10L, True]})

        state_2 = NamedState(attribute_system, p, {
                             ("attr_1", "s1"): [Point(1.0), 2],
                             ("attr_2", "s1"): [False]})

        state_3 = NamedState(attribute_system, p, {
                             ("attr_1", "s1"): [Interval(3, 4)],
                             ("attr_2", "s1"): [65.4, 10L, False, True]})

        state_4 = NamedState(attribute_system, p, {
                             ("attr_1", "s1"): [Interval(2, 4)],
                             ("attr_2", "s1"): [65.4, 10L, True]})

        state_5 = NamedState(attribute_system, p, {
                             ("attr_1", "s1"): [1, Interval(3, 4)],
                             ("attr_2", "s1"): [65.4, False]})

        state_6 = NamedState(attribute_system, p, {
                             ("attr_1", "s1"): [Point(1.0), Interval(1, 4)],
                             ("attr_2", "s1"): [65.4]})

        extensions = [state_1, state_2]

        assert state.is_named_alternate_extension(state_3, *extensions)
        assert state.is_named_alternate_extension(state_4, *extensions)
        assert state.is_named_alternate_extension(state_5, *extensions)
        assert state.is_named_alternate_extension(state_6, *extensions)

    test_paper_example()
    test_objects_simple()


def test_get_named_alternate_extensions():
    """Test get_named_alternate_extensions() function for NamedState."""
    def test_paper_example():
        """Test for the example provided in the paper."""
        color = Attribute("color", ['R', 'B', 'G'])
        size = Attribute("size", ['S', 'M', 'L'])
        objects = ['s1', 's2']
        attribute_system = AttributeSystem(
            AttributeStructure(color, size), objects)

        vocabulary = Vocabulary([], [], [])
        p = ConstantAssignment(vocabulary, attribute_system, {})

        state = NamedState(attribute_system, p, {
                           ("color", "s1"): ['R', 'B'],
                           ("size", "s2"): ['M', 'L']})

        state_1 = NamedState(attribute_system, p, {
                             ("color", "s1"): ['B'],
                             ("size", "s1"): ['S', 'M'],
                             ("color", "s2"): ['B', 'G'],
                             ("size", "s2"): ['M', 'L']})

        state_2 = NamedState(attribute_system, p, {
                             ("color", "s1"): ['R', 'B'],
                             ("size", "s1"): ['L'],
                             ("color", "s2"): ['R', 'B', 'G'],
                             ("size", "s2"): ['L']})

        state_3 = NamedState(attribute_system, p, {
                             ("color", "s1"): ['R'],
                             ("size", "s1"): ['S', 'M', 'L'],
                             ("color", "s2"): ['R', 'B', 'G'],
                             ("size", "s2"): ['M', 'L']})

        state_4 = NamedState(attribute_system, p, {
                             ("color", "s1"): ['B'],
                             ("size", "s1"): ['L'],
                             ("color", "s2"): ['R', 'B', 'G'],
                             ("size", "s2"): ['M']})

        state_5 = NamedState(attribute_system, p, {
                             ("color", "s1"): ['B'],
                             ("size", "s1"): ['S', 'M'],
                             ("color", "s2"): ['R'],
                             ("size", "s2"): ['M', 'L']})

        state_6 = NamedState(attribute_system, p, {
                             ("color", "s1"): ['B'],
                             ("size", "s1"): ['S', 'M', 'L'],
                             ("color", "s2"): ['R'],
                             ("size", "s2"): ['M']})

        alternate_extensions = state.get_named_alternate_extensions(
            state_1, state_2, state_3)

        assert state_4 in alternate_extensions
        assert state_5 in alternate_extensions
        assert state_6 in alternate_extensions

    def test_objects_simple():
        """Do a test using Point and Interval object."""
        attr_1 = Attribute("attr_1", [Point(1.0), Interval(1, 4)])
        attr_2 = Attribute("attr_2", [10L, 65.4, True, False])
        objects = ['s1']
        attribute_system = AttributeSystem(
            AttributeStructure(attr_1, attr_2), objects)
        vocabulary = Vocabulary([], [], [])
        p = ConstantAssignment(vocabulary, attribute_system, {})

        state = NamedState(attribute_system, p, {})

        state_1 = NamedState(attribute_system, p, {
                             ("attr_1", "s1"): [Point(1.0), 1],
                             ("attr_2", "s1"): [10L, True]})

        state_2 = NamedState(attribute_system, p, {
                             ("attr_1", "s1"): [Point(1.0), 2],
                             ("attr_2", "s1"): [False]})

        state_3 = NamedState(attribute_system, p, {
                             ("attr_1", "s1"): [Interval(3, 4)],
                             ("attr_2", "s1"): [65.4, 10L, False, True]})

        state_4 = NamedState(attribute_system, p, {
                             ("attr_1", "s1"): [Interval(2, 4)],
                             ("attr_2", "s1"): [65.4, 10L, True]})

        state_5 = NamedState(attribute_system, p, {
                             ("attr_1", "s1"): [1, Interval(3, 4)],
                             ("attr_2", "s1"): [65.4, False]})

        state_6 = NamedState(attribute_system, p, {
                             ("attr_1", "s1"): [Point(1.0), Interval(1, 4)],
                             ("attr_2", "s1"): [65.4]})

        extensions = [state_1, state_2]

        alternate_extensions = state.get_named_alternate_extensions(
            *extensions)

        assert state_3 in alternate_extensions
        assert state_4 in alternate_extensions
        assert state_5 in alternate_extensions
        assert state_6 in alternate_extensions

    def test_objects_complex():
        """Do a complex test using all inherent types including objects."""
        attr_1 = Attribute("attr_1",
                           [Point(1.0), Interval(1, 10), Point(2.0, 2.0)])
        attr_2 = Attribute("attr_2",
                           [10L, 65.4, True, False, Interval(5.0, 17.0)])
        objects = ["s1", "s2"]
        attribute_system = AttributeSystem(
            AttributeStructure(attr_1, attr_2), objects)
        vocabulary = Vocabulary([], [], [])
        p = ConstantAssignment(vocabulary, attribute_system, {})

        state = NamedState(attribute_system, p, {
                           ("attr_1", "s1"): [Point(1.0), Interval(1, 10)],
                           ("attr_2", "s1"): [10L, 65.4, True, False],
                           ("attr_1", "s2"): [Point(1.0), Point(2.0, 2.0)],
                           ("attr_2", "s2"): [True, False, Interval(5.0, 15.0)]
                           })

        state_1 = NamedState(attribute_system, p, {
                             ("attr_1", "s1"): [Point(1.0), 4, 7],
                             ("attr_2", "s1"): [10L, True, False],
                             ("attr_1", "s2"): [Point(2.0, 2.0)],
                             ("attr_2", "s2"): [Interval(5.0, 15.0)]})

        state_2 = NamedState(attribute_system, p, {
                             ("attr_1", "s1"): [Interval(1, 10)],
                             ("attr_2", "s1"): [10L, 65.4, True, False],
                             ("attr_1", "s2"): [Point(1.0)],
                             ("attr_2", "s2"): [True]})

        state_3 = NamedState(attribute_system, p, {
                             ("attr_1", "s1"): [Point(1.0), 5],
                             ("attr_2", "s1"): [10L],
                             ("attr_1", "s2"): [Point(1.0), Point(2.0, 2.0)],
                             ("attr_2", "s2"): [False]})

        extensions = [state_1, state_2, state_3]

        alternate_extensions = state.get_named_alternate_extensions(*extensions)
        assert len(alternate_extensions) == 26

        l_4 = NamedState(attribute_system, p, {
                         ("attr_1", "s1"): [Interval(1, 3), 6, Interval(8, 10)],
                         ("attr_2", "s1"): [10L, 65.4, True, False],
                         ("attr_1", "s2"): [Point(2.0, 2.0)],
                         ("attr_2", "s2"): [True, False, Interval(5.0, 15.0)]})

        l_5 = NamedState(attribute_system, p, {
                         ("attr_1", "s1"): [Interval(1, 3), Interval(5, 6), Interval(8, 10)],
                         ("attr_2", "s1"): [65.4, True, False],
                         ("attr_1", "s2"): [Point(2.0, 2.0)],
                         ("attr_2", "s2"): [True, False, Interval(5.0, 15.0)]})

        l_6 = NamedState(attribute_system, p, {
                         ("attr_1", "s1"): [Interval(1, 3), Interval(5, 6), Interval(8, 10)],
                         ("attr_2", "s1"): [10L, 65.4, True, False],
                         ("attr_1", "s2"): [Point(2.0, 2.0)],
                         ("attr_2", "s2"): [True, Interval(5.0, 15.0)]})

        l_7 = NamedState(attribute_system, p, {
                         ("attr_1", "s1"): [Interval(1, 3), 6, Interval(8, 10)],
                         ("attr_2", "s1"): [10L, 65.4, True, False],
                         ("attr_1", "s2"): [Point(1.0), Point(2.0, 2.0)],
                         ("attr_2", "s2"): [False, Interval(5.0, 15.0)]})

        l_8 = NamedState(attribute_system, p, {
                         ("attr_1", "s1"): [Interval(1, 3), Interval(5, 6), Interval(8, 10)],
                         ("attr_2", "s1"): [65.4, True, False],
                         ("attr_1", "s2"): [Point(1.0), Point(2.0, 2.0)],
                         ("attr_2", "s2"): [False, Interval(5.0, 15.0)]})

        l_9 = NamedState(attribute_system, p, {
                         ("attr_1", "s1"): [Interval(1, 3), Interval(5, 6), Interval(8, 10)],
                         ("attr_2", "s1"): [10L, 65.4, True, False],
                         ("attr_1", "s2"): [Point(1.0), Point(2.0, 2.0)],
                         ("attr_2", "s2"): [Interval(5.0, 15.0)]})

        l_11 = NamedState(attribute_system, p, {
                          ("attr_1", "s1"): [Point(1.0)],
                          ("attr_2", "s1"): [65.4],
                          ("attr_1", "s2"): [Point(1.0), Point(2.0, 2.0)],
                          ("attr_2", "s2"): [True, False, Interval(5.0, 15.0)]})

        l_12 = NamedState(attribute_system, p, {
                          ("attr_1", "s1"): [Point(1.0)],
                          ("attr_2", "s1"): [65.4],
                          ("attr_1", "s2"): [Point(1.0), Point(2.0, 2.0)],
                          ("attr_2", "s2"): [True, Interval(5.0, 15.0)]})

        l_13 = NamedState(attribute_system, p, {
                          ("attr_1", "s1"): [Interval(1, 4), Interval(6, 10)],
                          ("attr_2", "s1"): [65.4],
                          ("attr_1", "s2"): [Point(2.0, 2.0)],
                          ("attr_2", "s2"): [True, False, Interval(5.0, 15.0)]})

        l_14 = NamedState(attribute_system, p, {
                          ("attr_1", "s1"): [Point(1.0), Interval(1, 10)],
                          ("attr_2", "s1"): [65.4],
                          ("attr_1", "s2"): [Point(2.0, 2.0)],
                          ("attr_2", "s2"): [True, False, Interval(5.0, 15.0)]})

        l_15 = NamedState(attribute_system, p, {
                          ("attr_1", "s1"): [Point(1.0), Interval(1, 10)],
                          ("attr_2", "s1"): [65.4],
                          ("attr_1", "s2"): [Point(2.0, 2.0)],
                          ("attr_2", "s2"): [True, Interval(5.0, 15.0)]})

        l_16 = NamedState(attribute_system, p, {
                          ("attr_1", "s1"): [Interval(1, 4), Interval(6, 10)],
                          ("attr_2", "s1"): [65.4],
                          ("attr_1", "s2"): [Point(1.0), Point(2.0, 2.0)],
                          ("attr_2", "s2"): [False, Interval(5.0, 15.0)]})

        l_17 = NamedState(attribute_system, p, {
                          ("attr_1", "s1"): [Point(1.0), Interval(1, 10)],
                          ("attr_2", "s1"): [65.4],
                          ("attr_1", "s2"): [Point(1.0), Point(2.0, 2.0)],
                          ("attr_2", "s2"): [False, Interval(5.0, 15.0)]})

        l_18 = NamedState(attribute_system, p, {
                          ("attr_1", "s1"): [Point(1.0), Interval(1, 10)],
                          ("attr_2", "s1"): [65.4],
                          ("attr_1", "s2"): [Point(1.0), Point(2.0, 2.0)],
                          ("attr_2", "s2"): [Interval(5.0, 15.0)]})

        l_20 = NamedState(attribute_system, p, {
                          ("attr_1", "s1"): [Point(1.0)],
                          ("attr_2", "s1"): [65.4, True, False],
                          ("attr_1", "s2"): [Point(1.0)],
                          ("attr_2", "s2"): [True, False, Interval(5.0, 15.0)]})

        l_21 = NamedState(attribute_system, p, {
                          ("attr_1", "s1"): [Point(1.0)],
                          ("attr_2", "s1"): [10L, 65.4, True, False],
                          ("attr_1", "s2"): [Point(1.0)],
                          ("attr_2", "s2"): [True, Interval(5.0, 15.0)]})

        l_25 = NamedState(attribute_system, p, {
                          ("attr_1", "s1"): [Interval(1, 4), Interval(6, 10)],
                          ("attr_2", "s1"): [10L, 65.4, True, False],
                          ("attr_1", "s2"): [Point(1.0)],
                          ("attr_2", "s2"): [False, Interval(5.0, 15.0)]})

        l_26 = NamedState(attribute_system, p, {
                          ("attr_1", "s1"): [Point(1.0), Interval(1, 10)],
                          ("attr_2", "s1"): [65.4, True, False],
                          ("attr_1", "s2"): [Point(1.0)],
                          ("attr_2", "s2"): [False, Interval(5.0, 15.0)]})

        l_27 = NamedState(attribute_system, p, {
                          ("attr_1", "s1"): [Point(1.0), Interval(1, 10)],
                          ("attr_2", "s1"): [10L, 65.4, True, False],
                          ("attr_1", "s2"): [Point(1.0)],
                          ("attr_2", "s2"): [Interval(5.0, 15.0)]})

        l_29 = NamedState(attribute_system, p, {
                          ("attr_1", "s1"): [Point(1.0)],
                          ("attr_2", "s1"): [65.4, True, False],
                          ("attr_1", "s2"): [Point(1.0), Point(2.0, 2.0)],
                          ("attr_2", "s2"): [True, False]})

        l_30 = NamedState(attribute_system, p, {
                          ("attr_1", "s1"): [Point(1.0)],
                          ("attr_2", "s1"): [10L, 65.4, True, False],
                          ("attr_1", "s2"): [Point(1.0), Point(2.0, 2.0)],
                          ("attr_2", "s2"): [True]})

        l_31 = NamedState(attribute_system, p, {
                          ("attr_1", "s1"): [Interval(1, 4), Interval(6, 10)],
                          ("attr_2", "s1"): [10L, 65.4, True, False],
                          ("attr_1", "s2"): [Point(2.0, 2.0)],
                          ("attr_2", "s2"): [True, False]})

        l_32 = NamedState(attribute_system, p, {
                          ("attr_1", "s1"): [Point(1.0), Interval(1, 10)],
                          ("attr_2", "s1"): [65.4, True, False],
                          ("attr_1", "s2"): [Point(2.0, 2.0)],
                          ("attr_2", "s2"): [True, False]})

        l_33 = NamedState(attribute_system, p, {
                          ("attr_1", "s1"): [Point(1.0), Interval(1, 10)],
                          ("attr_2", "s1"): [10L, 65.4, True, False],
                          ("attr_1", "s2"): [Point(2.0, 2.0)],
                          ("attr_2", "s2"): [True]})

        l_34 = NamedState(attribute_system, p, {
                          ("attr_1", "s1"): [Interval(1, 4), Interval(6, 10)],
                          ("attr_2", "s1"): [10L, 65.4, True, False],
                          ("attr_1", "s2"): [Point(1.0), Point(2.0, 2.0)],
                          ("attr_2", "s2"): [False]})

        l_35 = NamedState(attribute_system, p, {
                          ("attr_1", "s1"): [Point(1.0), Interval(1, 10)],
                          ("attr_2", "s1"): [65.4, True, False],
                          ("attr_1", "s2"): [Point(1.0), Point(2.0, 2.0)],
                          ("attr_2", "s2"): [False]})

        for i in [l_4, l_5, l_6, l_7, l_8, l_9, l_11, l_12,
                  l_13, l_14, l_15, l_16, l_17, l_18, l_20,
                  l_21, l_25, l_26, l_27, l_29, l_30, l_31,
                  l_32, l_33, l_34, l_35]:
            assert i in alternate_extensions

    test_paper_example()
    test_objects_simple()
    test_objects_complex()


def test_satisfies_formula():
    """Test satisfies_formula() function for NamedState."""
    def test_TypeError(world, formula, attribute_interpretation, X):
        """Test TypeError catching in satisfies_formula()."""
        with pytest.raises(TypeError) as excinfo:
            world.satisfies_formula(formula, attribute_interpretation, X)

    def test_ValueError(world, formula, attribute_interpretation, X):
        """Test ValueError catching in satisfies_formula()."""
        with pytest.raises(ValueError) as excinfo:
            world.satisfies_formula(formula, attribute_interpretation, X)

    def standard_test():
        """Do regular tests."""
        a = Attribute('hour', [Interval(0, 23)])
        a2 = Attribute('minute', [Interval(0, 59)])
        r_pm = Relation('R1(h1) <=> h1 > 11', ['hour'], 1)
        r_am = Relation('R2(h1) <=> h1 <= 11', ['hour'], 2)
        r_ahead = Relation('R3(h1,m1,h2,m2) <=> h1 > h2 or (h1 = h2 and m1 > m2)',
                           ['hour', 'minute', 'hour', 'minute'], 3)
        r_behind = Relation('R4(h1,m1,h2,m2) <=> h1 < h2 or (h1 = h2 and m1 < m2)',
                            ['hour', 'minute', 'hour', 'minute'], 4)
        attribute_structure = AttributeStructure(
            a, a2, r_ahead, r_behind, r_pm, r_am)

        pm_rs = RelationSymbol('PM', 1)
        am_rs = RelationSymbol('AM', 1)
        ahead_rs = RelationSymbol('Ahead', 4)
        behind_rs = RelationSymbol('Behind', 4)
        vocabulary = Vocabulary(
            ['C1', 'C2'], [pm_rs, am_rs, ahead_rs, behind_rs], ['V1', 'V2'])

        profiles = [
            [pm_rs, ('hour', 1)],
            [am_rs, ('hour', 1)],
            [behind_rs, ('hour', 1), ('minute', 1), ('hour', 2), ('minute', 2)],
            [ahead_rs, ('hour', 1), ('minute', 1), ('hour', 2), ('minute', 2)]]

        attribute_interpretation = AttributeInterpretation(
            vocabulary,
            attribute_structure,
            {pm_rs: 1, am_rs: 2, ahead_rs: 3, behind_rs: 4},
            profiles)

        objs = ['c1', 'c2', 'x1', 'x2']
        asys = AttributeSystem(attribute_structure, objs)

        const_mapping = {'C1': 'c1', 'C2': 'c2'}
        var_mapping = {'V1': 'x1', 'V2': 'x2'}
        p = ConstantAssignment(vocabulary, asys, const_mapping)
        X = VariableAssignment(vocabulary, asys, var_mapping)

        world = NamedState(asys, p)
        named_state = NamedState(asys, p)

        world.set_ascription(('hour', 'c1'), [21])
        world.set_ascription(('minute', 'c1'), [9])
        world.set_ascription(('hour', 'c2'), [11])
        world.set_ascription(('minute', 'c2'), [40])

        world.set_ascription(('hour', 'x1'), [21])
        world.set_ascription(('minute', 'x1'), [9])
        world.set_ascription(('hour', 'x2'), [11])
        world.set_ascription(('minute', 'x2'), [40])

        named_state.set_ascription(('hour', 'c1'), [21, 11])
        named_state.set_ascription(('minute', 'c1'), [9])
        named_state.set_ascription(('hour', 'c2'), [11, Interval(20, 22)])
        named_state.set_ascription(('minute', 'c2'), [40])

        named_state.set_ascription(('hour', 'x1'), [21])
        named_state.set_ascription(('minute', 'x1'), [9])
        named_state.set_ascription(('hour', 'x2'), [11])
        named_state.set_ascription(('minute', 'x2'), [40])

        f1 = Formula(vocabulary, 'PM', 'C1')
        f2 = Formula(vocabulary, 'AM', 'C1')
        f3 = Formula(vocabulary, 'Ahead', 'C1', 'C2')
        f4 = Formula(vocabulary, 'Behind', 'C1', 'C2', 'V1', 'V2')
        f5 = Formula(vocabulary, 'Behind', 'C2', 'C1', 'V1', 'V2')

        from copy import deepcopy
        world2 = deepcopy(world)
        world2.set_ascription(('hour', 'c1'), [1])

        test_TypeError(world, None, attribute_interpretation, X)
        test_TypeError(world, object, attribute_interpretation, X)
        test_TypeError(world, f1, None, X)
        test_TypeError(world, f1, object, X)
        test_TypeError(world, f1, attribute_interpretation, None)
        test_TypeError(world, f1, attribute_interpretation, object)
        test_ValueError(named_state, f1, X, attribute_interpretation)

        assert world.satisfies_formula(f1, X, attribute_interpretation)
        assert not world.satisfies_formula(f2, X, attribute_interpretation)
        assert world.satisfies_formula(f3, X, attribute_interpretation)
        assert not world.satisfies_formula(f4, X, attribute_interpretation)
        assert world.satisfies_formula(f5, X, attribute_interpretation)

        assert not world2.satisfies_formula(f1, X, attribute_interpretation)
        assert world2.satisfies_formula(f2, X, attribute_interpretation)
        assert not world2.satisfies_formula(f3, X, attribute_interpretation)
        assert world2.satisfies_formula(f4, X, attribute_interpretation)
        assert not world2.satisfies_formula(f5, X, attribute_interpretation)

    def point_test():
        """Do Point object tests."""
        point = Attribute('point', [Point('x', 'x', 'x', 'x')])
        r_is_on = Relation('R1(h1, h2, h3) <=> is_on(h1, h2, h3)',
                           ['point', 'point', 'point'], 1)
        r_not_same_point = Relation('R2(h1, h2) <=> not_same_point(h1, h2)',
                                    ['point', 'point'], 2)
        r_clocks_unequal = Relation('R3(h1, h2) <=> clocks_unequal(h1, h2)',
                                    ['point', 'point'], 3)
        r_can_observe = Relation(
            'R4(p, sp_loc, wls, wle) <=> can_observe(p, sp_loc, wls, wle)',
            ['point', 'point', 'point', 'point'], 4)

        attribute_structure = AttributeStructure(
            point, r_is_on, r_not_same_point, r_clocks_unequal, r_can_observe)

        rs_is_on = RelationSymbol('IS_ON', 3)
        rs_not_same_point = RelationSymbol('NOT_SAME_POINT', 2)
        rs_clocks_unequal = RelationSymbol('CLOCKS_UNEQUAL', 2)
        rs_can_observe = RelationSymbol('CAN_OBSERVE', 4)

        vocabulary = Vocabulary(['P1', 'P2', 'P3', 'P4', 'P5'],
                                [rs_is_on, rs_not_same_point,
                                 rs_clocks_unequal, rs_can_observe],
                                [])

        profiles = [
            [rs_is_on, ('point', 1), ('point', 2), ('point', 3)],
            [rs_not_same_point, ('point', 1), ('point', 2)],
            [rs_clocks_unequal, ('point', 1), ('point', 2)],
            [rs_can_observe,
             ('point', 1), ('point', 2), ('point', 3), ('point', 4)]]

        mapping = {rs_is_on: 1, rs_not_same_point: 2, rs_clocks_unequal: 3,
                   rs_can_observe: 4}

        attribute_interpretation = AttributeInterpretation(vocabulary,
                                                           attribute_structure,
                                                           mapping,
                                                           profiles)

        objects = ['p1', 'p2', 'p3', 'p4', 'p5']
        attribute_system = AttributeSystem(attribute_structure, objects)
        p = ConstantAssignment(vocabulary, attribute_system,
                               {'P1': 'p1', 'P2': 'p2', 'P3': 'p3', 'P4': 'p4',
                                'P5': 'p5'})

        world = NamedState(attribute_system, p, {
                           ('point', 'p1'): [Point(1.5, 1.5, 1.5, 1.5)],
                           ('point', 'p2'): [Point(2.0, 2.0, 2.0, 2.0)],
                           ('point', 'p3'): [Point(1.0, 1.0, 1.0, 1.0)],
                           ('point', 'p4'): [Point(3.0, 3.0, 3.0, 3.0)]})

        f1 = Formula(vocabulary, 'IS_ON', 'P1', 'P3', 'P4')
        f2 = Formula(vocabulary, 'NOT_SAME_POINT', 'P1', 'P2')
        f3 = Formula(vocabulary, 'CLOCKS_UNEQUAL', 'P1', 'P2')
        f4 = Formula(vocabulary, 'CAN_OBSERVE', 'P1', 'P2', 'P3', 'P4')

        VA = VariableAssignment(vocabulary, attribute_system, {}, dummy=True)

        assumption_base = AssumptionBase(f1, f2, f3, f4)

        for f in assumption_base:
            assert world.satisfies_formula(f, VA, attribute_interpretation)

        f1_bad = Formula(vocabulary, 'IS_ON', 'P3', 'P1', 'P4')
        assert not world.satisfies_formula(f1_bad, VA, attribute_interpretation)
        f2_bad = Formula(vocabulary, 'CAN_OBSERVE', 'P1', 'P3', 'P2', 'P4')
        assert not world.satisfies_formula(f2_bad, VA, attribute_interpretation)
        f3_bad = Formula(vocabulary, 'NOT_SAME_POINT', 'P1', 'P1')
        assert not world.satisfies_formula(f3_bad, VA, attribute_interpretation)
        f4_bad = Formula(vocabulary, 'CLOCKS_UNEQUAL', 'P2', 'P2')
        assert not world.satisfies_formula(f4_bad, VA, attribute_interpretation)

    standard_test()
    point_test()


def test_satisfies_named_state():
    """Test satisfies_named_state() function for NamedState."""
    def test_TypeError(world, named_state):
        """Test TypeError catching in satisfies_named_state()."""
        with pytest.raises(TypeError) as excinfo:
            world.satisfies_named_state(named_state)

    def test_ValueError(world, named_state):
        """Test ValueError catching in satisfies_named_state()."""
        with pytest.raises(ValueError) as excinfo:
            world.satisfies_named_state(named_state)

    def standard_test():
        """Do regular tests."""
        a = Attribute('hour', [Interval(0, 23)])
        a2 = Attribute('minute', [Interval(0, 59)])
        r_pm = Relation('R1(h1) <=> h1 > 11', ['hour'], 1)
        r_am = Relation('R2(h1) <=> h1 <= 11', ['hour'], 2)
        r_ahead = Relation('R3(h1,m1,h2,m2) <=> h1 > h2 or (h1 = h2 and m1 > m2)',
                           ['hour', 'minute', 'hour', 'minute'], 3)
        r_behind = Relation('R4(h1,m1,h2,m2) <=> h1 < h2 or (h1 = h2 and m1 < m2)',
                            ['hour', 'minute', 'hour', 'minute'], 4)
        attribute_structure = AttributeStructure(
            a, a2, r_ahead, r_behind, r_pm, r_am)

        pm_rs = RelationSymbol('PM', 1)
        am_rs = RelationSymbol('AM', 1)
        ahead_rs = RelationSymbol('Ahead', 4)
        behind_rs = RelationSymbol('Behind', 4)
        vocabulary = Vocabulary(
            ['C1', 'C2'], [pm_rs, am_rs, ahead_rs, behind_rs], ['V1', 'V2'])

        objs = ['c1', 'c2']
        asys = AttributeSystem(attribute_structure, objs)

        p = ConstantAssignment(vocabulary, asys, {'C1': 'c1', 'C2': 'c2'})

        named_state = NamedState(asys, p)
        named_state.set_ascription(('hour', 'c1'), [1])
        named_state.set_ascription(('hour', 'c2'), [1])
        named_state.set_ascription(('minute', 'c1'), [47, 33, 13, 6, 19])
        named_state.set_ascription(('minute', 'c2'), [1, 4, 9, 12, 55])

        worlds = [w for w in named_state.get_worlds()]
        for world in worlds:
            assert world.satisfies_named_state(named_state)

        from copy import deepcopy
        w_copy = deepcopy(worlds[0])
        w_copy.set_ascription(('hour', 'c1'), [2])

        assert w_copy.satisfies_named_state(w_copy)
        assert not w_copy.satisfies_named_state(named_state)

        test_TypeError(worlds[0], None)
        test_TypeError(worlds[0], object)
        test_ValueError(named_state, named_state)

    def point_test():
        """Do Point object tests."""
        point = Attribute('point', [Point('x', 'x', 'x', 'x')])
        r_is_on = Relation('R1(h1, h2, h3) <=> is_on(h1, h2, h3)',
                           ['point', 'point', 'point'], 1)
        r_not_same_point = Relation('R2(h1, h2) <=> not_same_point(h1, h2)',
                                    ['point', 'point'], 2)
        r_clocks_unequal = Relation('R3(h1, h2) <=> clocks_unequal(h1, h2)',
                                    ['point', 'point'], 3)
        r_can_observe = Relation(
            'R4(p, sp_loc, wls, wle) <=> can_observe(p, sp_loc, wls, wle)',
            ['point', 'point', 'point', 'point'], 4)

        attribute_structure = AttributeStructure(
            point, r_is_on, r_not_same_point, r_clocks_unequal, r_can_observe)

        vocabulary = Vocabulary(['P1', 'P2', 'P3', 'P4', 'P5'], [], [])

        objects = ['p1', 'p2', 'p3', 'p4', 'p5']
        attribute_system = AttributeSystem(attribute_structure, objects)
        p = ConstantAssignment(vocabulary, attribute_system,
                               {'P1': 'p1', 'P2': 'p2', 'P3': 'p3', 'P4': 'p4',
                                'P5': 'p5'})

        named_state = NamedState(attribute_system, p, {})
        world = NamedState(attribute_system, p, {
                           ('point', 'p1'): [Point(1.5, 1.5, 1.5, 1.5)],
                           ('point', 'p2'): [Point(2.0, 2.0, 2.0, 2.0)],
                           ('point', 'p3'): [Point(1.0, 1.0, 1.0, 1.0)],
                           ('point', 'p4'): [Point(3.0, 3.0, 3.0, 3.0)]})

        assert world.satisfies_named_state(named_state)

    standard_test()
    point_test()


def test_satisfies_context():
    """Test satisfies_context() function for NamedState."""
    def test_TypeError(world, context, X, attribute_interpretation):
        """Test TypeError catching in satisfies_context()."""
        with pytest.raises(TypeError) as excinfo:
            world.satisfies_context(context, X, attribute_interpretation)

    def test_ValueError(world, context, X, attribute_interpretation):
        """Test ValueError catching in satisfies_context()."""
        with pytest.raises(ValueError) as excinfo:
            world.satisfies_context(context, X, attribute_interpretation)

    def standard_test():
        """Do regular tests."""
        a = Attribute('hour', [Interval(0, 23)])
        a2 = Attribute('minute', [Interval(0, 59)])
        r_pm = Relation('R1(h1) <=> h1 > 11', ['hour'], 1)
        r_am = Relation('R2(h1) <=> h1 <= 11', ['hour'], 2)
        r_ahead = Relation('R3(h1,m1,h2,m2) <=> h1 > h2 or (h1 = h2 and m1 > m2)',
                           ['hour', 'minute', 'hour', 'minute'], 3)
        r_behind = Relation('R4(h1,m1,h2,m2) <=> h1 < h2 or (h1 = h2 and m1 < m2)',
                            ['hour', 'minute', 'hour', 'minute'], 4)
        attribute_structure = AttributeStructure(
            a, a2, r_ahead, r_behind, r_pm, r_am)

        pm_rs = RelationSymbol('PM', 1)
        am_rs = RelationSymbol('AM', 1)
        ahead_rs = RelationSymbol('Ahead', 4)
        behind_rs = RelationSymbol('Behind', 4)
        vocabulary = Vocabulary(
            ['C1', 'C2'], [pm_rs, am_rs, ahead_rs, behind_rs], ['V1', 'V2'])

        profiles = [
            [pm_rs, ('hour', 1)],
            [am_rs, ('hour', 1)],
            [behind_rs, ('hour', 1), ('minute', 1), ('hour', 2), ('minute', 2)],
            [ahead_rs, ('hour', 1), ('minute', 1), ('hour', 2), ('minute', 2)]]

        attribute_interpretation = AttributeInterpretation(
            vocabulary,
            attribute_structure,
            {pm_rs: 1, am_rs: 2, ahead_rs: 3, behind_rs: 4},
            profiles)

        objs = ['c1', 'c2', 'x1', 'x2']
        asys = AttributeSystem(attribute_structure, objs)

        const_mapping = {'C1': 'c1', 'C2': 'c2'}
        var_mapping = {'V1': 'x1', 'V2': 'x2'}
        p = ConstantAssignment(vocabulary, asys, const_mapping)
        X = VariableAssignment(vocabulary, asys, var_mapping)

        world = NamedState(asys, p)
        named_state = NamedState(asys, p)

        world.set_ascription(('hour', 'c1'), [21])
        world.set_ascription(('minute', 'c1'), [9])
        world.set_ascription(('hour', 'c2'), [11])
        world.set_ascription(('minute', 'c2'), [40])

        world.set_ascription(('hour', 'x1'), [21])
        world.set_ascription(('minute', 'x1'), [9])
        world.set_ascription(('hour', 'x2'), [11])
        world.set_ascription(('minute', 'x2'), [40])

        named_state.set_ascription(('hour', 'c1'), [21, 11])
        named_state.set_ascription(('minute', 'c1'), [9])
        named_state.set_ascription(('hour', 'c2'), [11, Interval(20, 22)])
        named_state.set_ascription(('minute', 'c2'), [40])

        named_state.set_ascription(('hour', 'x1'), [21])
        named_state.set_ascription(('minute', 'x1'), [9])
        named_state.set_ascription(('hour', 'x2'), [11])
        named_state.set_ascription(('minute', 'x2'), [40])

        f1 = Formula(vocabulary, 'PM', 'C1')
        f2 = Formula(vocabulary, 'AM', 'C1')
        f3 = Formula(vocabulary, 'Ahead', 'C1', 'C2')
        f4 = Formula(vocabulary, 'Behind', 'C1', 'C2', 'V1', 'V2')
        f5 = Formula(vocabulary, 'Behind', 'C2', 'C1', 'V1', 'V2')

        good_assumption_base = AssumptionBase(f3)
        good_assumption_base2 = AssumptionBase(f1, f3)
        good_assumption_base3 = AssumptionBase(f5)
        bad_assumption_base = AssumptionBase(f2)
        bad_assumption_base2 = AssumptionBase(f1, f2, f3)
        bad_assumption_base3 = AssumptionBase(f4)

        good_context = Context(good_assumption_base, world)
        good_context2 = Context(good_assumption_base2, world)
        good_context3 = Context(good_assumption_base3, world)
        bad_context = Context(bad_assumption_base, world)
        bad_context2 = Context(bad_assumption_base2, world)
        bad_context3 = Context(bad_assumption_base3, world)

        assert world.satisfies_context(good_context, X, attribute_interpretation)
        assert world.satisfies_context(good_context2, X, attribute_interpretation)
        assert world.satisfies_context(good_context3, X, attribute_interpretation)
        assert not world.satisfies_context(
            bad_context, X, attribute_interpretation)
        assert not world.satisfies_context(
            bad_context2, X, attribute_interpretation)
        assert not world.satisfies_context(
            bad_context3, X, attribute_interpretation)

        from copy import deepcopy
        world2 = deepcopy(world)
        world2.set_ascription(('hour', 'c1'), [1])

        bad_assumption_base = AssumptionBase(f1)
        bad_assumption_base2 = AssumptionBase(f1, f2)
        bad_assumption_base3 = AssumptionBase(f3)
        good_assumption_base = AssumptionBase(f4)
        good_assumption_base2 = AssumptionBase(f2, f4)

        good_context = Context(good_assumption_base, world2)
        good_context2 = Context(good_assumption_base2, world2)
        bad_context = Context(bad_assumption_base, world2)
        bad_context2 = Context(bad_assumption_base2, world2)
        bad_context3 = Context(bad_assumption_base3, world2)

        assert world2.satisfies_context(good_context, X, attribute_interpretation)
        assert world2.satisfies_context(good_context2, X, attribute_interpretation)
        assert not world2.satisfies_context(
            bad_context, X, attribute_interpretation)
        assert not world2.satisfies_context(
            bad_context2, X, attribute_interpretation)
        assert not world2.satisfies_context(
            bad_context3, X, attribute_interpretation)

        test_TypeError(world, None, attribute_interpretation, X)
        test_TypeError(world, object, attribute_interpretation, X)
        test_TypeError(world, good_context, None, X)
        test_TypeError(world, good_context, object, X)
        test_TypeError(world, good_context, attribute_interpretation, None)
        test_TypeError(world, good_context, attribute_interpretation, object)
        test_ValueError(named_state, good_context, X, attribute_interpretation)

    def point_test():
        """Do Point object tests."""
        point = Attribute('point', [Point('x', 'x', 'x', 'x')])
        r_is_on = Relation('R1(h1, h2, h3) <=> is_on(h1, h2, h3)',
                           ['point', 'point', 'point'], 1)
        r_not_same_point = Relation('R2(h1, h2) <=> not_same_point(h1, h2)',
                                    ['point', 'point'], 2)
        r_clocks_unequal = Relation('R3(h1, h2) <=> clocks_unequal(h1, h2)',
                                    ['point', 'point'], 3)
        r_can_observe = Relation(
            'R4(p, sp_loc, wls, wle) <=> can_observe(p, sp_loc, wls, wle)',
            ['point', 'point', 'point', 'point'], 4)

        attribute_structure = AttributeStructure(
            point, r_is_on, r_not_same_point, r_clocks_unequal, r_can_observe)

        rs_is_on = RelationSymbol('IS_ON', 3)
        rs_not_same_point = RelationSymbol('NOT_SAME_POINT', 2)
        rs_clocks_unequal = RelationSymbol('CLOCKS_UNEQUAL', 2)
        rs_can_observe = RelationSymbol('CAN_OBSERVE', 4)

        vocabulary = Vocabulary(['P1', 'P2', 'P3', 'P4', 'P5'],
                                [rs_is_on, rs_not_same_point,
                                 rs_clocks_unequal, rs_can_observe],
                                [])

        profiles = [
            [rs_is_on, ('point', 1), ('point', 2), ('point', 3)],
            [rs_not_same_point, ('point', 1), ('point', 2)],
            [rs_clocks_unequal, ('point', 1), ('point', 2)],
            [rs_can_observe,
             ('point', 1), ('point', 2), ('point', 3), ('point', 4)]]

        mapping = {rs_is_on: 1, rs_not_same_point: 2, rs_clocks_unequal: 3,
                   rs_can_observe: 4}

        attribute_interpretation = AttributeInterpretation(vocabulary,
                                                           attribute_structure,
                                                           mapping,
                                                           profiles)

        objects = ['p1', 'p2', 'p3', 'p4', 'p5']
        attribute_system = AttributeSystem(attribute_structure, objects)
        p = ConstantAssignment(vocabulary, attribute_system,
                               {'P1': 'p1', 'P2': 'p2', 'P3': 'p3', 'P4': 'p4',
                                'P5': 'p5'})

        world = NamedState(attribute_system, p, {
                           ('point', 'p1'): [Point(1.5, 1.5, 1.5, 1.5)],
                           ('point', 'p2'): [Point(2.0, 2.0, 2.0, 2.0)],
                           ('point', 'p3'): [Point(1.0, 1.0, 1.0, 1.0)],
                           ('point', 'p4'): [Point(3.0, 3.0, 3.0, 3.0)]})

        f1 = Formula(vocabulary, 'IS_ON', 'P1', 'P3', 'P4')
        f2 = Formula(vocabulary, 'NOT_SAME_POINT', 'P1', 'P2')
        f3 = Formula(vocabulary, 'CLOCKS_UNEQUAL', 'P1', 'P2')
        f4 = Formula(vocabulary, 'CAN_OBSERVE', 'P1', 'P2', 'P3', 'P4')

        VA = VariableAssignment(vocabulary, attribute_system, {}, dummy=True)

        named_state = NamedState(attribute_system, p, {})
        assumption_base = AssumptionBase(f1, f2, f3, f4)
        context = Context(assumption_base, named_state)

        assert world.satisfies_context(context, VA, attribute_interpretation)

        f_bad = Formula(vocabulary, 'NOT_SAME_POINT', 'P1', 'P1')
        assumption_base_bad = AssumptionBase(f1, f_bad, f3, f4)
        context_bad = Context(assumption_base_bad, named_state)
        assert not world.satisfies_context(context_bad, VA,
                                           attribute_interpretation)

    standard_test()
    point_test()


def test__generate_variable_assignments():
    """Test generate_variable_assignments function."""
    objects = ['s1', 's2']
    attribute_system = AttributeSystem(AttributeStructure(), objects)
    vocabulary = Vocabulary([], [], [])
    p = ConstantAssignment(vocabulary, attribute_system, {})
    state = NamedState(attribute_system, p, {})

    assert [VariableAssignment(vocabulary, attribute_system, {}, dummy=True)] == \
        [X for X in state._generate_variable_assignments()]

    objects = ['s1']
    attribute_system = AttributeSystem(AttributeStructure(), objects)
    vocabulary = Vocabulary([], [], ['V1', 'V2'])
    p = ConstantAssignment(vocabulary, attribute_system, {})
    state = NamedState(attribute_system, p, {})
    V1 = VariableAssignment(vocabulary, attribute_system, {'V1': 's1'})
    V2 = VariableAssignment(vocabulary, attribute_system, {'V2': 's1'})
    variable_assignments = [X for X in state._generate_variable_assignments()]
    assert len(variable_assignments) == 2
    assert V1 in variable_assignments
    assert V2 in variable_assignments

    objects = ['s1', 's2']
    attribute_system = AttributeSystem(AttributeStructure(), objects)
    vocabulary = Vocabulary([], [], ['V1', 'V2'])
    p = ConstantAssignment(vocabulary, attribute_system, {})
    state = NamedState(attribute_system, p, {})
    V1 = VariableAssignment(vocabulary, attribute_system,
                            {'V1': 's1', 'V2': 's2'})
    V2 = VariableAssignment(vocabulary, attribute_system,
                            {'V1': 's2', 'V2': 's1'})
    variable_assignments = [X for X in state._generate_variable_assignments()]
    assert len(variable_assignments) == 2
    assert V1 in variable_assignments
    assert V2 in variable_assignments

    objects = ['s1', 's2', 's3', 's4']
    attribute_system = AttributeSystem(AttributeStructure(), objects)
    vocabulary = Vocabulary([], [], ['V1', 'V2'])
    p = ConstantAssignment(vocabulary, attribute_system, {})
    state = NamedState(attribute_system, p, {})
    V1 = VariableAssignment(vocabulary, attribute_system,
                            {'V1': 's1', 'V2': 's2'})
    V2 = VariableAssignment(vocabulary, attribute_system,
                            {'V1': 's1', 'V2': 's3'})
    V3 = VariableAssignment(vocabulary, attribute_system,
                            {'V1': 's1', 'V2': 's4'})
    V4 = VariableAssignment(vocabulary, attribute_system,
                            {'V1': 's2', 'V2': 's1'})
    V5 = VariableAssignment(vocabulary, attribute_system,
                            {'V1': 's2', 'V2': 's3'})
    V6 = VariableAssignment(vocabulary, attribute_system,
                            {'V1': 's2', 'V2': 's4'})
    V7 = VariableAssignment(vocabulary, attribute_system,
                            {'V1': 's3', 'V2': 's1'})
    V8 = VariableAssignment(vocabulary, attribute_system,
                            {'V1': 's3', 'V2': 's2'})
    V9 = VariableAssignment(vocabulary, attribute_system,
                            {'V1': 's3', 'V2': 's4'})
    V10 = VariableAssignment(vocabulary, attribute_system,
                             {'V1': 's4', 'V2': 's1'})
    V11 = VariableAssignment(vocabulary, attribute_system,
                             {'V1': 's4', 'V2': 's2'})
    V12 = VariableAssignment(vocabulary, attribute_system,
                             {'V1': 's4', 'V2': 's3'})
    # V2 = VariableAssignment(vocabulary, attribute_system,
    #                        {'V1': 's2', 'V2': 's1'})
    variable_assignments = [X for X in state._generate_variable_assignments()]
    vas = [V1, V2, V3, V4, V5, V6, V7, V8, V9, V10, V11, V12]
    assert len(variable_assignments) == 12
    for v in vas:
        assert v in variable_assignments


def test_is_named_entailment():
    """Test is_named_entailment() function for NamedState."""
    def simple_test():
        """Do simple tests for named entailment."""
        a = Attribute('hour', [Interval(0, 23)])
        a2 = Attribute('minute', [Interval(0, 59)])
        r_pm = Relation('R1(h1) <=> h1 > 11', ['hour'], 1)
        r_am = Relation('R2(h1) <=> h1 <= 11', ['hour'], 2)
        r_ahead = Relation('R3(h1,m1,h2,m2) <=> h1 > h2 or (h1 = h2 and m1 > m2)',
                           ['hour', 'minute', 'hour', 'minute'], 3)
        r_behind = Relation('R4(h1,m1,h2,m2) <=> h1 < h2 or (h1 = h2 and m1 < m2)',
                            ['hour', 'minute', 'hour', 'minute'], 4)
        attribute_structure = AttributeStructure(
            a, a2, r_ahead, r_behind, r_pm, r_am)
        objects = ['s1', 's2', 's3', 's4']
        attribute_system = AttributeSystem(attribute_structure, objects)

        pm_rs = RelationSymbol('PM', 1)
        am_rs = RelationSymbol('AM', 1)
        ahead_rs = RelationSymbol('Ahead', 4)
        behind_rs = RelationSymbol('Behind', 4)
        vocabulary = Vocabulary(
            ['C1', 'C2'], [pm_rs, am_rs, ahead_rs, behind_rs], ['V1', 'V3', 'V2'])
        p = ConstantAssignment(
            vocabulary, attribute_system, {'C1': 's1', 'C2': 's2'})
        X = VariableAssignment(vocabulary, attribute_system, {}, dummy=True)

        named_state = NamedState(attribute_system, p, {
                                ('minute', 's1'): [0],
                                ('minute', 's2'): [0],
                                ('minute', 's3'): [0],
                                ('minute', 's4'): [0],
                                ('hour', 's1'): [9, 10, 11, 13],
                                ('hour', 's2'): [4, 5, 6, 8],
                                ('hour', 's3'): [0],
                                ('hour', 's4'): [0]})

        named_state_1 = NamedState(attribute_system, p, {
                                  ('minute', 's1'): [0],
                                  ('minute', 's2'): [0],
                                  ('minute', 's3'): [0],
                                  ('minute', 's4'): [0],
                                  ('hour', 's1'): [9, 11, 13],
                                  ('hour', 's2'): [4, 5, 8],
                                  ('hour', 's3'): [0],
                                  ('hour', 's4'): [0]})

        named_state_2 = NamedState(attribute_system, p, {
                                  ('minute', 's1'): [0],
                                  ('minute', 's2'): [0],
                                  ('minute', 's3'): [0],
                                  ('minute', 's4'): [0],
                                  ('hour', 's1'): [9, 10, 13],
                                  ('hour', 's2'): [4, 6],
                                  ('hour', 's3'): [0],
                                  ('hour', 's4'): [0]})

        profiles = [
            [pm_rs, ('hour', 1)],
            [am_rs, ('hour', 1)],
            [behind_rs, ('hour', 1), ('minute', 1), ('hour', 2), ('minute', 2)],
            [ahead_rs, ('hour', 1), ('minute', 1), ('hour', 2), ('minute', 2)]]

        attribute_interpretation = AttributeInterpretation(
            vocabulary, attribute_structure,
            {pm_rs: 1, am_rs: 2, ahead_rs: 3, behind_rs: 4}, profiles)

        f1 = Formula(vocabulary, 'PM', 'C1')
        f2 = Formula(vocabulary, 'AM', 'C1')
        f3 = Formula(vocabulary, 'Ahead', 'C1', 'C2')
        f4 = Formula(vocabulary, 'Behind', 'C1', 'C2', 'V1', 'V2')

        assumption_base = AssumptionBase(f1)

        assert named_state.is_named_entailment(assumption_base,
                                               attribute_interpretation,
                                               named_state_1,
                                               named_state_2)

        named_state_2.set_ascription(("hour", "s1"), [9, 10])
        assert not named_state.is_named_entailment(assumption_base,
                                                   attribute_interpretation,
                                                   named_state_1,
                                                   named_state_2)
        f1 = Formula(vocabulary, 'Ahead', 'C2', 'C1')
        f2 = Formula(vocabulary, 'Behind', 'C1', 'C2', 'V1', 'V2')
        assumption_base = AssumptionBase(f1, f2)
        assert named_state.is_named_entailment(assumption_base,
                                               attribute_interpretation,
                                               named_state_1,
                                               named_state_2)

    simple_test()


def test___str__():
    """Test str(NamedState)."""
    color = Attribute('color', ['R', 'G'])
    size = Attribute('size', ['S', 'L'])
    attribute_structure = AttributeStructure(color, size)
    objects = ['s1', 's2']
    attribute_system = AttributeSystem(attribute_structure, objects)
    vocabulary = Vocabulary(['a', 'b'], [], [])

    p = ConstantAssignment(vocabulary, attribute_system, {})
    p_1 = ConstantAssignment(
        vocabulary, attribute_system, {'a': 's1', 'b': 's2'})

    ascr = {('color', 's1'): ['R']}

    ns = NamedState(attribute_system, p, ascr)
    ns1 = NamedState(attribute_system, p_1, ascr)
    assert str(ns) == "color(s1): {V(R)}\ncolor(s2): {V(G, R)}\nsize(s1): {V(L, S)}\nsize(s2): {V(L, S)}\nCA{}"
    assert str(ns1) == "color(s1): {V(R)}\ncolor(s2): {V(G, R)}\nsize(s1): {V(L, S)}\nsize(s2): {V(L, S)}\nCA{'a': 's1', 'b': 's2'}"


def test___repr__():
    """Test repr(NamedState)."""
    color = Attribute('color', ['R', 'G'])
    size = Attribute('size', ['S', 'L'])
    attribute_structure = AttributeStructure(color, size)
    objects = ['s1', 's2']
    attribute_system = AttributeSystem(attribute_structure, objects)
    vocabulary = Vocabulary(['a', 'b'], [], [])

    p = ConstantAssignment(vocabulary, attribute_system, {})
    p_1 = ConstantAssignment(
        vocabulary, attribute_system, {'a': 's1', 'b': 's2'})

    ascr = {('color', 's1'): ['R']}

    ns = NamedState(attribute_system, p, ascr)
    ns1 = NamedState(attribute_system, p_1, ascr)
    assert repr(ns) == "color(s1): {V(R)}\ncolor(s2): {V(G, R)}\nsize(s1): {V(L, S)}\nsize(s2): {V(L, S)}\nCA{}"
    assert repr(ns1) == "color(s1): {V(R)}\ncolor(s2): {V(G, R)}\nsize(s1): {V(L, S)}\nsize(s2): {V(L, S)}\nCA{'a': 's1', 'b': 's2'}"
