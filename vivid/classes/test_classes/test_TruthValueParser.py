"""TruthValueParser unit tests."""

from vivid.classes.parsers.truth_value_parser import TruthValueParser


def test_eval():
    """Test TruthValueParser evaluation."""
    lmtp = TruthValueParser()
    assert lmtp('True') is True
    assert lmtp('True or 1 = 1') is True
    assert lmtp(
        '(4 < 5 * cos(2 * PI) and 4 * e^3 > 3 * 3 * (3 + 3)) and !!(2 < 3)') \
        is True
    assert lmtp(
        '!(4 < 5 * cos(2 * PI) and 4 * e^3 > 3 * 3 * (3 + 3)) and !!(2 < 3)') \
        is False
