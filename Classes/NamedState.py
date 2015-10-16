"""Named State class."""

class NamedState(State):
    """
    Class for named state;

    subclasses State and adds p (ConstantAssignment).
    """

    def __init__(self, asys, p, ascriptions=None):
        """
        Initialize a NamedState object with AttributeSystem asys
        and constant assignment p.

        Raise TypeError if asys parameter is not of type
        AttributeSystem or p parameter is not of type
        ConstantAssignment.
        """

        #check for exceptions
        if not isinstance(asys, AttributeSystem):
            raise TypeError(
                "asys parameter must be of type AttributeSystem")
        if not isinstance(p, ConstantAssignment):
            raise TypeError(
                "p parameter must be a constant assignment"
                "(i.e., of type ConstantAssignment)")
        
        State.__init__(self, asys, ascriptions)
        self._p = p

    def __eq__(self, other):
        """
        Return boolean for whether or not this NamedState is equivalent
        to other NamedState.
        """
        
        if not State.__eq__(self, other):                                               #if this NamedState's state is not equal to other NamedState's state
            return False                                                                #this NamedState != other NamedState, return False
        
        if self.get_p() != other.get_p():                                               #if this NamedState's const assignment is not equal to other NamedState's const assignment
            return False                                                                #this NamedState != other NamedState, return False
        
        return True                                                                     #this NamedState's and other NamedState's states and constant assignments equal, return True
    
    def __ne__(self, other):
        """
        Return boolean for whether or not this NamedState is not
        equivalent to other NamedState.
        """
        
        if not State.__eq__(self, other):                                               #if this NamedState's state is not equal to other NamedState's state
            return True                                                                 #this NamedState != other NamedState, return False
        
        if self.get_p() != other.get_p():                                               #if this NamedState's const assignment is not equal to other NamedState's const assignment
            return True                                                                 #this NamedState != other NamedState, return False
        
        return False                                                                    #this NamedState's and other NamedState's states and constant assignments equal, return True

    def deep_copy(self):
        """Return a deep copy of this NamedState."""
        import copy
        
        attribute_system_copy = self._attribute_system.deep_copy()
        p_copy = self._p.deep_copy()
        ascriptions_copy = copy.copy(self._ascriptions)
        
        return NamedState(attribute_system_copy, p_copy, ascriptions_copy)

    def get_p(self):
        """
        Return the ConstantAssignment embedded in this
        NamedState object.
        """
        
        return self._p

    def set_p(self, p):
        """
        Replace the current constant assignment contained in this 
        NamedState with p parameter.

        Raise TypeError if p parameter is not of type ConstantAssignment.
        """

        if not isinstance(p, ConstantAssignment):
            raise TypeError(
                'p parameter must be of type dict')

        self._p = p

    def get_vocabulary(self):
        """
        Return the Vocabulary object of the ConstantAssignment
        object embedded in this NamedState object.
        """
        
        return self._p.get_vocabulary()

    def __str__(self):
        """Return a dtring representation of this NamedState object."""
        return 'ascriptions:\n'+ State.__str__(self) + '\nconstant assignment:\n' + str(self._p)

    def is_world(self):
        """Determine if this NamedState is a world."""

        #if state is a world and p is total, this NamedState is a world
        if State.is_world(self) and self.get_p().is_total():
            return True
        else:
            return False

    def is_extension(self, other):
        """
        Return a boolean for whether or not this NamedState object is
        an extension of other NamedState object.

        Raise TypeError if other parameter is not of Type NamedState
        """

        if not isinstance(other, NamedState):
            raise TypeError(
                'other parameter must be of type NamedState')
        
        #determine if this NamedState's State is an extension
        #of other NamedState's State
        state_condition = State.is_extension(self, other)
        #determine if this NamedState's ConstantAssignment
        #is a superset of other's
        constant_assignment_condition = is_subset(
            other._p.get_mapping(), self._p.get_mapping())

        #if both conditions hold, it is an extension
        if state_condition and constant_assignment_condition:
            return True
        else:
            return False

    def is_proper_extension(self, other):
        """
        Return a boolean for whether or not this NamedState object is
        a proper extension of other NamedState object.

        raise TypeError if other parameter is not of Type NamedState.
        """

        #Check for exceptions.
        if not isinstance(other, NamedState):
            raise TypeError(
                'other parameter must be of type NamedState')
        

        #Check if this NamedState is an extension of other NamedState.
        if NamedState.is_extension(self, other):

            #if other NamedState's ConstantAssignment is a proper subset of
            #this NamedState's ConstantAssignment return True.
            if is_proper_subset(
                other._p.get_mapping(), self._p.get_mapping()):
                return True
            else:
                #if this NamedState's State is a proper extension
                #of other NamedState's State, return True.
                if State.is_proper_extension(self, other):
                    return True

        return False

    def get_worlds(self):
        """
        Return a list of all possible worlds derivable from this 
        NamedState object.
        """

        source = self.get_vocabulary().get_C()
        target = self.get_attribute_system().get_objects()

        repeat_num = len(source) if len(source) < len(target) else len(target)

        from itertools import product

        combos = list(product(source, target, repeat=repeat_num))

        valid_combos = []

        for combo in combos:
            #bundle the combo elements into 2-tuples representing
            #domain-object pairs, then remove duplicates.
            combo = [combo[i:i+2] for i, item in enumerate(combo)
                                                            if i%2 == 0]
            combo = list(set(combo))
                
            #ensure that individual combos do not contain duplicate
            #domain elemens or duplicate objects.
            domain_elements = [pair[0] for pair in combo]
            object_elements = [pair[1] for pair in combo]

            no_domain_duplicates_cond = \
                        len(domain_elements) == len(set(domain_elements))
            no_object_duplicates_cond = \
                        len(object_elements) == len(set(object_elements))

            if no_domain_duplicates_cond and no_object_duplicates_cond:
                for vc in valid_combos:
                    if set(vc) == set(combo):
                        break
                else:
                    valid_combos.append(combo)

        #convert valid combinations to ConstantAssignments, removing any
        #mappings of the incorrect size they may have passed through b/c
        #list lenght evaluates to 2 even if there's a single 2-tuple in it
        #according to the above code block sometimes.
        const_assignments = []
        for combo in valid_combos:
            p = ConstantAssignment(
                self.get_vocabulary(), self.get_attribute_system(),
                dict(combo))

            if len(p.get_mapping()) == repeat_num:
                const_assignments.append(p)

        #get all the possible worlds of just the state alone and initialize
        #an empty list to hold all of the named worlds.
        worlds = []
        s_worlds = State.get_worlds(self)

        #create worlds for all constant assignments and worlds.
        for p in const_assignments:
            for s_world in s_worlds:
                world = NamedState(
                    self.get_attribute_system(), p, 
                    s_world.get_ascriptions())

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
        Raise TypeError if any item in named_states parameter is not of
        type NamedState.
        Raise ValueError if any of the NamedStates ns1,...,nsm is not a
        proper extension of this NamedState object.
        Raise ValueError if any NamedStates (including this NamedState)
        do not share the same Vocabulary or AttributeSystem.
        """
        
        vocabulary = self.get_p().get_vocabulary()
        attribute_system = self.get_attribute_system()
        
        #check for exceptions first.
        if not isinstance(ns_prime, NamedState):
            raise TypeError(
                "ns_prime parameter must be of type NamedState.")
        if not ns_prime.is_proper_extension(self):
            raise ValueError(
                "all NamedStates provided must be proper "
                "subsets of this NamedState object.")
        if ns_prime.get_p().get_vocabulary() != vocabulary:
            raise ValueError(
                "all vocabularies in this NamedState and optional "
                "positional NamedStates must be equivalent.")
        if ns_prime.get_attribute_system() != attribute_system:
            raise ValueError(
                "all AttributeSystems in this NamedState and optional "
                "positional NamedStates must be equivalent.")

        if not named_states:
            raise ValueError(
                "at least one NamedState object must be "
                "provided as an argument")
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

        aes = self.get_named_alternate_extensions(*named_states)
        
        for ae in aes:
            if ns_prime == ae:
                return True

        return False

    def get_named_alternate_extensions(self, *named_states):
        """
        Return all alternate extensions of this NamedState object with
        respect to NamedStates ns1,...,nsm within the named_states
        parameter.

        Raise ValueError if named_states parameter is empty.
        Raise TypeError if any item in named_states parameter is not of
        type NamedState.
        Raise ValueError if any of the NamedStates ns1,...,nsm is not a
        proper extension of this NamedState object.
        Raise ValueError if any NamedStates (including this NamedState)
        do not share the same Vocabulary or AttributeSystem.
        """

        def get_supersets():
            """
            Return the set of ConstantAssignments that are supersets
            of this NamedState object's p.
            """

            #grab the system objects for convenience.
            system_objects = self.get_attribute_system().get_objects()
            n = len(system_objects)

            #get the set theoretic difference between the union of the domains
            #of ns1,...,nsm and this NamedState's domain along with the total
            #domain
            domain_union = []

            for named_state in named_states:
                domain_union.extend(named_state.get_p().get_domain())
            
            #domain_difference = list(
                #set(domain_union) - set(self.get_p().get_domain()))
            #d = len(domain_difference)
            
            domain = list(set(domain_union))
            d = len(domain)

            #create set of all cartesian products of domain list and system
            #object list where each product is of length repeat_num, that is,
            #the minimum number to match the smaller list with exactly one
            #member of the bigger list.
            from itertools import product

            repeat_num = d if d < n else n

            combos = list(product(domain, system_objects, repeat=repeat_num))

            supersets_list = []

            for combo in combos:
                #bundle the combo elements into 2-tuples representing
                #domain-object pairs, then remove duplicates.
                combo = [combo[i:i+2] for i, item in enumerate(combo)
                                                                if i%2 == 0]
                combo = list(set(combo))
                    
                #ensure that individual combos do not contain duplicate
                #domain elemens or duplicate objects.
                domain_elements = [pair[0] for pair in combo]
                object_elements = [pair[1] for pair in combo]

                no_domain_duplicates_cond = \
                            len(domain_elements) == len(set(domain_elements))
                no_object_duplicates_cond = \
                            len(object_elements) == len(set(object_elements))

                if no_domain_duplicates_cond and no_object_duplicates_cond:
                    p_mapping = self.get_p().get_mapping()
                    p_list = [(key, value) for key, value in p_mapping.items()]
                    
                    #if this combo is a superset of this NamedState's p, and
                    #hasn't already been saved in supersets_list, save it.
                    if is_subset(p_list, combo):
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
                    vocabulary, attribute_system, dict(superset))
                supersets.append(p_prime)

            return supersets

        vocabulary = self.get_p().get_vocabulary()
        attribute_system = self.get_attribute_system()

        #check for exceptions first.
        if not named_states:
            raise ValueError(
                "at least one NamedState object must be "
                "provided as an argument")

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

        #get supsets of this NamedState's ConstantAssignment and create an
        #empty list to hold all alternate extensions.
        supersets = get_supersets()
        named_alternate_extensions = []
        
        for p_prime in supersets:
            
            #get the list of provided NamedStates not in conflict with each
            #superset of this NamedState's ConstantAssignment.
            Sigma_i = []
            for ns in named_states:
                if not vocabulary.check_conflict(p_prime, ns.get_p()):
                    Sigma_i.append(ns)

            #if there are such states, get the alternate extensions of this
            #NamedState's State component w.r.t. the list of non-conflicted
            #States in Sigma_i.
            if Sigma_i: 
                phi_i = self.get_alternate_extensions(*Sigma_i)
                #for each alternate extension, create a new NamedState with
                #that alternate extensions ascriptions and the superset 
                #p_prime and add to named_alternate_extensions.
                for s_prime in phi_i:
                    nae = NamedState(
                        attribute_system, p_prime, s_prime.get_ascriptions())
                    named_alternate_extensions.append(nae)
            #There is no provided NamedState not in conflict with this
            #NamedState's ConstantAssignment, so create a new NamedState with
            #this NamedState's ascriptions and p_prime and add to 
            #named_alternate_extensions.
            else:
                nae = NamedState(
                    attribute_system, self.get_p(), self.get_ascriptions())
                named_alternate_extensions.append(nae)

        return named_alternate_extensions

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
        
    def satisfies_formula(self, f, X, vocab, interpretation_table=None):
        """
        Return boolean for whether or not this NamedState
        (which is a world) satisfies Formula f w.r.t. 
        variable assignment X.

        vocab parameter of type Vocabulary is required to check if 
        world is indeed a world.

        Raise TypeError if f parameter is not of type Formula.
        Raise TypeError if X parameter is not of type ConstantAssignment.
        Raise TypeError if vocab parameter is not of type Vocabulary.
        Raise ValueError if this NamedState is not a world.
        """

        from F_and_AB import Formula

        if not isinstance(f, Formula):                                                  #if f parameter is not of type Formula
            raise TypeError(                                                            #explicitly raise TypeError
                'f parameter must be of type Formula')

        if not isinstance(X, VariableAssignment):                                                     #if X parameter is not of type VariableAssignment
            raise TypeError(                                                            #explicitly raise TypeError
                'X parameter must be of type VariableAssignment')

        if not isinstance(vocab, Vocabulary):                                           #if vocab paramter is not of type Vocabulary
            raise TypeError(                                                            #explicitly raise TypeError
                'vocab parameter must be of type Vocabulary')

        if not self.is_world():                                                    #if this NamedState is not a world
            raise ValueError(                                                           #explicitly raise ValueError
                'world parameter must be a world')

        truth_value = assign_truth_value(
            f, self, X, vocab, interpretation_table)                                    #get the truth value of the formula in the world

        if truth_value == True:                                                         #if truth value is explicitly true (note: can't do "if truth_value:" as unknown token is truthy)
            return True                                                                 #return True
        else:                                                                           #if truth value is unknown or False 
            return False                                                                #return False

    def satisfies_named_state(self, named_state, vocab):
        """
        Return boolean for whether or not this NamedState
        (which is a world) satisfies NamedState object named_state.

        vocab parameter of type Vocabulary is required to check if 
        world is indeed a world.

        Raise TypeError if named_state parameter is not of 
        type NamedState
        Raise TypeError if vocab parameter is not of type Vocabulary
        Raise ValueError if this NamedState is not a world.
        """

        #check for exceptions first.
        if not isinstance(named_state, NamedState):
            raise TypeError(
                'named_state parameter must be of type NamedState')

        if not isinstance(vocab, Vocabulary):
            raise TypeError(
                'vocab parameter must be of type Vocabulary')

        if not self.is_world():
            raise ValueError(
                'world parameter must be a world')

        #simply return truth value of extension
        return self.is_extension(named_state)
    
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

def main():
    """Main method; quick testing."""

    a, b, c = Attribute("a", []), Attribute("b", []), Attribute("c", [])
    r = Relation("R1(a,b) <=> ", ["a", "b"])

    a = AttributeStructure(a, b, c, r)
    o = ['o1', 'o2']

    asys = AttributeSystem(a, o)
    s = State(asys)

if __name__ == "__main__":
    main()
