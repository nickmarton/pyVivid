"""Parser for Point object related operations."""

import os
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from Point import Point


class PointParser(object):
    """Class for parsing Point object related operations."""

    def __init__(self):
        """Initialize a PointParser object."""
        self._is_Parser = True

    def __call__(self, *args):
        """Implement callable for PointParser object."""
        return self._eval(*args)

    def _eval(self, string):
        """Try to evaluate given string."""
        print string


def main():
    """."""
    pass

if __name__ == "__main__":
    main()
