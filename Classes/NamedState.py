"""Named State class."""

from State import State
from ConstantAssignment import ConstantAssignment
from VariableAssignment import VariableAssignment


class NamedState(State):
    """
    Class for named state;

    subclasses State and adds p (ConstantAssignment).
    """

    def __init__(self, attribute_system, p, ascriptions={}):
        """
        Initialize a NamedState object with AttributeSystem attribute_system
        and constant assignment p.

        Raise TypeError if attribute_system parameter is not of type
        AttributeSystem or p parameter is not of type
        ConstantAssignment.
        Raise ValueError if AttributeSystem of p doesn't match
        AttributeSystem object provided in attribute_system.
        """

        if not hasattr(p, "_is_ConstantAssignment"):
            raise TypeError("p parameter must be a ConstantAssignment object")

        if p._attribute_system != attribute_system:
            raise ValueError(
                "ConstantAssignment AttributeSystem and "
                "State AttributeSystem must match")

        from copy import deepcopy
        State.__init__(self, attribute_system, ascriptions)
        self._p = deepcopy(p)
        # reassign vocabulary to keep reference since Vocabulary's are mutable
        self._p._vocabulary = p._vocabulary
        self._is_NamedState = True

    def __eq__(self, other):
        """Implement == operator for NamedState object."""
        if not hasattr(other, "_is_NamedState"):
            raise TypeError("Can only compare two NamedState objects")

        if State.__eq__(self, other) and self._p == other._p:
            return True
        else:
            return False

    def __ne__(self, other):
        """Implement != operator for NamedState object."""
        return not self.__eq__(other)

    def __deepcopy__(self, memo):
        """Return a deep copy of this NamedState."""
        from copy import deepcopy

        return NamedState(
            deepcopy(self._attribute_system),
            deepcopy(self._p),
            deepcopy(self._ascriptions))

    def __lt__(self, other):
        """Implement overloaded < operator for NamedState proper extension."""
        if not hasattr(other, "_is_NamedState"):
            raise TypeError('other parameter must be of type NamedState')

        same_attr_systems = self._attribute_system == other._attribute_system
        same_vocabularies = self._p._vocabulary == other._p._vocabulary

        # not same AttributeSystem or Vocabulary, not an extension
        if not same_attr_systems or not same_vocabularies:
            return False

        # if this State is an extension of other State
        if self <= other:
            self_state = State(self._attribute_system, self._ascriptions)
            other_state = State(other._attribute_system, other._ascriptions)

            # if this State is a proper extension of other State or this
            # ConstantAssignment is a proper superset of other
            # ConstantAssignment, this NamedState is a proper extension of
            # other NamedState
            if self_state < other_state or self._p > other._p:
                return True

        return False

    def __le__(self, other):
        """Implement overloaded <= operator for NamedState extension."""
        if not hasattr(other, "_is_NamedState"):
            raise TypeError('other parameter must be of type NamedState')

        same_attr_systems = self._attribute_system == other._attribute_system
        same_vocabularies = self._p._vocabulary == other._p._vocabulary

        # not same AttributeSystem or Vocabulary, not an extension
        if not same_attr_systems or not same_vocabularies:
            return False

        self_state = State(self._attribute_system, self._ascriptions)
        other_state = State(other._attribute_system, other._ascriptions)

        if self_state <= other_state and self._p >= other._p:
            return True
        else:
            return False

    def add_object(self, obj, ascriptions=None, constant_symbol=None):
        """
        Add an object to the NamedState with option to bind it to a Constant in
        ConstantAssignment.
        """

        if constant_symbol:
            # If constant symbol provided is an unbound string
            if type(constant_symbol) is not str:
                raise TypeError("constant_symbol parameter must be a string")
            if constant_symbol in self._p._source:
                raise ValueError(
                    "Constant Symbol " + constant_symbol + " is already bound")

            # If constant symbol isn't in Vocabulary, add it
            if constant_symbol not in self._p._vocabulary._C:
                self._p._vocabulary.add_constant(constant_symbol)

            # Add object, then add mapping so any errors happen before mutation
            State.add_object(self, obj, ascriptions)
            self._p._attribute_system._objects = sorted(
                self._p._attribute_system._objects + [obj])

            self._p._mapping[constant_symbol] = obj
            self._p._source.append(constant_symbol)
            self._p._target.append(obj)
        else:
            State.add_object(self, obj, ascriptions)
            self._p._attribute_system._objects = sorted(
                self._p._attribute_system._objects + [obj])

    def is_world(self):
        """Determine if this NamedState is a world."""
        # if state is a world and p is total, this NamedState is a world
        return State.is_world(self) and self._p.is_total()

    def get_worlds(self):
        """
        Return a list of all possible worlds derivable from this
        NamedState object.
        """

        if self.is_world():
            from copy import deepcopy
            return [deepcopy(self)]

        source = self._p._vocabulary._C
        target = self._attribute_system._objects

        repeat_num = len(source) if len(source) < len(target) else len(target)

        from itertools import product
        # create all combinations of source and target elements
        combos = list(product(source, target, repeat=repeat_num))

        # remove combinations with duplicate source or target elements
        combos = [
            c for c in combos if len(set(c)) == len(source) + len(target)]
        # group the combinations into 2-tuples
        combos = [
            [combo[i:i + 2] for i, item in enumerate(combo) if i % 2 == 0]
            for combo in combos]
        # sort the combinations by vocabulary elements
        combos = [sorted(combo, key=lambda x: x[0]) for combo in combos]

        # remove duplcate combinations
        unique_combos = []

        for combo in combos:
            if combo not in unique_combos:
                unique_combos.append(combo)

        # remove combinations in conflict with this NamedState
        valid_constant_assignments = []
        for combo in unique_combos:
            CA = ConstantAssignment(
                self._p._vocabulary,
                self._attribute_system,
                {vocab: obj for (vocab, obj) in combo})

            if not ConstantAssignment.in_conflict(self._p, CA):
                valid_constant_assignments.append(CA)

        self_worlds = State.get_worlds(self)

        # create worlds for all constant assignment and world combos.
        worlds = []
        if valid_constant_assignments:
            for p in valid_constant_assignments:
                for self_world in self_worlds:
                    # construct world and save it
                    world = NamedState(
                        self._attribute_system, p, self_world._ascriptions)
                    worlds.append(world)
        else:
            for self_world in self_worlds:
                    # construct world and save it
                    world = NamedState(
                        self._attribute_system,
                        self._p,
                        self_world._ascriptions)
                    worlds.append(world)

        return worlds

    def is_named_alternate_extension(self, ns_prime, *named_states):
        """
        Return True if ns_prime is an alternate extension of this
        NamedState w.r.t. named_states provided in named_states
        parameter.

        Raise TypeError if ns_prime parameter is not of type NamedState.
        Raise ValueError if ns_prime is not a proper extension of this
        NamedState object.
        Raise ValueError if named_states parameter is empty.
        Raise TypeError if any item in named_states parameter is not of type
        NamedState.
        Raise ValueError if any of the NamedStates ns1,...,nsm is not a proper
        extension of this NamedState object (This checks for mistmatched
        Vocabulary's and AttributeSystem's).
        """

        if not named_states:
            raise ValueError(
                "at least one NamedState object must be "
                "provided as an argument")

        for named_state in list(named_states) + [ns_prime]:
            if not hasattr(named_state, "_is_NamedState"):
                raise TypeError(
                    "all optional positional arguments must be NamedState "
                    "objects.")

            if not named_state < self:
                raise ValueError(
                    "all NamedStates provided must be proper "
                    "subsets of this NamedState object.")

        aes = self.get_named_alternate_extensions(*named_states)
        return True if ns_prime in aes else False

    def get_named_alternate_extensions(self, *named_states):
        """
        Return all alternate extensions of this NamedState object with
        respect to NamedStates ns1,...,nsm within the named_states
        parameter.

        Raise ValueError if named_states parameter is empty.
        Raise TypeError if any item in named_states parameter is not of
        type NamedState.
        Raise ValueError if any of the NamedStates ns1,...,nsm is not a
        proper extension of this NamedState object (this checks for matching
        Vocabulary's and AttributeSystem's.
        """

        def get_supersets():
            """
            Return the set of ConstantAssignments that are supersets
            of this NamedState object's p.
            """

            # grab the system objects for convenience.
            system_objects = self._attribute_system._objects
            n = len(system_objects)

            # Get the union of all domains of provided NamedState objects
            domain_union = []
            for named_state in named_states:
                domain_union.extend(named_state._p.get_domain())
            domain_union = list(set(domain_union))

            # create set of all cartesian products of domain list and system
            # object list where each product is of length arity, that is,
            # the minimum number to match the smaller list with exactly one
            # member of the bigger list.
            from itertools import product

            arity = len(domain_union) if len(domain_union) < n else n
            combos = list(product(domain_union, system_objects, repeat=arity))

            supersets_list = []

            for combo in combos:
                # bundle the combo elements into 2-tuples representing
                # domain-object pairs, then remove duplicates.
                combo = [
                    combo[i:i + 2] for i, item in enumerate(combo)
                    if i % 2 == 0]
                combo = list(set(combo))

                # ensure that individual combos do not contain duplicate
                # domain elemens or duplicate objects.
                domain = [pair[0] for pair in combo]
                objects = [pair[1] for pair in combo]
                domain_duplicates = len(domain) != len(set(domain))
                object_duplicates = len(objects) != len(set(objects))

                if not domain_duplicates and not object_duplicates:
                    # if this combo is a superset of this NamedState's p, and
                    # hasn't already been saved in supersets_list, save it.
                    if set(self._p._mapping.items()) <= set(combo):
                        for superset in supersets_list:
                            if set(superset) == set(combo):
                                break
                        else:
                            supersets_list.append(combo)

            # create a ConstantAssignment for each superset; easily transform
            # each superset (list of 2-tuples) into mapping by casting to dict
            supersets = []
            for superset in supersets_list:
                p_prime = ConstantAssignment(self._p._vocabulary,
                                             self._attribute_system,
                                             dict(superset))
                supersets.append(p_prime)

            return supersets

        if not named_states:
            raise ValueError(
                "at least one NamedState object must be "
                "provided as an argument")

        for named_state in named_states:
            if not hasattr(named_state, "_is_NamedState"):
                raise TypeError(
                    "all optional positional arguments must be NamedState "
                    "objects.")

            if not named_state < self:
                raise ValueError(
                    "all NamedStates provided must be proper "
                    "subsets of this NamedState object.")

        # get supsets of this NamedState's ConstantAssignment and create an
        # empty list to hold all alternate extensions.
        supersets = get_supersets()

        named_alternate_extensions = []

        for p_prime in supersets:
            # get the list of provided NamedStates not in conflict with each
            # superset of this NamedState's ConstantAssignment, i.e., the
            # NamedState's where the p'_i >= p_j and sigma_j < sigma.
            Sigma_i = [ns for ns in named_states if p_prime >= ns._p]

            # if there are such states, get the alternate extensions of this
            # NamedState's State component w.r.t. the list of non-conflicted
            # States in Sigma_i.
            if Sigma_i:
                phi_i = self.get_alternate_extensions(*Sigma_i)
                # for each alternate extension, create a new NamedState with
                # that alternate extensions ascriptions and the superset
                # p_prime and add to named_alternate_extensions if not already
                # in named_alternate_extensions.
                for s_prime in phi_i:
                    nae = NamedState(
                        self._attribute_system, p_prime, s_prime._ascriptions)

                    if nae not in named_alternate_extensions:
                        named_alternate_extensions.append(nae)
            # There is no provided NamedState not in conflict with this
            # NamedState's ConstantAssignment, so create a new NamedState with
            # this NamedState's ascriptions and p_prime and add to
            # named_alternate_extensions.
            else:
                from copy import deepcopy
                nae = deepcopy(self)
                if nae not in named_alternate_extensions:
                    named_alternate_extensions.append(nae)

        return named_alternate_extensions

    def satisfies_formula(self, formula, X, attribute_interpretation):
        """
        Determine if NamedState object (which must be a world) satisfies given
        formula with respect to VariableAssignment X.
        """

        if not hasattr(formula, "_is_Formula"):
            raise TypeError(
                'f parameter must be of type Formula')

        if not hasattr(X, "_is_VariableAssignment"):
            raise TypeError(
                'X parameter must be a VariableAssignment object')

        if not self.is_world():
            raise ValueError('this NamedState object must be a world')

        truth_value = formula.assign_truth_value(
            attribute_interpretation, self, X)

        if truth_value is True:
            return True
        else:
            return False

    def satisfies_named_state(self, named_state):
        """
        Determine if this NamedState (which is a world) satisfies NamedState
        object named_state.

        Raise TypeError if named_state parameter is not a NamedState object.
        Raise ValueError if this NamedState object is not a world.
        """

        # check for exceptions first.
        if not isinstance(named_state, NamedState):
            raise TypeError(
                "named_state parameter must be of type NamedState")

        if not hasattr(named_state, "_is_NamedState"):
            raise TypeError(
                "named_state parameter must be NamedState object.")

        if not self.is_world():
            raise ValueError(
                "this NamedState object must be a world")

        # simply return truth value of extension
        return self <= named_state

    def satisfies_context(self, context, X, attribute_interpretation):
        """
        Determine if this NamedState object (which is a world) satisfies a
        given context w.r.t. some VariableAssignment X.
        """

        if not hasattr(context, "_is_Context"):
            raise TypeError(
                'context parameter must be of type Context')

        if not isinstance(X, VariableAssignment):
            raise TypeError(
                'X parameter must be of type VariableAssignment')

        if not self.is_world():
            raise ValueError(
                'this NamedState object must be a world')

        named_state = context._named_state
        assumption_base = context._assumption_base

        # if this world doesn't satisfy Context's NamedState, doesn't satisfy
        # Context
        if not self <= named_state:
            return False

        # If there's some formula for which the world does not satisfy, doesn't
        # satisfy the Context
        for formula in assumption_base:
            truth_value = self.satisfies_formula(
                formula, X, attribute_interpretation)

            if truth_value is False or truth_value == "unknown":
                return False

        return True

    def _generate_variable_assignments(self):
        """
        Return a list of all possible VariableAssignments that can
        be created from this NamedState object.
        """

        if not self._p._vocabulary._V:
            yield VariableAssignment(self._p._vocabulary,
                                     self._attribute_system,
                                     {}, dummy=True)
        else:
            V = self._p._vocabulary._V
            objects = self._attribute_system._objects
            bound_objects = self._p._target
            unbound_objects = [
                obj for obj in objects if obj not in bound_objects]
            smaller = V if len(V) <= len(unbound_objects) else unbound_objects
            bigger = V if len(V) > len(unbound_objects) else unbound_objects

            import itertools
            if smaller == V:
                combos = [zip(smaller, x) for x in itertools.permutations(
                    bigger, len(smaller))]
            else:
                combos = [zip(x, smaller) for x in itertools.permutations(
                    bigger, len(smaller))]

            for combo in combos:
                mapping = {pair[0]: pair[1] for pair in combo}
                X = VariableAssignment(self._p._vocabulary,
                                       self._attribute_system,
                                       mapping)
                yield X

    def is_named_entailment(self, assumption_base, attribute_interpretation,
                            *named_states):
        """
        Determine if this NamedState entails NamedStates contained in
        named_states parameter w.r.t. AssumptionBase assumption_base.
        """

        if not hasattr(assumption_base, "_is_AssumptionBase"):
            raise TypeError(
                "assumption_base parameter must be an AssumptionBase object")
        if not hasattr(attribute_interpretation,
                       "_is_AttributeInterpretation"):
            raise TypeError(
                "attribute_interpretation parameter must be an "
                "AttributeInterpretation object")

        for named_state in named_states:
            if not hasattr(named_state, "_is_NamedState"):
                raise TypeError(
                    "all optional positional arguments must be "
                    "NamedState objects.")
            if named_state._p._vocabulary is not self._p._vocabulary:
                raise ValueError(
                    "all vocabularies in this NamedState and optional "
                    "positional NamedStates must be the same.")
            if named_state._attribute_system != self._attribute_system:
                raise ValueError(
                    "all AttributeSystems in this NamedState and optional "
                    "positional NamedStates must be equivalent.")
            if not named_state < self:
                raise ValueError(
                    "all NamedStates provided must be proper "
                    "extensions of this NamedState object.")

        vocabs_match = self._p._vocabulary is assumption_base._vocabulary is \
            attribute_interpretation._vocabulary

        if not vocabs_match:
            raise ValueError(
                "Vocabulary's of NamedState, AssumptionBase, and "
                "AttributeInterpretation must all match")

        # Get all possible alternate extensions first.
        alternate_extensions = self.get_named_alternate_extensions(
            *named_states)

        for alternate_extension in alternate_extensions:
            for X in self._generate_variable_assignments():
                for formula in assumption_base:
                    truth_value = formula.assign_truth_value(
                        attribute_interpretation, alternate_extension, X)
                    if truth_value is not False:
                        return False
        return True

    def __str__(self):
        """Implement str(NamedState)."""
        return State.__str__(self) + '\n' + str(self._p)

    def __repr__(self):
        """Implement repr(NamedState)."""
        return self.__str__()


def main():
    """quick dev tests."""
    pass

if __name__ == "__main__":
    main()
