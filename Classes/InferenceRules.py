"""This module intends to provide the rules of diagrammatic inference."""

from vivid.Classes.Context import Context
from vivid.Classes.VariableAssignment import VariableAssignment


def thinning(context, named_state, assumption_base=None,
             attribute_interpretation=None):
    """
    Verify that named_state can be obtained by thinning from the NamedState
    contained in Context w.r.t. the AssumptionBase formed by assumption_base.

    By Corollary 26, is_named_entailment suffices to show thinning holds.
    """

    if not hasattr(context, "_is_Context"):
        raise TypeError("context parameter must be a Context object.")

    if not hasattr(named_state, "_is_NamedState"):
        raise TypeError("named_state parameter must be a NamedState object.")

    # If no assumption_base are provided, just do thinning for Named States,
    # otherwise, we're doing the full thinning inference rule
    if not assumption_base:
        return named_state <= context._named_state
    else:
        return context._named_state.is_named_entailment(
            assumption_base, attribute_interpretation, named_state)


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
    for formula in context._assumption_base:
        truth_value = formula.assign_truth_value(attribute_interpretation,
                                                 context._named_state,
                                                 variable_assignment)
        if truth_value is False:
            return True

    return False


def diagram_reiteration(context):
    """Perform Diagram Reiteration to retrieve the current diagram."""
    return context._named_state


def sentential_to_sentential(context, F1, F2, G, attribute_interpretation):
    """
    Verify that in the case of a disjunction F1 OR F2 holding a Context entails
    Formula G either way w.r.t. and AttributeInterpretation.
    """

    variable_assignment = VariableAssignment(
        context._named_state._p._vocabulary,
        context._named_state._attribute_system, {}, dummy=True)

    F1_holds = F1.assign_truth_value(attribute_interpretation,
                                     context._named_state,
                                     variable_assignment)

    F2_holds = F2.assign_truth_value(attribute_interpretation,
                                     context._named_state,
                                     variable_assignment)

    if F1_holds is False and F2_holds is False:
        raise ValueError("disjunction F1 OR F2 does not hold")

    f1_assumption_base = F1 + context._assumption_base
    f2_assumption_base = F2 + context._assumption_base

    f1_context = Context(f1_assumption_base, context._named_state)
    f2_context = Context(f2_assumption_base, context._named_state)

    f1_entails_g = f1_context.entails_formula(G, attribute_interpretation)
    f2_entails_g = f2_context.entails_formula(G, attribute_interpretation)

    if f1_entails_g and f2_entails_g:
        return True
    else:
        return False


def sentential_to_diagrammatic(context, F1, F2, named_state,
                               attribute_interpretation):
    """
    Verify that in the case of a disjunction F1 OR F2 holding a Context entails
    NamedState named_state either way w.r.t. and AttributeInterpretation.
    """

    variable_assignment = VariableAssignment(
        context._named_state._p._vocabulary,
        context._named_state._attribute_system, {}, dummy=True)

    F1_holds = F1.assign_truth_value(attribute_interpretation,
                                     context._named_state,
                                     variable_assignment)

    F2_holds = F2.assign_truth_value(attribute_interpretation,
                                     context._named_state,
                                     variable_assignment)

    if F1_holds is False and F2_holds is False:
        raise ValueError("disjunction F1 OR F2 does not hold")

    f1_assumption_base = F1 + context._assumption_base
    f2_assumption_base = F2 + context._assumption_base

    f1_context = Context(f1_assumption_base, context._named_state)
    f2_context = Context(f2_assumption_base, context._named_state)

    f1_entails_named_state = f1_context.entails_formula(
        named_state, attribute_interpretation)
    f2_entails_named_state = f2_context.entails_formula(
        named_state, attribute_interpretation)

    if f1_entails_named_state and f2_entails_named_state:
        return True
    else:
        return False


def main():
    """dev tests."""
    pass


if __name__ == "__main__":
    main()
