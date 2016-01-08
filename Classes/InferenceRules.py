"""This module intends to provide the rules of diagrammatic inference."""

from vivid.Classes.VariableAssignment import VariableAssignment
from vivid.Classes.AssumptionBase import AssumptionBase


def thinning(context, named_state, attribute_interpretation, *formulae):
    """
    Verify that named_state can be obtained by thinning from the NamedState
    contained in Context w.r.t. the AssumptionBase formed by formulae.

    By Corollary 26, is_named_entailment suffices to show thinning holds.
    """

    if not hasattr(context, "_is_Context"):
        raise TypeError("context parameter must be a Context object.")

    if not hasattr(named_state, "_is_NamedState"):
        raise TypeError("named_state parameter must be a NamedState object.")

    # If no formulae are provided, just do thinning for Named States,
    # otherwise, we're doing the full thinning inference rule
    if not formulae:
        return named_state <= context._named_state
    else:
        assumption_base = AssumptionBase(formulae)
        return context._named_state._is_named_entailment(
            assumption_base, attribute_interpretation, [named_state])


def widening(context, named_state, attribute_interpretation=None):
    """
    Verify that NamedState named_state can be obtained from Context context by
    widening.
    """

    if not hasattr(context, "_is_Context"):
        raise TypeError("context parameter must be a Context object.")

    if not hasattr(named_state, "_is_NamedState"):
        raise TypeError("named_state parameter must be a NamedState object.")

    if attribute_interpretation:
        context.entails_named_state(named_state, attribute_interpretation)

    return context._named_state <= named_state


def observe(context, formula, attribute_interpretation):
    """
    Determine if a given Formula can be observed in a given Context w.r.t. an
    AttributeInterpretation.
    """

    return context.entails_formula(formula, attribute_interpretation)


def diagrammatic_absurdity(context, named_state, attribute_interpretation,
                           variable_assignment=None):
    """Verify that NamedState named_state can be obtained from Context context by
    absurdity, i.e., there is some Fomrula in the Context's AssumptionBase that
    is False for every world derivable from the Context's NamedState w.r.t. the
    AttributeInterpretation and (optionally the VariableAssignment) provided.
    """
    if not hasattr(context, "_is_Context"):
        raise TypeError("context parameter must be a Context object.")

    if not hasattr(named_state, "_is_NamedState"):
        raise TypeError("named_state parameter must be a NamedState object.")

    # Create a dummy VariableAssignment if one isn't provided
    if not variable_assignment:
        variable_assignment = VariableAssignment(
            context._named_state._p._vocabulary,
            context._named_state._attribute_system, {}, dummy=True)

    # For each Formula in the Context's AssumptionBase, if a Formula always
    # evaulates to False, absurdity holds
    for formula in context._assumption_base:
        truth_value = formula.assign_truth_value(attribute_interpretation,
                                                 context._named_state,
                                                 variable_assignment)

        if truth_value is False:
            return True

    return False


def sentential_absurdity(context, formula, attribute_interpretation,
                         variable_assignment=None):
    """Verify that NamedState named_state can be obtained from Context context by
    absurdity, i.e., there is some Fomrula in the Context's AssumptionBase that
    is False for every world derivable from the Context's NamedState w.r.t. the
    AttributeInterpretation and (optionally the VariableAssignment) provided.
    """
    if not hasattr(context, "_is_Context"):
        raise TypeError("context parameter must be a Context object.")

    if not hasattr(formula, "_is_Formula"):
        raise TypeError("formula parameter must be a Formula object.")

    # Create a dummy VariableAssignment if one isn't provided
    if not variable_assignment:
        variable_assignment = VariableAssignment(
            context._named_state._p._vocabulary,
            context._named_state._attribute_system, {}, dummy=True)

    # For each Formula in the Context's AssumptionBase, if a Formula always
    # evaulates to False, absurdity holds
    for f in context._assumption_base:
        truth_value = f.assign_truth_value(attribute_interpretation,
                                           context._named_state,
                                           variable_assignment)

        if truth_value is False:
            return True

    return False


def diagram_reiteration(context, named_state=None):
    """Perform Diagram Reiteration to retrieve the current diagram."""
    if named_state:
        if not hasattr(named_state, "_is_NamedState"):
            raise TypeError(
                "named_state parameter must be a NamedState object")
            if context._named_state != named_state:
                raise ValueError(
                    "named_state parameter must match NamedState object "
                    "within Context context")

            return named_state

    return context._named_state


def main():
    """dev tests."""
    pass


if __name__ == "__main__":
    main()
