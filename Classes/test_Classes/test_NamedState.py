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
from vivid.Classes.State import AttributeSystem
from vivid.Classes.State import AttributeStructure
from vivid.Classes.State import Attribute, Relation
from vivid.Classes.ValueSet import ValueSet
from vivid.Classes.Interval import Interval

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
    
    vocabulary = Vocabulary(['a', 'b', 'c', 'd', 'e', 'f', 'g'],[],[])
    p = ConstantAssignment(vocabulary, attribute_system, {'a': 's1'})
    p_bad = ConstantAssignment(vocabulary, attribute_system_bad, {'a': 's1'})

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
    vocabulary = Vocabulary(['a', 'b', 'c', 'd', 'e', 'f', 'g'],[],[])


    p = ConstantAssignment(vocabulary, attribute_system, {'a': 's1'})
    p_1 = ConstantAssignment(vocabulary, attribute_system, {'a': 's1', 'b': 's2'})
    
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
    vocabulary = Vocabulary(['a', 'b', 'c', 'd', 'e', 'f', 'g'],[],[])


    p = ConstantAssignment(vocabulary, attribute_system, {'a': 's1'})
    p_1 = ConstantAssignment(vocabulary, attribute_system, {'a': 's1', 'b': 's2'})
    
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
    vocabulary = Vocabulary(['a', 'b', 'c', 'd', 'e', 'f', 'g'],[],[])


    p = ConstantAssignment(vocabulary, attribute_system, {'a': 's1'})
    p_1 = ConstantAssignment(vocabulary, attribute_system, {'a': 's1', 'b': 's2'})
    
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
    vocabulary = Vocabulary(['a', 'b', 'c', 'd', 'e', 'f', 'g'],[],[])


    p = ConstantAssignment(vocabulary, attribute_system, {'a': 's1'})
    p_1 = ConstantAssignment(vocabulary, attribute_system, {'a': 's1', 'b': 's2'})
    
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
    vocabulary = Vocabulary(['a', 'b', 'c', 'd', 'e', 'f', 'g'],[],[])


    p = ConstantAssignment(vocabulary, attribute_system, {'a': 's1'})
    p_1 = ConstantAssignment(vocabulary, attribute_system, {'a': 's1', 'b': 's2'})
    
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
    vocabulary = Vocabulary(['a', 'b'], [], [])


    p = ConstantAssignment(vocabulary, attribute_system, {'a': 's1'})
    p_total = ConstantAssignment(vocabulary, attribute_system, {'a': 's1', 'b': 's2'})
    
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
    p_1 = ConstantAssignment(vocabulary, attribute_system, {'a': 's1', 'b': 's2'})
    p_2 = ConstantAssignment(vocabulary, attribute_system, {'a': 's2', 'b': 's1'})
    
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
    def test_TypeError(world, formula, attribute_interpretation, X):
        """Test TypeError catching in satisfies_formula()."""
        with pytest.raises(TypeError) as excinfo:
            world.satisfies_formula(formula, attribute_interpretation, X)
    def test_ValueError(world, formula, attribute_interpretation, X):
        """Test ValueError catching in satisfies_formula()."""
        with pytest.raises(ValueError) as excinfo:
            world.satisfies_formula(formula, attribute_interpretation, X)

    a = Attribute('hour', [Interval(0, 23)])
    a2 = Attribute('minute', [Interval(0, 59)])
    r_pm = Relation('R1(h1) <=> h1 > 11', ['hour'], 1)
    r_am = Relation('R2(h1) <=> h1 <= 11', ['hour'], 2)
    r_ahead = Relation('R3(h1,m1,h2,m2) <=> h1 > h2 or (h1 = h2 and m1 > m2)', ['hour', 'minute', 'hour', 'minute'], 3)
    r_behind = Relation('R4(h1,m1,h2,m2) <=> h1 < h2 or (h1 = h2 and m1 < m2)', ['hour', 'minute', 'hour', 'minute'], 4)
    attribute_structure = AttributeStructure(a, a2, r_ahead, r_behind, r_pm, r_am)

    pm_rs = RelationSymbol('PM', 1)
    am_rs = RelationSymbol('AM', 1)
    ahead_rs = RelationSymbol('Ahead', 4)
    behind_rs = RelationSymbol('Behind', 4)
    vocabulary = Vocabulary(['C1', 'C2'], [pm_rs, am_rs, ahead_rs, behind_rs], ['V1', 'V2'])

    profiles = [    
        [pm_rs, ('hour', 1)],
        [am_rs, ('hour', 1)],
        [behind_rs, ('hour', 1), ('minute', 1), ('hour', 2), ('minute', 2)],
        [ahead_rs, ('hour', 1), ('minute', 1), ('hour', 2), ('minute', 2)]]

    attribute_interpretation = AttributeInterpretation(
        vocabulary, attribute_structure, {pm_rs: 1, am_rs: 2, ahead_rs: 3, behind_rs: 4}, profiles)

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

    a = Attribute('hour', [Interval(0, 23)])
    a2 = Attribute('minute', [Interval(0, 59)])
    r_pm = Relation('R1(h1) <=> h1 > 11', ['hour'], 1)
    r_am = Relation('R2(h1) <=> h1 <= 11', ['hour'], 2)
    r_ahead = Relation('R3(h1,m1,h2,m2) <=> h1 > h2 or (h1 = h2 and m1 > m2)', ['hour', 'minute', 'hour', 'minute'], 3)
    r_behind = Relation('R4(h1,m1,h2,m2) <=> h1 < h2 or (h1 = h2 and m1 < m2)', ['hour', 'minute', 'hour', 'minute'], 4)
    attribute_structure = AttributeStructure(a, a2, r_ahead, r_behind, r_pm, r_am)

    pm_rs = RelationSymbol('PM', 1)
    am_rs = RelationSymbol('AM', 1)
    ahead_rs = RelationSymbol('Ahead', 4)
    behind_rs = RelationSymbol('Behind', 4)
    vocabulary = Vocabulary(['C1', 'C2'], [pm_rs, am_rs, ahead_rs, behind_rs], ['V1', 'V2'])

    objs = ['c1', 'c2']
    asys = AttributeSystem(attribute_structure, objs)

    p = ConstantAssignment(vocabulary, asys, {'C1': 'c1', 'C2': 'c2'})

    named_state = NamedState(asys, p)
    named_state.set_ascription(('hour', 'c1'), [1])
    named_state.set_ascription(('hour', 'c2'), [1])
    named_state.set_ascription(('minute', 'c1'), [47, 33, 13, 6, 19])
    named_state.set_ascription(('minute', 'c2'), [1, 4, 9, 12, 55])

    worlds = named_state.get_worlds()
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

    a = Attribute('hour', [Interval(0, 23)])
    a2 = Attribute('minute', [Interval(0, 59)])
    r_pm = Relation('R1(h1) <=> h1 > 11', ['hour'], 1)
    r_am = Relation('R2(h1) <=> h1 <= 11', ['hour'], 2)
    r_ahead = Relation('R3(h1,m1,h2,m2) <=> h1 > h2 or (h1 = h2 and m1 > m2)', ['hour', 'minute', 'hour', 'minute'], 3)
    r_behind = Relation('R4(h1,m1,h2,m2) <=> h1 < h2 or (h1 = h2 and m1 < m2)', ['hour', 'minute', 'hour', 'minute'], 4)
    attribute_structure = AttributeStructure(a, a2, r_ahead, r_behind, r_pm, r_am)

    pm_rs = RelationSymbol('PM', 1)
    am_rs = RelationSymbol('AM', 1)
    ahead_rs = RelationSymbol('Ahead', 4)
    behind_rs = RelationSymbol('Behind', 4)
    vocabulary = Vocabulary(['C1', 'C2'], [pm_rs, am_rs, ahead_rs, behind_rs], ['V1', 'V2'])

    profiles = [    
        [pm_rs, ('hour', 1)],
        [am_rs, ('hour', 1)],
        [behind_rs, ('hour', 1), ('minute', 1), ('hour', 2), ('minute', 2)],
        [ahead_rs, ('hour', 1), ('minute', 1), ('hour', 2), ('minute', 2)]]

    attribute_interpretation = AttributeInterpretation(
        vocabulary, attribute_structure, {pm_rs: 1, am_rs: 2, ahead_rs: 3, behind_rs: 4}, profiles)

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
    assert not world.satisfies_context(bad_context, X, attribute_interpretation)
    assert not world.satisfies_context(bad_context2, X, attribute_interpretation)
    assert not world.satisfies_context(bad_context3, X, attribute_interpretation)

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
    assert not world2.satisfies_context(bad_context, X, attribute_interpretation)
    assert not world2.satisfies_context(bad_context2, X, attribute_interpretation)
    assert not world2.satisfies_context(bad_context3, X, attribute_interpretation)

    test_TypeError(world, None, attribute_interpretation, X)
    test_TypeError(world, object, attribute_interpretation, X)
    test_TypeError(world, good_context, None, X)
    test_TypeError(world, good_context, object, X)
    test_TypeError(world, good_context, attribute_interpretation, None)
    test_TypeError(world, good_context, attribute_interpretation, object)
    test_ValueError(named_state, good_context, X, attribute_interpretation)

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
    vocabulary = Vocabulary(['a', 'b'], [], [])


    p = ConstantAssignment(vocabulary, attribute_system, {})
    p_1 = ConstantAssignment(vocabulary, attribute_system, {'a': 's1', 'b': 's2'})

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
    p_1 = ConstantAssignment(vocabulary, attribute_system, {'a': 's1', 'b': 's2'})

    ascr = {('color', 's1'): ['R']}

    ns = NamedState(attribute_system, p, ascr)
    ns1 = NamedState(attribute_system, p_1, ascr)
    assert repr(ns) == "color(s1): {V(R)}\ncolor(s2): {V(G, R)}\nsize(s1): {V(L, S)}\nsize(s2): {V(L, S)}\nCA{}"
    assert repr(ns1) == "color(s1): {V(R)}\ncolor(s2): {V(G, R)}\nsize(s1): {V(L, S)}\nsize(s2): {V(L, S)}\nCA{'a': 's1', 'b': 's2'}"
