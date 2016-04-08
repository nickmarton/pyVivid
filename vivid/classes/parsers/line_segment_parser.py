"""This section introduces the LineSegmentParser class."""

import os
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from point import Point
from line_segment import LineSegment


class LineSegmentParser(object):
    """
    LineSegmentParser class. The PointParser class is used for parsing
    LineSegment object related expressions (some of which can involve Point
    objects).

    :ivar _is_Parser: An identifier to use in place of ``type`` or \
    ``isinstance``.
    """

    def __init__(self):
        """
        Construct a LineSegmentParser object.
        """

        self._is_Parser = True

    def __call__(self, *args):
        """
        Call LineSegmentParser object
        (e.g., ``LineSegmentParser(expression)``).
        """

        return self._eval(*args)

    def _eval(self, string):
        """
        Try to evaluate given string
        (e.g., "``is_on(P(2.0,2.0),P(1.0,1.0),P(3.0,3.0))``").

        :param string: The expression to evaluate; the LineSegmentParser \
        object unstringifies LineSegment and Point objects in ``string`` \
        parameter and tries to call a function of the LineSegment object \
        (also given by ``string`` parameter) with unstringified objects as \
        arguments.
        :type  string: ``str``

        :raises ValueError: Function provided in ``string`` parameter is not \
        a function in the LineSegment class, some argument is not a Point or \
        LineSegment after trying to unstringify or the ``string`` parameter \
        is improperly formatted.
        """

        fn_start, fn_end = string.find("("), string.rfind(")")
        fn_name, fn_args = string[:fn_start], string[fn_start + 1: fn_end]

        for fn in dir(LineSegment):
            if fn_name == fn:
                line_segment_function = getattr(LineSegment, fn)
                break
        else:
            raise ValueError("Function not contained in dir of Point")

        import re
        parsed_args = []
        line_segment_pattern = r'(L\(P\(-?\d\.\d+(,-?\d\.\d+)*\),P\(-?\d\.\d+(,-?\d\.\d+)*\)\)|P\(x(,x)*\),P\(x(,x)*\)\))|P\(-?\d\.\d+(,-?\d\.\d+)*\)|P\(x(,x)*\)'
        match_obj_iter = re.finditer(line_segment_pattern, fn_args)
        for match in match_obj_iter:
            if match.group()[0] == 'L':
                parsed_args.append(LineSegment.unstringify(match.group()))
            else:
                parsed_args.append(Point.unstringify(match.group()))
            fn_args = fn_args.replace(match.group(), '', 1)

        if not all([char == "," for char in fn_args]):
            raise ValueError("Only Point arguments acceptable")

        try:
            return line_segment_function(*parsed_args)
        except Exception, e:
            raise ValueError("Bad args provided")


def main():
    """."""
    pass

if __name__ == "__main__":
    main()
