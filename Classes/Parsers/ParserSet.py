"""A sequence class for Parsers."""

from TruthValueParser import TruthValueParser


class ParserSet(object):
    """ParserSet object functioning as a sequence/collection."""

    def __init__(self):
        """Construct ParserSet object."""
        self._parsers = [TruthValueParser()]

    def __iter__(self):
        """Implement iterator for ParserSet."""
        for parser in self._parsers:
            yield parser


def main():
    """."""
    pass

if __name__ == "__main__":
    main()
