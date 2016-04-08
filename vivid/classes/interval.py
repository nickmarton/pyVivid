"""This section introduces the Interval class."""

from copy import deepcopy


class Interval(object):
    """
    Interval class. Intervals are over natural or real values.

    :ivar infimum: The infimum of the interval.
    :ivar supremum: The supremum of the interval.
    :ivar type: The type of the Interval object (int, float, or long).
    :ivar _is_Interval: An identifier to use in place of ``type`` or \
    ``isinstance``.
    """

    def __init__(self, inf, sup):
        """
        Construct an Interval object.

        :param inf: The value to use as the infimum of the Interval.
        :type  inf: int|float|long
        :param sup: The value to use as the supremum of the Interval.
        :type  sup: int|float|long

        :raises ValueError: The infimum must be strictly less than the \
        supremum.
        :raises TypeError: The infimum and supremum provided must be ints, \
        floats, or longs and their types must match.
        """

        # handle int Interval construction
        if isinstance(inf, int) and isinstance(sup, int):
            self._type = int
        # handle float Interval construction
        elif isinstance(inf, float) and isinstance(sup, float):
            self._type = float
        # handle long Interval construction
        elif isinstance(inf, long) and isinstance(sup, long):
            self._type = long
        else:
            raise TypeError(
                "infimum and supremum must both be type int, float, or long")

        if inf >= sup:
            raise ValueError("infimum must be strictly less than supremum")

        self._infimum = deepcopy(inf)
        self._supremum = deepcopy(sup)
        self._is_Interval = True

    def __lt__(self, other):
        """
        Overloaded ``<`` operator for Interval. Determine if the calling
        Interval is strictly less than another interval; that is, the supremum
        of the calling Interval is strictly less than the infimum of the
        Interval in ``other`` parameter:
        :math:`{(s_{inf}, s_{sup}) (o_{inf}, o_{sup})}`.
        """

        return self._supremum < other._infimum

    def __le__(self, other):
        """
        Overloaded ``<=`` operator for Interval. Determine if the calling
        Interval is less than another Interval; that is, the supremum of the
        calling Interval is greater than the Interval in ``other``'s infimum,
        less than the Interval in ``other``'s supremum and the infimum of the
        calling Interval is strictly less than the infimum of the Interval in
        ``other`` parameter:
        :math:`{(s_{inf}, (o_{inf}, s_{sup}), o_{sup})}`.
        """

        c_inf = self._infimum < other._infimum
        c_sup = other._infimum <= self._supremum < other._supremum
        return c_inf and c_sup

    def __eq__(self, other):
        """
        Determine if two Interval objects are equal via the ``==`` operator.
        """

        c_type = self._type == other._type
        c_inf = self._infimum == other._infimum
        c_sup = self._supremum == other._supremum
        return c_type and c_inf and c_sup

    def __ge__(self, other):
        """
        Overloaded ``>=`` operator for Interval. Determine if the calling
        Interval is greater than another Interval; that is, the infimum of the
        Interval in ``other`` parameter is strictly less than the calling
        Interval's infimum, and the supremum of the interval in ``other``
        parameter is less than the calling Interval's supremum:
        :math:`{(o_{inf}, (s_{inf}, o_{sup}), s_{sup})}`.
        """

        c_inf = other._infimum < self._infimum
        c_sup = self._infimum <= other._supremum < self._supremum
        return c_inf and c_sup

    def __gt__(self, other):
        """
        Overloaded ``>`` operator for Interval. Determine if the calling
        Interval is strictly greater than another interval; that is, the
        infimum of the calling Interval is strictly greater than the supremum
        of the Interval in ``other`` parameter:
        :math:`{(o_{inf}, o_{sup}) (s_{inf}, s_{sup})}`.
        """

        return other._supremum < self._infimum

    def __ne__(self, other):
        """
        Determine if two Interval objects are not equal via the ``!=``
        operator.
        """

        return not self.__eq__(other)

    def __or__(self, other):
        """
        Overloaded ``|`` operator; return the union of two Interval objects.

        :raises ValueError: Intervals must overlap to take the union.
        """

        if self <= other:
            return Interval(
                min(self._infimum, other._infimum),
                max(self._supremum, other._supremum))
        elif other <= self:
            return Interval(
                min(self._infimum, other._infimum),
                max(self._supremum, other._supremum))
        elif other in self:
            return deepcopy(self)
        elif self in other:
            return deepcopy(other)
        elif other == self:
            return deepcopy(self)
        else:
            raise ValueError(
                "Cannot add two non-overlapping Intervals")

    def __and__(self, other):
        """
        Overloaded ``&`` operator; return the intersection of two Interval
        objects.

        :raises ValueError: Intervals must overlap to take the intersection.
        """

        if self <= other:
            return Interval(
                max(self._infimum, other._infimum),
                min(self._supremum, other._supremum))
        elif other <= self:
            return Interval(
                max(self._infimum, other._infimum),
                min(self._supremum, other._supremum))
        elif other in self:
            return deepcopy(other)
        elif self in other:
            return deepcopy(self)
        elif other == self:
            return deepcopy(self)
        else:
            raise ValueError(
                "Cannot add two non-overlapping Intervals")

    def __contains__(self, key):
        """
        Determine if the calling Interval contains an int, float, long, or
        another Interval.

        :param key: The value to check for membership in the calling Interval.
        :type  key: int|float|long|Interval
        """

        #  Check containership for another Interval (i.e. subset)
        if hasattr(key, "_is_Interval"):
            o_inf, o_sup = key._infimum, key._supremum
            if self._infimum <= o_inf and o_sup <= self._supremum:
                return True
            else:
                return False

        #  not contained if type mismatch
        if type(key) != self._type:
            return False
        else:
            if self._infimum <= key <= self._supremum:
                return True
            else:
                return False

    def __getitem__(self, index):
        """
        Retrieve the infimum or supremum of the calling Interval via indexing
        (e.g. ``Interval[0]``).

        :raises IndexError: Index must be either "``0``" or "``1``".
        :raises TypeError: Index must be an ``int``.
        """
        if type(index) != int:
            raise TypeError("Index must be 0 or 1.")
        if index == 0:
            return self._infimum
        elif index == 1:
            return self._supremum
        else:
            raise IndexError(" Index must be 0 or 1.")

    def __deepcopy__(self, memo):
        """
        Deepcopy an Interval object via the ``copy.deepcopy`` method.
        """

        return Interval(self._infimum, self._supremum)

    def _key(self):
        """
        Private key function for hashing.

        :return: 2-tuple consisting of (infimum, supremum).
        :rtype: ``tuple``
        """

        return (self._infimum, self._supremum)

    def __hash__(self):
        """Hash implementation for set functionality of Interval objects."""
        return hash(self._key())

    def discretize(self, jump=None):
        """
        Return all values within the range of the calling interval.

        :param jump: The jump to use after each value. Defaults to ``1``, \
        ``1.0`` and ``1`` for int, float, and long Intervals respectively.
        :type  jump: None|int|float|long

        :return: A list of discrete values contained in the calling Interval \
        with a step size of ``jump``\.
        :rtype: ``list``

        :raises TypeError: If a jump is provided, it must be an ``int``, \
        ``float``, or ``long`` and match the type of the calling Interval.
        """

        def frange(x, y, jump):
                """Get value in an inclusive range with step size of jump."""
                while x <= y:
                    yield x
                    x += jump

        # if jump is provided, check if it's compatible with the calling Interval
        if jump:
            if type(jump) != int and type(jump) != float and type(jump) != long:
                raise TypeError(
                    "jump must be of type int, float, or long.")

            if type(jump) != self._type:
                raise TypeError(
                    "jump must be same type as Interval values.")
        # otherwise, set default jumps
        else:
            if self._type == int:
                jump = 1
            elif self._type == float:
                jump = 1.0
            else:
                jump = 1L

        return [i for i in frange(self._infimum, self._supremum, jump)]

    def __str__(self):
        """
        Return a readable string representation of the Interval object.
        """

        return "I(" + str(self._infimum) + ", " + str(self._supremum) + ")"

    def __repr__(self):
        """
        Return a string representation of the Interval object.
        """

        return self.__str__()

    @staticmethod
    def collapse_intervals(intervals):
        """
        Collapse a list of overlapping intervals.

        :param intervals: A list of intervals to collapse.
        :type  intervals: list

        :return: A new list of totally disjoint, collapsed Intervals.
        :rtype: ``list``

        :raises TypeError: ``interval`` parameter must be a ``list`` \
        containing only Interval objects.
        """

        def can_collapse(lis):
            """Try to collapse some 2 Interval's returning True on success."""
            for i, interval_i in enumerate(lis):
                for j, interval_j in enumerate(lis):
                    # ignore when we're looking at the same Interval
                    if i == j:
                        continue
                    # if Interval i is subsumed by Interval j, get rid of it
                    if interval_i in interval_j:
                        lis.remove(interval_i)
                        return True
                    # if Intervals overlap, add them and remove old Intervals
                    elif interval_i <= interval_j:
                        lis.append(interval_i | interval_j)
                        lis.remove(interval_i)
                        lis.remove(interval_j)
                        return True

            return False

        if not isinstance(intervals, list):
            raise TypeError("intervals must be a list")

        # Ensure no bad input; only Intervals.
        if any([not hasattr(i, "_is_Interval") for i in intervals]):
            raise TypeError(
                "Only Intervals objects can be collapsed.")

        # split intervals by type
        int_intervals = [i for i in intervals if i._type == int]
        float_intervals = [i for i in intervals if i._type == float]
        long_intervals = [i for i in intervals if i._type == long]

        # collapse Intervals for as long as posible
        while can_collapse(int_intervals): pass
        while can_collapse(float_intervals): pass
        while can_collapse(long_intervals): pass

        # recombine and send back
        output = int_intervals + float_intervals + long_intervals
        return output
