"""parser_set module."""

from truth_value_parser import TruthValueParser
from point_parser import PointParser


class ParserSet(object):
    """
    ParserSet class. ParserSet objects function as a sequence/collection. The
    ParserSet class is part of the vivid object extension protocol.

    :ivar parsers: The parsers contained in the ParserSet object.
    :ivar _is_ParserSet: An identifier to use in place of type or isinstance.
    """

    def __init__(self):
        """
        Construct a ParserSet object.
        """

        self._parsers = [TruthValueParser(), PointParser()]
        self._is_ParserSet = True

    def __len__(self):
        """
        Determine the length of the ParserSet object via the ``len`` built-in
        function e.g.(``len(ParserSet)``).
        """

        return len(self._parsers)

    def __getitem__(self, key):
        """
        Retrive the parser located at the index given by ``key`` parameter via
        indexing (e.g. ``ParserSet[key]``).

        :param key: The index to use for retrieval.
        :type  key: ``int``

        :raises TypeError: ``key`` parameter must be an index.
        """

        if not isinstance(key, int):
            raise TypeError("Indexing of ParserSet requires type int")
        return self._parsers[key]

    def __iter__(self):
        """
        Provides an iterator for ParserSet
        (e.g. \"``for parser in ParserSet:``\").
        """

        for parser in self._parsers:
            yield parser


def main():
    """."""
    ParserSet()

if __name__ == "__main__":
    main()
