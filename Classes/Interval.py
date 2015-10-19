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
        c_sup = other._infimum < self._supremum < other._supremum
        return c_inf and c_sup

    def __eq__(self, other):
        """Implement == for Interval objects."""
        c_inf = self._infimum == other._infimum
        c_sup = self._supremum == other._supremum
        return c_inf and c_sup

    def __ge__(self, other):
        """
        Implement overloaded >= operator for Interval. 

        (o1,[s1, o2), s2]
        Return True when other Interval's infimum is strictly less than this
        Interval's infimum, other Interval supremum is less than this Interval's supremum
        """
        c_inf = other._infimum < self._infimum
        c_sup = self._infimum < other._supremum < self._supremum
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
        return self.__eq__(other)

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

    def __str__(self):
        """Human readable string for Interval object."""
        return "I(" + str(self._infimum) + ", " + str(self._supremum) + ")"

    def __repr__(self):
        """Machine representation of this Interval object."""
        return self.__str__()