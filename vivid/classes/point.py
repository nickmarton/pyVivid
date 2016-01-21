"""point module."""


class Point(object):
    """
    Point class.
    Point objects represent a point of N\ :sub:`d` cartesian space. Point
    objects are immutable.

    :ivar is_generic: Whether or not the Point object is generic \
    (i.e., the coordinates have not been defined).
    :ivar coordinate: The coordinate of the Point object.
    :ivar dimension: The dimension of space the Point object exists in.
    :ivar _is_Point: An identifier to use in place of ``type`` or \
    ``isinstance``.
    """

    def __init__(self, *coordinates):
        """
        Construct a Point object.

        :param coordinates: The values to use as the coordinates of the \
        Point object. At least one coordinate must be provided; \
        to create a generic point object, pass values of ``\"x\"``.
        :type  coordinates: strs|floats

        :raises ValueError: At least one coordinate must be provided.
        :raises TypeError: All cooridnates must be either strings \
        (equal to ``\"x\"``) or floats.
        """

        # assert that point is at least one dimensional
        if not coordinates:
            raise ValueError("Point must be at least 1-D")

        # check if each dimension is a float and grab longest decimal precision
        generic_flag = True
        for x_i in coordinates:
            if not isinstance(x_i, str) or not x_i == 'x':
                generic_flag = False

        if not generic_flag:

            longest_precision = 0

            for x_i in coordinates:
                if not isinstance(x_i, float):
                    raise TypeError(
                        'values for dimensions must all be of type float or x')

        self._is_generic = generic_flag
        self._coordinate = tuple(coordinates)
        self._dimension = len(coordinates)
        self._is_Point = True

    def __eq__(self, other):
        """
        Determine if two Point objects are equal via the ``==`` operator.
        """

        return self._coordinate == other._coordinate

    def __ne__(self, other):
        """
        Determine if two Point objects are not equal via the ``!=`` operator.
        """

        return not self.__eq__(other)

    def __deepcopy__(self, memo):
        """
        Deepcopy a Point object via the ``copy.deepcopy`` method.
        """

        return Point(*self._coordinate)

    def _key(self):
        """
        Private key function for hashing.

        :return: :math:`d`\ -tuple consisting of coordinates.
        :rtype: ``tuple``
        """

        return self._coordinate

    def __getitem__(self, key):
        """
        Retrieve the :math:`i`\ th cooridinate from a Point object via
        indexing (e.g., ``Point[i]``).

        :raises TypeError: ``key`` parameter must be an ``int``.
        :raises IndexError: ``key`` parameter must be within the set \
        :math:`\{0, \ldots, d\}` where :math:`d` is the dimension of the \
        Point object.
        """

        if type(key) != int:
            raise TypeError("indicies must be of type int")
        if key in range(self._dimension):
            return self._coordinate[key]
        else:
            raise IndexError("Invalid index: " + str(key))

    def __hash__(self):
        """Hash implementation for set functionality of Point objects."""
        return hash(self._key())

    def __str__(self):
        """
        Return a readable string representation of the Point object.
        """

        point_string = 'P(' + ''.join(
            [str(x_i) + ',' for x_i in self._coordinate])[:-1] + ')'

        return point_string

    def __repr__(self):
        """
        Return a string representation of the Point object.
        """

        point_string = 'P(' + ''.join(
            [str(x_i) + ',' for x_i in self._coordinate])[:-1] + ')'

        return point_string

    def is_on(self, endpoint_1, endpoint_2):
        """
        Determine if the calling Point object lies on line segment defined by
        the endpoint Point objects provided in the ``endpoint_1`` and
        ``endpoint_2`` parameters.

        :raises ValueError: The calling Point object and the Point objects in \
        the ``endpoint_1`` and ``endpoint_2`` parameters must all be in the \
        same dimension of space and no Point object involved can be generic.

        :return: Whether or not the calling Point object lies on the line \
        segment.
        :rtype: ``bool``
        """

        def distance(p1, p2):
            from math import sqrt
            return sqrt(
                sum([(p1[i] - p2[i]) ** 2 for i in range(self._dimension)]))

        def is_between(p1, p2, p3):
            epsilon = .000000000000001
            delta = (distance(p1, p2) + distance(p1, p3)) - distance(p2, p3)
            return - epsilon < delta < epsilon

        if self._is_generic or endpoint_1._is_generic or endpoint_2._is_generic:
            raise ValueError("Coordinates for each point must be specified")

        # Enforce all points being of same dimension
        endpoints_dim_flag = endpoint_1._dimension == endpoint_2._dimension
        if not endpoints_dim_flag:
            raise ValueError("Endpoints must be of same dimension")

        if self._dimension != endpoint_1._dimension:
            raise ValueError("point must be of same dimension as endpoints")

        return is_between(self, endpoint_1, endpoint_2)

    def not_same_point(self, other):
        """
        Determine if the calling Point object and the Point object contained in
        ``other`` parameter are not the same.

        :return: Whether or not the calling Point object is unequal to the \
        Point object in ``other`` parameter.
        :rtype: ``bool``
        """

        return self.__ne__(other)

    def clocks_unequal(self, other):
        """
        Determine if the clocks of two spacetime locations are unequal
        wherein the last coordinate of each represents time.

        :return: Whether or not the calling Point object's last coordinate is \
        equal to the last coordinate of the Point object in ``other`` \
        parameter.
        :rtype: ``bool``

        :raises ValueError: Dimensions of the Point object contained in \
        ``other`` parameter and the calling Point must match.
        """

        if self._dimension != other._dimension:
            raise ValueError("dimensions must match")

        return self._coordinate[-1] != other._coordinate[-1]

    def can_observe(self, spacetime_loc, worldline_start, worldline_end):
        """
        Determine if the calling Point object can observe the spacetime
        location represented by the Point object in ``spacetime_loc`` parameter
        on the worldline segment determined by the Point objects in
        ``worldline_start`` and ``worldline_end`` parameters.

        :return: Whether or not the calling Point object can observe \
        ``spacetime_loc`` through the worldine defined by the Point objects \
        in the ``worldline_start`` and ``worldline_end`` parameters.
        :rtype: ``bool``
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
        Determine if the worldline segments defined by the Point objects in the
        ``worldline_1_start`` and ``worldline_1_end`` parameters and the
        ``worldline_2_start`` and ``worldline_2_end`` parameters meet at
        the calling Point object's coordinates.

        :return: Whether or not worldines meet at the calling Point object's \
        coordinates.
        :rtype: ``bool``

        :raises ValueError: All Point objects must have the same dimension \
        and cannot be generic.
        """

        sp_on_m1 = self.is_on(worldline_1_start, worldline_1_end)
        sp_on_m2 = self.is_on(worldline_2_start, worldline_2_end)

        if sp_on_m1 and sp_on_m2:
            return True
        else:
            return False

    @staticmethod
    def unstringify(point_string):
        """
        Reconstruct a Point object from its string representation.

        :return: Point object reconstructed from string representation.
        :rtype: Point

        :raises ValueError: The string must match the form given by \
        ``str(Point)`` or ``repr(Point)``, i.e., \
        :math:`P(c_{1}, \ldots, c_{d})`.
        """

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
