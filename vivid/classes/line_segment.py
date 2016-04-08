"""This section introduces the LineSegment class."""

from point import Point


class LineSegment(object):
    """
    LineSegment class.
    Each LineSegment object represents a line segment in N\ :sub:`d` cartesian
    space. LineSegment objects are immutable.


    :ivar is_generic: Whether or not the LineSegment object is generic \
    (i.e., the set of coordinates have not been defined).
    :ivar start_point: The first endpoint of the LineSegment.
    :ivar end_point: The second endpoint of the LineSegment.
    :ivar dimension: The dimension of space the LineSegment object exists in.
    :ivar _is_LineSegment: An identifier to use in place of ``type`` or \
    ``isinstance``.
    """

    def __init__(self, start_point, end_point):
        """
        Construct a LineSegment object.

        :param start_point: The starting point of the LineSegment object.
        :type  start_point: Point
        :param end_point: The end point of the LineSegment object.
        :type  end_point: Point

        :raises ValueError: both ``start_point`` and ``end_point`` parameters \
        must be Point objects, agree on their gnerality, share the same \
        dimension and be unequal.
        """

        if not hasattr(start_point, "_is_Point") or \
                not hasattr(end_point, "_is_Point"):
            raise ValueError(
                "start_point and end_point parameters mustbe Point objects")

        if start_point._is_generic is not end_point._is_generic:
            raise ValueError("Both Points must be generic or not generic")

        if start_point._dimension is not end_point._dimension:
            raise ValueError("Both Points must be share the same dimension")

        from copy import deepcopy
        self._is_generic = start_point._is_generic
        self._start_point = deepcopy(start_point)
        self._end_point = deepcopy(end_point)
        self._dimension = start_point._dimension
        self._is_LineSegment = True

    def __eq__(self, other):
        """
        Determine if two LineSegment objects are equal via the ``==`` operator.
        """

        starts_equal = self._start_point == other._start_point
        ends_equal = self._end_point == other._end_point
        return starts_equal and ends_equal

    def __ne__(self, other):
        """
        Determine if two LineSegment objects are not equal via the ``!=``
        operator.
        """

        return not self.__eq__(other)

    def __ge__(self, other):
        """
        Overloaded ``>=`` operator for LineSegment object. Determine if the
        calling LineSegment object is a superset of the LineSegment object
        contained in ``other`` parameter where we view both LineSegment as a
        set of possible Point objects.
        """

        if self._dimension != other._dimension:
            return False

        if self._is_generic:
            return True
        if other._is_generic and not self._is_generic:
            return False

        start_cond = other[0].is_on(self[0], self[1])
        end_cond = other[1].is_on(self[0], self[1])

        return start_cond and end_cond

    def __gt__(self, other):
        """
        Overloaded ``>`` operator for LineSegment object. Determine if the
        calling LineSegment object is a strict superset of the LineSegment
        object contained in ``other`` parameter where we view both LineSegment
        as a set of possible Point objects.
        """

        if self._dimension != other._dimension:
            return False

        if self._is_generic and not other._is_generic:
            return True
        if self._is_generic and other._is_generic:
            return False

        start_cond = other[0].is_on(self[0], self[1])
        end_cond = other[1].is_on(self[0], self[1])
        strict_cond = self[0] != other[0] or self[1] != other[1]

        return start_cond and end_cond and strict_cond

    def __le__(self, other):
        """
        Overloaded ``<=`` operator for LineSegment object. Determine if the
        calling LineSegment object is a subset of the LineSegment object
        contained in ``other`` parameter where we view both LineSegment as a
        set of possible Point objects.
        """

        if self._dimension != other._dimension:
            return False

        if other._is_generic:
            return True
        if self._is_generic and not other._is_generic:
            return False

        start_cond = self[0].is_on(other[0], other[1])
        end_cond = self[1].is_on(other[0], other[1])

        return start_cond and end_cond

    def __lt__(self, other):
        """
        Overloaded ``<`` operator for LineSegment object. Determine if the
        calling LineSegment object is a strict subset of the LineSegment object
        contained in ``other`` parameter where we view both LineSegment as a
        set of possible Point objects.
        """

        if self._dimension != other._dimension:
            return False

        if other._is_generic and not self._is_generic:
            return True
        if other._is_generic and self._is_generic:
            return False

        start_cond = self[0].is_on(other[0], other[1])
        end_cond = self[1].is_on(other[0], other[1])
        strict_cond = self[0] != other[0] or self[1] != other[1]

        return start_cond and end_cond and strict_cond

    def __contains__(self, key):
        """
        Determine if a Point object or LineSegment object given in the ``key``
        parameter is on the calling LineSegment object via the ``in`` operator.

        :param key: The Point or LineSegment to check for membership in the \
        calling LineSegment.
        :type  key: Point  | LineSegment

        :raises TypeError: ``key`` parameter must be a Point or LineSegment \
        object.
        """

        if key._dimension != self._dimension:
            return False

        if hasattr(key, "_is_Point"):
            if self._is_generic:
                return True
            else:
                return key.is_on(self[0], self[1])

        if hasattr(key, "_is_LineSegment"):
            return key <= self

    def __deepcopy__(self, memo):
        """
        Deepcopy a LineSegment object via the ``copy.deepcopy`` method.
        """

        return LineSegment(self._start_point, self._end_point)

    def __getitem__(self, key):
        """
        Retrieve the :math:`i`\ th endpoint from a LineSegment object via
        indexing (e.g., ``LineSegment[i]``).

        :raises TypeError: ``key`` parameter must be an ``int``.
        :raises IndexError: ``key`` parameter must be either ``0`` or ``1``.
        """

        if type(key) != int:
            raise TypeError("indicies must be of type int")
        if key == 0:
            return self._start_point
        if key == 1:
            return self._end_point
        else:
            raise IndexError("Invalid index: " + str(key))

    def _key(self):
        """
        Private key function for hashing.

        :return: 2-tuple consisting of Point objects.
        :rtype: ``tuple``
        """

        return (self._start_point, self._end_point)

    def __hash__(self):
        """Hash implementation for set functionality of LineSegment objects."""
        return hash(self._key())

    def __str__(self):
        """
        Return a readable string representation of the LineSegment object.
        """

        return "L({},{})".format(self._start_point, self._end_point)

    def __repr__(self):
        """Return a string representation of the LineSegment object."""
        return self.__str__()

    @staticmethod
    def meets(point, line_1, line_2):
        """
        Determine if LineSegment objects given by the ``line_1`` and ``line_2``
        parameters meet at the Point object given by ``point`` parameter.

        :param point: The potential intersection point of the two LineSegment \
        objects.
        :type  point: Point
        :param line_1: The first LineSegment of the possible intersecting \
        pair of line segments.
        :type  line_1: LineSegment
        :param line_2: The second LineSegment of the possible intersecting \
        pair of line segments.
        :type  line_2: LineSegment
        """

        return point.meets(line_1[0], line_1[1], line_2[0], line_2[1])

    @staticmethod
    def unstringify(line_segment_string):
        """
        Reconstruct a LineSegment object from its string representation.

        :return: LineSegment object reconstructed from string representation.
        :rtype: LineSegment

        :raises ValueError: The string must match the form given by \
        ``str(LineSegment)`` or ``repr(LineSegment)``.
        """

        try:
            end_points = line_segment_string[2:-1].split(',P')
            start_point, end_point = end_points[0], "P" + end_points[1]
            return LineSegment(Point.unstringify(start_point),
                               Point.unstringify(end_point))
        except ValueError:
            raise ValueError(
                "line_segment_string must be of form str(LineSegment)")
        except TypeError:
            raise ValueError(
                "line_segment_string must be of form str(LineSegment)")


def main():
    """."""

    l1 = LineSegment(Point(1.0, 1.0), Point(2.0, 2.0))
    l2 = LineSegment(Point(1.0, 0.4, -112.2, 2.0), Point(1.0, 2.0, 4.5, 55.4))
    l3 = LineSegment(Point(0.0, 0.0), Point(3.0, 3.0))
    l4 = LineSegment(Point(0.0, 0.0), Point(2.0, 2.0))
    l5 = LineSegment(Point(1.0, 1.0), Point(3.0, 3.0))

    assert l1 not in l2
    assert l1 in l3
    assert l1 in l4
    assert l1 in l5
    assert l3 not in l1
    assert l4 not in l1
    assert l5 not in l1

    assert not l1 < l2
    assert not l1 <= l2
    assert not l1 >= l2
    assert not l1 > l2

    assert l1 <= l1
    assert not l1 < l1
    assert l1 >= l1
    assert not l1 > l1

    assert l1 <= l3
    assert l1 < l3
    assert l1 <= l4
    assert l1 < l4
    assert l1 <= l5
    assert l1 < l5
    assert not l1 >= l3
    assert not l1 > l3
    assert not l1 >= l4
    assert not l1 > l4
    assert not l1 >= l5
    assert not l1 > l5

    l6 = LineSegment(Point('x', 'x'), Point('x', 'x'))

if __name__ == "__main__":
    main()
