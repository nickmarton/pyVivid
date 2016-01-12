# -*- coding: utf-8 -*-
"""This module intends to provide the rules of diagrammatic inference."""

from Formula import Formula
from AssumptionBase import AssumptionBase
from Context import Context
from VariableAssignment import VariableAssignment


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
        proviso = context._named_state.is_named_entailment(
            assumption_base, attribute_interpretation, named_state)

        if not proviso:
            raise ValueError("Thinning Proviso does not hold")

        extended_context = Context(assumption_base, context._named_state)
        if extended_context.entails_named_state(
                named_state, attribute_interpretation):
            return True
        else:
            return False


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
    absurdity, i.e., there is some Formula in the Context's AssumptionBase that
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


def sentential_to_sentential(context, F1, F2, G, attribute_interpretation,
                             variable_assignment=None):
    """
    Verify that in the case of a disjunction F1 ∨ F2 holding a Context entails
    Formula G either way w.r.t. and AttributeInterpretation.
    """

    if not variable_assignment:
        variable_assignment = VariableAssignment(
            context._named_state._p._vocabulary,
            context._named_state._attribute_system, {}, dummy=True)

    F1_holds = F1.assign_truth_value(attribute_interpretation,
                                     context._named_state,
                                     variable_assignment)

    F2_holds = F2.assign_truth_value(attribute_interpretation,
                                     context._named_state,
                                     variable_assignment)

    if F1_holds is not True and F2_holds is not True:
        raise ValueError("disjunction F1 OR F2 does not hold")

    G_holds = G.assign_truth_value(attribute_interpretation,
                                   context._named_state,
                                   variable_assignment)

    if F1_holds and not G_holds:
        return False

    if F2_holds and not G_holds:
        return False

    return True


def diagrammatic_to_diagrammatic(context, inferred_named_state, named_states,
                                 attribute_interpretation, variable_assignment,
                                 *formulae):
    """
    Verify that on the basis of the present diagram and some formulas F1,...,Fk
    contained in formulae, k >= 0, that for each named_state
    (σ1; ρ1),...,(σn; ρn), n > 0, contained in named_states, a named state
    (σ'; ρ') can be derived in every one of these n cases.

    This is rule [C1].
    """

    if formulae:
        constant_assignment = context._named_state._p
        basis = Formula.get_basis(constant_assignment, variable_assignment,
                                  attribute_interpretation, *formulae)

        if not context._named_state.is_exhaustive(basis, *named_states):
            raise ValueError(
                "named states are not exahustive on basis of formulae.")

        assumption_base = AssumptionBase(*formulae)
    else:
        assumption_base = AssumptionBase(context._assumption_base._vocabulary)

    proviso = context._named_state.is_named_entailment(
        assumption_base, attribute_interpretation, *named_states)

    if not proviso:
        raise ValueError("[C1] proviso does not hold")

    formulae_union = context._assumption_base._formulae + list(formulae)
    if formulae_union:
        assumption_base_union = AssumptionBase(*formulae_union)
    else:
        assumption_base_union = AssumptionBase(
            context._assumption_base._vocabulary)

    # Determine if (β ∪ {F1,...,Fk}; (σ; ρ)) |= (σ'; ρ'); proviso holds at this
    # point
    extended_context = Context(assumption_base_union, context._named_state)
    if extended_context.entails_named_state(inferred_named_state,
                                            attribute_interpretation):
        return True
    else:
        return False


def sentential_to_diagrammatic(context, F1, F2, named_state,
                               attribute_interpretation,
                               variable_assignment=None):
    """
    Verify that in the case of a disjunction F1 ∨ F2 holding a Context entails
    NamedState named_state either way w.r.t. and AttributeInterpretation.

    This is rule [C2].
    """

    if not variable_assignment:
        variable_assignment = VariableAssignment(
            context._named_state._p._vocabulary,
            context._named_state._attribute_system, {}, dummy=True)

    F1_holds = F1.assign_truth_value(attribute_interpretation,
                                     context._named_state,
                                     variable_assignment)

    F2_holds = F2.assign_truth_value(attribute_interpretation,
                                     context._named_state,
                                     variable_assignment)

    if F1_holds is not True and F2_holds is not True:
        raise ValueError("disjunction F1 OR F2 does not hold")

    if F1 not in context._assumption_base:
        f1_assumption_base = F1 + context._assumption_base
    else:
        f1_assumption_base = context._assumption_base

    if F2 not in context._assumption_base:
        f2_assumption_base = F2 + context._assumption_base
    else:
        f2_assumption_base = context._assumption_base

    f1_context = Context(f1_assumption_base, context._named_state)
    f2_context = Context(f2_assumption_base, context._named_state)

    # get all possible worlds and variable assignments of given named state;
    # because the worlds come from the entailed named state but the contexts
    # use the original context's named state, we're showing that
    # (β ∪ {F1 ∨ F2}; (σ; ρ)) |= (σ'; ρ') by showing that in the case of either
    # F1 or F2, all worlds of the entailed state satisify both contexts and
    # thus (σ'; ρ') follows either way
    possible_worlds = named_state.get_worlds()

    for world in possible_worlds:
        for X in world._generate_variable_assignments():
            satisfies_f1_context = world.satisfies_context(
                f1_context, X, attribute_interpretation)
            satisfies_f2_context = world.satisfies_context(
                f2_context, X, attribute_interpretation)

            if not satisfies_f1_context or not satisfies_f2_context:
                return False
    return True


def diagrammatic_to_sentential(context, F, named_states,
                               attribute_interpretation, variable_assignment,
                               *formulae):
    """
    Verify that on the basis of the present diagram and some formulas F1,...,Fk
    contained in formulae, k >= 0, that for each named_state
    (σ1; ρ1),...,(σn; ρn), n > 0, contained in named_states, a named state
    (σ'; ρ') can be derived in every one of these n cases.

    This is rule [C3].
    """

    if formulae:
        constant_assignment = context._named_state._p
        basis = Formula.get_basis(constant_assignment, variable_assignment,
                                  attribute_interpretation, *formulae)

        if not context._named_state.is_exhaustive(basis, *named_states):
            raise ValueError(
                "named states are not exahustive on basis of formulae.")

        assumption_base = AssumptionBase(*formulae)
    else:
        assumption_base = AssumptionBase(context._assumption_base._vocabulary)

    proviso = context._named_state.is_named_entailment(
        assumption_base, attribute_interpretation, *named_states)

    if not proviso:
        raise ValueError("[C3] proviso does not hold")

    formulae_union = context._assumption_base._formulae + list(formulae)
    if formulae_union:
        assumption_base_union = AssumptionBase(*formulae_union)
    else:
        assumption_base_union = AssumptionBase(
            context._assumption_base._vocabulary)

    # Determine if (β ∪ {F1,...,Fk}; (σ; ρ)) |= F; proviso holds at this point
    extended_context = Context(assumption_base_union, context._named_state)
    if extended_context.entails_formula(F, attribute_interpretation):
        return True
    else:
        return False


def main():
    """dev tests."""
    pass


if __name__ == "__main__":
    main()
