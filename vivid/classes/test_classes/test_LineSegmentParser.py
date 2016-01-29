"""LineSegmentParser unit tests."""

from vivid.classes.parsers.line_segment_parser import LineSegmentParser


def test___init__():
    """Test PointParser constructor."""
    assert hasattr(LineSegmentParser(), "_is_Parser")


def test___call__():
    """Test callable functionality."""
    assert hasattr(LineSegmentParser(), '__call__')


def test__eval():
    """Test _eval function."""
    # Test eval of is_on function contained in Point class
    eval_str = "meets(P(2.5,2.5),L(P(0.0,0.0),P(5.0,5.0)),L(P(5.0,0.0),P(0.0,5.0)))"
    parser = LineSegmentParser()
    assert parser(eval_str)
