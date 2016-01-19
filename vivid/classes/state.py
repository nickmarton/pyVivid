"""state module."""

from copy import deepcopy
from functools import total_ordering
from valueset import ValueSet
from attribute import Attribute
from attribute_structure import AttributeStructure
from attribute_system import AttributeSystem


@total_ordering
class State(object):
    """
    State class. Each State object is a state of an AttributeSystem; that is a
    set of functions :math:`\sigma = \{\delta_{1}`,
    :math:`\ldots, \delta_{k}`} where each :math:`\delta_{i}` is a
    function from :math:`\{s_{1}, \ldots, s_{n}\}` to the set of
    all non-empty finite subsets of :math:`A_{i}`, i.e.,

    .. centered:: :math:`\delta_{i} : \{s_{1}, \ldots, s_{n}\}` \
    :math:`\\rightarrow \mathcal{P}_{fin} (A_{i}) \\textbackslash  \emptyset`.

    The State class uses the ``total_ordering`` decorator so
    proper extensions, contravariant extensions and contravariant proper
    extensions are also available via the ``<``, ``>=``, and ``>`` operators
    respectively, despite the lack of magic functions for them.

    :ivar attribute_system: A copy of the AttributeSytem object that the \
    State object comes from.
    :ivar ascriptions: The ascriptions of the state, i.e., (the set of \
    attribute-object pairs and their corresponding ValueSet objects)
    :ivar _is_State: An identifier to use in place of type or isinstance.
    """

    def __init__(self, attribute_system, ascriptions={}):
        """
        Construct a State object.

        :param attribute_system: The AttributeSystem object from which the \
        State comes from.
        :type  attribute_system: AttributeSystem
        :param ascriptions: An optional dictionary of attribute-object pairs \
        to use as ascriptions; if some attribute-object pair is not provided, \
        the full ValueSet of the Attribute object corresponding to the \
        attribute label in the attribute-object pair is used.
        :type  ascriptions: ``dict``

        :raises TypeError: ``attribute_system`` parameter must be an \
        AttributeSystem object and ``ascriptions`` parameter must be a \
        ``dict``.
        """

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
        Determine if two State objects are equal via the ``==`` operator.
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

    def __le__(self, other):
        """
        Overloaded ``<=`` operator for State; Determine if this State is an
        extension of State object in ``other`` parameter.

        :raises TypeError: ``other`` parameter must be a State object.
        :raises ValueError: State object in ``other`` parameter must share \
        the same AttributeSystem object as this State object.
        """

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
        """
        Determine if two State objects are not equal via the ``!=`` operator.
        """

        return not self.__eq__(other)

    def __deepcopy__(self, memo):
        """
        Deepcopy a State object via the ``copy.deepcopy`` method.
        """

        return State(self._attribute_system, self._ascriptions)

    def set_ascription(self, ao_pair, new_valueset):
        """
        Set an ascription, given by ``ao_pair`` parameter, of this State object
        to the ValueSet object provided in ``new_valueset`` parameter.

        :param ao_pair: The attribute-object pair to use as a key for the \
        ascription ``dict`` member.
        :type  ao_pair: ``tuple``
        :param new_valueset: The new ValueSet object to assign to the \
        corresponding attribute-object pair given by the ``ao_pair`` \
        paramater in the ascription member
        :type  new_valueset: ValueSet

        :raise TypeError: ``ao_pair`` parameter must be a ``tuple`` and \
        ``new_valueset`` parameter must be a ``list``, ``set``, or ValueSet \
        object.
        :raise ValueError: ``ao_pair`` parameter must be a 2-tuple \
        (``str``,\ ``str``) and ``new_valueset`` parameter must be a \
        non-empty subset of the ValueSet object of the Attribute object \
        corresponding to the attribute in the ``ao_pair`` parameter.
        :raise KeyError: ``ao_pair`` must be a key in ``ascriptions`` member \
        of this State object.
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
        """
        Retrive the ascription or ValueSet corresponding to the
        attribute-object pair given by ``key`` parameter via indexing
        (e.g. ``State[key]``).

        :raises KeyError: ``key`` parameter must be a valid Attribute label \
        or valid attribute-object pair in the underlying AttributeSystem of \
        the State object.
        :raises TypeError: ``key`` parameter must be a ``str`` or ``tuple`` \
        containing only ``str``\s.
        """

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

    def add_object(self, obj, ascriptions=None):
        """
        Add an object to this State's AttributeSystem and optionally update any
        ascriptions provided.

        :param obj: The new object to add to the State.
        :type  obj: ``str``
        :param ascriptions: The optional ValueSets to assign to \
        attribute-object pairs corresponding to the new object.
        :type  ascriptions: ``dict``

        :raises TypeError: ``obj`` parameter must be a non-empty ``str`` and \
        if ``ascriptions`` parameter is provided, it must be a ``dict``.
        :raises ValueError: Duplicate objects cannot be added and all \
        ascriptions provided must be from an existing Attribute to ``obj`` \
        parameter.
        """

        # If object is a fresh string, add it to AttributeSystem
        if type(obj) is not str or obj == "":
            raise TypeError("obj must be a non-empty string")

        if obj in self._attribute_system._objects:
            raise ValueError("Cannot add duplicate object.")

        attributes = self._attribute_system._attribute_structure._attributes
        attribute_labels = [attribute._label for attribute in attributes]

        # If any ascriptions were provided, check they're well formed then add
        if ascriptions:
            if type(ascriptions) is not dict:
                raise TypeError(
                    "Any ascriptions provided must be in a dictionary")

            if not all([type(key) is tuple and len(key) == 2
                        for key in ascriptions.keys()]):
                raise ValueError(
                    "Ascription keys must be of form (attribute, object)")

            for ao_pair in ascriptions.keys():
                if ao_pair[0] not in attribute_labels or ao_pair[1] != obj:
                    raise ValueError(
                        "Invalid attribute-object pair: " + str(ao_pair))

            self._attribute_system._objects = sorted(
                self._attribute_system._objects + [obj])
            # Extend ascriptions with new object
            for Ai in attributes:
                self._ascriptions[(Ai._label, obj)] = deepcopy(Ai._value_set)

            # Set any optional ascriptions
            for ao_pair, valueset in ascriptions.iteritems():
                self.set_ascription(ao_pair, valueset)
        else:
            self._attribute_system._objects = sorted(
                self._attribute_system._objects + [obj])
            # Extend ascriptions with new object
            for Ai in attributes:
                self._ascriptions[(Ai._label, obj)] = deepcopy(Ai._value_set)

    def is_valuation(self, label):
        """
        Determine if ascription :math:`\delta_{i}` corresponding to
        ``label`` parameter is a valuation; that is
        :math:`\lvert \delta_{i}(s_{j}) \lvert = 1` for every
        :math:`j = 1, \ldots, n`.

        :param label: The label corresponding to the :math:`\delta`\ :sub:`i` \
        to check for valuation.
        :type  label: ``str``

        :return: whether or not ascription corresponding to ``label`` is a \
        valuation.
        :rtype: ``bool``
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
        """
        Determine if this State is a world; that is every ascription of this
        :math:`\sigma` is a valuation.

        :return: Whether or not the State is a world.
        :rtype: ``bool``
        """

        for label in self._attribute_system._attribute_structure.get_labels():
            if not self.is_valuation(label):
                return False
        return True

    def get_worlds(self):
        """
        Return a list of all possible worlds derivable from this State object.

        :return: all worlds derivable from this State object.
        :rtype: ``list``
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
        """
        Determine if this State is disjoint from the State in ``other``
        parameter.

        :return: Whether or not this State object and State object contained \
        in ``other`` parameter are disjoint.
        :rtype: ``bool``
        """

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
        Determine if ``s_prime`` parameter is an alternate extension of this
        State object w.r.t. states provided by optional positional arguments
        of ``states`` parameter, i.e., evaluate
        *Alt*\ (:math:`\sigma, \{\sigma_{1}, \ldots, \
        \sigma_{m}\}, \sigma^{\prime}`).

        :param s_prime: The State object to verify as the alternate \
        extension, :math:`\sigma^{\prime}`
        :type  s_prime: State
        :param states: The states {:math:`\sigma`\ :sub:`1`, :math:`\ldots, \
        \sigma`\ :sub:`m`} to use for the derivation of the alternate \
        extensions of this State.
        :type  states: State

        :return: the result of the evaluate of \
        *Alt*\ (:math:`\sigma, \{\sigma_{1}, \ldots, \
        \sigma_{m}\}, \sigma^{\prime}`).
        :rtype: ``bool``

        :raises TypeError: ``s_prime`` parameter must be a State object.
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
        respect to states provided by optional positional arguments
        of ``states`` parameter, i.e., generate **AE**\ :math:`(\{\sigma_{1}, \
        \ldots, \sigma_{m}\}, \sigma^{\prime})`.

        :param states: The states {:math:`\sigma`\ :sub:`1`, :math:`\ldots, \
        \sigma`\ :sub:`m`} to use for the derivation of the alternate \
        extensions of this State.
        :type  states: State

        :return: **AE**\ :math:`(\{\sigma_{1}, \
        \ldots, \sigma_{m}\}, \sigma^{\prime})`.
        :rtype: ``list``

        :raises TypeError: all optional positional arguments must be State \
        objects.
        :raises ValueError: at least one State object must be provided in \
        optional positional arguments and all provided State objects must be \
        proper extensions of this State object.
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
        """
        Join two states if possible.

        :param s1: The left operand to use for the union operation.
        :type  s1: State
        :param s2: The right operand to use for the union operation.
        :type  s2: State

        :raises ValueError: ``s1`` and ``s2`` parameters must share the same \
        underlying AttributeSystem.
        """

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
        """Return a readable string representation of the State object."""
        labels = self._attribute_system._attribute_structure.get_labels()
        objects = self._attribute_system._objects

        state_str = ''
        for label in labels:
            for obj in objects:
                state_str += label + "(" + obj + "): {"
                state_str += str(self._ascriptions[(label, obj)]) + "}\n"
        return state_str[:-1]

    def __repr__(self):
        """Return a string representation of the State object."""
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
