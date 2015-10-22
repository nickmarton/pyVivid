"""Interval class."""
from copy import deepcopy

class Interval(object):
    """Interval class."""

    def __init__(self, inf, sup):
        """Construct an Interval object."""

        #handle int Interval construction
        if isinstance(inf, int) and isinstance(sup, int):
            self._type = int
        #handle float Interval construction
        elif isinstance(inf, float) and isinstance(sup, float):
            self._type = float
        #handle long Interval construction
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
        Implement overloaded < operator for Interval. 

        [s1, s2](o1, o2)
        Return True when this Interval's supremum is less than other
        Interval's infimum.
        """

        return self._supremum < other._infimum

    def __le__(self, other):
        """
        Implement overloaded <= operator for Interval. 

        [s1,(o1, s2], o2)
        Return True when this Interval's supremum is strictly greater than
        other Interval's infimum, less than other Interval's supremum and this
        Interval's infimum is strictly less than other Interval's infimum.
        """

        c_inf = self._infimum < other._infimum
        c_sup = other._infimum <= self._supremum < other._supremum
        return c_inf and c_sup

    def __eq__(self, other):
        """Implement == for Interval objects."""
        c_type = self._type == other._type
        c_inf = self._infimum == other._infimum
        c_sup = self._supremum == other._supremum
        return c_type and c_inf and c_sup

    def __ge__(self, other):
        """
        Implement overloaded >= operator for Interval. 

        (s1,[o1, s2), o2]
        Return True when other Interval's infimum is strictly less than this
        Interval's infimum, other Interval supremum is less than this Interval's supremum
        """
        c_inf = other._infimum < self._infimum
        c_sup = self._infimum <= other._supremum < self._supremum
        return c_inf and c_sup

    def __gt__(self, other):
        """
        Implement overloaded > operator for Interval. 

        (o1, o2)[s1, s2]
        Return True when this Interval's infimum is strictly greater than other
        Interval's infimum.
        """
        return other._supremum < self._infimum

    def __ne__(self, other):
        """Implement != for Interval objects."""
        return not self.__eq__(other)

    def __or__(self, other):
        """Implement | operator for intervals (union)."""
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
        """Implement & operator for intervals (intersection)."""
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
        Determine if this Interval contains some {int,float,long} or another Interval.
        """

        #Check containership for another Interval (i.e. subset)
        if hasattr(key, "_is_Interval"):
            o_inf, o_sup = key._infimum, key._supremum
            if self._infimum <= o_inf and o_sup <= self._supremum:
                return True
            else:
                return False

        #raise error if type mismatch
        if type(key) != self._type:
            raise TypeError(
                "Cannot check if " + str(type(key)) + "is in " + 
                str(self._type) + " Interval")
        else:
            if self._infimum <= key <= self._supremum:
                return True
            else:
                return False

    def __getitem__(self, index):
        """
        Implement indexing for Interval.
        Just 0 or 1 accepted for infimum or supremum respectively.
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
        """Implement copy.deepcopy for Interval object."""
        return Interval(self._infimum, self._supremum)

    def _key(self):
        """Tuple key for hash function."""
        return (self._infimum, self._supremum)

    def __hash__(self):
        """Hash so sets can use Interval's."""
        return hash(self._key())

    def discretize(self, jump=None):
        """Return all values within range of this interval."""
        def frange(x, y, jump):
                """Get value in an inclusive range with step size of jump."""
                while x <= y:
                    yield x
                    x += jump   

        #if jump is provided, check if it's compatible with this Interval
        if jump:
            if type(jump) != int and type(jump) != float and type(jump) != long:
                raise TypeError(
                    "jump must be of type int, float, or long.")
            
            if type(jump) != self._type:
                raise TypeError(
                    "jump must be same type as Interval values.")
        #otherwise, set default jumps
        else:
            if self._type == int:
                jump = 1
            elif self._type == float:
                jump = 1.0
            else:
                jump = 1L

        return [i for i in frange(self._infimum, self._supremum, jump)]

    def __str__(self):
        """Human readable string for Interval object."""
        return "I(" + str(self._infimum) + ", " + str(self._supremum) + ")"

    def __repr__(self):
        """Machine representation of this Interval object."""
        return self.__str__()

    @staticmethod
    def collapse_intervals(intervals):
        """Collapse overlapping intervals."""
        #Ensure no bad input; only Intervals.
        if any([not hasattr(i, "_is_Interval") for i in intervals]):
            raise TypeError(
                "Only Intervals objects can be collapsed.")

        def can_collapse(lis):
            """Try to collapse some 2 Interval's returning True on success."""
            for i, interval_i in enumerate(lis):
                for j, interval_j in enumerate(lis):
                    #ignore when we're looking at the same Interval
                    if i == j:
                        continue
                    #if Interval i is subsumed by Interval j, get rid of it
                    if interval_i in interval_j:
                        lis.remove(interval_i)
                        return True
                    #if Intervals overlap, add them and remove old Intervals
                    elif interval_i <= interval_j:
                        lis.append(interval_i | interval_j)
                        lis.remove(interval_i)
                        lis.remove(interval_j)
                        return True

            return False

        #split intervals by type
        int_intervals = [i for i in intervals if i._type == int]
        float_intervals = [i for i in intervals if i._type == float]
        long_intervals = [i for i in intervals if i._type == long]

        #collapse Intervals for as long as posible
        while can_collapse(int_intervals): pass
        while can_collapse(float_intervals): pass
        while can_collapse(long_intervals): pass

        #recombine and send back
        output = int_intervals + float_intervals + long_intervals
        return output
