# -*- coding: utf-8 -*-
"""This module provides the rules of diagrammatic inference."""

from formula import Formula
from assumption_base import AssumptionBase
from context import Context
from variable_assignment import VariableAssignment


def thinning(context, named_state, assumption_base=None,
             attribute_interpretation=None):
    """
    Verify that the NamedState object :math:`(\sigma^{\prime};\\rho^{\prime})`
    in the ``named_state`` parameter can be obtained by thinning from the
    NamedState object :math:`(\sigma;\\rho)` contained in the Context object
    :math:`(\\beta;(\sigma;\\rho))` in the ``context`` parameter w.r.t. the
    AssumptionBase object :math:`\{F_{1}, \ldots, F_{n}\}` given by the
    ``assumption_base`` parameter, using the AttributeInterpretation object
    :math:`I` in the ``attribute_interpretation`` parameter to interpret truth
    values.

    By Corollary 26, if
    :math:`(\sigma;\\rho) \\Vvdash_{\{F_{1}, \ldots, F_{n}\}} \
    (\sigma^{\prime};\\rho^{\prime})`
    then
    :math:`(\{F_{1}, \ldots, F_{n}\}; (\sigma; \\rho)) \models \
    (\sigma^{\prime};\\rho^{\prime})`.

    Then, by weakening, :math:`(\\beta \cup \{F_{1}, \ldots, F_{n}\}; \
    (\sigma; \\rho)) \models (\sigma^{\prime};\\rho^{\prime})` and thinning
    holds, thus it suffices to show that a call to ``entails_named_state`` with
    context :math:`(\{F_{1}, \ldots, F_{n}\};(\sigma;\\rho))` and named state
    :math:`(\sigma^{\prime};\\rho^{\prime})`, that is
    :math:`(\sigma;\\rho) \\Vvdash_{\{F_{1}, \ldots, F_{n}\}} \
    (\sigma^{\prime};\\rho^{\prime})`, holds to show that thinning holds.

    :param context: The Context object :math:`(\\beta;(\sigma;\\rho))`.
    :type  context: Context
    :param named_state: The NamedState object \
    :math:`(\sigma^{\prime};\\rho^{\prime})`
    :type  named_state: NamedState
    :param assumption_base: The set of Formula objects to thin with \
    :math:`\{F_{1},\ldots, F_{n}\}` if thinning is to be done with any \
    Formula (i.e., :math:`n > 0`), otherwise ``None``.
    :type  assumption_base: AssumptionBase | ``None``
    :param attribute_interpretation: The AttributeInterpretation object \
    :math:`I` to use to interpret truth values if :math:`n > 0`, otherwise \
    ``None``.
    :type  attribute_interpretation: AttributeInterpretation | ``None``

    :return: Whether or not thinning holds, i.e., the result of \
    :math:`(\sigma;\\rho) \\Vvdash_{\{F_{1}, \ldots, F_{n}\}} \
    (\sigma^{\prime};\\rho^{\prime})`
    :rtype: ``bool``

    :raises TypeError: ``context`` parameter must be a Context object and \
    ``named_state`` parameter must be a NamedState object.
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
        return proviso


def widening(context, named_state, attribute_interpretation=None):
    """
    Verify that the NamedState object :math:`(\sigma^{\prime};\\rho^{\prime})`
    in the ``named_state`` parameter can be obtained from the Context object
    :math:`(\\beta;(\sigma;\\rho))` in the ``context`` parameter by widening,
    using the AttributeInterpretation object :math:`I` in the
    ``attribute_interpretation`` parameter to interpret truth values.

    :param context: The Context object :math:`(\\beta;(\sigma;\\rho))`.
    :type  context: Context
    :param named_state: The NamedState object \
    :math:`(\sigma^{\prime};\\rho^{\prime})`
    :type  named_state: NamedState
    :param attribute_interpretation: The AttributeInterpretation object \
    :math:`I` to use to interpret truth values if widening should consider \
    the AssumptionBase object of the ``context`` parameter, otherwise ``None``.
    :type  attribute_interpretation: AttributeInterpretation | ``None``

    :return: Whether or not the NamedState object \
    :math:`(\sigma^{\prime};\\rho^{\prime})` in the ``named_state`` parameter \
    can be obtained from the Context object :math:`(\\beta;(\sigma;\\rho))` \
    in the ``context`` parameter by widening, i.e., whether or not \
    :math:`(\\beta;(\sigma;\\rho)) \models (\sigma^{\prime};\\rho^{\prime})`
    :rtype: ``bool``

    :raises TypeError: ``context`` parameter must be a Context object and \
    ``named_state`` parameter must be a NamedState object.
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
    Determine if the Formula object :math:`F` given by the ``formula``
    parameter can be observed in the Context object
    :math:`(\\beta;(\sigma;\\rho))` given by the ``context`` parameter, using
    the AttributeInterpretation object :math:`I` in the
    ``attribute_interpretation`` parameter to interpret truth values, i.e.,
    determine if **observe** :math:`F` holds in
    :math:`(\\beta;(\sigma;\\rho))`.

    :param context: The Context object :math:`(\\beta;(\sigma;\\rho))` in \
    which the Formula object :math:`F` can potentially be observed.
    :type  context: Context
    :param formula: The (potentially) observable Formula object :math:`F`.
    :type  formula: Formula
    :param attribute_interpretation: The AttributeInterpretation object \
    :math:`I` to use to interpet truth values in the ``context`` and \
    ``formula`` parameters.
    :type  attribute_interpretation: AttributeInterpretation

    :return: Whether or not **observe** *F* holds in \
    :math:`(\\beta;(\sigma;\\rho))`, that is, whether or not \
    :math:`(\\beta;(\sigma;\\rho)) \models F`.
    :rtype: ``bool``
    """

    return context.entails_formula(formula, attribute_interpretation)


def diagrammatic_absurdity(context, named_state, attribute_interpretation):
    """
    Verify that the NamedState object :math:`(\sigma^{\prime};\\rho^{\prime})`
    in the ``named_state`` parameter can be obtained from the Context object
    :math:`(\\beta;(\sigma;\\rho))` in the ``context`` parameter by absurdity,
    using the AttributeInterpretation object :math:`I` provided in the
    ``attribute_interpretation`` parameter to interpet truth values.

    To show :math:`(\sigma^{\prime};\\rho^{\prime})` **by absurdity**, we must
    show :math:`(\\beta \cup \{\\textbf{false}\}; (\sigma;\\rho)) \
    \models (\sigma^{\prime};\\rho^{\prime})`.

    By lemma 20, :math:`(\\beta \cup \{\\textbf{false}\}; (\sigma;\\rho)) \
    \models (\sigma^{\prime};\\rho^{\prime})`, thus it suffices to show that
    a call to ``entails_named_state`` with context
    :math:`(\\beta;(\sigma;\\rho))` and named state
    :math:`(\sigma^{\prime};\\rho^{\prime})`, that is,
    :math:`(\\beta;(\sigma;\\rho)) \models (\sigma^{\prime};\\rho^{\prime})`
    holds, implicitly assuming that some :math:`F \in \\beta` evaulates
    to **false** (as then no world can satisify the context, i.e., for any
    world :math:`(w; \widehat{\\rho})` derivable from the context
    :math:`(\\beta;(\sigma;\\rho))`,
    :math:`(w; \widehat{\\rho}) \\not\models_{\chi} (\\beta;(\sigma;\\rho))`
    and thus ``entails_named_state`` will always hold yielding
    :math:`(\sigma^{\prime};\\rho^{\prime})` **by absurdity** regardless of
    the NamedState object :math:`(\sigma^{\prime};\\rho^{\prime})` provided in
    the ``named_state`` parameter)

    :param context: The Context object :math:`(\\beta;(\sigma;\\rho))`.
    :type  context: Context
    :param named_state: The NamedState object \
    :math:`(\sigma^{\prime};\\rho^{\prime})`.
    :type  named_state: NamedState
    :param attribute_interpretation:
    :type  attribute_interpretation: AttributeInterpretation

    :return: Whether or not :math:`(\sigma^{\prime};\\rho^{\prime})` \
    **by absurdity**, that is, whether or not :math:`(\\beta;(\sigma;\\rho)) \
    \models (\sigma^{\prime};\\rho^{\prime})` holds.
    :rtype: ``bool``

    :raises TypeError: ``context`` parameter must be a Context object, \
    ``named_state`` parameter must be a NamedState object and \
    ``attribute_interpretation`` parameter must be an AttributeInterpretation \
    object.
    """

    if not hasattr(context, "_is_Context"):
        raise TypeError("context parameter must be a Context object.")

    if not hasattr(named_state, "_is_NamedState"):
        raise TypeError("named_state parameter must be a NamedState object.")

    if not hasattr(attribute_interpretation, "_is_AttributeInterpretation"):
        raise TypeError(
            "attribute_interpretation parameter must be a "
            "AttributeInterpretation object.")

    return context.entails_named_state(named_state, attribute_interpretation)


def diagram_reiteration(context):
    """
    Perform :math:`[Diagram-Reiteration]` to retrieve the current diagram of
    the Context object :math:`(\\beta;(\sigma;\\rho))` provided in the
    ``context`` parameter, i.e., from lemma 19:
    :math:`(\\beta;(\sigma;\\rho)) \models (\sigma;\\rho)`.

    :param context: The Context object :math:`(\\beta;(\sigma;\\rho))` from \
    which to retrieve the current NamedState object :math:`(\sigma;\\rho)`.
    :type  context: Context

    :return: The NamedState object :math:`(\sigma;\\rho)` of the Context \
    object :math:`(\\beta;(\sigma;\\rho))` in ``context`` parameter.
    :rtype: NamedState
    """

    return context._named_state


def sentential_to_sentential(context, F1, F2, G, attribute_interpretation,
                             variable_assignment=None):
    """
    Verify that a disjunction :math:`F_{1} \lor F_{2}` holds in the Context
    object :math:`(\\beta;(\sigma;\\rho))` in the ``context`` parameter and
    that the Formula object :math:`G` in the ``G`` parameter follows in either
    case, using the AttributeInterpretation object :math:`I` in the
    ``attribute_interpretation`` parameter to interpret truth values.

    To perform the **sentential-to-sentential** inference, first the
    disjunction :math:`F_{1} \lor F_{2}` is verified. Then the truth values of
    :math:`F_{1} \Rightarrow G` and :math:`F_{1} \Rightarrow G` are determined.
    If either :math:`F_{1} \Rightarrow G` or :math:`F_{1} \Rightarrow G` do not
    hold, then **sentential-to-sentential** does not hold, otherwise,
    **sentential-to-sentential** holds.

    :param context: The Context object :math:`(\\beta;(\sigma;\\rho))` in \
    which the the Formula objects in the parameters ``F1``, ``F2`` apply and \
    in which the Formula object in the ``G`` parameter would follow.
    :type  context: Context
    :param F1: The left operand of the disjunction :math:`F_{1}`.
    :type  F1: Formula
    :param F2: The right operand of the disjunction :math:`F_{2}`.
    :type  F2: Formula
    :param G: The Formula object :math:`G` potentially following the \
    disjunction in either case.
    :type  G: Formula
    :param attribute_interpretation: The AttributeInterpretation object \
    :math:`I` to use for interpeting truth values.
    :type  attribute_interpretation: AttributeInterpretation
    :param variable_assignment: The optional VariableAssignment object \
    :math:`\chi` to consider in the interpretation of truth values.
    :type  variable_assignment: VariableAssignment | ``None``

    :return: Whether or not **sentential-to-sentential** holds.
    :rtype: ``bool``

    :raises ValueError: The disjunction :math:`F_{1} \lor F_{2}` does not hold.
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
    Verify that on the basis of the present diagram :math:`(\sigma;\\rho)` of
    the Context object :math:`(\\beta;(\sigma;\\rho))` in the ``context``
    parameter and some set of Formula objects
    :math:`F_{1}, \ldots, F_{k}, k \ge 0` provided as optional positional
    arguments in the ``formulae`` parameter, that for each NamedState object
    :math:`(\sigma_{1}; \\rho_{1}), \ldots,(\sigma_{n}; \\rho_{n}), n > 0`,
    contained in the ``named_states`` parameter, a NamedState object
    :math:`(\sigma^{\prime};\\rho^{\prime})` provided in the
    ``inferred_named_state`` parameter can be derived in every one of these
    :math:`n` cases.

    This is rule :math:`[C_{1}]`.

    This function works as follows:

    1. If :math:`k > 0` (i.e., if at least one Formula object is provided as an
    optional positional argument to the ``formulae`` parameter), compute the
    basis :math:`\mathcal{B}(F_{1}, \\rho, \chi) ~ \cup ~ \cdots ~ \cup ~ \
    \mathcal{B}(F_{k}, \\rho, \chi)` of :math:`F_{1}, \ldots, F_{k}` and
    determine if the NamedState objects
    :math:`(\sigma_{1}; \\rho_{1}), \ldots,(\sigma_{n}; \\rho_{n})`
    provided in the ``named_states`` parameter form an exhuastive set of
    possibilities on this basis.

    2. Determine if the proviso
    :math:`(\sigma;\\rho) \\Vvdash_{\{F_{1}, \ldots, F_{k}\}} \
    \{(\sigma_{1}; \\rho_{1}), \ldots,(\sigma_{n}; \\rho_{n})\}` (where
    :math:`k \ge 0`) holds.

    3. Return the evaluation of
    :math:`(\\beta \cup \{F_{1}, \ldots, F_{k}\};(\sigma;\\rho)) \models \
    (\sigma^{\prime};\\rho^{\prime})`.

    :param context: The Context object :math:`(\\beta;(\sigma;\\rho))` from \
    which the present diagram :math:`(\sigma;\\rho)` comes from.
    :type  context: Context
    :param inferred_named_state: The NamedState object \
    :math:`(\sigma^{\prime};\\rho^{\prime})` derivable in the :math:`n > 0` \
    cases provided by the NamedState objects \
    :math:`(\sigma_{1}; \\rho_{1}), \ldots,(\sigma_{n}; \\rho_{n})` in the \
    ``named_state`` parameter.
    :type  inferred_named_state: NamedState
    :param named_states: The NamedState objects \
    :math:`(\sigma_{1}; \\rho_{1}), \ldots,(\sigma_{n}; \\rho_{n}), n > 0` \
    functioning as the set of :math:`n` exhaustive cases from which :math:`F` \
    can be derived.
    :type  named_states: ``list``
    :param attribute_interpretation: The AttributeInterpretation object \
    :math:`I` to use for the interpretation of truth values and the \
    computation of the basis of :math:`F_{1}, \ldots, F_{k}`.
    :type  attribute_interpretation: AttributeInterpretation
    :param variable_assignment: The VariableAssignment object :math:`\chi` to \
    consider when computing the basis \
    :math:`\mathcal{B}(F_{1}, \\rho, \chi) ~ \cup ~ \cdots ~ \cup ~ \
    \mathcal{B}(F_{k}, \\rho, \chi)` of :math:`F_{1}, \ldots, F_{k}` or \
    ``None`` if all terms of the :math:`F_{1}, \ldots, F_{k}` are in \
    :math:`\\rho`.
    :type  variable_assignment: VariableAssignment | ``None``
    :param formulae: The :math:`{k \ge 0}` Formula objects \
    :math:`F_{1}, \ldots, F_{k}` to use in the computation of the basis, \
    computation of the proviso and the evaluation of \
    :math:`{(\\beta \cup \{F_{1}, \ldots, F_{k}\};(\sigma;\\rho)) \models \
    (\sigma^{\prime};\\rho^{\prime})}`.
    :type  formulae: Formula

    :return: The result of the evaluation of \
    :math:`(\\beta \cup \{F_{1}, \ldots, F_{k}\};(\sigma;\\rho)) \models \
    (\sigma^{\prime};\\rho^{\prime})`.
    :rtype: ``bool``

    :raises ValueError: If :math:`{k > 0}`, the NamedState objects \
    :math:`{(\sigma_{1}; \\rho_{1}), \ldots,(\sigma_{n}; \\rho_{n}), n > 0}` \
    are not exhaustive on the basis of the Formula objects \
    :math:`F_{1}, \ldots, F_{k}` or the proviso \
    :math:`{(\sigma;\\rho) \\Vvdash_{\{F_{1}, \ldots, F_{k}\}} \
    \{(\sigma_{1}; \\rho_{1}), \ldots,(\sigma_{n}; \\rho_{n})\}}` (where \
    :math:`k \ge 0`) does not hold.
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
    Verify that a disjunction :math:`F_{1} \lor F_{2}` holds in the Context
    object :math:`(\\beta;(\sigma;\\rho))` in the ``context`` parameter and
    that the NamedState object :math:`(\sigma^{\prime};\\rho^{\prime})` in the
    ``named_state`` parameter follows in either case, using the
    AttributeInterpretation object :math:`I` in the
    ``attribute_interpretation`` parameter to interpet truth values.

    This is rule :math:`[C_{2}]`.

    This function works as follows:

    1. Verify that the disjunction :math:`F_{1} \cup F_{2}` given by ``F1`` and
    ``F2`` parameters holds in the Context object
    :math:`(\\beta;(\sigma;\\rho))` given by ``context`` parameter.

    2. Generate two new Context objects
    :math:`\gamma_{1} = (\\beta_{1};(\sigma;\\rho))` where
    :math:`\\beta_{1} = \\beta \cup F_{1}` and
    :math:`\gamma_{2} = (\\beta_{2};(\sigma;\\rho))` where
    :math:`\\beta_{2} = \\beta \cup F_{2}`.

    3. For all possible worlds
    :math:`\Big(w^{\prime};\widehat{\\rho^{\prime}}\Big)` and variable
    assignments :math:`\chi` of the NamedState object
    :math:`(\sigma^{\prime};\\rho^{\prime})`, determine if the world
    :math:`\Big(w^{\prime};\widehat{\\rho^{\prime}}\Big)` satisfies both
    Context objects :math:`\gamma_{1}` and :math:`\gamma_{2}`, that is
    :math:`\Big(w^{\prime};\widehat{\\rho^{\prime}}\Big) \models \gamma_{1} \
    ~ \\bigwedge ~`
    :math:`\Big(w^{\prime};\widehat{\\rho^{\prime}}\Big) \models \gamma_{2}`.

    4. If any world :math:`\Big(w^{\prime};\widehat{\\rho^{\prime}}\Big)` and
    variable assignments :math:`\chi` of the NamedState object
    :math:`(\sigma^{\prime};\\rho^{\prime})` does not satisify both
    :math:`\gamma_{1}` and :math:`\gamma_{2}`, then
    **sentential-to-diagrammatic** does not hold, otherwise,
    **sentential-to-diagrammatic** holds.

    In this way, we capture the idea that any world
    :math:`\Big(w^{\prime};\widehat{\\rho^{\prime}}\Big)` and variable
    assignments :math:`\chi` of the NamedState object
    :math:`(\sigma^{\prime};\\rho^{\prime})` (and thus the NamedState object
    :math:`(\sigma^{\prime};\\rho^{\prime})` itself) follows from the context
    :math:`(\\beta \cup \{F_{1} \lor F_{2}\};(\sigma;\\rho))` in either case of
    the disjunction :math:`F_{1} \lor F_{2}`.

    :param context: The Context object :math:`(\\beta;(\sigma;\\rho))` in \
    which the Formula objects in the parameters ``F1`` and ``F2`` apply and \
    in which the NamedState object :math:`(\sigma^{\prime};\\rho^{\prime})` \
    in ``named_state`` parameter would follow.
    :type  context: Context
    :param F1: The left operand of the disjunction :math:`F_{1}`.
    :type  F1: Formula
    :param F2: The right operand of the disjunction :math:`F_{2}`.
    :type  F2: Formula
    :param named_state: The NamedState object \
    :math:`(\sigma^{\prime};\\rho^{\prime})` potentially following the \
    disjunction in either case.
    :type  named_state: NamedState
    :param attribute_interpretation: The AttributeInterpretation object \
    :math:`I` to use for the interpretation of truth values.
    :type  attribute_interpretation: AttributeInterpretation
    :param variable_assignment: The optional VariableAssignment object \
    :math:`\chi` to consider in the interpretation of truth values.
    :type  variable_assignment: VariableAssignment | ``None``

    :return: Whether or not **sentential-to-diagrammatic** holds.
    :rtype: ``bool``

    :raises ValueError: The disjunction :math:`F_{1} \lor F_{2}` does not hold.
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
    Verify that on the basis of the present diagram :math:`(\sigma;\\rho)` of
    the Context object :math:`(\\beta;(\sigma;\\rho))` in the ``context``
    parameter and some set of Formula objects
    :math:`F_{1}, \ldots, F_{k}, k \ge 0` provided as optional positional
    arguments in the ``formulae`` parameter, that for each NamedState object
    :math:`(\sigma_{1}; \\rho_{1}), \ldots,(\sigma_{n}; \\rho_{n}), n > 0`,
    contained in the ``named_states`` parameter, a Formula object :math:`F`
    provided in the ``F`` parameter can be derived in every one of these
    :math:`n` cases.

    This is rule :math:`[C_{3}]`.

    This function works as follows:

    1. If :math:`k > 0` (i.e., if at least one Formula object is provided as an
    optional positional argument to the ``formulae`` parameter),  compute the
    basis :math:`\mathcal{B}(F_{1}, \\rho, \chi) ~ \cup ~ \cdots ~ \cup ~ \
    \mathcal{B}(F_{k}, \\rho, \chi)` of :math:`F_{1}, \ldots, F_{k}` and
    determine if the NamedState objects
    :math:`(\sigma_{1}; \\rho_{1}), \ldots,(\sigma_{n}; \\rho_{n})`
    provided in the ``named_states`` parameter form an exhuastive set of
    possibilities on this basis.

    2. Determine if the proviso
    :math:`(\sigma;\\rho) \\Vvdash_{\{F_{1}, \ldots, F_{k}\}} \
    \{(\sigma_{1}; \\rho_{1}), \ldots,(\sigma_{n}; \\rho_{n})\}` (where
    :math:`k \ge 0`) holds.

    3. Return the evaluation of
    :math:`(\\beta \cup \{F_{1}, \ldots, F_{k}\};(\sigma;\\rho)) \models F`.

    :param context: The Context object :math:`(\\beta;(\sigma;\\rho))` from \
    which the present diagram :math:`(\sigma;\\rho)` comes from.
    :type  context: Context
    :param F: The Formula object :math:`F` derivable in the :math:`n > 0` \
    cases provided by the NamedState objects \
    :math:`(\sigma_{1}; \\rho_{1}), \ldots,(\sigma_{n}; \\rho_{n})` in the \
    ``named_state`` parameter.
    :type  F: Formula
    :param named_states: The NamedState objects \
    :math:`(\sigma_{1}; \\rho_{1}), \ldots,(\sigma_{n}; \\rho_{n}), n > 0` \
    functioning as the set of :math:`n` exhaustive cases from which :math:`F` \
    can be derived.
    :type  named_states: ``list``
    :param attribute_interpretation: The AttributeInterpretation object \
    :math:`I` to use for the interpretation of truth values and the \
    computation of the basis of :math:`F_{1}, \ldots, F_{k}`.
    :type  attribute_interpretation: AttributeInterpretation
    :param variable_assignment: The VariableAssignment object :math:`\chi` to \
    consider when computing the basis \
    :math:`\mathcal{B}(F_{1}, \\rho, \chi) ~ \cup ~ \cdots ~ \cup ~ \
    \mathcal{B}(F_{k}, \\rho, \chi)` of :math:`F_{1}, \ldots, F_{k}` or \
    ``None`` if all terms of the :math:`F_{1}, \ldots, F_{k}` are in \
    :math:`\\rho`.
    :type  variable_assignment: VariableAssignment | ``None``
    :param formulae: The :math:`{k \ge 0}` Formula objects \
    :math:`F_{1}, \ldots, F_{k}` to use in the computation of the basis, \
    computation of the proviso and the evaluation of \
    :math:`{(\\beta \cup \{F_{1}, \ldots, F_{k}\};(\sigma;\\rho)) \models F}`.
    :type  formulae: Formula

    :return: The result of the evaluation of \
    :math:`(\\beta \cup \{F_{1}, \ldots, F_{k}\};(\sigma;\\rho)) \models F`.
    :rtype: ``bool``

    :raises ValueError: If :math:`{k > 0}`, the NamedState objects \
    :math:`{(\sigma_{1}; \\rho_{1}), \ldots,(\sigma_{n}; \\rho_{n}), n > 0}` \
    are not exhaustive on the basis of the Formula objects \
    :math:`F_{1}, \ldots, F_{k}` or the proviso \
    :math:`{(\sigma;\\rho) \\Vvdash_{\{F_{1}, \ldots, F_{k}\}} \
    \{(\sigma_{1}; \\rho_{1}), \ldots,(\sigma_{n}; \\rho_{n})\}}` (where \
    :math:`k \ge 0`) does not hold.
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
