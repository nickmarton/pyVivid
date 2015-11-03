"""Point class."""

class Point(object):
    """
    Class to represent a point of N-D cartesian space.

    Point object is immutable.
    """

    def __init__(self, *dimension_values):
        """Initialize a Point object."""

        #assert that point is at least one dimensional
        if not dimension_values:
            raise ValueError("Point must be at least 1-D")

        #check if each dimension is a float and grab longest decimal precision
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
        """
        Return a boolean for whether or not this Point is equal 
        to other Point.
        """

        #simple equality suffices as coordinate is ordered

        if self.get_coordinate() == other.get_coordinate():
            return True
        else:
            return False

    def __ne__(self, other):
        """
        Return a boolean for whether or not this Point is not equal to
        other Point
        """

        #simple equality suffices as coordinate is ordered

        if self.get_coordinate() == other.get_coordinate():
            return False
        else:
            return True

    def __deepcopy__(self, memo):
        """Implement copy.deepcopy for Point object."""
        return Point(*self._coordinate)

    def _key(self):
        """Tuple key for hash function."""
        return self._coordinate

    def __hash__(self):
        """Hash so sets can use Interval's."""
        return hash(self._key())

    def is_generic(self):
        """Return whether or not this Point is generic."""

        return self._generic

    def get_dimension(self):
        """Return this Point's dimension."""

        return self._dimension

    def get_coordinate(self):
        """Return this Point's coordinate."""

        return self._coordinate

    def __str__(self):
        """Return a readable Point."""

        point_string = 'P(' + ''.join(
            [str(x_i) + ',' for x_i in self.get_coordinate()])[:-1] + ')'
        
        return point_string

    def __repr__(self):
        """Return a unambiguous Point."""

        point_string = 'P(' + ''.join(
            [str(x_i) + ',' for x_i in self.get_coordinate()])[:-1] + ')'
        
        return point_string
