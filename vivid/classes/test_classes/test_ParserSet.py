"""ParserSet unit tests."""

import pytest
from vivid.classes.parsers.parser_set import ParserSet


def test___len__():
    """Test len(ParserSet)."""
    parset_set = ParserSet()
    assert len(parset_set) == 2


def test___getitem__():
    """Test ParserSet[key]."""
    def test_TypeError(parser_set, key):
        """Test ParserSet[key] for TypeErrors."""
        with pytest.raises(TypeError) as excinfo:
            parser_set[key]

    def test_IndexError(parser_set, key):
        """Test ParserSet[key] for IndexErrors."""
        with pytest.raises(IndexError) as excinfo:
            parser_set[key]

    parser_set = ParserSet()
    test_TypeError(parser_set, '')
    test_TypeError(parser_set, None)
    test_TypeError(parser_set, object)
    test_IndexError(parser_set, -3)
    test_IndexError(parser_set, 3)


def test___iter__():
    """Test iter(ParserSet)."""
    parset_set = ParserSet()
    for parser in parset_set:
        assert hasattr(parser, "_is_Parser")
