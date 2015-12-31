"""TruthValueParser unit tests."""

from vivid.Classes.Parsers.TruthValueParser import TruthValueParser


def test_eval():
    """Test TruthValueParser evaluation."""
    lmtp = TruthValueParser()
    assert lmtp.eval('True') is True
    assert lmtp.eval('True or 1 = 1') is True
    assert lmtp.eval(
        '(4 < 5 * cos(2 * PI) and 4 * e^3 > 3 * 3 * (3 + 3)) and !!(2 < 3)') \
        is True
    assert lmtp.eval(
        '!(4 < 5 * cos(2 * PI) and 4 * e^3 > 3 * 3 * (3 + 3)) and !!(2 < 3)') \
        is False
