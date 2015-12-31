"""Point class."""


class Point(object):
    """
    Class to represent a point of N-D cartesian space.

    Point object is immutable.
    """

    def __init__(self, *dimension_values):
        """Initialize a Point object."""

        # assert that point is at least one dimensional
        if not dimension_values:
            raise ValueError("Point must be at least 1-D")

        # check if each dimension is a float and grab longest decimal precision
        generic_flag = True
        for x_i in dimension_values:
            if not isinstance(x_i, str) or not x_i == 'x':
                generic_flag = False

        if not generic_flag:

            longest_precision = 0

            for x_i in dimension_values:
                if not isinstance(x_i, float):
                    raise TypeError(
                        'values for dimensions must all be of type float or x')

        self._generic = generic_flag
        self._coordinate = tuple(dimension_values)
        self._dimension = len(dimension_values)
        self._is_Point = True

    def __eq__(self, other):
        """Implement == operator for Point object."""
        return self._coordinate == other._coordinate

    def __ne__(self, other):
        """Implement != operator for Point object."""
        return not self.__eq__(other)

    def __deepcopy__(self, memo):
        """Implement copy.deepcopy for Point object."""
        return Point(*self._coordinate)

    def _key(self):
        """Tuple key for hash function."""
        return self._coordinate

    def __hash__(self):
        """Hash so sets can use Interval's."""
        return hash(self._key())

    def __str__(self):
        """Return a readable Point."""

        point_string = 'P(' + ''.join(
            [str(x_i) + ',' for x_i in self._coordinate])[:-1] + ')'

        return point_string

    def __repr__(self):
        """Return a unambiguous Point."""

        point_string = 'P(' + ''.join(
            [str(x_i) + ',' for x_i in self._coordinate])[:-1] + ')'

        return point_string

    @staticmethod
    def unstringify(point_string):
        """Reconstruct a Point object from its string representation."""
        try:
            coordinates = point_string[2:-1].split(',')
            if all([coord == 'x' for coord in coordinates]):
                return Point(*coordinates)
            else:
                return Point(*[float(coord) for coord in coordinates])
        except ValueError:
            raise ValueError("String must be of form P('x') or P('x','x')")
        except TypeError:
            raise ValueError("String must be of form P('x') or P('x','x')")
