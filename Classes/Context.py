"""
This module proivdes a Context object for the Vivid framework.

Every Context is built from an AssumptionBase object and NamedState object.
"""

from State import NamedState
from F_and_AB import Formula, AssumptionBase
from Assignment import VariableAssignment

def generate_variable_assignments(variables, context):
    """
    Return a list of all possible VariableAssignments that can
    be created from the variables in variables parameter and
    the unmatched objects within Context object's
    NamedState object.

    note: this function is intended to be used internally from Context
    for the purpose of determining entailment only.
    """

    c_target = context.get_named_state().get_p().get_target()
    objects = context.get_named_state().get_attribute_system().get_objects()
    unmatched_objects = [obj for obj in objects if obj not in c_target]

    #get proper length of variable assignments
    if len(variables) <= len(unmatched_objects):
        smaller_length = len(variables)
    else:
        smaller_length = len(unmatched_objects)

    from itertools import product

    #get cartesian product of variables and objects such that the
    #products created are of the smaller cardinality.
    products = [
    zip(variables, item) for item in product(
            unmatched_objects, repeat=smaller_length)]

    #filter out the products with duplicate targets.
    mapping_list = []
    for product in products:
        product_objs = [p[1] for p in product]
        if len(product_objs) == len(set(product_objs)):
            mapping_list.append(dict(product))

    X_list = []

    #if there are variable terms and unmatched object, form all
    #possible VariableAssignments and store them in X_list,
    #otherwise return an empty list
    if smaller_length > 0:
        for mapping in mapping_list:
            X = VariableAssignment(
                context.get_named_state().get_vocabulary(),
                context.get_named_state().get_attribute_system(),
                mapping)

            X_list.append(X)

    return X_list

class Context(object):
    """
    This class represents a Context, that is, a pair composed of an
    AssumptionBase and a NamedState.
    """

    def __init__(self, beta, named_state):
        """
        Initialize a Context object with AssumptionBase beta and
        NamedState named_state.

        Raise TypeError if beta parameter is not of type AssumptionBase
        or if named_state parameter is not of type NamedState.
        """

        #Check for exceptions first.
        if not isinstance(beta, AssumptionBase):
            raise TypeError(
                "beta parameter must be of type AssumptionBase")
        if not isinstance(named_state, NamedState):
            raise TypeError(
                "named_state parameter must be of type NamedState")

        self._named_state = named_state
        self._assumption_base = beta

    def __eq__(self, other):
        """
        Determine if self == other where both are Context objects.
        """

        #if NamedStates or AssumptionBases aren't equal,
        #neither are Contexts.
        if self.get_named_state() != other.get_named_state():
            return False
        if self.get_assumption_base() != other.get_assumption_base():
            return False

        return True

    def __ne__(self, other):
        """
        Determine if self != other where both are Context objects.
        """

        #if NamedStates or AssumptionBases aren't equal,
        #neither are Contexts.
        if self.get_named_state() != other.get_named_state():
            return True
        if self.get_assumption_base() != other.get_assumption_base():
            return True

        return False

    def get_named_state(self):
        """Return this Context's NamedState object."""
        return self._named_state

    def set_named_state(self, named_state):
        """
        Set this Context's NamedState equal to named_state parameter.

        Raise TypeError if named_state parameter is not of type NamedState.
        Raise ValueError if named_state parameter's Vocabulary object is
        not equal to Vocabulary of AssumptionBase within this Context.
        """

        if not isinstance(named_state, NamedState):
            raise TypeError(
                "named_state parameter must be of type NamedState")

        beta_vocabulary = self.get_assumption_base().get_vocabulary()
        ns_vocabulary = named_state.get_p().get_vocabulary()

        if beta_vocabulary != ns_vocabulary:
            raise ValueError(
                "vocabulary used in NamedState's ConstantAssignment must "
                "match this Context's AssumptionBase's Vocabulary")

        self._named_state = named_state

    def get_assumption_base(self):
        """Return this Context's AssumptionBase object."""
        return self._assumption_base

    def set_assumption_base(self, beta):
        """
        Set this Context's AssumptionBase equal to beta parameter.

        Raise TypeError if beta parameter is not of type AssumptionBase.
        Raise ValueError if beta parameter's Vocabulary object is
        not equal to Vocabulary of NamedState within this Context.
        """

        if not isinstance(beta, AssumptionBase):
            raise TypeError(
                "beta parameter must be of type AssumptionBase")

        beta_vocabulary = beta.get_vocabulary()
        ns_vocabulary = self.get_named_state().get_p().get_vocabulary()

        if beta_vocabulary != ns_vocabulary:
            raise ValueError(
                "vocabulary used in NamedState's ConstantAssignment must "
                "match this Context's AssumptionBase's Vocabulary")

        self._assumption_base = beta

    def entails_formula(self, formula, interpretation_table=None):
        """
        Determine if this Context entails formula provided by
        formula parameter w.r.t. all worlds and possible variable
        assignments.

        Note: possible variable assignments are determined as follows:
        get terms of formula and extract the variables
        (in the formula's Vocabulary) from terms, then extract list of
        objects from this Context's NamedState's AttributeSystem.
        Filter the objects to those objects for which
        the ConstantAssignment does not have match; then take the
        Cartesian product of variables in terms and unmatched objects
        to form all possible VariableAssignments filtering out those
        products with duplicate objects.

        Raise TypeError if formula parameter is not of type Formula.
        Raise ValueError if Vocabulary of formula isn't equal to
        Vocabulary embedded in this Context's NamedState.
        """

        #Check for exceptions first.
        if not isinstance(formula, Formula):
            raise TypeError(
                "formula parameter must be of type Formula")

        f_vocabulary = formula.get_vocabulary()
        c_vocabulary = self.get_named_state().get_p().get_vocabulary()

        if f_vocabulary != c_vocabulary:
            raise ValueError(
                "Formula must be over the same vocabulary used to create"
                "ConstantAssignment within this Context.")

        #get list of variables from Formula terms
        terms = formula.get_terms()
        c_source = self.get_named_state().get_p().get_source()
        variables = [t for t in terms if t not in c_source]

        #get all possible worlds and variable assignments.
        possible_worlds = self.get_named_state().get_worlds()
        variable_assignments = generate_variable_assignments(variables, self)


        #if there are no variable assignments possible, add a dummy one.
        if not variable_assignments:
            dummy_X = VariableAssignment(f_vocabulary,
                self.get_named_state().get_attribute_system(), {},
                dummy=True)
            variable_assignments.append(dummy_X)

        #for every possible world and variable assignment, if the world
        #satisfies the context, but not the formula, this Context does not
        #entail the Formula, return False, otherwise return True aftewards.
        for X in variable_assignments:
            for world in possible_worlds:

                sats_context = world.satisfies_context(
                    self, X, f_vocabulary, interpretation_table)
                sats_formula = world.satisfies_formula(
                    formula, X, f_vocabulary, interpretation_table)

                if sats_context and not sats_formula:
                    return False

        return True

    def entails_named_state(self, named_state, interpretation_table=None):
        """
        Determine if this Context entails named_state provided by
        named_state parameter w.r.t. all worlds and possible variable
        assignments.

        NOTE: possible worlds are generated from NamedState of this
        Context and not from named_state parameter! The reasoning for
        this and not the converse is because in the event that all
        possible worlds are created from named_state parameter, then
        those worlds always satisfy named_state and thus this function
        can never return False.

        Note: possible variable assignments are determined as follows:
        get terms of formula and extract the variables
        (in the formula's Vocabulary) from terms, then extract list of
        objects from this Context's NamedState's AttributeSystem.
        Filter the objects to those objects for which
        the ConstantAssignment does not have match; then take the
        Cartesian product of variables in terms and unmatched objects
        to form all possible VariableAssignments filtering out those
        products with duplicate objects.

        Raise TypeError if named_state parameter is not of type
        NamedState.
        Raise ValueError if Vocabulary of named_state isn't equal to
        Vocabulary embedded in this Context's NamedState.
        """

        #Check for exceptions first.
        if not isinstance(named_state, NamedState):
            raise TypeError(
                "named_state parameter must be of type NamedState")

        ns_vocabulary = named_state.get_vocabulary()
        c_vocabulary = self.get_named_state().get_p().get_vocabulary()

        if ns_vocabulary != c_vocabulary:
            raise ValueError(
                "named_state parameter must have the same Vocabulary in its "
                "ConstantAssignment as the Vocabulary of the "
                "ConstantAssignment within this Context.")

        #get list of variabels from vocabulary V list.
        variables = ns_vocabulary.get_V()

        #get all possible worlds and variable assignments.
        possible_worlds = self.get_named_state().get_worlds()
        variable_assignments = generate_variable_assignments(variables, self)

        #if there are no variable assignments possible, add a dummy one.
        if not variable_assignments:
            dummy_X = VariableAssignment(ns_vocabulary,
                self.get_named_state().get_attribute_system(), {},
                dummy=True)
            variable_assignments.append(dummy_X)

        #for every possible world and variable assignment, if the world
        #satisfies this Context, but not the NamedState, this Context does not
        #entail the NamedState, return False, otherwise return True aftewards.
        for X in variable_assignments:
            for world in possible_worlds:

                sats_context = world.satisfies_context(
                    self, X, ns_vocabulary, interpretation_table)
                sats_named_state = world.satisfies_named_state(
                    named_state, ns_vocabulary)

                if sats_context and not sats_named_state:
                    return False
        return True

    def __str__(self):
        """Return string representation of this Context object."""
        context_str = str(self._named_state) + '\n'
        context_str += 'assumption base:' + '\n' + str(self._assumption_base)
        return context_str
