"""This section introduces the PointParser class."""

import os
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from point import Point


class PointParser(object):
    """
    PointParser class. The PointParser class is used for parsing Point object
    related expressions.

    :ivar _is_Parser: An identifier to use in place of ``type`` or \
    ``isinstance``.
    """

    def __init__(self):
        """
        Construct a PointParser object.
        """

        self._is_Parser = True

    def __call__(self, *args):
        """
        Call PointParser object (e.g., ``PointParser(expression)``).
        """

        return self._eval(*args)

    def _eval(self, string):
        """
        Try to evaluate given string
        (e.g., "``is_on(P(2.0,2.0),P(1.0,1.0),P(3.0,3.0))``").

        :param string: The expression to evaluate; the PointParser object \
        unstringifies Point objects in ``string`` parameter and tries to call \
        a function of the Point object (also given by ``string`` parameter) \
        with unstringified Points as arguments.
        :type  string: ``str``

        :raises ValueError: Function provided in ``string`` parameter is not \
        a function in the Point class, some argument is not a Point after \
        trying to unstringify or the ``string`` parameter is improperly \
        formatted.
        """

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
        point_pattern = r'P\(-?\d\.\d+(,-?\d\.\d+)*\)|P\(x(,x)*\)'
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
