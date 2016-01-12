"""Context unit tests."""

import pytest
from vivid.Classes.Interval import Interval
from vivid.Classes.RelationSymbol import RelationSymbol
from vivid.Classes.Vocabulary import Vocabulary
from vivid.Classes.AttributeInterpretation import AttributeInterpretation
from vivid.Classes.Formula import Formula
from vivid.Classes.AssumptionBase import AssumptionBase
from vivid.Classes.Attribute import Attribute
from vivid.Classes.Relation import Relation
from vivid.Classes.AttributeStructure import AttributeStructure
from vivid.Classes.AttributeSystem import AttributeSystem
from vivid.Classes.ConstantAssignment import ConstantAssignment
from vivid.Classes.NamedState import NamedState
from vivid.Classes.Context import Context
from vivid.Classes.VariableAssignment import VariableAssignment


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
    vocabulary = Vocabulary(
        ['C1', 'C2'], [ahead_rs, behind_rs, pm_rs, am_rs], ['V1', 'V2'])
    bad_vocabulary = Vocabulary(
        ['C1', 'C2'], [ahead_rs, behind_rs, pm_rs, am_rs], ['V1'])

    f = Formula(vocabulary, 'Ahead', 'C1', 'V1')
    f2 = Formula(vocabulary, 'Behind', 'C1', 'V1')
    f_bad = Formula(bad_vocabulary, 'Ahead', 'C1', 'V1')

    a = Attribute('hour', [Interval(0, 23)])
    a2 = Attribute('minute', [Interval(0, 59)])
    r_pm = Relation('R1(h1) <=> h1 > 11', ['hour'], 1)
    r_am = Relation('R2(h1) <=> h1 <= 11', ['hour'], 2)
    r_ahead = Relation(
        'R3(h1,m1,hhh2,mm2) <=> h1 > hhh2 or (h1 = hhh2 and m1 > mm2)',
        ['hour', 'minute', 'hour', 'minute'], 3)
    r_behind = Relation(
        'R4(h1,m1,h2,m2) <=> h1 <= h2 or (h1 = h2 and m1 < m2)',
        ['hour', 'minute', 'hour', 'minute'], 4)
    attribute_structure = AttributeStructure(
        a, a2, r_ahead, r_behind, r_pm, r_am)
    objects = ['s1', 's2']
    attribute_system = AttributeSystem(attribute_structure, objects)
    p = ConstantAssignment(
        vocabulary, attribute_system, {'C1': 's1', 'C2': 's2'})
    bad_p = ConstantAssignment(
        bad_vocabulary, attribute_system, {'C1': 's1', 'C2': 's2'})

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
    # assert C._assumption_base is not assumption_base
    assert C._named_state == named_state
    # assert C._named_state is not named_state


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
    vocabulary = Vocabulary(
        ['C1', 'C2'], [ahead_rs, behind_rs, pm_rs, am_rs], ['V1', 'V2'])

    f = Formula(vocabulary, 'Ahead', 'C1', 'V1')
    f2 = Formula(vocabulary, 'Behind', 'C1', 'V1')
    f_copy = Formula(vocabulary, 'Ahead', 'C1', 'V1')

    a = Attribute('hour', [Interval(0, 23)])
    a2 = Attribute('minute', [Interval(0, 59)])
    r_ahead = Relation(
        'R3(h1,m1,hhh2,mm2) <=> h1 > hhh2 or (h1 = hhh2 and m1 > mm2)',
        ['hour', 'minute', 'hour', 'minute'], 3)
    attribute_structure = AttributeStructure(a, a2, r_ahead)
    objects = ['s1', 's2']
    attribute_system = AttributeSystem(attribute_structure, objects)
    attribute_system_copy = AttributeSystem(attribute_structure, objects)
    p = ConstantAssignment(
        vocabulary, attribute_system, {'C1': 's1', 'C2': 's2'})
    p2 = ConstantAssignment(
        vocabulary, attribute_system, {'C1': 's2', 'C2': 's1'})
    p_copy = ConstantAssignment(
        vocabulary, attribute_system, {'C1': 's1', 'C2': 's2'})

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
    vocabulary = Vocabulary(
        ['C1', 'C2'], [ahead_rs, behind_rs, pm_rs, am_rs], ['V1', 'V2'])

    f = Formula(vocabulary, 'Ahead', 'C1', 'V1')
    f2 = Formula(vocabulary, 'Behind', 'C1', 'V1')
    f_copy = Formula(vocabulary, 'Ahead', 'C1', 'V1')

    a = Attribute('hour', [Interval(0, 23)])
    a2 = Attribute('minute', [Interval(0, 59)])
    r_ahead = Relation(
        'R3(h1,m1,hhh2,mm2) <=> h1 > hhh2 or (h1 = hhh2 and m1 > mm2)',
        ['hour', 'minute', 'hour', 'minute'], 3)
    attribute_structure = AttributeStructure(a, a2, r_ahead)
    objects = ['s1', 's2']
    attribute_system = AttributeSystem(attribute_structure, objects)
    attribute_system_copy = AttributeSystem(attribute_structure, objects)
    p = ConstantAssignment(
        vocabulary, attribute_system, {'C1': 's1', 'C2': 's2'})
    p2 = ConstantAssignment(
        vocabulary, attribute_system, {'C1': 's2', 'C2': 's1'})
    p_copy = ConstantAssignment(
        vocabulary, attribute_system, {'C1': 's1', 'C2': 's2'})

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
    vocabulary = Vocabulary(
        ['C1', 'C2'], [ahead_rs, behind_rs, pm_rs, am_rs], ['V1', 'V2'])

    f = Formula(vocabulary, 'Ahead', 'C1', 'V1')

    a = Attribute('hour', [Interval(0, 23)])
    a2 = Attribute('minute', [Interval(0, 59)])
    r_pm = Relation('R1(h1) <=> h1 > 11', ['hour'], 1)
    r_am = Relation('R2(h1) <=> h1 <= 11', ['hour'], 2)
    r_ahead = Relation(
        'R3(h1,m1,hhh2,mm2) <=> h1 > hhh2 or (h1 = hhh2 and m1 > mm2)',
        ['hour', 'minute', 'hour', 'minute'], 3)
    r_behind = Relation(
        'R4(h1,m1,h2,m2) <=> h1 <= h2 or (h1 = h2 and m1 < m2)',
        ['hour', 'minute', 'hour', 'minute'], 4)
    attribute_structure = AttributeStructure(
        a, a2, r_ahead, r_behind, r_pm, r_am)
    objects = ['s1', 's2']
    attribute_system = AttributeSystem(attribute_structure, objects)
    p = ConstantAssignment(
        vocabulary, attribute_system, {'C1': 's1', 'C2': 's2'})

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
    vocabulary = Vocabulary(
        ['C1', 'C2'], [ahead_rs, behind_rs, pm_rs, am_rs], ['V1', 'V2'])

    f = Formula(vocabulary, 'Ahead', 'C1', 'V1')

    a = Attribute('hour', [Interval(0, 23)])
    a2 = Attribute('minute', [Interval(0, 59)])
    r_pm = Relation('R1(h1) <=> h1 > 11', ['hour'], 1)
    r_am = Relation('R2(h1) <=> h1 <= 11', ['hour'], 2)
    r_ahead = Relation(
        'R3(h1,m1,hhh2,mm2) <=> h1 > hhh2 or (h1 = hhh2 and m1 > mm2)',
        ['hour', 'minute', 'hour', 'minute'], 3)
    r_behind = Relation(
        'R4(h1,m1,h2,m2) <=> h1 <= h2 or (h1 = h2 and m1 < m2)',
        ['hour', 'minute', 'hour', 'minute'], 4)
    attribute_structure = AttributeStructure(
        a, a2, r_ahead, r_behind, r_pm, r_am)
    objects = ['s1', 's2']
    attribute_system = AttributeSystem(attribute_structure, objects)
    p = ConstantAssignment(
        vocabulary, attribute_system, {'C1': 's1', 'C2': 's2'})

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
    vocabulary = Vocabulary(
        ['C1', 'C2'], [ahead_rs, behind_rs, pm_rs, am_rs], ['V1', 'V2'])

    f = Formula(vocabulary, 'Ahead', 'C1', 'V1')

    a = Attribute('hour', [Interval(0, 23)])
    a2 = Attribute('minute', [Interval(0, 59)])
    r_pm = Relation('R1(h1) <=> h1 > 11', ['hour'], 1)
    r_am = Relation('R2(h1) <=> h1 <= 11', ['hour'], 2)
    r_ahead = Relation(
        'R3(h1,m1,hhh2,mm2) <=> h1 > hhh2 or (h1 = hhh2 and m1 > mm2)',
        ['hour', 'minute', 'hour', 'minute'], 3)
    r_behind = Relation(
        'R4(h1,m1,h2,m2) <=> h1 <= h2 or (h1 = h2 and m1 < m2)',
        ['hour', 'minute', 'hour', 'minute'], 4)
    attribute_structure = AttributeStructure(
        a, a2, r_ahead, r_behind, r_pm, r_am)
    objects = ['s1', 's2']
    attribute_system = AttributeSystem(attribute_structure, objects)
    p = ConstantAssignment(
        vocabulary, attribute_system, {'C1': 's1', 'C2': 's2'})

    assumption_base = AssumptionBase(f)
    named_state = NamedState(attribute_system, p)

    C = Context(assumption_base, named_state)

    from copy import deepcopy
    C_copy = deepcopy(C)
    #assert C_copy == C
    #assert C_copy is not C
    #assert C_copy._assumption_base is not C._assumption_base
    #assert C_copy._named_state is not C._named_state


def test_entails_formula():
    """Test entails_formula() function for Context."""
    def standard_test():
        """Do test with standard parser."""
        hour = Attribute('hour', [Interval(0, 23)])
        minute = Attribute('minute', [Interval(0, 59)])
        r_pm = Relation('R1(h1) <=> h1 > 11', ['hour'], 1)
        r_am = Relation('R2(h1) <=> h1 <= 11', ['hour'], 2)
        r_ahead = Relation(
            'R3(h1,m1,hhh2,mm2) <=> h1 > hhh2 or (h1 = hhh2 and m1 > mm2)',
            ['hour', 'minute', 'hour', 'minute'], 3)
        r_behind = Relation(
            'R4(h1,m1,h2,m2) <=> h1 <= h2 or (h1 = h2 and m1 < m2)',
            ['hour', 'minute', 'hour', 'minute'], 4)
        attribute_structure = AttributeStructure(
            hour, minute, r_ahead, r_behind, r_pm, r_am)

        rs_ahead = RelationSymbol('Ahead', 4)
        rs_behind = RelationSymbol('Behind', 4)
        rs_pm = RelationSymbol('PM', 1)
        rs_am = RelationSymbol('AM', 1)
        vocabulary = Vocabulary(
            ['C1', 'C2'], [rs_ahead, rs_behind, rs_pm, rs_am], ['V1', 'V2'])

        objects = ['s1', 's2']
        attribute_system = AttributeSystem(attribute_structure, objects)
        p = ConstantAssignment(
            vocabulary, attribute_system, {'C1': 's1', 'C2': 's2'})

        profiles = [
            [rs_pm, ('hour', 1)],
            [rs_am, ('hour', 1)],
            [rs_behind, ('hour', 1), ('minute', 1), ('hour', 2), ('minute', 2)],
            [rs_ahead, ('hour', 1), ('minute', 1), ('hour', 2), ('minute', 2)]]

        attribute_interpretation = AttributeInterpretation(
            vocabulary, attribute_structure,
            {rs_pm: 1, rs_am: 2, rs_ahead: 3, rs_behind: 4}, profiles)

        f1 = Formula(vocabulary, 'Ahead', 'C1', 'C2')
        f2 = Formula(vocabulary, 'Behind', 'C2', 'C1')
        f3 = Formula(vocabulary, 'PM', 'C1')
        f4 = Formula(vocabulary, 'AM', 'C2')
        assumption_base = AssumptionBase(f1, f3, f4)
        named_state = NamedState(attribute_system, p, {
                                 ("hour", "s1"): [Interval(15, 17)],
                                 ("hour", "s2"): [11],
                                 ("minute", "s1"): [23],
                                 ("minute", "s2"): [23]})

        context = Context(assumption_base, named_state)

        assert context.entails_formula(f1, attribute_interpretation)
        assert context.entails_formula(f2, attribute_interpretation)
        assert context.entails_formula(f3, attribute_interpretation)
        assert context.entails_formula(f4, attribute_interpretation)

        vocabulary = Vocabulary(
            ['C1'], [rs_ahead, rs_behind, rs_pm, rs_am], ['V1', 'V2'])

        objects = ['s1', 's2']
        attribute_system = AttributeSystem(attribute_structure, objects)
        p = ConstantAssignment(
            vocabulary, attribute_system, {'C1': 's1'})

        profiles = [
            [rs_pm, ('hour', 1)],
            [rs_am, ('hour', 1)],
            [rs_behind, ('hour', 1), ('minute', 1), ('hour', 2), ('minute', 2)],
            [rs_ahead, ('hour', 1), ('minute', 1), ('hour', 2), ('minute', 2)]]

        attribute_interpretation = AttributeInterpretation(
            vocabulary, attribute_structure,
            {rs_pm: 1, rs_am: 2, rs_ahead: 3, rs_behind: 4}, profiles)

        f1 = Formula(vocabulary, 'Ahead', 'C1', 'V1')
        f2 = Formula(vocabulary, 'PM', 'C1')
        f3 = Formula(vocabulary, 'AM', 'V1')
        f4 = Formula(vocabulary, 'AM', 'V2')
        f5 = Formula(vocabulary, 'Behind', 'V1', 'C1')
        assumption_base = AssumptionBase(f1)
        named_state = NamedState(attribute_system, p, {
                                 ("hour", "s1"): [Interval(15, 17)],
                                 ("hour", "s2"): [11],
                                 ("minute", "s1"): [23],
                                 ("minute", "s2"): [23]})

        context = Context(assumption_base, named_state)
        assert context.entails_formula(f1, attribute_interpretation)
        assert context.entails_formula(f2, attribute_interpretation)
        assert context.entails_formula(f3, attribute_interpretation)
        # assert not here as it does not hold for every variable assignment;
        # e.g. the following configuration is valid but its truth value is unknown:
        # profile: [('hour', 'V1')]
        #           CA{'C1': 's1'}
        #           VA{'V2': 's2'}, which means all terms are not defined
        assert not context.entails_formula(f4, attribute_interpretation)
        assert context.entails_formula(f5, attribute_interpretation)

    def point_test():
        """Do test with Point object and its parser."""
        from vivid.Classes.Point import Point
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

        assumption_base = AssumptionBase(f2, f3, f4)
        context = Context(assumption_base, world)

        # Whenever we can observe a Point, we're either at that point or on
        # same worldline so IS_ON should hold
        assert context.entails_formula(f1, attribute_interpretation)
        # We always entail our own formulae
        assert context.entails_formula(f2, attribute_interpretation)
        assert context.entails_formula(f3, attribute_interpretation)
        assert context.entails_formula(f4, attribute_interpretation)

    standard_test()
    point_test()


def test_entails_named_state():
    """Test entails_named_state() function for Context."""
    def standard_test():
        """Do test with standard parser."""
        hour = Attribute('hour', [Interval(0, 23)])
        minute = Attribute('minute', [Interval(0, 59)])
        r_pm = Relation('R1(h1) <=> h1 > 11', ['hour'], 1)
        r_am = Relation('R2(h1) <=> h1 <= 11', ['hour'], 2)
        r_ahead = Relation(
            'R3(h1,m1,hhh2,mm2) <=> h1 > hhh2 or (h1 = hhh2 and m1 > mm2)',
            ['hour', 'minute', 'hour', 'minute'], 3)
        r_behind = Relation(
            'R4(h1,m1,h2,m2) <=> h1 <= h2 or (h1 = h2 and m1 < m2)',
            ['hour', 'minute', 'hour', 'minute'], 4)
        attribute_structure = AttributeStructure(
            hour, minute, r_ahead, r_behind, r_pm, r_am)

        rs_ahead = RelationSymbol('Ahead', 4)
        rs_behind = RelationSymbol('Behind', 4)
        rs_pm = RelationSymbol('PM', 1)
        rs_am = RelationSymbol('AM', 1)
        vocabulary = Vocabulary(
            ['C1', 'C2'], [rs_ahead, rs_behind, rs_pm, rs_am], ['V1', 'V2'])

        objects = ['s1', 's2']
        attribute_system = AttributeSystem(attribute_structure, objects)
        p = ConstantAssignment(
            vocabulary, attribute_system, {'C1': 's1', 'C2': 's2'})

        profiles = [
            [rs_pm, ('hour', 1)],
            [rs_am, ('hour', 1)],
            [rs_behind, ('hour', 1), ('minute', 1), ('hour', 2), ('minute', 2)],
            [rs_ahead, ('hour', 1), ('minute', 1), ('hour', 2), ('minute', 2)]]

        attribute_interpretation = AttributeInterpretation(
            vocabulary, attribute_structure,
            {rs_pm: 1, rs_am: 2, rs_ahead: 3, rs_behind: 4}, profiles)

        f1 = Formula(vocabulary, 'Ahead', 'C1', 'C2')
        f2 = Formula(vocabulary, 'Behind', 'C2', 'C1')
        f3 = Formula(vocabulary, 'PM', 'C1')
        f4 = Formula(vocabulary, 'AM', 'C2')
        assumption_base = AssumptionBase(f1, f3, f4)
        named_state = NamedState(attribute_system, p, {
                                 ("hour", "s1"): [Interval(15, 17)],
                                 ("hour", "s2"): [Interval(6, 9)],
                                 ("minute", "s1"): [23],
                                 ("minute", "s2"): [23]})
        context = Context(assumption_base, named_state)

        # A context always entails its own named state
        assert context.entails_named_state(
            named_state, attribute_interpretation)

        named_state = NamedState(attribute_system, p, {
                                 ("hour", "s1"): [Interval(15, 17)],
                                 ("hour", "s2"): [Interval(4, 11)],
                                 ("minute", "s1"): [23],
                                 ("minute", "s2"): [23]})
        # A context entails named states that when the worlds of the context
        # extend the named state
        assert context.entails_named_state(
            named_state, attribute_interpretation)

        f1 = Formula(vocabulary, 'PM', 'C1')
        assumption_base = AssumptionBase(f1)
        named_state = NamedState(attribute_system, p, {
                                 ("hour", "s1"): [Interval(15, 17)],
                                 ("hour", "s2"): [Interval(6, 9)],
                                 ("minute", "s1"): [23],
                                 ("minute", "s2"): [23]})
        context = Context(assumption_base, named_state)

        named_state = NamedState(attribute_system, p, {
                                 ("hour", "s1"): [23],
                                 ("hour", "s2"): [13],
                                 ("minute", "s1"): [23],
                                 ("minute", "s2"): [23]})
        # A context does not entail a named state when the worlds of the
        # context do not extend the named state
        assert not context.entails_named_state(
            named_state, attribute_interpretation)

        f1 = Formula(vocabulary, 'PM', 'C1')
        assumption_base = AssumptionBase(f1)
        named_state = NamedState(attribute_system, p, {
                                 ("hour", "s1"): [Interval(6, 9)],
                                 ("hour", "s2"): [Interval(15, 17)],
                                 ("minute", "s1"): [23],
                                 ("minute", "s2"): [23]})
        context = Context(assumption_base, named_state)

        named_state = NamedState(attribute_system, p, {
                                 ("hour", "s1"): [23],
                                 ("hour", "s2"): [13],
                                 ("minute", "s1"): [23],
                                 ("minute", "s2"): [23]})

        # A context trivially entails a named state when no world of the
        # context satisfies the context
        assert context.entails_named_state(
            named_state, attribute_interpretation)

    def point_test():
        """Do test with Point object and its parser."""
        from vivid.Classes.Point import Point
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

        vocabulary = Vocabulary(['P1', 'P2', 'P3', 'P4'],
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

        objects = ['p1', 'p2', 'p3', 'p4']
        attribute_system = AttributeSystem(attribute_structure, objects)
        p = ConstantAssignment(vocabulary, attribute_system,
                               {'P1': 'p1', 'P2': 'p2', 'P3': 'p3', 'P4': 'p4'})

        named_state = NamedState(attribute_system, p, {
                                 ('point', 'p1'): [Point(1.5, 1.5, 1.5, 1.5)],
                                 ('point', 'p2'): [Point(2.0, 2.0, 2.0, 2.0)],
                                 ('point', 'p3'): [Point(1.0, 1.0, 1.0, 1.0)],
                                 ('point', 'p4'): [Point(3.0, 3.0, 3.0, 3.0)]})

        f1 = Formula(vocabulary, 'IS_ON', 'P1', 'P3', 'P4')
        f2 = Formula(vocabulary, 'NOT_SAME_POINT', 'P1', 'P2')
        f3 = Formula(vocabulary, 'CLOCKS_UNEQUAL', 'P1', 'P2')
        f4 = Formula(vocabulary, 'CAN_OBSERVE', 'P1', 'P2', 'P3', 'P4')

        VA = VariableAssignment(vocabulary, attribute_system, {}, dummy=True)

        assumption_base = AssumptionBase(f2, f3, f4)
        context = Context(assumption_base, named_state)

        # A context always entails its own named state
        assert context.entails_named_state(
            named_state, attribute_interpretation)

        named_state = NamedState(attribute_system, p, {
                                 ('point', 'p1'): [Point(1.5, 1.5, 1.5, 1.5),
                                                   Point(2.5, 2.5, 2.5, 2.5)],
                                 ('point', 'p2'): [Point(2.0, 2.0, 2.0, 2.0)],
                                 ('point', 'p3'): [Point(1.0, 1.0, 1.0, 1.0)],
                                 ('point', 'p4'): [Point(3.0, 3.0, 3.0, 3.0)]})

        # A context entails named states that when the worlds of the context
        # extend the named state
        assert context.entails_named_state(
            named_state, attribute_interpretation)

        named_state = NamedState(attribute_system, p, {
                                 ('point', 'p1'): [Point(1.5, 1.5, 1.5, 1.5),
                                                   Point(2.5, 2.5, 2.5, 2.5)],
                                 ('point', 'p2'): [Point(2.0, 2.0, 2.0, 2.0)],
                                 ('point', 'p3'): [Point(1.0, 1.0, 1.0, 1.0)],
                                 ('point', 'p4'): [Point(3.0, 3.0, 3.0, 3.0)]})
        context = Context(assumption_base, named_state)

        named_state = NamedState(attribute_system, p, {
                                 ('point', 'p1'): [Point(4.25, 1.3, 5.4, 7.5)],
                                 ('point', 'p2'): [Point(2.0, 2.4, 2.0, 2.0)],
                                 ('point', 'p3'): [Point(1.0, 1.0, 5.0, 1.0)],
                                 ('point', 'p4'): [Point(3.0, 3.0, 3.0, 8.0)]})
        # A context does not entail a named state when the worlds of the
        # context do not extend the named state
        assert not context.entails_named_state(
            named_state, attribute_interpretation)

        assumption_base = AssumptionBase(
            Formula(vocabulary, 'NOT_SAME_POINT', 'P1', 'P1'))
        context = Context(assumption_base, named_state)

        named_state = NamedState(attribute_system, p, {
                                 ('point', 'p1'): [Point(8.5, 1.4, 2.1, 3.6)],
                                 ('point', 'p2'): [Point(2.0, 2.0, 2.0, 2.0)],
                                 ('point', 'p3'): [Point(1.0, 1.0, 1.0, 1.0)],
                                 ('point', 'p4'): [Point(3.0, 3.0, 3.0, 3.0)]})
        # A context trivially entails a named state when no world of the
        # context satisfies the context
        assert context.entails_named_state(
            named_state, attribute_interpretation)

    standard_test()
    point_test()
