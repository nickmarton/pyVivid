"""Context class."""


class Context(object):
    """
    This class represents a Context, that is, a pair composed of an
    AssumptionBase and a NamedState.
    """

    def __init__(self, assumption_base, named_state):
        """Construct a Context object."""

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
        """Determine if self == other where both are Context objects."""
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
        """Implement != operator for Context objects."""
        return not self.__eq__(other)

    def __str__(self):
        """Return string representation of this Context object."""
        context_str = str(self._named_state) + '\n'
        context_str += str(self._assumption_base)
        return context_str

    def __repr__(self):
        """Implement repr(Context)."""
        return self.__str__()

    def __deepcopy__(self, memo):
        """Implement copy.deepcopy for Context object."""
        from copy import deepcopy
        return Context(deepcopy(self._assumption_base),
                       deepcopy(self._named_state))

    def entails_formula(self, formula, attribute_interpretation):
        """
        Determine if this Context entails formula provided by
        formula parameter w.r.t. all worlds and possible variable
        assignments.

        Raise TypeError if formula parameter is not of type Formula.
        Raise ValueError if Vocabulary of formula isn't equal to
        Vocabulary embedded in this Context's NamedState.
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
        Determine if this Context entails named_state provided by
        named_state parameter w.r.t. all worlds and possible variable
        assignments.

        Raise TypeError if named_state parameter is not of type
        NamedState.
        Raise ValueError if Vocabulary of named_state isn't equal to
        Vocabulary embedded in this Context's NamedState.
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
