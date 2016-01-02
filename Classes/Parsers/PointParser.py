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
        fn_start, fn_end = string.find("("), string.rfind(")")
        fn_name, fn_args = string[:fn_start], string[fn_start + 1: fn_end]

        for fn in dir(Point):
            if fn_name == fn:
                point_function = getattr(Point, fn)
                break
        else:
            raise ValueError("Function not contained in dir of Point")

        import re
        parsed_args = []
        point_pattern = r'P\(\d\.\d+(,\d\.\d+)*\)|P\(x(,x)*\)'
        match_obj_iter = re.finditer(point_pattern, fn_args)
        for match in match_obj_iter:
            parsed_args.append(Point.unstringify(match.group()))
            fn_args = fn_args.replace(match.group(), '', 1)

        if not all([char == "," for char in fn_args]):
            raise ValueError("Only Point arguments acceptable")

        try:
            return point_function(*parsed_args)
        except Exception, e:
            raise ValueError("Bad args provided")


def main():
    """."""
    pass

if __name__ == "__main__":
    main()
