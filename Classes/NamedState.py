"""Named State class."""

from State import Attribute, Relation, AttributeStructure, AttributeSystem, State
from RelationSymbol import RelationSymbol
from Vocabulary import Vocabulary
from ConstantAssignment import ConstantAssignment
from VariableAssignment import VariableAssignment

def generate_variable_assignments(variables, named_state):
    """
    Return a list of all possible VariableAssignments that can
    be created from 
        1. the variables in variables parameter and
        2. the unmatched objects within Context object's
    NamedState object.

    note: this function is intended to be used internally from Context
    for the purpose of determining entailment only.
    """

    if not named_state.get_vocabulary().get_V():
        return []

    c_target = named_state.get_p().get_target()
    objects = named_state.get_attribute_system().get_objects()
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

    for i in mapping_list:
        print i

    X_list = []
    
    #if there are variable terms and unmatched object, form all
    #possible VariableAssignments and store them in X_list,
    #otherwise return an empty list
    if smaller_length > 0:
        for mapping in mapping_list:
            X = VariableAssignment(
                named_state.get_vocabulary(),
                named_state.get_attribute_system(),
                mapping)

            X_list.append(X)

    return X_list

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

        #not same AttributeSystem or Vocabulary, not an extension
        if not same_attr_systems or not same_vocabularies:
            return False

        #if this State is an extension of other State
        if self <= other:
            self_state = State(self._attribute_system, self._ascriptions)
            other_state = State(other._attribute_system, other._ascriptions)

            #if this State is a proper extension of other State or this
            #ConstantAssignment is a proper superset of other
            #ConstantAssignment, this NamedState is a proper extension of other
            #NamedState
            if self_state < other_state or self._p > other._p:
                return True

        return False

    def __le__(self, other):
        """Implement overloaded <= operator for NamedState extension."""
        if not hasattr(other, "_is_NamedState"):
            raise TypeError('other parameter must be of type NamedState')

        same_attr_systems = self._attribute_system == other._attribute_system
        same_vocabularies = self._p._vocabulary == other._p._vocabulary

        #not same AttributeSystem or Vocabulary, not an extension
        if not same_attr_systems or not same_vocabularies:
            return False

        self_state = State(self._attribute_system, self._ascriptions)
        other_state = State(other._attribute_system, other._ascriptions)

        if self_state <= other_state and self._p >= other._p:
            return True
        else:
            return False

    def is_world(self):
        """Determine if this NamedState is a world."""
        #if state is a world and p is total, this NamedState is a world
        return State.is_world(self) and self._p.is_total()

    def get_worlds(self):
        """
        Return a list of all possible worlds derivable from this 
        NamedState object.
        """

        source = self._p._vocabulary._C
        target = self._attribute_system._objects

        repeat_num = len(source) if len(source) < len(target) else len(target)

        from itertools import product

        #create all combinations of source and target elements
        combos = list(product(source, target, repeat=repeat_num))
        #remove combinations with duplicate source or target elements
        combos = [c for c in combos if len(set(c)) == len(source) + len(target)]
        #group the combinations into 2-tuples
        combos = [[combo[i:i+2] for i, item in enumerate(combo) if i%2 == 0] for combo in combos]
        #sort the combinations by vocabulary elements
        combos = [sorted(combo, key=lambda x: x[0]) for combo in combos]

        #remove duplcate combinations
        unique_combos = []

        for combo in combos:
            if combo not in unique_combos:
                unique_combos.append(combo)

        #remove combinations in conflict with this NamedState
        valid_constant_assignments = []
        for combo in unique_combos:
            CA = ConstantAssignment(
                self._p._vocabulary,
                self._attribute_system,
                {vocab: obj for (vocab, obj) in combo})

            if not ConstantAssignment.in_conflict(self._p, CA):
                valid_constant_assignments.append(CA)

        self_worlds = State.get_worlds(self)

                
        #create worlds for all constant assignment and world combos.
        worlds = []
        for p in valid_constant_assignments:
            for self_world in self_worlds:
                #construct world and save it
                world = NamedState(
                    self._attribute_system, p, self_world._ascriptions)
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

            #grab the system objects for convenience.
            system_objects = self._attribute_system._objects
            n = len(system_objects)

            #Get the union of all domains of provided NamedState objects
            domain_union = []
            for named_state in named_states:
                domain_union.extend(named_state._p.get_domain())
            domain_union = list(set(domain_union))
            
            #create set of all cartesian products of domain list and system
            #object list where each product is of length arity, that is,
            #the minimum number to match the smaller list with exactly one
            #member of the bigger list.
            from itertools import product

            arity = len(domain_union) if len(domain_union) < n else n
            combos = list(product(domain_union, system_objects, repeat=arity))

            supersets_list = []

            for combo in combos:
                #bundle the combo elements into 2-tuples representing
                #domain-object pairs, then remove duplicates.
                combo = [combo[i:i+2] for i, item in enumerate(combo) if i%2 == 0]
                combo = list(set(combo))
                
                #ensure that individual combos do not contain duplicate
                #domain elemens or duplicate objects.
                domain = [pair[0] for pair in combo]
                objects = [pair[1] for pair in combo]
                domain_duplicates = len(domain) != len(set(domain))
                object_duplicates = len(objects) != len(set(objects))

                if not domain_duplicates and not object_duplicates:
                    #if this combo is a superset of this NamedState's p, and
                    #hasn't already been saved in supersets_list, save it.
                    if set(self._p._mapping.items()) <= set(combo):
                        for superset in supersets_list:
                            if set(superset) == set(combo):
                                break
                        else:
                            supersets_list.append(combo)
            
            #create a ConstantAssignment for each superset; easily transform
            #each superset (list of 2-tuples) into mapping by casting to dict
            supersets = []
            for superset in supersets_list:
                p_prime = ConstantAssignment(
                            self._p._vocabulary,
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

        #get supsets of this NamedState's ConstantAssignment and create an
        #empty list to hold all alternate extensions.
        supersets = get_supersets()
        named_alternate_extensions = []


        for p_prime in supersets:
            
            #get the list of provided NamedStates not in conflict with each
            #superset of this NamedState's ConstantAssignment, i.e., the
            #NamedState's where the p'_i >= p_j and sigma_j < sigma.
            Sigma_i = [ns for ns in named_states if p_prime >= ns._p]

            #if there are such states, get the alternate extensions of this
            #NamedState's State component w.r.t. the list of non-conflicted
            #States in Sigma_i.
            if Sigma_i: 
                phi_i = self.get_alternate_extensions(*Sigma_i)
                #for each alternate extension, create a new NamedState with
                #that alternate extensions ascriptions and the superset 
                #p_prime and add to named_alternate_extensions if not already
                #in named_alternate_extensions.
                for s_prime in phi_i:
                    nae = NamedState(
                        self._attribute_system, p_prime, s_prime._ascriptions)

                    if nae not in named_alternate_extensions:
                        named_alternate_extensions.append(nae)
            #There is no provided NamedState not in conflict with this
            #NamedState's ConstantAssignment, so create a new NamedState with
            #this NamedState's ascriptions and p_prime and add to 
            #named_alternate_extensions.
            else:
                from copy import deepcopy
                nae = deepcopy(self)
                if nae not in named_alternate_extensions:
                    named_alternate_extensions.append(nae)

        return named_alternate_extensions

    def satisfies_formula(self, formula, attribute_interpretation, X):
        """
        Determine if NamedState object (which must be a world) satisfies given
        formula with respect to VariableAssignment X.
        """

        from F_and_AB import Formula

        if not hasattr(formula, "_is_Formula"):
            raise TypeError(
                'f parameter must be of type Formula')

        if not hasattr(X, "_is_VariableAssignment"):
            raise TypeError(
                'X parameter must be a VariableAssignment object')

        if not self.is_world():
            raise ValueError('this NamedState object must be a world')

        formula.assign_truth_value(attribute_interpretation, self, X)

        if truth_value == True:
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

        #check for exceptions first.
        if not isinstance(named_state, NamedState):
            raise TypeError(
                "named_state parameter must be of type NamedState")

        if not hasattr(named_state, "_is_NamedState"):
            raise TypeError(
                "named_state parameter must be NamedState object.")

        if not self.is_world():
            raise ValueError(
                "this NamedState object must be a world")

        #simply return truth value of extension
        return self <= named_state

    def satisfies_context(self, context, X, vocab, interpretation_table=None):
        """
        Return a boolean for whether or not this NamedState
        (which is a world) satisfies a given context. 
        
        vocab parameter of type Vocabulary is required to check if 
        world is indeed a world.
        
        Raise TypeError if context parameter is not of type Context.
        Raise TypeError if X parameter is not of type VariableAssignment.
        Raise TypeError if vocab parameter is not of type Vocabulary.
        Raise ValueError if this NamedState is not a world.
        """

        from Context import Context

        if not isinstance(context, Context):                                            #if context parameter is not of type Context
            raise TypeError(                                                            #explicitly raise TypeError
                'context parameter must be of type Context')

        if not isinstance(X, VariableAssignment):                                                     #if X parameter is not of type VariableAssignment
            raise TypeError(                                                            #explicitly raise TypeError
                'X parameter must be of type VariableAssignment')

        if not isinstance(vocab, Vocabulary):                                           #if vocab paramter is not of type Vocabulary
            raise TypeError(
                'vocab parameter must be of type Vocabulary')

        if not self.is_world():                                                         #if this NamedState is not a world
            raise ValueError(                                                           #explicitly raise ValueError
                'this NamedState object must be a world')

        named_state = context.get_named_state()                                         #get NamedState from Context
        
        if not self.is_extension(named_state):                                          #if world is does not satisfy the NamedState of the Context
            return False                                                                #the world does not satisfy the Context

        assumption_base = context.get_assumption_base()                                 #get AssumptionBase from the Context
        
        for formula in assumption_base:                                                 #for each Formula within the AssumptionBase
            
            truth_value = self.satisfies_formula(
                formula, X, vocab, interpretation_table)                                #get truth value of formula in world w.r.t. X
            
            if truth_value == False or truth_value == "unknown":                        #if world doesn't satisfy some formula in the AssumptionBase
                return False                                                            #world does not satisfy context, return False

        return True                                                                     #world satisfies NamedState of Context and every Formula in AssumptionBase of Context
    
    def is_named_entailment(self, beta, interpretation_table=None, *named_states):
        """
        Determine if this NamedState entails NamedStates contained in
        named_states parameter w.r.t. AssumptionBase beta.

        Raise TypeError if beta parameter is not of type AssumptionBase.
        Raise TypeError if any member of named_states parameter is not
        of type NamedState.
        Raise ValueError if any member of named_states does not share
        the same Vocabulary or AttributeSystem as this NamedState.
        Raise ValueError if any member of named_states parameter is
        not a proper extension of this NamedState.
        """

        #check for exceptions first.
        from F_and_AB import AssumptionBase
        if not isinstance(beta, AssumptionBase):
            raise TypeError(
                "beta parameter must be of type AssumptionBase")

        vocabulary = self.get_p().get_vocabulary()
        attribute_system = self.get_attribute_system()

        for named_state in named_states:
            if not isinstance(named_state, NamedState):
                raise TypeError(
                    "all optional positional arguments must be of "
                    "type NamedState.")
            if named_state.get_p().get_vocabulary() != vocabulary:
                raise ValueError(
                    "all vocabularies in this NamedState and optional "
                    "positional NamedStates must be equivalent.")
            if named_state.get_attribute_system() != attribute_system:
                raise ValueError(
                    "all AttributeSystems in this NamedState and optional "
                    "positional NamedStates must be equivalent.")
            if not named_state.is_proper_extension(self):
                raise ValueError(
                    "all NamedStates provided must be proper "
                    "subsets of this NamedState object.")

        #Get all possible alternate extensions first.
        alternate_extensions = self.get_named_alternate_extensions(
            *named_states)

        for alternate_extension in alternate_extensions:
            #make list to hold which formula have failed to evaluate to False for
            #every possible VariableAssignment.
            bad_formulae = []

            for formula in beta:

                #if a formula has already failed, we don't need to consider
                #it again.
                if formula in bad_formulae:
                    continue

                bad_formula = False

                #get free variables in formula and generate all possible 
                #VariableAssignments w.r.t. the free variable set.
                c_source = self.get_p().get_source()
                terms = formula.get_terms()
                variables = [t for t in terms if t not in c_source]
                
                X_list = generate_variable_assignments(variables, self)

                #if there are no possible VariableAssignments, add a dummy one.
                if not X_list:
                    X_list.append(VariableAssignment(
                        vocabulary, attribute_system, {}, dummy=True))
                
                #determine if formula truth value is False for every 
                #VariableAssignment and set flag if it isn't
                for X in X_list:

                    truth_value = assign_truth_value(
                        formula, alternate_extension, X, vocabulary,
                        interpretation_table)

                    if truth_value != False:
                        bad_formula = True
                        break
                
                #Formula failed for some VariableAssignment; this formula is
                #bad, add to bad list
                if bad_formula:
                    bad_formulae.append(formula)

            #if there's not a single formula that always evaluates to False,
            #then no entailment, return False.
            if len(beta.get_formulae()) == len(bad_formulae):
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
    color = Attribute('color', ['R', 'G', 'B'])
    size = Attribute('size', ['S', 'M', 'L'])

    attribute_structure = AttributeStructure(color, size)

    objects = ['s1', 's2', 's3']
    attribute_system = AttributeSystem(attribute_structure, objects)

    
    sigma = Vocabulary(['a', 'b', 'c', 'd', 'e', 'f', 'g'],[],[])

    p = ConstantAssignment(sigma, attribute_system, {'a': 's1'})
    ascr = {
        ('color', 's1'): ['R', 'B'], ('size', 's1'): ['S', 'M', 'L'],
        ('color', 's2'): ['R', 'B', 'G'], ('size', 's2'): ['M', 'L']}
    named_state = NamedState(attribute_system, p, ascr)


    p_1 = ConstantAssignment(sigma, attribute_system, {'a': 's1', 'b': 's2'})
    ascr_1 = {
        ('color', 's1'): ['B'], ('size', 's1'): ['S', 'M'],
        ('color', 's2'): ['B', 'G'], ('size', 's2'): ['M', 'L']}
    named_state_1 = NamedState(attribute_system, p_1, ascr_1)


    p_2 = ConstantAssignment(sigma, attribute_system, {'a': 's1', 'f': 's2', 'c': 's3'})
    ascr_2 = {
        ('color', 's1'): ['R', 'B'], ('size', 's1'): ['L'],
        ('color', 's2'): ['R', 'B', 'G'], ('size', 's2'): ['L']}
    named_state_2 = NamedState(attribute_system, p_2, ascr_2)


    p_3 = ConstantAssignment(sigma, attribute_system, {'a': 's1', 'g': 's2', 'c': 's3'})
    ascr_3 = {
        ('color', 's1'): ['R'], ('size', 's1'): ['S', 'M', 'L'],
        ('color', 's2'): ['R', 'B', 'G'], ('size', 's2'): ['M', 'L']}
    named_state_3 = NamedState(attribute_system, p_3, ascr_3)

    aes = named_state.get_named_alternate_extensions(named_state_1, named_state_2, named_state_3)

    from copy import deepcopy
    tester = deepcopy(aes[1])

    print named_state.is_named_alternate_extension(tester, named_state_1, named_state_2, named_state_3)



if __name__ == "__main__":
    main()