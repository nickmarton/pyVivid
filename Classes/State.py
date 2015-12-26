"""State object."""

from copy import deepcopy
from ValueSet import ValueSet
from AttributeSystem import AttributeSystem
from AttributeSystem import AttributeStructure
from AttributeSystem import Attribute


class State(object):
    """
    Class for a state of an AttributeSystem

    attribute_system:       copy of Attriute system from which the state came;
                            stored as an AttributeSystem.
    ascriptions:            dictionary of attribute-object pair keys with
                            Attribute value sets as values.
    """

    def __init__(self, attribute_system, ascriptions={}):
        """Return an initialized State object."""

        if not hasattr(attribute_system, "_is_AttributeSystem"):
            raise TypeError(
                "asys parameter must be of type AttributeSystem")

        if not isinstance(ascriptions, dict):
            raise TypeError("ascriptions parameter must be of type dict")

        self._attribute_system = deepcopy(attribute_system)
        self._ascriptions = {}
        self._is_State = True

        # Initialize the state as empty
        for Ai in self._attribute_system._attribute_structure._attributes:
            for s_i in self._attribute_system._objects:
                self._ascriptions[(Ai._label, s_i)] = deepcopy(Ai._value_set)

        # Set any ascriptions provided to constructor
        for ao_pair, valueset in ascriptions.iteritems():
            self.set_ascription(ao_pair, valueset)

        # break references by copying ascriptions
        self._ascriptions = deepcopy(self._ascriptions)

    def __eq__(self, other):
        """
        Return a boolean for whether or not self and other
        State objects are equal.
        """

        # if AttributeSystems aren't the same, then States can't be
        if self._attribute_system != other._attribute_system:
            return False

        # if Attribute-object pairs are not the same, unequal
        if set(self._ascriptions.keys()) != set(other._ascriptions.keys()):
            return False
        # ValueSet is unordered, simple equality works for testing
        for ao_pair in self._ascriptions.keys():
            if self._ascriptions[ao_pair] != other._ascriptions[ao_pair]:
                return False

        return True

    def __lt__(self, other):
        """
        Implement < operator for State object.
        Overloaded for proper extension.
        """

        # if this State is an extension of other State and other State is not
        # an extension of this State, this State properly extends other State
        self_extends_other = self <= other
        other_extends_self = other <= self

        if self_extends_other and not other_extends_self:
            return True
        else:
            return False

    def __le__(self, other):
        """Implement <= operator for State; overloaded for is_extension."""
        if not hasattr(other, "_is_State"):
            raise TypeError(
                'other parameter must be a State object')

        # if State's are from different AttributeSystems, raise ValueError
        if self._attribute_system != other._attribute_system:
            raise ValueError(
                "other State must be of same AttributeSystem as this State")

        ao_pairs = self._ascriptions.keys()

        # for each attribute-object pair
        for ao_pair in ao_pairs:
            # if the ValueSet of the ao-pair in this State is not a subset of
            # the corresponding ValueSet of the ao-pair in other State
            if not self._ascriptions[ao_pair] <= other._ascriptions[ao_pair]:
                return False

        return True

    def __ne__(self, other):
        """Implement != for State object."""

        return not self.__eq__(other)

    def __deepcopy__(self, memo):
        """
        Implement copy.deepcopy for State object.

        Constructor copies implicitly so just return new object.
        """

        return State(self._attribute_system, self._ascriptions)

    def set_ascription(self, ao_pair, new_valueset):
        """
        Set an ascription denoted by ao_pair (label,obj)to new_valueset.

        Raise TypeError if v parameter is not a list, set, or ValueSet
        Raise ValueError if v parameter is not subset of valueset.
        Raise KeyError if ao_pair parameter not in ascriptions,
        """

        if not isinstance(ao_pair, tuple):
            raise TypeError("ao_pair must be of type tuple")
        if len(ao_pair) != 2:
            raise ValueError("ao_pair must be a 2-tuple")
        if not isinstance(ao_pair[0], str) or not isinstance(ao_pair[1], str):
            raise ValueError(
                "ao_pair must be a 2-tuple of strings (label, object)")

        new_values = None
        # Enforce new_value_set as a list, set, or ValueSet
        if isinstance(new_valueset, list) or isinstance(new_valueset, set):
            new_values = ValueSet(new_valueset)
        elif hasattr(new_valueset, "_is_ValueSet"):
            new_values = deepcopy(new_valueset)
        else:
            raise TypeError(
                "Ascription values must be of type list, set, or ValueSet")

        # ensure non-empty Ascriptions
        if not new_values:
            raise ValueError("Ascriptions must be non-empty.")

        # check if ao pair is a valid key for ascriptions
        if ao_pair in self._ascriptions.keys():
            label, obj = ao_pair
            # Get ValueSet of Attribute with provided label in ao_pair
            attribute = self._attribute_system._attribute_structure[label]
            possible_values = attribute._value_set

            # If new value_set provided is a subset of the possible value_set
            # of the Attribute
            if new_values <= possible_values:
                self._ascriptions[ao_pair] = new_values
            else:
                raise ValueError(
                    str(new_values) + ' is not a subset of ' +
                    str(possible_values))
        else:
            raise KeyError(
                str(ao_pair) + ' not in ascriptions')

    def __getitem__(self, key):
        """Implement indexing for State."""
        # if key is a string (i.e., label), return copy of list of ValueSets
        if type(key) == str:
            # get labels of all ascriptions
            labels = self._attribute_system._attribute_structure.get_labels()
            if key not in labels:
                raise KeyError(
                    key + " is not a valid Attribute label.")
            # extract objects
            objects = self._attribute_system._objects
            # get ascription ValueSets li(sj) with li = key
            ascription_i = [self._ascriptions[(key, obj)] for obj in objects]
            return ascription_i
        # if key is an attribute-object pair return that li(sj)
        elif type(key) == tuple:
            if len(key) != 2:
                raise TypeError(
                    "key must be string or 2-tuple (attribute-object pair)")
            try:
                return self._ascriptions[key]
            except KeyError:
                raise KeyError(
                    str(key) + " not a valid key.")
        else:
            raise TypeError(
                "Only Attribute label strings and attribute-object "
                "2-tuples are valid keys")

    def is_valuation(self, label):
        """
        Determine if value set of ascription li is a valuation.

        raise KeyError of key parameter is not a valid ascription key.
        """

        # get list of li(sj) ValueSets with label provided
        valuesets = self[label]
        # try to look up the valueset of given ao_pair
        for valueset in valuesets:
            if len(valueset) == 1:
                # if the only element in ValueSet is an Interval, ValueSet is
                # not a valuation
                if hasattr(valueset[0], "_is_Interval"):
                    return False
            else:
                return False
        return True

    def is_world(self):
        """Returns True if this State is a world; false otherwise."""
        for label in self._attribute_system._attribute_structure.get_labels():
            if not self.is_valuation(label):
                return False
        return True

    def get_worlds(self):
        """
        Return a list of all possible worlds derivable from this
        NamedState object.
        """

        from itertools import product

        # get a copy of the ascriptions
        ascription_list = [item for item in self._ascriptions.items()]
        new_valuesets = []
        labels = []
        # for each ascription
        for (label, valueset) in ascription_list:
            # discretize any Intervals within the valueset
            new_valueset = []
            for value in valueset:
                if hasattr(value, "_is_Interval"):
                    new_valueset.extend(value.discretize())
                else:
                    new_valueset.append(value)
            # set ascription to discretized version
            new_valuesets.append(new_valueset)
            labels.append(label)

        combos = list(product(*new_valuesets))

        worlds = []

        # create each possible world from this NamedState and
        # return them in a list.
        for values in combos:
            world = State(self._attribute_system)
            for i, label in enumerate(labels):
                world.set_ascription(label, [values[i]])
            worlds.append(world)

        return worlds

    def is_disjoint(self, other):
        """Determine if this State is disjoint from other."""
        # get all possible worlds for both States
        self_worlds = self.get_worlds()
        other_worlds = other.get_worlds()

        # iterate over both sets of worlds and compare
        for self_world in self_worlds:
            for other_world in other_worlds:
                # if both states share some world, they're not disjoint
                if self_world == other_world:
                    return False

        return True

    def is_alternate_extension(self, s_prime, *states):
        """
        Determine if s_prime is an alternate extension of this State
        w.r.t. states s1,...,sm provided by optional positional
        arguments in states parameter.
        """

        if not hasattr(s_prime, "_is_State"):
            raise TypeError(
                "s_prime parameter must be of type State.")

        # generate all alternate extensions of this State
        alternate_extensions = self.get_alternate_extensions(*states)

        # check if s_prime is within list of all alternate extensions
        for alternate_extension in alternate_extensions:
            if s_prime == alternate_extension:
                return True
        return False

    def get_alternate_extensions(self, *states):
        """
        Return all alternate extensions of this State object with
        respect to States s1,...,sm within the states parameter.

        Raise ValueError if state parameter is empty.
        Raise TypeError if any item in states parameter is not of
        type State.
        Raise ValueError if any of the states s1,...,sm is not a
        proper extenstion of this State object.
        """

        def get_properly_spanning_lists():
            """
            Return those lists that properly span s1,...,sm
            w.r.t. this State.

            This function is based on the algorithm found in the paper;
            as such, it follows its steps extremely closely.
            """

            # create filtered table of all proper subset ascriptions among all
            # the states; this is step 1 of the algorithm outlined in the paper
            table = []
            for state in states:
                row = []
                for (ao_pair, value_set) in state._ascriptions.items():
                    if state[ao_pair] < self[ao_pair]:
                        row.append([ao_pair, value_set])
                table.append(row)

            # make all possible spanning lists from filtered table
            # this is step 2 of the algorithm outlined in the paper.
            from itertools import product, combinations
            spanning_lists = [list(tup) for tup in list(product(*table))]

            # we now proceed to step 3 of the algorithm outlined in the paper
            # by filtering out the non-properly spanning lists.
            for sl_index, spanning_list in reversed(
                    list(enumerate(spanning_lists))):

                non_spanning_flag = False
                # try every sublist with length greater than 1 as 1 is already
                # ensured not to be properly spanning by virtue of step 2.
                for i in range(2, len(spanning_list) + 1):
                    sublists = list(combinations(spanning_list, i))

                    for sublist in sublists:
                        # check if sublist labels are homogeneous, i.e.,
                        # if a.o. pairs are all equal in sublist
                        ao_pairs = [ao_pair for ao_pair, valueset in sublist]
                        if ao_pairs.count(ao_pairs[0]) == len(ao_pairs):

                            # sublist is homogeneous so merge the value sets
                            # of the a.o. pairs
                            value_sets = [
                                valueset for ao_pair, valueset in sublist]
                            # flatten value sets into signle merged list
                            merged_value_set = [item for sublist in value_sets
                                                for item in sublist]

                            # determine if ascription in self is equal to union
                            # of merged ascriptions in sublist
                            if self[ao_pairs[0]] == ValueSet(merged_value_set):
                                non_spanning_flag = True
                                break

                    if non_spanning_flag:
                        break
                # if non-spannig flag was tripped, erase current spanning list
                # from the set of spanning lists; we're going in reverse so we
                # can do this in one pass
                if non_spanning_flag:
                    del spanning_lists[sl_index]

            return spanning_lists

        def make_ascriptions(proper_spanning_list):
            """
            Take the union of all sets of equal a.o. pairs and return
            a dictionary of the ascriptions with their value sets.
            """

            # Make a default dict with empty list as default value so value
            # sets can be extended when there are multiple a.o. pair copies in
            # proper_spanning_list
            from collections import defaultdict
            ascriptions = defaultdict(list)
            for (ao_pair, value_set) in proper_spanning_list:
                ascriptions[ao_pair].extend(value_set)

            # There could be duplicates in ascriptions from extending lists;
            # delete any duplicates that might be in ascriptions by simply
            # casting to ValueSet which enforces no duplicates.
            for (ao_pair, value_set) in ascriptions.items():
                ascriptions[ao_pair] = ValueSet(ascriptions[ao_pair])

            # cast back to a regular dict and return
            return dict(ascriptions)

        def make_alternate_extension(proper_spanning_list):
            """
            Make an alternate extension from a single properly spanning list.
            """

            # First make a new copy of this State and create the ascriptions
            # available from the properly spanning list
            ae = State(self._attribute_system, self._ascriptions)
            ascriptions = make_ascriptions(proper_spanning_list)

            # for each ascription, complement it w.r.t. the original ascription
            # and replace the original ascription with the complement
            for (ao_pair, valueset) in ascriptions.items():
                complement_valueset = self._ascriptions[ao_pair] - valueset
                ae.set_ascription(ao_pair, complement_valueset)

            return ae

        # check for exceptions first

        if not states:
            raise ValueError(
                "at least one State object must be provided as an argument")

        for state in states:
            if not hasattr(state, "_is_State"):
                raise TypeError(
                    "all optional positional arguments must be of type State.")

        for state in states:
            if not state < self:
                raise ValueError(
                    "all states provided must be proper "
                    "extensions of this State object.")

        proper_spanning_lists = get_properly_spanning_lists()

        alternate_extensions = []
        for psl in proper_spanning_lists:
            ae = make_alternate_extension(psl)
            alternate_extensions.append(ae)

        return alternate_extensions

    @staticmethod
    def join(s1, s2):
        """Join two states if possible."""
        if s1._attribute_system != s2._attribute_system:
            raise ValueError(
                "Cannot join two states from different attribute systems")

        ao_pairs = s1._ascriptions.keys()
        join_ascriptions = {
            ao_pair: s1[ao_pair] + s2[ao_pair] for ao_pair in ao_pairs}

        join_state = State(s1._attribute_system)

        # Directly assign ascriptions so it doesn't pass through
        # set_ascriptions for optimization
        join_state._ascriptions = join_ascriptions
        return join_state

    def __str__(self):
        """Implement str() for State object."""
        labels = self._attribute_system._attribute_structure.get_labels()
        objects = self._attribute_system._objects

        state_str = ''
        for label in labels:
            for obj in objects:
                state_str += label + "(" + obj + "): {"
                state_str += str(self._ascriptions[(label, obj)]) + "}\n"
        return state_str[:-1]

    def __repr__(self):
        """Implement repr() for State object."""
        return self.__str__()


def main():
    """."""
    color = Attribute("color", ['R', 'G', 'B'])
    size = Attribute("size", ['S', 'M', 'L'])

    a = AttributeStructure(color, size)
    o = ['s']

    asys = AttributeSystem(a, o)
    s = State(asys)

    s1 = deepcopy(s)
    s1.set_ascription(('color', 's'), ['B', 'G'])
    s1.set_ascription(('size', 's'), ['S'])

    aes = s.get_alternate_extensions(s1)
    for ae in aes:
        print ae
        print

    s2 = deepcopy(s)
    s2.set_ascription(('color', 's'), ['R'])
    s2.set_ascription(('size', 's'), ['S', 'M', 'L'])
    s3 = deepcopy(s)
    s3.set_ascription(('color', 's'), ['R', 'B', 'G'])
    s3.set_ascription(('size', 's'), ['L', 'M'])

if __name__ == "__main__":
    main()
