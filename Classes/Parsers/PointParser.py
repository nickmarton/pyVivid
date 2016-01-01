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
        for fn in dir(Point):
            pass#print fn
        fn_start, fn_end = string.find("("), string.rfind(")")
        fn_name, fn_args = string[:fn_start], string[fn_start + 1: fn_end]

        #fn_args = "P(x), P(1,2)"
        print fn_args
        import re
        point_pattern = r'P\(\d\.\d+(,\d\.\d+)*\)|P\(x(,x)*\)'
        match_obj = re.match(point_pattern, fn_args)
        if match_obj:
            print match_obj.group()


def main():
    """."""
    pass

if __name__ == "__main__":
    main()
