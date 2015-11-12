"""Context unit tests."""

import pytest
from vivid.Classes.Interval import Interval
from vivid.Classes.RelationSymbol import RelationSymbol
from vivid.Classes.Vocabulary import Vocabulary
from vivid.Classes.Formula import Formula
from vivid.Classes.AssumptionBase import AssumptionBase
from vivid.Classes.Attribute import Attribute
from vivid.Classes.Relation import Relation
from vivid.Classes.AttributeStructure import AttributeStructure
from vivid.Classes.AttributeSystem import AttributeSystem
from vivid.Classes.ConstantAssignment import ConstantAssignment
from vivid.Classes.NamedState import NamedState
from vivid.Classes.Context import Context

def test___init__():
    """Test Context construction."""
    def test_TypeError(assumption_base, named_state):
        """Test TypeError raising in Context construction."""
        with pytest.raises(TypeError) as excinfo:
            Context(assumption_base, named_state)
    def test_ValueError(assumption_base, named_state):
        """Test ValueError raising in Context construction."""
        with pytest.raises(ValueError) as excinfo:
            Context(assumption_base, named_state)

    ahead_rs = RelationSymbol('Ahead', 4)
    behind_rs = RelationSymbol('Behind', 4)
    pm_rs = RelationSymbol('PM', 1)
    am_rs = RelationSymbol('AM', 1)
    vocabulary = Vocabulary(['C1', 'C2'], [ahead_rs, behind_rs, pm_rs, am_rs], ['V1', 'V2'])
    bad_vocabulary = Vocabulary(['C1', 'C2'], [ahead_rs, behind_rs, pm_rs, am_rs], ['V1'])

    f = Formula(vocabulary, 'Ahead', 'C1', 'V1')
    f2 = Formula(vocabulary, 'Behind', 'C1', 'V1')
    f_bad = Formula(bad_vocabulary, 'Ahead', 'C1', 'V1')

    a = Attribute('hour', [Interval(0, 23)])
    a2 = Attribute('minute', [Interval(0, 59)])
    r_pm = Relation('R1(h1) <=> h1 > 11', ['hour'], 1)
    r_am = Relation('R2(h1) <=> h1 <= 11', ['hour'], 2)
    r_ahead = Relation('R3(h1,m1,hhh2,mm2) <=> h1 > hhh2 or (h1 = hhh2 and m1 > mm2)', ['hour', 'minute', 'hour', 'minute'], 3)
    r_behind = Relation('R4(h1,m1,h2,m2) <=> h1 <= h2 or (h1 = h2 and m1 < m2)', ['hour', 'minute', 'hour', 'minute'], 4)
    attribute_structure = AttributeStructure(a, a2, r_ahead, r_behind, r_pm, r_am)
    objects = ['s1', 's2']
    attribute_system = AttributeSystem(attribute_structure, objects)
    p = ConstantAssignment(vocabulary, attribute_system, {'C1': 's1', 'C2': 's2'})
    bad_p = ConstantAssignment(bad_vocabulary, attribute_system, {'C1': 's1', 'C2': 's2'})
    

    assumption_base = AssumptionBase(f, f2)
    named_state = NamedState(attribute_system, p)
    bad_assumption_base = AssumptionBase(f_bad)
    bad_named_state = NamedState(attribute_system, bad_p)

    test_TypeError(assumption_base, None)
    test_TypeError(assumption_base, object)
    test_TypeError(None, named_state)
    test_TypeError(object, named_state)
    test_ValueError(bad_assumption_base, named_state)
    test_ValueError(assumption_base, bad_named_state)

    C = Context(assumption_base, named_state)
    assert C._assumption_base == assumption_base
    assert C._assumption_base is assumption_base
    assert C._named_state == named_state
    assert C._named_state is named_state
    
def test___eq__():
    """Test == operator for Context."""
    def test_TypeError(self, other):
        """Test TypeError raising in == operator of Context."""
        with pytest.raises(TypeError) as excinfo:
            self == other

    ahead_rs = RelationSymbol('Ahead', 4)
    behind_rs = RelationSymbol('Behind', 4)
    pm_rs = RelationSymbol('PM', 1)
    am_rs = RelationSymbol('AM', 1)
    vocabulary = Vocabulary(['C1', 'C2'], [ahead_rs, behind_rs, pm_rs, am_rs], ['V1', 'V2'])

    f = Formula(vocabulary, 'Ahead', 'C1', 'V1')
    f2 = Formula(vocabulary, 'Behind', 'C1', 'V1')
    f_copy = Formula(vocabulary, 'Ahead', 'C1', 'V1')

    a = Attribute('hour', [Interval(0, 23)])
    a2 = Attribute('minute', [Interval(0, 59)])
    r_ahead = Relation('R3(h1,m1,hhh2,mm2) <=> h1 > hhh2 or (h1 = hhh2 and m1 > mm2)', ['hour', 'minute', 'hour', 'minute'], 3)
    attribute_structure = AttributeStructure(a, a2, r_ahead)
    objects = ['s1', 's2']
    attribute_system = AttributeSystem(attribute_structure, objects)
    attribute_system_copy = AttributeSystem(attribute_structure, objects)
    p = ConstantAssignment(vocabulary, attribute_system, {'C1': 's1', 'C2': 's2'})
    p2 = ConstantAssignment(vocabulary, attribute_system, {'C1': 's2', 'C2': 's1'})
    p_copy = ConstantAssignment(vocabulary, attribute_system, {'C1': 's1', 'C2': 's2'})
    

    assumption_base = AssumptionBase(f)
    assumption_base_copy = AssumptionBase(f_copy)
    assumption_base2 = AssumptionBase(f, f2)
    named_state = NamedState(attribute_system, p)
    named_state_copy = NamedState(attribute_system_copy, p_copy)
    named_state2 = NamedState(attribute_system, p2)

    C = Context(assumption_base, named_state)
    C2 = Context(assumption_base, named_state)
    C3 = Context(assumption_base_copy, named_state_copy)
    C4 = Context(assumption_base2, named_state)
    C5 = Context(assumption_base, named_state2)

    test_TypeError(C, None)
    test_TypeError(C, object)
    test_TypeError(C, named_state)
    test_TypeError(C, assumption_base)
    assert C == C
    assert C is C
    assert C == C2
    assert C is not C2
    assert C == C3
    assert C is not C3
    assert not C == C4
    assert not C == C5

def test___ne__():
    """Test != operator for Context."""
    def test_TypeError(self, other):
        """Test TypeError raising in != operator of Context."""
        with pytest.raises(TypeError) as excinfo:
            self != other

    ahead_rs = RelationSymbol('Ahead', 4)
    behind_rs = RelationSymbol('Behind', 4)
    pm_rs = RelationSymbol('PM', 1)
    am_rs = RelationSymbol('AM', 1)
    vocabulary = Vocabulary(['C1', 'C2'], [ahead_rs, behind_rs, pm_rs, am_rs], ['V1', 'V2'])

    f = Formula(vocabulary, 'Ahead', 'C1', 'V1')
    f2 = Formula(vocabulary, 'Behind', 'C1', 'V1')
    f_copy = Formula(vocabulary, 'Ahead', 'C1', 'V1')

    a = Attribute('hour', [Interval(0, 23)])
    a2 = Attribute('minute', [Interval(0, 59)])
    r_ahead = Relation('R3(h1,m1,hhh2,mm2) <=> h1 > hhh2 or (h1 = hhh2 and m1 > mm2)', ['hour', 'minute', 'hour', 'minute'], 3)
    attribute_structure = AttributeStructure(a, a2, r_ahead)
    objects = ['s1', 's2']
    attribute_system = AttributeSystem(attribute_structure, objects)
    attribute_system_copy = AttributeSystem(attribute_structure, objects)
    p = ConstantAssignment(vocabulary, attribute_system, {'C1': 's1', 'C2': 's2'})
    p2 = ConstantAssignment(vocabulary, attribute_system, {'C1': 's2', 'C2': 's1'})
    p_copy = ConstantAssignment(vocabulary, attribute_system, {'C1': 's1', 'C2': 's2'})
    

    assumption_base = AssumptionBase(f)
    assumption_base_copy = AssumptionBase(f_copy)
    assumption_base2 = AssumptionBase(f, f2)
    named_state = NamedState(attribute_system, p)
    named_state_copy = NamedState(attribute_system_copy, p_copy)
    named_state2 = NamedState(attribute_system, p2)

    C = Context(assumption_base, named_state)
    C2 = Context(assumption_base, named_state)
    C3 = Context(assumption_base_copy, named_state_copy)
    C4 = Context(assumption_base2, named_state)
    C5 = Context(assumption_base, named_state2)

    test_TypeError(C, None)
    test_TypeError(C, object)
    test_TypeError(C, named_state)
    test_TypeError(C, assumption_base)
    assert not C != C
    assert C is C
    assert not C != C2
    assert C is not C2
    assert not C != C3
    assert C is not C3
    assert C != C4
    assert C != C5

def test___str__():
    """Test str(Context)."""
    ahead_rs = RelationSymbol('Ahead', 4)
    behind_rs = RelationSymbol('Behind', 4)
    pm_rs = RelationSymbol('PM', 1)
    am_rs = RelationSymbol('AM', 1)
    vocabulary = Vocabulary(['C1', 'C2'], [ahead_rs, behind_rs, pm_rs, am_rs], ['V1', 'V2'])

    f = Formula(vocabulary, 'Ahead', 'C1', 'V1')

    a = Attribute('hour', [Interval(0, 23)])
    a2 = Attribute('minute', [Interval(0, 59)])
    r_pm = Relation('R1(h1) <=> h1 > 11', ['hour'], 1)
    r_am = Relation('R2(h1) <=> h1 <= 11', ['hour'], 2)
    r_ahead = Relation('R3(h1,m1,hhh2,mm2) <=> h1 > hhh2 or (h1 = hhh2 and m1 > mm2)', ['hour', 'minute', 'hour', 'minute'], 3)
    r_behind = Relation('R4(h1,m1,h2,m2) <=> h1 <= h2 or (h1 = h2 and m1 < m2)', ['hour', 'minute', 'hour', 'minute'], 4)
    attribute_structure = AttributeStructure(a, a2, r_ahead, r_behind, r_pm, r_am)
    objects = ['s1', 's2']
    attribute_system = AttributeSystem(attribute_structure, objects)
    p = ConstantAssignment(vocabulary, attribute_system, {'C1': 's1', 'C2': 's2'})

    assumption_base = AssumptionBase(f)
    named_state = NamedState(attribute_system, p)

    C = Context(assumption_base, named_state)

    assert str(C) == "hour(s1): {V(I(0, 23))}\n" + \
                     "hour(s2): {V(I(0, 23))}\n" + \
                     "minute(s1): {V(I(0, 59))}\n" + \
                     "minute(s2): {V(I(0, 59))}\n" + \
                     "CA{'C2': 's2', 'C1': 's1'}\n" + \
                     "AB(Ahead(C1, V1))"

def test___repr__():
    """Test str(Context)."""
    ahead_rs = RelationSymbol('Ahead', 4)
    behind_rs = RelationSymbol('Behind', 4)
    pm_rs = RelationSymbol('PM', 1)
    am_rs = RelationSymbol('AM', 1)
    vocabulary = Vocabulary(['C1', 'C2'], [ahead_rs, behind_rs, pm_rs, am_rs], ['V1', 'V2'])

    f = Formula(vocabulary, 'Ahead', 'C1', 'V1')

    a = Attribute('hour', [Interval(0, 23)])
    a2 = Attribute('minute', [Interval(0, 59)])
    r_pm = Relation('R1(h1) <=> h1 > 11', ['hour'], 1)
    r_am = Relation('R2(h1) <=> h1 <= 11', ['hour'], 2)
    r_ahead = Relation('R3(h1,m1,hhh2,mm2) <=> h1 > hhh2 or (h1 = hhh2 and m1 > mm2)', ['hour', 'minute', 'hour', 'minute'], 3)
    r_behind = Relation('R4(h1,m1,h2,m2) <=> h1 <= h2 or (h1 = h2 and m1 < m2)', ['hour', 'minute', 'hour', 'minute'], 4)
    attribute_structure = AttributeStructure(a, a2, r_ahead, r_behind, r_pm, r_am)
    objects = ['s1', 's2']
    attribute_system = AttributeSystem(attribute_structure, objects)
    p = ConstantAssignment(vocabulary, attribute_system, {'C1': 's1', 'C2': 's2'})

    assumption_base = AssumptionBase(f)
    named_state = NamedState(attribute_system, p)

    C = Context(assumption_base, named_state)

    assert repr(C) == "hour(s1): {V(I(0, 23))}\n" + \
                     "hour(s2): {V(I(0, 23))}\n" + \
                     "minute(s1): {V(I(0, 59))}\n" + \
                     "minute(s2): {V(I(0, 59))}\n" + \
                     "CA{'C2': 's2', 'C1': 's1'}\n" + \
                     "AB(Ahead(C1, V1))"

def test___deepcopy__():
    """Test copy.deepcopy for Context object."""
    ahead_rs = RelationSymbol('Ahead', 4)
    behind_rs = RelationSymbol('Behind', 4)
    pm_rs = RelationSymbol('PM', 1)
    am_rs = RelationSymbol('AM', 1)
    vocabulary = Vocabulary(['C1', 'C2'], [ahead_rs, behind_rs, pm_rs, am_rs], ['V1', 'V2'])

    f = Formula(vocabulary, 'Ahead', 'C1', 'V1')

    a = Attribute('hour', [Interval(0, 23)])
    a2 = Attribute('minute', [Interval(0, 59)])
    r_pm = Relation('R1(h1) <=> h1 > 11', ['hour'], 1)
    r_am = Relation('R2(h1) <=> h1 <= 11', ['hour'], 2)
    r_ahead = Relation('R3(h1,m1,hhh2,mm2) <=> h1 > hhh2 or (h1 = hhh2 and m1 > mm2)', ['hour', 'minute', 'hour', 'minute'], 3)
    r_behind = Relation('R4(h1,m1,h2,m2) <=> h1 <= h2 or (h1 = h2 and m1 < m2)', ['hour', 'minute', 'hour', 'minute'], 4)
    attribute_structure = AttributeStructure(a, a2, r_ahead, r_behind, r_pm, r_am)
    objects = ['s1', 's2']
    attribute_system = AttributeSystem(attribute_structure, objects)
    p = ConstantAssignment(vocabulary, attribute_system, {'C1': 's1', 'C2': 's2'})

    assumption_base = AssumptionBase(f)
    named_state = NamedState(attribute_system, p)

    C = Context(assumption_base, named_state)

    from copy import deepcopy
    C_copy = deepcopy(C)
    assert C_copy == C
    assert C_copy is not C
    assert C_copy._assumption_base is not C._assumption_base
    assert C_copy._named_state is not C._named_state

def test_entails_formula():
    """Test entails_formula() function for Context."""
    pass

def test_entails_named_state():
    """Test entails_named_state() function for Context."""
    pass
