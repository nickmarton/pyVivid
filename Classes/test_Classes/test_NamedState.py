"""NamedState unit tests."""

import pytest
from vivid.Classes.NamedState import NamedState

from vivid.Classes.ConstantAssignment import ConstantAssignment
from vivid.Classes.VariableAssignment import VariableAssignment

from vivid.Classes.RelationSymbol import RelationSymbol
from vivid.Classes.Vocabulary import Vocabulary

from vivid.Classes.State import State
from vivid.Classes.State import AttributeSystem
from vivid.Classes.State import AttributeStructure
from vivid.Classes.State import Attribute, Relation
from vivid.Classes.ValueSet import ValueSet

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
    
    sigma = Vocabulary(['a', 'b', 'c', 'd', 'e', 'f', 'g'],[],[])
    p = ConstantAssignment(sigma, attribute_system, {'a': 's1'})
    p_bad = ConstantAssignment(sigma, attribute_system_bad, {'a': 's1'})

    #Test bad p types
    test_TypeError(attribute_system, [])
    test_TypeError(attribute_system, None)
    test_TypeError(attribute_system, object)
    #test mismatched AttributeSystem's
    test_ValueError(attribute_system_bad, p)
    test_ValueError(attribute_system, p_bad)

    s = NamedState(attribute_system, p)
    assert s._attribute_system == attribute_system
    assert s._attribute_system is not attribute_system
    assert s._p == p
    assert s._p is not p
    
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
    sigma = Vocabulary(['a', 'b', 'c', 'd', 'e', 'f', 'g'],[],[])


    p = ConstantAssignment(sigma, attribute_system, {'a': 's1'})
    p_1 = ConstantAssignment(sigma, attribute_system, {'a': 's1', 'b': 's2'})
    
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
    sigma = Vocabulary(['a', 'b', 'c', 'd', 'e', 'f', 'g'],[],[])


    p = ConstantAssignment(sigma, attribute_system, {'a': 's1'})
    p_1 = ConstantAssignment(sigma, attribute_system, {'a': 's1', 'b': 's2'})
    
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
    sigma = Vocabulary(['a', 'b', 'c', 'd', 'e', 'f', 'g'],[],[])


    p = ConstantAssignment(sigma, attribute_system, {'a': 's1'})
    p_1 = ConstantAssignment(sigma, attribute_system, {'a': 's1', 'b': 's2'})
    
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
    sigma = Vocabulary(['a', 'b', 'c', 'd', 'e', 'f', 'g'],[],[])


    p = ConstantAssignment(sigma, attribute_system, {'a': 's1'})
    p_1 = ConstantAssignment(sigma, attribute_system, {'a': 's1', 'b': 's2'})
    
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
    #test superset p
    assert named_state_1 < named_state
    #test subset ascriptions
    assert named_state_2 < named_state
    #test both and chaining
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
    sigma = Vocabulary(['a', 'b', 'c', 'd', 'e', 'f', 'g'],[],[])


    p = ConstantAssignment(sigma, attribute_system, {'a': 's1'})
    p_1 = ConstantAssignment(sigma, attribute_system, {'a': 's1', 'b': 's2'})
    
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
    #test superset p
    assert named_state_1 <= named_state
    #test subset ascriptions
    assert named_state_2 <= named_state
    #test both and chaining
    assert named_state_4 <= named_state_3 <= named_state_1 <= named_state
    assert named_state_4 <= named_state_3 <= named_state_2 <= named_state

def test_is_world():
    """Test is_world() function for NamedState."""
    color = Attribute('color', ['R', 'G', 'B'])
    size = Attribute('size', ['S', 'M', 'L'])
    attribute_structure = AttributeStructure(color, size)
    objects = ['s1', 's2']
    attribute_system = AttributeSystem(attribute_structure, objects)
    sigma = Vocabulary(['a', 'b'], [], [])


    p = ConstantAssignment(sigma, attribute_system, {'a': 's1'})
    p_total = ConstantAssignment(sigma, attribute_system, {'a': 's1', 'b': 's2'})
    
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
    sigma = Vocabulary(['a', 'b'], [], [])


    p = ConstantAssignment(sigma, attribute_system, {})
    p_1 = ConstantAssignment(sigma, attribute_system, {'a': 's1', 'b': 's2'})
    p_2 = ConstantAssignment(sigma, attribute_system, {'a': 's2', 'b': 's1'})
    
    ascr = {('color', 's1'): ['R']}

    ns = NamedState(attribute_system, p, ascr)
    worlds = ns.get_worlds()

    worlds_manual = [
        NamedState(attribute_system, p_1, {('color', 's1'): ['R'], ('color', 's2'): ['G'], ('size', 's1'): ['L'], ('size', 's2'): ['L']}),
        NamedState(attribute_system, p_1, {('color', 's1'): ['R'], ('color', 's2'): ['G'], ('size', 's1'): ['L'], ('size', 's2'): ['S']}),
        NamedState(attribute_system, p_1, {('color', 's1'): ['R'], ('color', 's2'): ['G'], ('size', 's1'): ['S'], ('size', 's2'): ['L']}),
        NamedState(attribute_system, p_1, {('color', 's1'): ['R'], ('color', 's2'): ['G'], ('size', 's1'): ['S'], ('size', 's2'): ['S']}),
        NamedState(attribute_system, p_1, {('color', 's1'): ['R'], ('color', 's2'): ['R'], ('size', 's1'): ['L'], ('size', 's2'): ['L']}),
        NamedState(attribute_system, p_1, {('color', 's1'): ['R'], ('color', 's2'): ['R'], ('size', 's1'): ['L'], ('size', 's2'): ['S']}),
        NamedState(attribute_system, p_1, {('color', 's1'): ['R'], ('color', 's2'): ['R'], ('size', 's1'): ['S'], ('size', 's2'): ['L']}),
        NamedState(attribute_system, p_1, {('color', 's1'): ['R'], ('color', 's2'): ['R'], ('size', 's1'): ['S'], ('size', 's2'): ['S']}),
        NamedState(attribute_system, p_2, {('color', 's1'): ['R'], ('color', 's2'): ['G'], ('size', 's1'): ['L'], ('size', 's2'): ['L']}),
        NamedState(attribute_system, p_2, {('color', 's1'): ['R'], ('color', 's2'): ['G'], ('size', 's1'): ['L'], ('size', 's2'): ['S']}),
        NamedState(attribute_system, p_2, {('color', 's1'): ['R'], ('color', 's2'): ['G'], ('size', 's1'): ['S'], ('size', 's2'): ['L']}),
        NamedState(attribute_system, p_2, {('color', 's1'): ['R'], ('color', 's2'): ['G'], ('size', 's1'): ['S'], ('size', 's2'): ['S']}),
        NamedState(attribute_system, p_2, {('color', 's1'): ['R'], ('color', 's2'): ['R'], ('size', 's1'): ['L'], ('size', 's2'): ['L']}),
        NamedState(attribute_system, p_2, {('color', 's1'): ['R'], ('color', 's2'): ['R'], ('size', 's1'): ['L'], ('size', 's2'): ['S']}),
        NamedState(attribute_system, p_2, {('color', 's1'): ['R'], ('color', 's2'): ['R'], ('size', 's1'): ['S'], ('size', 's2'): ['L']}),
        NamedState(attribute_system, p_2, {('color', 's1'): ['R'], ('color', 's2'): ['R'], ('size', 's1'): ['S'], ('size', 's2'): ['S']})]

    assert worlds == worlds_manual

def test_is_named_alternate_extension():
    """Test is_named_alternate_extension() function for NamedState."""
    pass

def test_get_named_alternate_extensions():
    """Test get_named_alternate_extensions() function for NamedState."""
    pass

def test_satisfies_formula():
    """Test satisfies_formula() function for NamedState."""
    pass

def test_satisfies_named_state():
    """Test satisfies_named_state() function for NamedState."""
    pass

def test_satisfies_context():
    """Test satisfies_context() function for NamedState."""
    pass

def test_is_named_entailment():
    """Test is_named_entailment() function for NamedState."""
    pass

def test___str__():
    """Test str(NamedState)."""
    color = Attribute('color', ['R', 'G'])
    size = Attribute('size', ['S', 'L'])
    attribute_structure = AttributeStructure(color, size)
    objects = ['s1', 's2']
    attribute_system = AttributeSystem(attribute_structure, objects)
    sigma = Vocabulary(['a', 'b'], [], [])


    p = ConstantAssignment(sigma, attribute_system, {})
    p_1 = ConstantAssignment(sigma, attribute_system, {'a': 's1', 'b': 's2'})

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
    sigma = Vocabulary(['a', 'b'], [], [])


    p = ConstantAssignment(sigma, attribute_system, {})
    p_1 = ConstantAssignment(sigma, attribute_system, {'a': 's1', 'b': 's2'})

    ascr = {('color', 's1'): ['R']}

    ns = NamedState(attribute_system, p, ascr)
    ns1 = NamedState(attribute_system, p_1, ascr)
    assert repr(ns) == "color(s1): {V(R)}\ncolor(s2): {V(G, R)}\nsize(s1): {V(L, S)}\nsize(s2): {V(L, S)}\nCA{}"
    assert repr(ns1) == "color(s1): {V(R)}\ncolor(s2): {V(G, R)}\nsize(s1): {V(L, S)}\nsize(s2): {V(L, S)}\nCA{'a': 's1', 'b': 's2'}"
