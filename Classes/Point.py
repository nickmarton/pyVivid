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

        self._is_generic = generic_flag
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

    def __getitem__(self, key):
        """implement indexing for Point object."""
        if type(key) != int:
            raise TypeError("indicies must be of type int")
        if key in range(self._dimension):
            return self._coordinate[key]
        else:
            raise IndexError("Invalid index: " + str(key))

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

    def is_on(self, endpoint_1, endpoint_2):
        """
        Determine if this Point object lies on line segment defined by the
        endpoint Point objects provided in endpoint_1 and endpoint_2.
        """

        def distance(p1, p2):
            from math import sqrt
            return sqrt(
                sum([(p1[i] - p2[i]) ** 2 for i in range(self._dimension)]))

        def is_between(p1, p2, p3):
            epsilon = .000000001
            delta = (distance(p1, p2) + distance(p1, p3)) - distance(p2, p3)
            return - epsilon < delta < epsilon

        # Enforce all points being of same dimension
        endpoints_dim_flag = endpoint_1._dimension == endpoint_2._dimension
        if not endpoints_dim_flag:
            raise ValueError("Endpoints must be of same dimension")

        if self._dimension != endpoint_1._dimension:
            raise ValueError("point must be of same dimension as endpoints")

        return is_between(self, endpoint_1, endpoint_2)

    def not_same_point(self, other):
        """Wrapper for __ne__ so parser can evaluate."""
        return self.__ne__(other)

    def clocks_unequal(self, other):
        """
        Determine if the clocks of two spacetime locations are unequal;
        this function assumes we're dealing with either 2D or 4D points
        wherein the last dimension represents time
        """

        if self._dimension != other._dimension:
            raise ValueError("dimensions must match")

        if self._dimension != 2 and self._dimension != 4:
            raise ValueError("dimensions must be either 2 or 4")

        return self._coordinate[-1] != other._coordinate[-1]

    def can_observe(self, spacetime_loc, worldline_start, worldline_end):
        """
        Determine if this Point can observe spacetime_loc on worldline segment
        determined by worldline_start-worldline_end.
        """

        p1_on_l = self.is_on(worldline_start, worldline_end)
        p2_on_l = spacetime_loc.is_on(worldline_start, worldline_end)

        # if they're both on the same worldine, then observes holds
        both_on_same_worldline = p1_on_l and p2_on_l

        # if the p1 and p2 are the same location or both on the same worldline,
        # then p1 and p2 are observable from one another
        if self == spacetime_loc or both_on_same_worldline:
            return True
        else:
            return False

    def meets(self, worldline_1_start, worldline_1_end, worldline_2_start,
              worldline_2_end):
        """
        Determine if worldline segments defined by
        worldline_1_start-worldline_1_end and worldline_2_start-worldline_2_end
        meet at this Point objects location.
        """

        sp_on_m1 = self.is_on(worldline_1_start, worldline_1_end)
        sp_on_m2 = self.is_on(worldline_2_start, worldline_2_end)

        if sp_on_m1 and sp_on_m2:
            return True
        else:
            return False

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
