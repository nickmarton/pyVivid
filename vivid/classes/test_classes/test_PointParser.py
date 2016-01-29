"""PointParser unit tests."""

from vivid.classes.parsers.point_parser import PointParser


def test___init__():
    """Test PointParser constructor."""
    assert hasattr(PointParser(), "_is_Parser")


def test___call__():
    """Test callable functionality."""
    assert hasattr(PointParser(), '__call__')


def test__eval():
    """Test _eval function."""
    # Test eval of is_on function contained in Point class
    eval_string_1 = "is_on(P(2.0,2.0),P(-1.0,-1.0),P(3.0,3.0))"
    eval_string_2 = "is_on(P(2.0,2.0,-2.0),P(1.0,1.0,-1.0),P(3.0,3.0,-3.0))"
    eval_string_3 = "is_on(P(2.0,2.0,2.0,2.0),P(1.0,1.0,1.0,1.0),P(3.0,3.0,3.0,3.0))"
    eval_string_4 = "is_on(P(2.0,2.0),P(6.0,1.0),P(3.0,2.0))"
    parser = PointParser()
    assert parser(eval_string_1)
    assert parser(eval_string_2)
    assert parser(eval_string_3)
    assert not parser(eval_string_4)
    assert parser("can_observe(P(1.5,1.5,1.5,1.5),P(2.0,2.0,2.0,2.0),P(1.0,1.0,1.0,1.0),P(3.0,3.0,3.0,3.0))")
    assert parser("clocks_unequal(P(1.5,1.5,1.5,1.5),P(2.0,2.0,2.0,2.0))")
    assert parser("is_on(P(1.5,1.5,1.5,1.5),P(1.0,1.0,1.0,1.0),P(3.0,3.0,3.0,3.0))")
    assert parser("not_same_point(P(1.5,1.5,1.5,1.5),P(2.0,2.0,2.0,2.0))")
    assert parser("meets(P(1.5,1.5,1.5,1.5),P(2.0,2.0,2.0,2.0),P(1.0,1.0,1.0,1.0),P(1.0,1.0,1.0,1.0),P(2.0,2.0,2.0,2.0))")
