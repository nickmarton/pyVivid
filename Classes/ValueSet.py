"""
ValueSet class.

Supports any object provided they implement __deepcopy__, __eq__, and __hash__.
"""

from copy import deepcopy
from functools import total_ordering
from Interval import Interval

@total_ordering
class ValueSet(object):
    """ValueSet object."""

    _base_types = [int, float, long, str, bool]
    _object_types = ["_is_Interval"]

    @classmethod
    def add_object_type(cls, object_identifier):
        """Add compatibility for object."""
        #Ensure object identifiers are strings
        if not isinstance(object_identifier,str):
            raise TypeError("Object identifier's must be strings")
        import re
        
        #Ensure they have the correct form
        if not re.match("_is_[A-Za-z]", object_identifier):
            raise ValueError(
                "object identifier must be of form _is_[object name]")
        
        #Add id to list of id's if it's not a duplicate
        if object_identifier not in cls._object_types:
            cls._object_types.append(object_identifier)

    def __init__(self, valueset):
        """Construct a ValueSet object."""
        if not isinstance(valueset, list):
            raise TypeError("valueset parameter must be of type list")
        #Save parsed output
        self._values = ValueSet._parse(valueset)
        self._is_ValueSet = True

    def __eq__(self, other):
        """Implement == for ValueSet object."""
        union = set(self._values) | set(other._values)
        intersection = set(self._values) & set(other._values)
        return union == intersection

    def __le__(self, other):
        """Implement <= for ValueSet object; overloaded for subset."""
        if len(self._values) > len(other._values):
            return False

        #if the intersection of both ValueSets is the same as this ValueSet
        #then this ValueSet is contained in other and is a subset.
        intersection = set(self._values) & set(other._values)
        return intersection == set(self._values)

    def __ne__(self, other):
        """Implement != for ValueSet object."""
        return not self.__eq__(other)

    def __sub__(self, other):
        """
        Implement - operator for ValueSet. 

        Overloaded to be set theoretic difference.
        """

        #Split the members of ValueSet's into lists defined by their
        #respective types
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
        #reconstruct list, sorting when possible
        for base_type in ValueSet._base_types:
            output_set += sorted(std_type_lists[base_type])
        for object_type in ValueSet._object_types:
            output_set += std_type_lists[object_type]

        return ValueSet(output_set)

    def __getitem__(self, key):
        """implement indexing for ValueSet object."""
        if type(key) != int:
            raise TypeError("indicies must be of type int")
        if key in range(len(self._values)):
            return self._values[key]
        else:
            raise IndexError("Invalid index: " + str(key))

    def __contains__(self, key):
        """Implement "in" operator for ValueSet."""
        for value in self:
            try:
                is_equal = key == value
                if is_equal:
                    return True
            except AttributeError:
                pass
        return False

    def __len__(self):
        """Implement len() for ValueSet."""
        return len(self._values)

    def __iter__(self):
        """Implement iterator for ValueSet."""
        for value in self._values:
            yield value

    def __nonzero__(self):
        """Define boolean behavior."""
        if self._values:
            return True
        else:
            return False

    def __deepcopy__(self, memo):
        """Implement copy.deepcopy for ValueSet object."""
        return ValueSet(deepcopy(self._values))

    def __str__(self):
        """Human readable representation of ValueSet object."""
        return "V(" + ', '.join([str(i) for i in self._values]) + ")"

    def __repr__(self):
        """Machine representation of ValueSet object."""
        return self.__str__()

    @staticmethod
    def _split_by_types(values):
        """Split valueset by types of elements within it."""
        #initialize a dictionary to separate types
        from collections import defaultdict
        type_lists = defaultdict(list)

        #for each value provided
        for value in values:
            #if it's a base type, simply add to it's corresponding list
            #while rejecting duplicates.
            if type(value) in ValueSet._base_types:
                if value not in type_lists[type(value)]:
                    type_lists[type(value)].append(value)
                continue
            
            #if it's an object type, check to see if it is in supported
            #object types
            identifier = None
            for object_identifier in ValueSet._object_types:
                if hasattr(value, object_identifier):
                    #Ensure no object has 2 identifiers
                    if identifier:
                        raise AttributeError(
                            "Any object passed must have only 1 "
                            "supported identifier")
                    identifier = object_identifier

            #store object in its corresponding list if it's not a duplicate
            if identifier:
                if value not in type_lists[identifier]:
                    type_lists[identifier].append(value)
            else:
                raise TypeError(
                    str(type(value)) + " not supported")

        return type_lists

    @staticmethod
    def _parse(values):
        """Parse a list into standard format."""

        def _filter_numerics(type_lists):
            """Filter out numeric values subsumed by some Interval."""
            #filter out the ints, floats, and longs, subsumed by some Interval.
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

        #only accept sets and lists for valueset parameter
        if not isinstance(values, list) and not isinstance(values, set):
            raise TypeError("values paramter must be a list or set")

        #make copy of input before processing
        input_set = deepcopy(values)

        #convert set to list
        if isinstance(input_set, set):
            input_set = list(input_set)

        type_lists = ValueSet._split_by_types(values)

        #If intervals are within this valueset
        if type_lists["_is_Interval"]:
            type_lists["_is_Interval"] = Interval.collapse_intervals(
                                            type_lists["_is_Interval"])
            _filter_numerics(type_lists)

        output_set = []
        #reconstruct list, sorting when possible
        for base_type in ValueSet._base_types:
            output_set += sorted(type_lists[base_type])
        for object_type in ValueSet._object_types:
            output_set += type_lists[object_type]

        return output_set


def main():
    """."""
    v = ValueSet(
        [Interval(0, 2), Interval(1, 4), 
        Interval(10, 20), Interval(9, 24),
        Interval(30, 35), Interval(31, 34), 
        Interval(60, 144), Interval(77, 150),
        Interval(9, 25), Interval(25, 30), "f", -1])
    
    v1 = ValueSet([-1, 'f', Interval(0, 4), Interval(60, 150), Interval(9, 35)])
    v2 = ValueSet([-1, 'f', Interval(60, 150)])
    print v1 - v2


if __name__ == "__main__":
    main()