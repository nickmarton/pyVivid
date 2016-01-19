"""named_state module."""

from functools import total_ordering
from state import State
from constant_assignment import ConstantAssignment
from variable_assignment import VariableAssignment


@total_ordering
class NamedState(State):
    """
    NamedState class. Each state is a pair (:math:`\sigma;\\rho`) consisting
    of a state :math:`\sigma` and a constant assignment :math:`\\rho`.

    The NamedState class uses the ``total_ordering`` decorator so
    proper extensions, contravariant extensions and contravariant proper
    extensions are also available via the ``<``, ``>=``, and ``>`` operators
    respectively, despite the lack of magic functions for them.

    :ivar attribute_system: A copy of the AttributeSytem object that the \
    NamedState object comes from.
    :ivar ascriptions: The ascriptions of the named state, i.e., (the set of \
    attribute-object pairs and their corresponding ValueSet objects)
    :ivar p: The ConstantAssignment object of the named state.
    :ivar _is_NamedState: An identifier to use in place of type or isinstance.
    """

    def __init__(self, attribute_system, p, ascriptions={}):
        """
        Construct a NamedState object.

        :param attribute_system: The AttributeSystem object from which the \
        NamedState comes from.
        :type  attribute_system: AttributeSystem
        :param p: The ConstantAssignment object of the named state.
        :type  p: ConstantAssignment
        :param ascriptions: An optional dictionary of attribute-object pairs \
        to use as ascriptions; if some attribute-object pair is not provided, \
        the full ValueSet of the Attribute object corresponding to the \
        attribute label in the attribute-object pair is used.
        :type  ascriptions: ``dict``

        :raises TypeError: ``p`` parameter must be a ConstantAssignment object.
        :raises ValueError: The AttributeSystem object provided and the \
        ConstantAssignment ``p`` parameter's AttributeSystem must match.
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
        """
        Determine if two NamedState objects are equal via the ``==`` operator.
        """

        if not hasattr(other, "_is_NamedState"):
            raise TypeError("Can only compare two NamedState objects")

        if State.__eq__(self, other) and self._p == other._p:
            return True
        else:
            return False

    def __ne__(self, other):
        """
        Determine if two NamedState objects are not equal via the ``!=``
        operator.
        """

        return not self.__eq__(other)

    def __deepcopy__(self, memo):
        """
        Deepcopy a NamedState object via the ``copy.deepcopy`` method.
        This does not break the reference to the underlying Vocabulary object.
        """

        from copy import deepcopy

        return NamedState(
            deepcopy(self._attribute_system),
            deepcopy(self._p),
            deepcopy(self._ascriptions))

    def __le__(self, other):
        """
        Overloaded ``<=`` operator for NamedState; Determine if this State is
        an extension of NamedState object in ``other`` parameter.

        :raises TypeError: ``other`` parameter must be a NamedState object.
        """

        if not hasattr(other, "_is_NamedState"):
            raise TypeError('other parameter must be of type NamedState')

        same_attr_systems = self._attribute_system == other._attribute_system
        same_vocabularies = self._p._vocabulary == other._p._vocabulary

        # not same AttributeSystem or Vocabulary, not an extension
        if not same_attr_systems or not same_vocabularies:
            return False

        self_state = State(self._attribute_system, self._ascriptions)
        other_state = State(other._attribute_system, other._ascriptions)

        # if this State is an extension of other State or this
        # ConstantAssignment is a superset of other ConstantAssignment,
        # this NamedState is an extension of other NamedState
        if self_state <= other_state and self._p >= other._p:
            return True
        else:
            return False

    def add_object(self, obj, ascriptions=None, constant_symbol=None):
        """
        Add an object to this NamedState's AttributeSystem, optionally update
        any ascriptions provided and optionally bind it to a constant given by
        ``constant_symbol`` (if the constant does not exist in the underlying
        Vocabulary object, it will be added to the Vocabulary object and
        furthermore all objects holding a reference to the Vocabulary will
        receive the update).

        :param obj: The new object to add to the NamedState.
        :type  obj: ``str``
        :param ascriptions: The optional ValueSets to assign to \
        attribute-object pairs corresponding to the new object.
        :type  ascriptions: ``dict``
        :param constant_symbol: The optional constant to bind to the new \
        object.
        :type  constant_symbol: ``str``

        :raises TypeError: ``obj`` parameter must be a non-empty ``str``, \
        if ``ascriptions`` parameter is provided, it must be a ``dict`` and \
        ``constant_symbol`` parameter must be a ``str``.
        :raises ValueError: Duplicate objects cannot be added, constant \
        corresponding to ``constant_symbol`` cannot be bound already and all \
        ascriptions provided must be from an existing Attribute to ``obj`` \
        parameter.
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
        """
        Determine if this NamedState object is a world; that is :math:`\sigma`
        is a world (every ascription of :math:`\sigma` is a valuation) and
        :math:`\\rho` is total.

        :return: Whether or not the NamedState is a world.
        :rtype: ``bool``
        """

        # if state is a world and p is total, this NamedState is a world
        return State.is_world(self) and self._p.is_total()

    def get_worlds(self):
        """
        Return a generator for the generation of all possible worlds
        derivable from this NamedState object.

        :return: A generator for the generation of all possible worlds \
        derivable from this NamedState object.
        :rtype: ``generator``
        """

        if self.is_world():
            from copy import deepcopy
            yield deepcopy(self)
        else:
            C = self._p._vocabulary._C
            bound_constants = self._p._source
            unbound_constants = [c for c in C if c not in bound_constants]

            objects = self._attribute_system._objects
            bound_objects = self._p._target
            unbound_objects = [
                obj for obj in objects if obj not in bound_objects]

            smaller = unbound_constants if len(unbound_constants) <= \
                len(unbound_objects) else unbound_objects
            bigger = unbound_constants if len(unbound_constants) > \
                len(unbound_objects) else unbound_objects

            import itertools
            if smaller == unbound_constants:
                combos = [zip(smaller, x) for x in itertools.permutations(
                    bigger, len(smaller))]
            else:
                combos = [zip(x, smaller) for x in itertools.permutations(
                    bigger, len(smaller))]

            constant_assignments = []
            for combo in combos:
                mapping = dict(combo + self._p._mapping.items())
                p = ConstantAssignment(self._p._vocabulary,
                                       self._attribute_system,
                                       mapping)
                constant_assignments.append(p)

            self_worlds = State.get_worlds(self)
            for p in constant_assignments:
                for self_world in self_worlds:
                    yield NamedState(self._attribute_system,
                                     p,
                                     self_world._ascriptions)

    def is_named_alternate_extension(self, ns_prime, *named_states):
        """
        Determine if ``ns_prime`` parameter is an alternate extension of this
        NamedState w.r.t. NamedState objects provided in ``named_states``
        parameter, i.e., evaluate *Alt*\ ((:math:`\sigma;\\rho`),\
        {(:math:`\sigma_{1}`\;\ :math:`\\rho_{1}`), :math:`\ldots, \
        (\sigma_{m}`;\ :math:`\\rho_{m}`)}, (:math:`\sigma^{\prime}`; \
        :math:`\\rho^{\prime}`)).

        :return: The result of the evaluation of *Alt*\ ((:math:`\sigma;\\rho`),\
        {(:math:`\sigma_{1}`\;\ :math:`\\rho_{1}`), :math:`\ldots, \
        (\sigma_{m}`;\ :math:`\\rho_{m}`)}, (:math:`\sigma^{\prime}`; \
        :math:`\\rho^{\prime}`)).
        :rtype: ``bool``

        :raises TypeError: ``ns_prime`` and all arguments provided to \
        optional positional arguments ``named_states`` must be NamedState \
        objects.
        :raises ValueError: At least one NamedState object must be provided \
        in ``named_states`` parameter and all NamedState objects in \
        ``ns_prime`` and ``named_states`` parameters must be proper \
        extensions of this NamedState.
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
        Obtain all alternate extensions of this NamedState w.r.t. NamedState
        objects provided in ``named_states`` parameter, i.e., compute
        **AE**\ (:math:`\Sigma_{i}`, :math:`\sigma`) for the various
        applicable *i* according to algorithm.

        :return: all alternative extensions of this NamedState object \
        (:math:`\sigma; \\rho`) w.r.t. \
        (:math:`\sigma_{1}`\;\ :math:`\\rho_{1}`), \
        :math:`\ldots, (\sigma_{m}`;\ :math:`\\rho_{m}`) provided as optional \
        positional arguments in ``named_states`` parameter.
        :rtype: ``list``

        :raises TypeError: ``ns_prime`` and all arguments provided to \
        optional positional arguments ``named_states`` must be NamedState \
        objects.
        :raises ValueError: At least one NamedState object must be provided \
        in ``named_states`` parameter and all NamedState objects in \
        ``ns_prime`` and ``named_states`` parameters must be proper \
        extensions of this NamedState.
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
        Determine if this NamedState object :math:`(w;\widehat{\\rho})`
        (which must be a world) satisfies given formula :math:`F` w.r.t.
        VariableAssignment :math:`\chi` and given AttributeInterpretation,
        i.e., :math:`(w;\widehat{\\rho})\models_{\chi}F`.

        :param formula: The formula :math:`F` to check for satisfaction.
        :type  formula: Formula
        :param X: The variable assignment :math:`\chi`
        :type  X: VariableAssignment
        :param attribute_interpretation: The fixed attribute interpretation \
        to use for interpreting which constants and variables get substituted \
        into the formula for evaluation.
        :type  attribute_interpretation: AttributeInterpretation

        :return: whether or not :math:`(w;\widehat{\\rho})\models_{\chi}F`.
        :rtype: ``bool``

        :raises TypeError: ``formula`` parameter must be a Formula object, \
        ``X`` parameter must be a VariableAssignment object and \
        ``attribute_interpretation`` must be an AttributeInterpretation object.
        :raises ValueError: this NamedState object must be a world.
        """

        if not hasattr(formula, "_is_Formula"):
            raise TypeError(
                'formula parameter must be of type Formula')

        if not hasattr(X, "_is_VariableAssignment"):
            raise TypeError(
                'X parameter must be a VariableAssignment object')

        if not hasattr(attribute_interpretation, "_is_AttributeInterpretation"):
            raise TypeError(
                "attribute_interpretation parameter must be of type "
                "AttributeInterpretation")

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
        Determine if this NamedState object :math:`(w;\widehat{\\rho})`
        (which must be a world) satisfies given NamedState object
        :math:`(\sigma;\\rho)` \
        i.e., :math:`(w;\widehat{\\rho}) \models (\sigma;\\rho)`.

        :param named_state: The named state :math:`(\sigma;\\rho)` \
        to check for satisfaction.
        :type  named_state: NamedState

        :return: Whether or not :math:`(w;\widehat{\\rho}) \models \
        (\sigma;\\rho)`.
        :rtype: ``bool``

        :raises TypeError: ``named_state`` parameter must be a NamedState \
        object.
        :raises ValueError: this NamedState object must be a world.
        """

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
        Determine if this NamedState object :math:`(w;\widehat{\\rho})`
        (which must be a world) satisfies given context
        :math:`\gamma = (\\beta;(\sigma;\\rho))` w.r.t. a given
        VariableAssignment :math:`\chi` and given AttributeInterpretation,
        i.e., :math:`(w;\widehat{\\rho})\models_{\chi}\gamma`
        (this NamedState object satisfies every Formula object in the
        AssumptionBase object of the Context object and this NamedState object
        satisfies the NamedState object of the Context object).

        :param context: The context :math:`\gamma` to check for satisfaction.
        :type  context: Context
        :param X: The variable assignment :math:`\chi`
        :type  X: VariableAssignment
        :param attribute_interpretation: The fixed attribute interpretation \
        to use for interpreting which constants and variables get substituted \
        into the formula for evaluation.
        :type  attribute_interpretation: AttributeInterpretation

        :return: whether or not :math:`(w;\widehat{\\rho})\models_{\chi}\gamma`.
        :rtype: ``bool``

        :raises TypeError: ``context`` parameter must be a Context object, \
        ``X`` parameter must be a VariableAssignment object and \
        ``attribute_interpretation`` must be an AttributeInterpretation object.
        :raises ValueError: This NamedState object must be a world.
        """

        if not hasattr(context, "_is_Context"):
            raise TypeError(
                "context parameter must be of type Context")

        if not hasattr(X, "_is_VariableAssignment"):
            raise TypeError(
                "X parameter must be of type VariableAssignment")

        if not hasattr(attribute_interpretation, "_is_AttributeInterpretation"):
            raise TypeError(
                "attribute_interpretation parameter must be of type "
                "AttributeInterpretation")

        if not self.is_world():
            raise ValueError(
                "this NamedState object must be a world")

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
        Generate all possible VariableAssignment objects derivable from this
        NamedState i.e., find all combinations of unbound objects and variables
        in the underlying Vocabulary object (a reference to it is held by the
        NamedState's ConstantAssignment). If no VariableAssignments can be
        created, a dummy VariableAssignment is returned.

        :return: A generator for all derivable VariableAssignment objects.
        :rtype: generator
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
        Determine if this NamedState object entails NamedState objects provided
        as optional positional arguments to ``named_states`` parameter w.r.t.
        the AssumptionBase object in the ``assumption_base`` parameter, using
        the AttributeInterpretation object provided in the
        ``attribute_interpretation`` parameter to resolve truth values of the
        Formula objects contained therein, i.e.,
        :math:`(\sigma;\\rho) \\Vvdash_{\\beta} \{(\sigma_{1};\\rho_{1}), \
        \ldots, (\sigma_{m};\\rho_{m})\}`.

        :param assumption_base: The AssumptionBase object to use when evaluating \
        :math:`I_{(\sigma^{\prime};\\rho^{\prime})/\chi}\\bigg(\\raisebox{3pt}{$\underset{F~\in~\\beta}{\\bigwedge} F$}\\bigg) =` \
        **false** for all :math:`\chi`.
        :type  assumption_base: AssumptionBase
        :param attribute_interpretation: The AttributeInterpretation object \
        to use to resolve the truth values of Formula objects in the \
        AssumptionBase object in ``assumption_base`` parameter.
        :type  attribute_interpretation: AttributeInterpretation
        :param named_states: Any amount of NamedState objects \
        :math:`(\sigma_{1};\\rho_{1}), \ldots, (\sigma_{m};\\rho_{m})` to \
        check for entailment.
        :type  named_states: NamedState

        :return: Whether or not :math:`(\sigma;\\rho) \\Vvdash_{\\beta} \
        \{(\sigma_{1};\\rho_{1}), \ldots, (\sigma_{m};\\rho_{m})\}`
        :rtype: ``bool``

        :raises TypeError: ``assumption_base`` parameter must be an \
        AssumptionBase, ``attribute_interpretation`` parameter must be an \
        AttributeInterpretation object, and all optional positional arguments \
        in ``named_states`` parameter must be NamedState objects.
        :raises ValueError: all NamedState objects provided as optional \
        positional arguments to ``named_states`` parameter must share the \
        same Vocabulary object, AttributeSystem object and be proper \
        extensions of this NamedState object.
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

    def is_exhaustive(self, basis, *named_states):
        """
        Determine if on some basis, a set of NamedState objects is exhaustive
        w.r.t this NamedState.

        :param basis: A list of attribute-object pairs \
        (``str``, ``str`` 2-tuples).
        :type  basis: ``list``
        :param named_states: Any positive amount of NamedState objects.
        :type  named_states: NamedState

        :return: Whether or not the NamedState objects provided as optional \
        positional arguments are exhaustive w.r.t. this NamedState object on \
        the basis provided in ``basis`` parameter.
        :rtype: ``bool``

        :raises ValueError: ``basis`` parameter cannot be empty and at least \
        one NamedState object must be provided.
        """

        if not basis:
            raise ValueError("Basis cannot be empty")

        if not named_states:
            raise ValueError("At least one NamedState must be provided")

        for ao_pair in basis:
            # Take union of the ValueSets of ascriptions of all named states
            valuesets = [named_state._ascriptions[ao_pair]
                         for named_state in named_states]

            union = valuesets[0]
            for valueset in valuesets[1:]:
                union += valueset
            # If union is not equal to this NamedState's Valueset of
            # corresponding ascription, the named states provided are not
            # exhaustive
            if union != self._ascriptions[ao_pair]:
                return False

        return True

    def __str__(self):
        """Return a readable string representation of the NamedState object."""
        return State.__str__(self) + '\n' + str(self._p)

    def __repr__(self):
        """Return a string representation of the State object."""
        return self.__str__()


def main():
    """quick dev tests."""

    from interval import Interval
    from relationSymbol import RelationSymbol
    from vocabulary import Vocabulary
    from attribute_interpretation import AttributeInterpretation
    from formula import Formula
    from assumption_base import AssumptionBase
    from attribute import Attribute
    from relation import Relation
    from attribute_structure import AttributeStructure
    from attribute_system import AttributeSystem
    from constant_assignment import ConstantAssignment
    from named_state import NamedState
    from context import Context
    from variable_assignment import VariableAssignment

    a = Attribute('hour', [Interval(0, 23)])
    a2 = Attribute('minute', [Interval(0, 59)])
    r_pm = Relation('R1(h1) <=> h1 > 11', ['hour'], 1)
    r_am = Relation('R2(h1) <=> h1 <= 11', ['hour'], 2)
    r_ahead = Relation('R3(h1,m1,h2,m2) <=> h1 > h2 or (h1 = h2 and m1 > m2)',
                       ['hour', 'minute', 'hour', 'minute'], 3)
    r_behind = Relation('R4(h1,m1,h2,m2) <=> h1 < h2 or (h1 = h2 and m1 < m2)',
                        ['hour', 'minute', 'hour', 'minute'], 4)
    attribute_structure = AttributeStructure(
        a, a2, r_ahead, r_behind, r_pm, r_am)

    pm_rs = RelationSymbol('PM', 1)
    am_rs = RelationSymbol('AM', 1)
    ahead_rs = RelationSymbol('Ahead', 4)
    behind_rs = RelationSymbol('Behind', 4)

    vocabulary = Vocabulary(
        ['C1', 'C2'], [pm_rs, am_rs, ahead_rs, behind_rs], ['V1', 'V2'])

    objs = ['s1', 's2', 's3']
    asys = AttributeSystem(attribute_structure, objs)

    const_mapping_2 = {'C1': 's1'}
    p2 = ConstantAssignment(vocabulary, asys, const_mapping_2)

    ascriptions_1 = {("hour", "s1"): [13, 15, 17], ("minute", "s1"): [10],
                     ("hour", "s2"): [1, 3, 5], ("minute", "s2"): [10],
                     ("hour", "s3"): [1, 3, 5], ("minute", "s3"): [10]}

    named_state_4 = NamedState(asys, p2, ascriptions_1)


if __name__ == "__main__":
    main()
