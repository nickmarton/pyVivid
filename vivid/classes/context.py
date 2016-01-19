"""context module."""


class Context(object):
    """
    Context class. A Context is a pair composed of an AssumptionBase object
    :math:`\\beta` and a NamedState object :math:`(\sigma;\\rho)`,
    i.e., :math:`\gamma = (\\beta; (\sigma; \\rho))`.

    :ivar assumption_base: The AssumptionBase object :math:`\\beta` of the \
    Context object.
    :ivar named_state: The NamedState object :math:`(\sigma;\\rho)` of the \
    Context object.
    :ivar is_Context: An identifier to use in place of type or isinstance.
    """

    def __init__(self, assumption_base, named_state):
        """
        Construct a Context object.

        :param assumption_base: The AssumptionBase object to use in the \
        Context object.
        :type  assumption_base: AssumptionBase
        :param named_state: The NamedState object to use in the Context object.
        :type  named_state: NamedState

        :raises TypeError: ``assumption_base`` parameter must be an \
        AssumptionBase object and ``named_state`` parameter must be a \
        NamedState object.
        :raises ValueError: The underlying Vocabulary objects of the \
        ``assumption_base`` and ``named_state`` parameters must be the same \
        Vocabulary object.
        """

        # Check for exceptions first.
        if not hasattr(assumption_base, "_is_AssumptionBase"):
            raise TypeError(
                "assumption_base parameter must be an AssumptionBase object")
        if not hasattr(named_state, "_is_NamedState"):
            raise TypeError(
                "named_state parameter must be a NamedState object")

        if assumption_base._vocabulary is not named_state._p._vocabulary:
            raise ValueError(
                "Vocabulary's of NamedState and AssumptionBase must match")

        from copy import deepcopy
        self._assumption_base = deepcopy(assumption_base)
        self._named_state = deepcopy(named_state)
        self._is_Context = True

    def __eq__(self, other):
        """
        Determine if two Context objects are equal via the ``==`` operator.
        """

        if not hasattr(other, "_is_Context"):
            raise TypeError(
                "Only Context object can be compared against another "
                "Context object")

        named_state_cond = self._named_state == other._named_state
        assumption_base_cond = self._assumption_base == other._assumption_base

        if named_state_cond and assumption_base_cond:
            return True
        else:
            return False

    def __ne__(self, other):
        """
        Determine if two Context objects are not equal via the ``!=`` operator.
        """

        return not self.__eq__(other)

    def __str__(self):
        """Return a readable string representation of the Context object."""
        context_str = str(self._named_state) + '\n'
        context_str += str(self._assumption_base)
        return context_str

    def __repr__(self):
        """Return a string representation of the NamedState object."""
        return self.__str__()

    def __deepcopy__(self, memo):
        """
        Deepcopy a Context object via the ``copy.deepcopy`` method.
        This does not break the reference to the underlying Vocabulary object.
        """

        from copy import deepcopy
        return Context(deepcopy(self._assumption_base),
                       deepcopy(self._named_state))

    def entails_formula(self, formula, attribute_interpretation):
        """
        Determine if this Context object entails the Formula object provided by
        ``formula`` parameter w.r.t. all worlds and possible variable
        assignments of this Context, using AttributeInterpretation object
        provided in ``attribute_interpretation`` to interpret truth values,
        i.e., determine if :math:`\gamma \models F`.

        :param formula: The Formula object to check for entailment.
        :type  formula: Formula
        :param attribute_interpretation: The AttributeInterpretation to use \
        for the interpretation of truth values during the evauation of the \
        entailment.
        :type  attribute_interpretation: AttributeInterpretation

        :return: Whether or not :math:`\gamma \models F`,that is \
        :math:`(w;\widehat{\\rho})\models_{\chi}\gamma` implies \
        :math:`(w;\widehat{\\rho})\models_{\chi}F` for all worlds \
        :math:`(w;\widehat{\\rho})` and variable assignments :math:`\chi`.
        :rtype: ``bool``

        :raises TypeError: ``formula`` parameter must be a Formula object and \
        ``attribute_interpretation`` parameter must be an \
        AttributeInterpretation object.
        :raises ValueError: This Context and the Formula object provided in \
        the ``formula`` parameter must share the same underlying Vocabulary \
        object.
        """

        # Check for exceptions first.
        if not hasattr(formula, "_is_Formula"):
            raise TypeError(
                "formula parameter must be of type Formula")

        f_vocabulary = formula._vocabulary
        c_vocabulary = self._named_state._p._vocabulary

        if f_vocabulary != c_vocabulary:
            raise ValueError(
                "Formula must be over the same vocabulary used to create"
                "ConstantAssignment within this Context.")

        # get all possible worlds and variable assignments.
        possible_worlds = self._named_state.get_worlds()

        # for every possible world and variable assignment, if the world
        # satisfies the context, but not the formula, this Context does not
        # entail the Formula, return False, otherwise return True aftewards.
        for world in possible_worlds:
            for X in world._generate_variable_assignments():
                satisfies_context = world.satisfies_context(
                    self, X, attribute_interpretation)
                satisfies_formula = world.satisfies_formula(
                    formula, X, attribute_interpretation)

                if satisfies_context and not satisfies_formula:
                    return False

        return True

    def entails_named_state(self, named_state, attribute_interpretation):
        """
        Determine if this Context object entails the NamedState object provided
        by ``named_state`` parameter w.r.t. all worlds and possible variable
        assignments of this Context, using AttributeInterpretation object
        provided in ``attribute_interpretation`` to interpret truth values,
        i.e., determine if
        :math:`\gamma \models (\sigma^{\prime};\\rho^{\prime})`.

        :param named_state: The NamedState object to check for entailment.
        :type  named_state: NamedState
        :param attribute_interpretation: The AttributeInterpretation to use \
        for the interpretation of truth values during the evauation of the \
        entailment.
        :type  attribute_interpretation: AttributeInterpretation

        :return: Whether or not \
        :math:`\gamma \models (\sigma^{\prime};\\rho^{\prime})`, \
        that is for all worlds :math:`(w;\widehat{\\rho})` and variable \
        assignments :math:`\chi`, \
        :math:`(w;\widehat{\\rho}) \models (\sigma^{\prime};\\rho^{\prime})` \
        whenever :math:`(w;\widehat{\\rho})\models_{\chi}\gamma`.
        :rtype: ``bool``

        :raises TypeError: ``named_state`` parameter must be a NamedState \
        object and ``attribute_interpretation`` parameter must be an \
        AttributeInterpretation object.
        :raises ValueError: This Context and the NamedState object provided \
        in the ``formula`` parameter must share the same underlying \
        Vocabulary object.
        """

        # Check for exceptions first.
        if not hasattr(named_state, "_is_NamedState"):
            raise TypeError(
                "named_state parameter must be of type NamedState")

        ns_vocabulary = named_state._p._vocabulary
        c_vocabulary = self._named_state._p._vocabulary

        if ns_vocabulary != c_vocabulary:
            raise ValueError(
                "named_state parameter must have the same Vocabulary in its "
                "ConstantAssignment as the Vocabulary of the "
                "ConstantAssignment within this Context.")

        # get all possible worlds and variable assignments.
        possible_worlds = self._named_state.get_worlds()

        # for every possible world and variable assignment, if the world
        # satisfies this Context, but not the NamedState, this Context does not
        # entail the NamedState, return False, otherwise return True aftewards.
        for world in possible_worlds:
            for X in world._generate_variable_assignments():
                satisfies_context = world.satisfies_context(
                    self, X, attribute_interpretation)
                satisfies_named_state = world.satisfies_named_state(
                    named_state)

                if satisfies_context and not satisfies_named_state:
                    return False
        return True


def main():
    """."""
    pass

if __name__ == "__main__":
    main()
