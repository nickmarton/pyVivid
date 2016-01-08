"""State unit tests."""

import pytest
from vivid.Classes.ValueSet import ValueSet
from vivid.Classes.State import State
from vivid.Classes.State import AttributeSystem
from vivid.Classes.State import AttributeStructure
from vivid.Classes.State import Attribute


def test___init__():
    """Test State constructor."""
    def test_TypeError(attribute_system, ascriptions={}):
        """Test constructor for TypeErrors with given params."""
        with pytest.raises(TypeError) as excinfo:
            State(attribute_system, ascriptions)

    color = Attribute("color", ['R', 'G', 'B'])
    size = Attribute("size", ['S', 'M', 'L'])
    a = AttributeStructure(color, size)
    o = ['s1', 's2']
    asys = AttributeSystem(a, o)

    # test no attribute system
    test_TypeError(a)
    test_TypeError(object)
    test_TypeError(None)
    # test bad ascriptions
    test_TypeError(asys, [])
    test_TypeError(asys, None)
    test_TypeError(asys, object)

    s = State(asys)
    assert s._attribute_system == asys
    assert s._attribute_system is not asys
    s = State(asys, {
        ('color', 's1'): ['R'],
        ('color', 's2'): ['B', 'G'],
        ('size', 's1'): ['M'],
        ('size', 's2'): ['L', 'S']})

    assert s[(('color', 's1'))] == ValueSet(['R'])
    assert s[(('color', 's2'))] == ValueSet(['G', 'B'])
    assert s[(('size', 's1'))] == ValueSet(['M'])
    assert s[(('size', 's2'))] == ValueSet(['L', 'S'])


def test___eq__():
    """Test == operator."""
    color = Attribute("color", ['R', 'G', 'B'])
    size = Attribute("size", ['S', 'M', 'L'])
    a = AttributeStructure(color, size)
    o = ['s1', 's2']
    asys = AttributeSystem(a, o)

    s = State(asys)
    s1 = State(asys, {
        ('color', 's1'): ['R'],
        ('color', 's2'): ['B', 'G'],
        ('size', 's1'): ['M'],
        ('size', 's2'): ['L', 'S']})

    s2 = State(asys, {
        ('size', 's1'): ['M'],
        ('color', 's2'): ['B', 'G'],
        ('color', 's1'): ['R'],
        ('size', 's2'): ['L', 'S']})

    assert s1 == s2

    assert not s == s1
    s.set_ascription(('color', 's1'), ['R'])
    assert not s == s1
    s.set_ascription(('color', 's2'), ['B', 'G'])
    assert not s == s1
    s.set_ascription(('size', 's1'), ['M'])
    assert not s == s1
    s.set_ascription(('size', 's2'), ['L', 'S'])
    assert s == s1
    assert s == s1 == s2


def test___lt__():
    """Test < operator overloaded for proper extension."""
    color = Attribute("color", ['R', 'G', 'B'])
    size = Attribute("size", ['S', 'M', 'L'])
    a = AttributeStructure(color, size)
    o = ['s1', 's2']
    asys = AttributeSystem(a, o)

    s = State(asys)

    ascr = {
        ('color', 's1'): ['R'],
        ('color', 's2'): ['B', 'G'],
        ('size', 's1'): ['M'],
        ('size', 's2'): ['L', 'S']}

    s1 = State(asys, ascr)

    s_empty = State(AttributeSystem(AttributeStructure(), []))

    assert not s < s
    assert s1 < s


def test___le__():
    """Test <= operator overloaded for extension."""
    color = Attribute("color", ['R', 'G', 'B'])
    size = Attribute("size", ['S', 'M', 'L'])
    a = AttributeStructure(color, size)
    o = ['s1', 's2']
    asys = AttributeSystem(a, o)

    s = State(asys)

    ascr = {
        ('color', 's1'): ['R'],
        ('color', 's2'): ['B', 'G'],
        ('size', 's1'): ['M'],
        ('size', 's2'): ['L', 'S']}

    s1 = State(asys, ascr)

    assert s <= s
    assert s1 <= s
    assert not s <= s1


def test___ne__():
    """Test != operator."""
    color = Attribute("color", ['R', 'G', 'B'])
    size = Attribute("size", ['S', 'M', 'L'])
    a = AttributeStructure(color, size)
    o = ['s1', 's2']
    asys = AttributeSystem(a, o)

    s = State(asys)
    s1 = State(asys, {
        ('color', 's1'): ['R'],
        ('color', 's2'): ['B', 'G'],
        ('size', 's1'): ['M'],
        ('size', 's2'): ['L', 'S']})

    s2 = State(asys, {
        ('size', 's1'): ['M'],
        ('color', 's2'): ['B', 'G'],
        ('color', 's1'): ['R'],
        ('size', 's2'): ['L', 'S']})

    assert not s1 != s2

    assert s != s1
    s.set_ascription(('color', 's1'), ['R'])
    assert s != s1
    s.set_ascription(('color', 's2'), ['B', 'G'])
    assert s != s1
    s.set_ascription(('size', 's1'), ['M'])
    assert s != s1
    s.set_ascription(('size', 's2'), ['L', 'S'])
    assert not s != s1
    assert not s != s1 != s2


def test___deepcopy__():
    """Test deepcopy"""
    color = Attribute("color", ['R', 'G', 'B'])
    size = Attribute("size", ['S', 'M', 'L'])
    a = AttributeStructure(color, size)
    o = ['s1', 's2']
    asys = AttributeSystem(a, o)

    ascr = {
        ('color', 's1'): ['R'],
        ('color', 's2'): ['B', 'G'],
        ('size', 's1'): ['M'],
        ('size', 's2'): ['L', 'S']}

    s = State(asys, ascr)

    from copy import deepcopy
    s_copy = deepcopy(s)

    assert s == s_copy
    assert s is not s_copy
    assert s._attribute_system == s_copy._attribute_system
    assert s._attribute_system is not s_copy._attribute_system
    assert s._ascriptions == s_copy._ascriptions
    assert s._ascriptions is not s_copy._ascriptions


def test_set_ascription():
    """Test set_ascription function."""
    def test_TypeError(state, ascription, valueset):
        """Test set_ascription for TypeErrors with given params."""
        with pytest.raises(TypeError) as excinfo:
            state.set_ascription(ascription, valueset)

    def test_ValueError(state, ascription, valueset):
        """Test set_ascription for ValueErrors with given params."""
        with pytest.raises(ValueError) as excinfo:
            state.set_ascription(ascription, valueset)

    def test_KeyError(state, ascription, valueset):
        """Test set_ascription for KeyErrors with given params."""
        with pytest.raises(KeyError) as excinfo:
            state.set_ascription(ascription, valueset)

    color = Attribute("color", ['R', 'G', 'B'])
    size = Attribute("size", ['S', 'M', 'L'])

    a = AttributeStructure(color, size)
    o = ['s1', 's2']

    asys = AttributeSystem(a, o)
    s = State(asys)

    # test bad ao_pair types/values
    test_TypeError(s, [], ['R'])
    test_ValueError(s, (), ['R'])
    test_ValueError(s, (1, 2, 3), ['R'])
    test_ValueError(s, (1, 2), ['R'])
    test_ValueError(s, (1, ''), ['R'])
    test_ValueError(s, ('', 1), ['R'])
    # test bad types for ValueSet
    test_TypeError(s, ('color', 's1'), None)
    test_TypeError(s, ('color', 's1'), ())
    test_TypeError(s, ('color', 's1'), 'a')
    test_TypeError(s, ('color', 's1'), object)
    # test empty ValueSet catching
    test_ValueError(s, ('color', 's1'), [])
    test_ValueError(s, ('color', 's1'), set([]))
    test_ValueError(s, ('color', 's1'), ValueSet([]))
    # test bad ao-pair keys
    test_KeyError(s, ('color', 'bad object'), ['R'])
    test_KeyError(s, ('bad label', 's2'), ['R'])
    # test nonsubset valuesets
    test_ValueError(s, ('color', 's2'), ['a'])
    test_ValueError(s, ('color', 's2'), [1])

    s.set_ascription(('color', 's2'), ['R'])
    assert s[('color', 's2')] == ValueSet(['R'])
    # check reversion to superset is possible
    s.set_ascription(('color', 's2'), ['R', 'G'])
    assert s[('color', 's2')] == ValueSet(['R', 'G'])
    s.set_ascription(('size', 's1'), ['M', 'S'])
    assert s[('size', 's1')] == ValueSet(['S', 'M'])


def test___getitem__():
    """Test indexing for State"""
    color = Attribute("color", ['R', 'G', 'B'])
    size = Attribute("size", ['S', 'M', 'L'])
    a = AttributeStructure(color, size)
    o = ['s1', 's2']
    asys = AttributeSystem(a, o)

    ascr = {
        ('color', 's1'): ['R'],
        ('color', 's2'): ['B', 'G'],
        ('size', 's1'): ['M'],
        ('size', 's2'): ['L', 'S']}

    s = State(asys, ascr)

    assert s[('color', 's1')] == ValueSet(['R'])
    assert s[('color', 's2')] == ValueSet(['G', 'B'])
    assert s[('size', 's1')] == ValueSet(['M'])
    assert s[('size', 's2')] == ValueSet(['L', 'S'])

    assert s['color'] == [ValueSet(['R']), ValueSet(['B', 'G'])]
    assert s['size'] == [ValueSet(['M']), ValueSet(['L', 'S'])]


def test_add_object():
    """Test add object function to state."""
    def test_TypeError(state, obj, ascriptions=None):
        """Test constructor for TypeErrors with given params."""
        with pytest.raises(TypeError) as excinfo:
            state.add_object(obj, ascriptions)

    def test_ValueError(state, obj, ascriptions=None):
        """Test constructor for ValueErrors with given params."""
        with pytest.raises(ValueError) as excinfo:
            state.add_object(obj, ascriptions)

    color = Attribute("color", ['R', 'G', 'B'])
    a = AttributeStructure(color)
    o = ['s1']
    asys = AttributeSystem(a, o)

    s = State(asys)

    test_TypeError(s, None)
    test_TypeError(s, 1)
    test_TypeError(s, object)
    test_TypeError(s, "")
    test_TypeError(s, "a", 1)
    test_TypeError(s, "a", object)
    test_ValueError(s, "s1")
    test_ValueError(s, "a", {"s1": 1})
    test_ValueError(s, "a", {("s1"): 1})
    test_ValueError(s, "a", {("s1", 's1', 's1'): 1})
    test_ValueError(s, "a", {("color", "s1"): 1})
    test_ValueError(s, "a", {("s", "a"): 1})

    s.add_object("a")
    ascr = {("color", "s1"): ValueSet(['R', 'G', 'B']),
            ("color", "a"): ValueSet(['R', 'G', 'B'])}
    assert s._ascriptions == ascr

    s = State(asys)
    s.add_object("a", {("color", "a"): ['R']})
    ascr = {("color", "s1"): ValueSet(['R', 'G', 'B']),
            ("color", "a"): ValueSet(['R'])}
    assert s._ascriptions == ascr


def test_is_valuation():
    """Test is_valuation function."""
    color = Attribute("color", ['R', 'G', 'B'])
    size = Attribute("size", ['S', 'M', 'L'])
    a = AttributeStructure(color, size)
    o = ['s1', 's2']
    asys = AttributeSystem(a, o)

    ascr = {
        ('color', 's1'): ['R'],
        ('color', 's2'): ['B', 'G'],
        ('size', 's1'): ['M'],
        ('size', 's2'): ['L', 'S']}

    s = State(asys, ascr)

    assert not s.is_valuation('color')
    assert not s.is_valuation('size')
    s.set_ascription(('color', 's2'), ['B'])
    assert s.is_valuation('color')
    s.set_ascription(('size', 's2'), ['L'])
    assert s.is_valuation('size')


def test_is_world():
    """Test is_world function."""
    color = Attribute("color", ['R', 'G', 'B'])
    size = Attribute("size", ['S', 'M', 'L'])
    a = AttributeStructure(color, size)
    o = ['s1', 's2']
    asys = AttributeSystem(a, o)

    ascr = {
        ('color', 's1'): ['R'],
        ('color', 's2'): ['B', 'G'],
        ('size', 's1'): ['M'],
        ('size', 's2'): ['L', 'S']}

    s = State(asys, ascr)

    assert not s.is_world()
    s.set_ascription(('color', 's2'), ['B'])
    s.set_ascription(('size', 's2'), ['L'])
    assert s.is_world()


def test_get_worlds():
    """Test get_worlds function."""
    color = Attribute("color", ['R', 'G', 'B'])
    size = Attribute("size", ['S', 'M', 'L'])
    a = AttributeStructure(color, size)
    o = ['s1', 's2']
    asys = AttributeSystem(a, o)

    ascr = {
        ('color', 's1'): ['R'],
        ('color', 's2'): ['B', 'G'],
        ('size', 's1'): ['M'],
        ('size', 's2'): ['L', 'S']}

    ascr1 = {
        ('color', 's1'): ['R'],
        ('color', 's2'): ['G'],
        ('size', 's1'): ['M'],
        ('size', 's2'): ['L']}

    ascr2 = {
        ('color', 's1'): ['R'],
        ('color', 's2'): ['G'],
        ('size', 's1'): ['M'],
        ('size', 's2'): ['S']}

    ascr3 = {
        ('color', 's1'): ['R'],
        ('color', 's2'): ['B'],
        ('size', 's1'): ['M'],
        ('size', 's2'): ['L']}

    ascr4 = {
        ('color', 's1'): ['R'],
        ('color', 's2'): ['B'],
        ('size', 's1'): ['M'],
        ('size', 's2'): ['S']}

    s = State(asys, ascr)

    w1 = State(asys, ascr1)
    w2 = State(asys, ascr2)
    w3 = State(asys, ascr3)
    w4 = State(asys, ascr4)
    worlds = [w1, w2, w3, w4]

    for w in s.get_worlds():
        assert w in worlds

    assert len(s.get_worlds()) == len(worlds)


def test_is_disjoint():
    """Test is_disjoint function."""
    color = Attribute("color", ['R', 'G', 'B'])
    size = Attribute("size", ['S', 'M', 'L'])
    a = AttributeStructure(color, size)
    o = ['s1', 's2']
    asys = AttributeSystem(a, o)

    ascr = {
        ('color', 's1'): ['R'],
        ('color', 's2'): ['B', 'G'],
        ('size', 's1'): ['M'],
        ('size', 's2'): ['L', 'S']}

    s1 = State(asys, ascr)

    s3 = State(asys, ascr)

    length = Attribute("length", [1, 3, 5])
    shape = Attribute("shape", ['circle', 'triangle', 'rectangle'])
    a = AttributeStructure(length, shape)
    o = ['s1', 's2']
    asys = AttributeSystem(a, o)

    ascr = {
        ('length', 's1'): [5],
        ('length', 's2'): [1, 3],
        ('shape', 's1'): ['circle'],
        ('shape', 's2'): ['triangle', 'rectangle']}

    s2 = State(asys, ascr)

    assert s1.is_disjoint(s2)
    assert not s1.is_disjoint(s1)
    assert not s1.is_disjoint(s3)


def test_is_alternate_extension():
    """Test is_alternate_extension function."""
    from copy import deepcopy
    color, size = Attribute(
        "color", ['R', 'G', 'B']), Attribute("size", ['S', 'M', 'L'])

    a = AttributeStructure(color, size)
    o = ['s1', 's2']

    asys = AttributeSystem(a, o)
    s = State(asys)

    s.set_ascription(('color', 's1'), ['R', 'B'])
    s.set_ascription(('size', 's2'), ['M', 'L'])

    s1 = deepcopy(s)
    s1.set_ascription(('color', 's1'), ['B'])
    s1.set_ascription(('size', 's1'), ['S', 'M'])
    s1.set_ascription(('color', 's2'), ['B', 'G'])
    s2 = deepcopy(s)
    s2.set_ascription(('size', 's1'), ['L'])
    s2.set_ascription(('size', 's2'), ['L'])
    s3 = deepcopy(s)
    s3.set_ascription(('color', 's1'), ['R'])

    aes = s.get_alternate_extensions(s1, s2, s3)
    ae_s5, ae_s6, ae_s4 = aes

    for ae in aes:
        print s.is_alternate_extension(ae, s1, s2, s3)

    color, size = Attribute(
        "color", ['R', 'G', 'B']), Attribute("size", ['S', 'M', 'L'])

    a = AttributeStructure(color, size)
    o = ['s']

    asys = AttributeSystem(a, o)
    s = State(asys)

    s1 = deepcopy(s)
    s1.set_ascription(('color', 's'), ['B', 'G'])
    s1.set_ascription(('size', 's'), ['S'])

    aes = s.get_alternate_extensions(s1)
    ae_s2, ae_s3 = aes

    for ae in aes:
        print s.is_alternate_extension(ae, s1)


def test_get_alternate_extensions():
    """Test get_alternate_extensions function."""
    from copy import deepcopy
    color, size = Attribute(
        "color", ['R', 'G', 'B']), Attribute("size", ['S', 'M', 'L'])

    a = AttributeStructure(color, size)
    o = ['s1', 's2']

    asys = AttributeSystem(a, o)
    s = State(asys)

    s.set_ascription(('color', 's1'), ['R', 'B'])
    s.set_ascription(('size', 's2'), ['M', 'L'])

    s1 = deepcopy(s)
    s1.set_ascription(('color', 's1'), ['B'])
    s1.set_ascription(('size', 's1'), ['S', 'M'])
    s1.set_ascription(('color', 's2'), ['B', 'G'])
    s2 = deepcopy(s)
    s2.set_ascription(('size', 's1'), ['L'])
    s2.set_ascription(('size', 's2'), ['L'])
    s3 = deepcopy(s)
    s3.set_ascription(('color', 's1'), ['R'])

    aes = s.get_alternate_extensions(s1, s2, s3)
    ae_s5, ae_s6, ae_s4 = aes

    s4 = State(asys)
    s4.set_ascription(('color', 's1'), ['B'])
    s4.set_ascription(('color', 's2'), ['B', 'G', 'R'])
    s4.set_ascription(('size', 's1'), ['L'])
    s4.set_ascription(('size', 's2'), ['M'])

    s5 = State(asys)
    s5.set_ascription(('color', 's1'), ['B'])
    s5.set_ascription(('color', 's2'), ['R'])
    s5.set_ascription(('size', 's1'), ['M', 'S'])
    s5.set_ascription(('size', 's2'), ['L', 'M'])

    s6 = State(asys)
    s6.set_ascription(('color', 's1'), ['B'])
    s6.set_ascription(('color', 's2'), ['R'])
    s6.set_ascription(('size', 's1'), ['L', 'M', 'S'])
    s6.set_ascription(('size', 's2'), ['M'])

    assert ae_s4 == s4
    assert ae_s5 == s5
    assert ae_s6 == s6

    color, size = Attribute(
        "color", ['R', 'G', 'B']), Attribute("size", ['S', 'M', 'L'])

    a = AttributeStructure(color, size)
    o = ['s']

    asys = AttributeSystem(a, o)
    s = State(asys)

    s1 = deepcopy(s)
    s1.set_ascription(('color', 's'), ['B', 'G'])
    s1.set_ascription(('size', 's'), ['S'])

    aes = s.get_alternate_extensions(s1)
    ae_s2, ae_s3 = aes

    s2 = deepcopy(s)
    s2.set_ascription(('color', 's'), ['R'])
    s2.set_ascription(('size', 's'), ['S', 'M', 'L'])
    s3 = deepcopy(s)
    s3.set_ascription(('color', 's'), ['R', 'B', 'G'])
    s3.set_ascription(('size', 's'), ['L', 'M'])

    assert ae_s2 == s2
    assert ae_s3 == s3


def test_join():
    """Test join function for States."""
    def test_ValueError(s1, s2):
        """Test constructor for ValueErrors with given params."""
        with pytest.raises(ValueError) as excinfo:
            State.join(s1, s2)

    color = Attribute("color", ['R', 'G', 'B'])
    size = Attribute("size", ['S', 'M', 'L'])
    a = AttributeStructure(color, size)
    o = ['s1', 's2']
    asys = AttributeSystem(a, o)

    ascr1 = {('color', 's1'): ['R'],
             ('color', 's2'): ['B'],
             ('size', 's1'): ['M'],
             ('size', 's2'): ['L', 'S']}
    ascr2 = {('color', 's1'): ['G'],
             ('color', 's2'): ['G'],
             ('size', 's1'): ['L'],
             ('size', 's2'): ['M', 'S']}
    ascr3 = {('color', 's1'): ['R', 'G'],
             ('color', 's2'): ['B', 'G'],
             ('size', 's1'): ['L', 'M'],
             ('size', 's2'): ['M', 'S', 'L']}

    s1 = State(asys, ascr1)
    s2 = State(asys, ascr2)
    s3 = State(asys, ascr3)

    assert s3 == State.join(s1, s2)

    length = Attribute("length", [1, 3, 5])
    shape = Attribute("shape", ['circle', 'triangle', 'rectangle'])
    a = AttributeStructure(length, shape)
    o = ['s1', 's2']
    bad_asys = AttributeSystem(a, o)
    bad_state = State(bad_asys)

    test_ValueError(s1, bad_state)


def test___str__():
    """Test str(State)"""
    color = Attribute("color", ['R', 'G', 'B'])
    size = Attribute("size", ['S', 'M', 'L'])
    a = AttributeStructure(color, size)
    o = ['s1', 's2']
    asys = AttributeSystem(a, o)

    s = State(asys)
    s1 = State(asys, {
        ('color', 's1'): ['R'],
        ('color', 's2'): ['B', 'G'],
        ('size', 's1'): ['M'],
        ('size', 's2'): ['L', 'S']})

    s_empty = State(AttributeSystem(AttributeStructure(), []))
    assert s_empty.__str__() == ""
    assert s.__str__() == "color(s1): {V(B, G, R)}\ncolor(s2): {V(B, G, R)}\nsize(s1): {V(L, M, S)}\nsize(s2): {V(L, M, S)}"
    assert s1.__str__() == "color(s1): {V(R)}\ncolor(s2): {V(B, G)}\nsize(s1): {V(M)}\nsize(s2): {V(L, S)}"


def test___repr__():
    """Test repr(State)."""
    color = Attribute("color", ['R', 'G', 'B'])
    size = Attribute("size", ['S', 'M', 'L'])
    a = AttributeStructure(color, size)
    o = ['s1', 's2']
    asys = AttributeSystem(a, o)

    s = State(asys)
    s1 = State(asys, {
        ('color', 's1'): ['R'],
        ('color', 's2'): ['B', 'G'],
        ('size', 's1'): ['M'],
        ('size', 's2'): ['L', 'S']})

    s_empty = State(AttributeSystem(AttributeStructure(), []))
    assert s_empty.__repr__() == ""
    assert s.__repr__() == "color(s1): {V(B, G, R)}\ncolor(s2): {V(B, G, R)}\nsize(s1): {V(L, M, S)}\nsize(s2): {V(L, M, S)}"
    assert s1.__repr__() == "color(s1): {V(R)}\ncolor(s2): {V(B, G)}\nsize(s1): {V(M)}\nsize(s2): {V(L, S)}"
