"""
valueset module.

Supports any object provided they implement
``__deepcopy__``, ``__eq__``, ``__str__``, ``__hash__``,
and provide a parser for truth value evaluation.
Additionally, ``__le__`` in ValueSet class must be extended to support the
object if the object uses a non-standard form of equality,
(e.g. Point objects are subset of generic Point of same dimension).
"""

# Known issues
# Subset does not test that an interval exists in discrete form in other

from copy import deepcopy
from functools import total_ordering
from interval import Interval
from point import Point


@total_ordering
class ValueSet(object):
    """
    ValueSet class.

    The ValueSet class uses the ``total_ordering`` decorator so strict
    subsets, supersets and strict supersets are also available via the ``<``,
    ``>=``, and ``>`` operators respectively, despite the lack of magic
    functions for them.

    :cvar _base_types: The literal types supported by the ValueSet class.
    :cvar _object_types: The object types supported by the ValueSet class.
    :ivar values: The values contained in the ValueSet object.
    :ivar _is_ValueSet: An identifier to use in place of type or isinstance.
    """

    _base_types = [int, float, long, str, bool]
    _object_types = ["_is_Interval", "_is_Point"]

    @classmethod
    def add_object_type(cls, object_identifier):
        """
        Add compatibility for an object to the ValueSet class.
        This is part of the vivid object extension protocol.

        :param object_identifier: The identifier used by each instance of a \
        class. This must be of the form: \"_is_Object\" \
        (e.g. ``_is_Point`` or ``_is_Interval``).
        :type  object_identifier: str
        """
        # Ensure object identifiers are strings
        if not isinstance(object_identifier, str):
            raise TypeError("Object identifier's must be strings")

        # Ensure they have the correct form
        import re
        if not re.match("_is_[A-Za-z]", object_identifier):
            raise ValueError(
                "object identifier must be of form _is_[object name]")

        # Add id to list of id's if it's not a duplicate
        if object_identifier not in cls._object_types:
            cls._object_types.append(object_identifier)

    def __init__(self, valueset):
        """
        Construct a ValueSet object.

        :param valueset: The values to place in the ValueSet object. These \
        values are passed through the ``_parse`` function before being stored.
        :type  valueset: list|set

        :raises TypeError: ``valueset`` parameter must be a python ``list`` \
        or ``set``.
        """

        if not isinstance(valueset, list) and not isinstance(valueset, set):
            raise TypeError("valueset parameter must be of type list or set")
        # Save parsed output
        self._values = ValueSet._parse(valueset)
        self._is_ValueSet = True

    def __eq__(self, other):
        """
        Determine if two ValueSet objects are equal via the ``==`` operator.
        """

        union = set(self._values) | set(other._values)
        intersection = set(self._values) & set(other._values)
        return union == intersection

    def __le__(self, other):
        """
        Overloaded ``<=`` operator for ValueSet object. Determine if this
        ValueSet object is a subset of the ValueSet object contained in
        ``other`` parameter.
        """

        self_dict = ValueSet._split_by_types(self)
        other_dict = ValueSet._split_by_types(other)

        # filter out ints, floats, or longs contained in any Interval in other
        filtered_self_values = []
        for _type, values in self_dict.iteritems():
            # Handle Interval related stuff
            if _type == int or _type == float or _type == long or \
                    _type == "_is_Interval":
                for value in values:
                    for interval in other_dict['_is_Interval']:
                        if value in interval:
                            break
                    else:
                        filtered_self_values.append(value)
            # Handle point related stuff; speicfically handled hear for
            # generic point support
            elif _type == "_is_Point":
                for value in values:
                    for point in other_dict["_is_Point"]:
                        if value._dimension == point._dimension:
                            if value == point or point._is_generic:
                                break
                    else:
                        return False
            else:
                filtered_self_values.extend(values)

        # At this point, only objects, str, and bool can be in new_self_values
        new_self_values = ValueSet(filtered_self_values)

        if len(new_self_values) > len(other._values):
            return False

        # if the intersection of both ValueSets is the same as this ValueSet
        # then this ValueSet is contained in other and is a subset.
        intersection = set(new_self_values) & set(other._values)
        return intersection == set(new_self_values)

    def __ne__(self, other):
        """
        Determine if two ValueSet objects are equal via the ``!=`` operator.
        """

        return not self.__eq__(other)

    def __add__(self, other):
        """
        Overloaded ``+`` operator for ValueSet. Take the union of two ValueSets
        or add a single element to this Valueset. If adding an object, the
        object must be within ``_object_types``.
        """

        if hasattr(other, "_is_ValueSet"):
            return ValueSet(self._values + other._values)

        try:
            other_values = [v for v in iter(other)]
            return ValueSet(self._values + other_values)
        except:
            new_values = self._values
            new_values.append(other)
            return ValueSet(new_values)

    def __iadd__(self, other):
        """
        Overloaded ``+=`` for ValueSet. Take the union of two ValueSets
        or add a single element to this Valueset. If adding an object, the
        object must be within ``_object_types``.
        """

        return self.__add__(other)

    def __sub__(self, other):
        """
        Overloaded ``-`` operator for ValueSet. This functions as the
        set-theoretic difference.
        """

        def resolve_intervals(intervals, other_type_lists):
            """
            Break intervals up according to corresponding types of
            non-iterables (int, long, float) in other.
            """

            def resolve_interval_interval(self, other, self_danglers,
                                          other_danglers, diff):
                """
                Break down a set of intervals according to another set of
                intervals.
                Use differential diff provided when splitting intervals.
                """

                for i, self_interval in enumerate(self):
                    for j, other_interval in enumerate(other):

                        other_inf = other_interval[0]
                        other_sup = other_interval[1]
                        self_inf = self_interval[0]
                        self_sup = self_interval[1]

                        if other_interval <= self_interval:
                            # split both,removing overlap
                            try:
                                new_self = Interval(other_sup + diff, self_sup)
                                self.append(new_self)
                            except ValueError:
                                self_danglers.append(self_sup)
                            try:
                                new_other = Interval(other_inf,
                                                     self_inf - diff)
                                other.append(new_other)
                            except ValueError:
                                other_danglers.append(other_inf)
                            del self[i]
                            del other[j]
                            return True
                        elif self_interval <= other_interval:
                            # split both, removing overlap
                            try:
                                new_self = Interval(self_inf, other_inf - diff)
                                self.append(new_self)
                            except ValueError:
                                self_danglers.append(self_inf)
                            try:
                                new_other = Interval(self_sup + diff,
                                                     other_sup)
                                other.append(new_other)
                            except ValueError:
                                other_danglers.append(other_sup)
                            del self[i]
                            del other[j]
                            return True
                        elif other_interval in self_interval:
                            # split self_interval and destroy other, this is
                            # the only case where we don't keep danglers
                            try:
                                new_l_self = Interval(self_inf,
                                                      other_inf - diff)
                                self.append(new_l_self)
                            except ValueError:
                                if self_inf == other_inf - diff:
                                    self_danglers.append(self_inf)
                            try:
                                new_h_self = Interval(other_sup + diff,
                                                      self_sup)
                                self.append(new_h_self)
                            except ValueError:
                                if other_sup + diff == self_sup:
                                    self_danglers.append(self_sup)
                            del self[i]
                            del other[j]
                            return True

                return False

            def resolve_interval_singletons(self, other, danglers, diff):
                """
                Break down a set of intervals according to a set of singletons.
                Use differential diff provided when splitting intervals.
                """

                for i, self_interval in enumerate(self):
                    for j, other_signleton in enumerate(other):

                        self_inf = self_interval[0]
                        self_sup = self_interval[1]

                        if other_signleton in self_interval:
                            if other_signleton == self_inf:
                                try:
                                    new_self = Interval(self_inf + diff,
                                                        self_sup)
                                    self.append(new_self)
                                except ValueError:
                                    danglers.append(self_sup)
                                del self[i]
                                del other[j]
                                return True
                            elif other_signleton == self_sup:
                                try:
                                    new_self = Interval(self_inf,
                                                        self_sup - diff)
                                    self.append(new_self)
                                except ValueError:
                                    danglers.append(self_inf)
                                del self[i]
                                del other[j]
                                return True
                            else:
                                try:
                                    new_l_self = Interval(
                                        self_inf, other_signleton - diff)
                                    self.append(new_l_self)
                                except ValueError:
                                    danglers.append(self_inf)
                                try:
                                    new_h_self = Interval(
                                        other_signleton + diff, self_sup)
                                    self.append(new_h_self)
                                except ValueError:
                                    danglers.append(self_sup)
                                del self[i]
                                del other[j]
                                return True

                return False

            self_danglers, other_danglers = [], []

            if intervals:
                # Split intervals by types
                int_Intervals = [i for i in intervals if i._type is int]
                long_Intervals = [i for i in intervals if i._type is long]
                float_Intervals = [i for i in intervals if i._type is float]

                # Split other type list into numerics and intervals
                other_ints = other_type_lists[int]
                other_longs = other_type_lists[long]
                other_floats = other_type_lists[float]
                other_intervals = other_type_lists["_is_Interval"]
                other_int_Intervals = [
                    i for i in other_intervals if i._type is int]
                other_long_Intervals = [
                    i for i in other_intervals if i._type is long]
                other_float_Intervals = [
                    i for i in other_intervals if i._type is float]

                # Note: at this point, all intervals are guarenteed to be
                # disjoint from collapse_intervals.

                # Break intervals apart until its impossible to keep breaking
                # them, then remove any singletons
                if int_Intervals:
                    while resolve_interval_interval(int_Intervals,
                                                    other_int_Intervals,
                                                    self_danglers,
                                                    other_danglers,
                                                    diff=1):
                            pass

                    # push dangling ints in other into other_ints, then reset
                    # other_danglers
                    other_ints.extend(other_danglers)
                    other_danglers = []

                    while resolve_interval_singletons(
                            int_Intervals, other_ints, self_danglers, diff=1):
                            pass

                if long_Intervals:
                    while resolve_interval_interval(long_Intervals,
                                                    other_long_Intervals,
                                                    self_danglers,
                                                    other_danglers,
                                                    diff=1L):
                            pass

                    # push dangling longs in other into other_longs, then reset
                    # other_danglers
                    other_longs.extend(other_danglers)
                    other_danglers = []

                    while resolve_interval_singletons(long_Intervals,
                                                      other_longs,
                                                      self_danglers,
                                                      diff=1L):
                            pass

                f_min = 0.00000000001
                if float_Intervals:
                    while resolve_interval_interval(float_Intervals,
                                                    other_float_Intervals,
                                                    self_danglers,
                                                    other_danglers,
                                                    diff=f_min):
                            pass

                    # push dangling floats in other into other_floats, then
                    # reset other_danglers
                    other_floats.extend(other_danglers)
                    other_danglers = []

                    while resolve_interval_singletons(float_Intervals,
                                                      other_floats,
                                                      self_danglers,
                                                      diff=f_min):
                            pass

                intervals = int_Intervals + long_Intervals + float_Intervals

                return intervals, self_danglers
            else:
                return intervals, self_danglers

        # Split the members of ValueSet's into lists defined by their
        # respective types
        self_type_lists = ValueSet._split_by_types(self._values)
        other_type_lists = ValueSet._split_by_types(other._values)

        from collections import defaultdict
        std_type_lists = defaultdict(list)

        for type_key, values in self_type_lists.iteritems():
            try:
                other_values = other_type_lists[type_key]
                diff = set(values) - set(other_values)
                std_type_lists[type_key] = diff
            except KeyError:
                std_type_lists[type_key] = values

        output_set = []

        # Break intervals if necessary and add any danglers to output_set
        std_type_lists["_is_Interval"], danglers = resolve_intervals(
            std_type_lists["_is_Interval"], other_type_lists)
        output_set.extend(danglers)

        # reconstruct list, sorting when possible
        for base_type in ValueSet._base_types:
            output_set += sorted(std_type_lists[base_type])
        for object_type in ValueSet._object_types:
            output_set += std_type_lists[object_type]

        return ValueSet(output_set)

    def __getitem__(self, key):
        """
        Retrive the value located at the index given by ``key`` parameter via
        indexing (e.g. ``ValueSet[key]``).

        :param key: The index to use for retrieval.
        :type  key: int

        :raises IndexError: ``key`` index must be in \
        {0,\ :math:`\ldots`, *n*-1} where *n* is the number of values \
        contained in the ValueSet object.
        :raises TypeError: ``key`` must be an int.
        """

        if type(key) != int:
            raise TypeError("indicies must be of type int")
        if key in range(len(self._values)):
            return self._values[key]
        else:
            raise IndexError("Invalid index: " + str(key))

    def __contains__(self, key):
        """
        Overloaded ``in`` operator for ValueSet. Determine if a value is
        contained in this ValueSet object.

        :param key: the item to test for membership in this ValueSet.
        """

        for value in self:
            try:
                is_equal = key == value
                if is_equal:
                    return True
            except AttributeError:
                pass
        return False

    def __len__(self):
        """
        Determine the length of a ValueSet object via the ``len`` built-in
        function e.g.(``len(ValueSet)``).
        """

        return len(self._values)

    def __iter__(self):
        """
        Provides an iterator for ValueSet
        (e.g. \"``for value in ValueSet:``\").
        """

        for value in self._values:
            yield value

    def __setitem__(self, key, value):
        """
        Assign a value in ``value`` parameter to a ValueSet object at the index
        given by ``key`` parameter (e.g. ``ValueSet[key] = value``).

        :param key: The index to use for assignment.
        :type  key: int
        :param value: The value to assign at index given by ``key``.

        :raises AttributeError: An invalid/unsupported object is given as \
        ``value`` parameter.
        :raises IndexError: ``key`` index must be in {0,\ :math:`\ldots`, *n*-1} \
        where *n* is the number of values contained in the ValueSet object.
        :raises TypeError: ``key`` must be an int.
        :raises ValueError: Duplicate values are not allowed in a ValueSet.
        """

        if type(key) != int:
            raise TypeError("indicies must be of type int")
        # ensure value is not a duplicate
        if value in self:
            raise ValueError("Duplicate values not permitted in ValueSet.")
        if key in range(len(self._values)):
            # if simple type, replace item at index with value
            if type(value) in ValueSet._base_types:
                self._values[key] = value
                return

            # not simple type, check if it's a valid object type
            identifier = None
            for object_identifier in ValueSet._object_types:
                if hasattr(value, object_identifier):
                    if identifier:
                        raise AttributeError(
                            "Any object passed must have only 1 "
                            "supported identifier")
                    identifier = object_identifier
            if identifier:
                self._values[key] = value
                return
        else:
            raise IndexError("Invalid index: " + str(key))

    def __nonzero__(self):
        """
        Determine if a ValueSet is falsy
        (e.g. ``if ValueSet`` or ``if not ValueSet``).
        """

        if self._values:
            return True
        else:
            return False

    def __deepcopy__(self, memo):
        """
        Deepcopy a ValueSet object via the ``copy.deepcopy`` method.
        """

        return ValueSet(deepcopy(self._values))

    def __str__(self):
        """
        Return a readable string representation of a ValueSet object with the
        following form: \"V(v\ :sub:`1`\ , :math:`\ldots` ,v\ :sub:`n`\)\".
        """

        return "V(" + ', '.join([str(i) for i in self._values]) + ")"

    def __repr__(self):
        """
        Return a string representation of a ValueSet object with the
        following form: \"V(v\ :sub:`1`\ , :math:`\ldots` ,v\ :sub:`n`\)\".
        """

        return self.__str__()

    @staticmethod
    def _split_by_types(values):
        """
        Split an iterable object by the types of elements within it and return
        a defaultdict where keys are the types composing the iterable object
        and the values are lists of the values of the iterable object falling
        into those types.

        :param values: An iterable object to split.
        :type  values: list|set|ValueSet|...

        :return: defaultdict of lists where keys correspond to \
        ``ValueSet._base_type`` and ``ValueSet._object_types`` present in \
        ``values`` parameter.
        :rtype: ``defaultdict(list)``

        :raises AttributeError: Only objects contianing a single identifier \
        in ``_object_types`` are supported.
        :raises TypeError: An invalid type exists in the iterable object.
        """

        # initialize a dictionary to separate types
        from collections import defaultdict
        type_lists = defaultdict(list)

        # for each value provided
        for value in values:
            # if it's a base type, simply add to it's corresponding list
            # while rejecting duplicates.
            if type(value) in ValueSet._base_types:
                if value not in type_lists[type(value)]:
                    type_lists[type(value)].append(value)
                continue

            # if it's an object type, check to see if it is in supported
            # object types
            identifier = None
            for object_identifier in ValueSet._object_types:
                if hasattr(value, object_identifier):
                    # Ensure no object has 2 identifiers
                    if identifier:
                        raise AttributeError(
                            "Any object passed must have only 1 "
                            "supported identifier")
                    identifier = object_identifier

            # store object in its corresponding list if it's not a duplicate
            if identifier:
                if value not in type_lists[identifier]:
                    type_lists[identifier].append(value)
            else:
                raise TypeError(
                    str(type(value)) + " not supported")

        return type_lists

    @staticmethod
    def _parse(values):
        """
        Parse a list into the standard format used by ValueSet objects.
        Any ints, longs, and floats are absorbed into an Interval object if
        they are contained by that Interval and the base types contained in
        ``values`` are sorted.

        :return: filtered, sorted values in a standard format.
        :rtype: ``list``

        :raises TypeError: ``values`` parameter must be either a python \
        ``list`` or ``set``.
        """

        def _extend_intervals(type_lists):
            """
            If int or long is just beyond infirmum or supremum, extend the
            interval.
            """

            for i in type_lists[int]:
                for index, interval in enumerate(type_lists["_is_Interval"]):
                    if interval._type == int:
                        if i == interval[0] - 1:
                            type_lists["_is_Interval"][index] = Interval(i, interval[1])
                            type_lists[int].remove(i)
                            return True
                        if i == interval[1] + 1:
                            type_lists["_is_Interval"][index] = Interval(interval[0], i)
                            type_lists[int].remove(i)
                            return True

            for i in type_lists[long]:
                for index, interval in enumerate(type_lists["_is_Interval"]):
                    if interval._type == long:
                        if i == interval[0] - 1:
                            type_lists["_is_Interval"][index] = Interval(i, interval[1])
                            type_lists[long].remove(i)
                            return True
                        if i == interval[1] + 1:
                            type_lists["_is_Interval"][index] = Interval(interval[0], i)
                            type_lists[long].remove(i)
                            return True
            return False

        def _filter_numerics(type_lists):
            """Filter out numeric values subsumed by some Interval."""
            # filter out the ints, floats, and longs, subsumed by some Interval
            bad_ints, bad_floats, bad_longs = [], [], []
            for i in type_lists[int]:
                for interval in type_lists["_is_Interval"]:
                    if interval._type == int:
                        if i in interval:
                            if i not in bad_ints:
                                bad_ints.append(i)

            for f in type_lists[float]:
                for interval in type_lists["_is_Interval"]:
                    if interval._type == float:
                        if f in interval:
                            if f not in bad_floats:
                                bad_floats.append(f)

            for l in type_lists[long]:
                for interval in type_lists["_is_Interval"]:
                    if interval._type == long:
                        if l in interval:
                            if l not in bad_longs:
                                bad_longs.append(l)

            for bi in bad_ints:
                type_lists[int].remove(bi)

            for bf in bad_floats:
                type_lists[float].remove(bf)

            for bl in bad_longs:
                type_lists[long].remove(bl)

        # only accept sets and lists for valueset parameter
        if not isinstance(values, list) and not isinstance(values, set):
            raise TypeError("values paramter must be a list or set")

        # make copy of input before processing
        input_set = deepcopy(values)

        # convert set to list
        if isinstance(input_set, set):
            input_set = list(input_set)

        type_lists = ValueSet._split_by_types(values)

        # If intervals are within this valueset
        if type_lists["_is_Interval"]:
            type_lists["_is_Interval"] = Interval.collapse_intervals(
                type_lists["_is_Interval"])
            while _extend_intervals(type_lists): pass
            _filter_numerics(type_lists)

        output_set = []
        # reconstruct list, sorting when possible
        for base_type in ValueSet._base_types:
            output_set += sorted(type_lists[base_type])
        for object_type in ValueSet._object_types:
            output_set += type_lists[object_type]

        return output_set


def main():
    """."""
    intervals = []
    removals = []

    # 1-4, 5-6, 7-8, 10-12
    ints = [-2, 0, 1, 2, 3, 5, 6, 10, 11, 13, 15, 16, 17, 20]

    prev_index, index = 0, 1
    while prev_index != len(ints) - 1:
        while ints[index] == ints[index - 1] + 1:
            index += 1

        if prev_index != index - 1:
            removals.append((index - 1, prev_index))
            intervals.append(Interval(ints[prev_index], ints[index - 1]))

        prev_index = index
        index += 1

    for pair in sorted(removals, reverse=True):
        for i in range(pair[0], pair[1] - 1, -1):
            del ints[i]

    print ints
    print intervals


if __name__ == "__main__":
    main()
