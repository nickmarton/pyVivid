"""A sequence class for Parsers."""

from TruthValueParser import TruthValueParser
from PointParser import PointParser


class ParserSet(object):
    """ParserSet object functioning as a sequence/collection."""

    def __init__(self):
        """Construct ParserSet object."""
        self._parsers = [TruthValueParser(), PointParser()]

    def __len__(self):
        """Implement len(ParserSet)."""
        return len(self._parsers)

    def __getitem__(self, key):
        """Implement ParserSet[index]."""
        if type(key) is not int:
            raise TypeError("Indexing of ParserSet requires type int")
        return self._parsers[key]

    def __iter__(self):
        """Implement iterator for ParserSet."""
        for parser in self._parsers:
            yield parser


def main():
    """."""
    ParserSet()

if __name__ == "__main__":
    main()
