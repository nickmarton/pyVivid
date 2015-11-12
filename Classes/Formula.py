"""Formula class; imutable."""

from RelationSymbol import RelationSymbol
from Vocabulary import Vocabulary

class Formula(object): 
    """Class for a formula in respect to some Vocabulary sigma."""

    def __init__(self, vocabulary, name, *terms):
        """Construct a Formula object."""

        if not hasattr(vocabulary, "_is_Vocabulary"): 
            raise TypeError("vocabulary parameter must be a Vocabulary object")
        if type(name) != str: 
            raise TypeError(name + " must be a string")
        
        relation_symbol_names = [rs._name for rs in vocabulary._R]
        if name not in relation_symbol_names: 
            raise ValueError(
                "Name must match some RelationSymbol in Vocabulary")

        if not terms: 
            raise ValueError("at least 1 term must be provided")
        
        C, V = vocabulary._C, vocabulary._V

        for t in terms:
            
            if t in C:
                in_C = True
            else: 
                in_C = False
            if t in V:
                in_V = True
            else: 
                in_V = False

            #Vocabulary takes care of ensuring no overlap between C and V
            if not in_C and not in_V:
                raise ValueError(
                    "all terms must be contained in vocabulary's C or V")
        
        from copy import deepcopy
        self._vocabulary = deepcopy(vocabulary)
        self._name = deepcopy(name)
        self._terms = list(set(list(terms)))
        self._is_Formula = True

    def __eq__(self, other):
        """Implement == operator for Formula."""
        if not hasattr(other, "_is_Formula"):
            raise TypeError(
                "can only compare Formula object with another Formula object")

        vocab_cond = self._vocabulary == other._vocabulary
        name_cond = self._name == other._name
        terms_cond = set(self._terms) == set(other._terms)

        if vocab_cond and name_cond and terms_cond:
            return True
        else: 
            return False
    
    def __ne__(self, other):
        """Implement != operator for Formula object."""
        return not self.__eq__(other)

    def __deepcopy__(self, memo):
        """Implement copy.deepcopy for formula object."""
        from copy import deepcopy
        return Formula(
            deepcopy(self._vocabulary),
            deepcopy(self._name),
            *self._terms)








    def assign_truth_value(self, attribute_interpretation, named_state, X):
        """
        Assign truth value in (true, false, unknown} to Formula given an
        arbitrary NamedState and VariableAssignment
        """

        if not hasattr(attribute_interpretation, "_is_AttributeInterpretation"):
            raise TypeError(
                "named_state parameter must be a NamedState object")

        if not hasattr(named_state, "_is_NamedState"):
            raise TypeError(
                "named_state parameter must be a NamedState object")

        if not hasattr(X, "_is_VariableAssignment"):
            raise TypeError(
                "X parameter must be a VariableAssignment object")

        if not self._vocabulary == X._vocabulary == named_state._p._vocabulary:
            raise ValueError(
                "Vocabulry's of Formula, NamedState and VariableAssignment "
                "must match")


    def bad_assign_truth_value(f, named_state, X, vocab, interpretation_table=None):
        """
        Map an atomic formula f to {true, flase, unknown}
        given a named state along with a variable assignment X. 
        
        This function is intended to map ONE formula at a time using the 
        procedure outlined in the paper. 
        
        As such, it considers an atomic formula R(t_1,...,t_n) where R is a
        relation symbol of arity n with a predefined profile; 
        the interpretation table constructed at the beginning of this 
        function (or passed as a parameter) must contain f 
        (i.e. f._name must match some entry's first element in the table)

        terms of the formula are automatically matched by the indicies of 
        the profile e.g. 
        given terms ['C1', 'C2', 'V1', 'V2'] 
        where each term belongs to only 1 of C or V in some Vocabulary
        and 
        profile [(h, 1), (m, 1), (h, 2), (m, 2)]
        1 -> 'C1', 2 -> 'C2', and nothing maps to 'V1' or 'V2'      
        so when the terms are substituted for the profile indicies, 
        the new profile becomes
        [(h, 'C1'), (m, 'C1'), (h, 'C2'), (m, 'C2')]                
        and the extra terms 'V1' and 'V2' are ignored completely.
        Note: substitutions try with the ConstantAssignment first; the
        function will only try to substitute a VariableAssignment if
        a ConstantAssignment match was not found.

        in addition, the cardinality of the pairs of profiles must match 
        the arity of the Relation R' in the Attribute Structure

        input:
        f:                  a formula object, the name of which must match
                            an entry in the interpretation_table
        named_state:        the named_state for which the formulae is 
                            being tested in
        X:                  the variable assignment; this should come 
                            from the same vocabulary that the named_state's 
                            constant assignment comes from
        vocab:              a Vocabulary object; f must be the name of some 
                            RelationSymbol in vocab._R, and every 
                            RelationSymbol object of vocab._R must have 
                            an entry in the interpretation_table where its 
                            realization comes from the Relation objects of 
                            the AttributeStructure embedded within 
                            named_state
        
        output:
        True, False, or unknown.
        """

        from vivid import Formula, NamedState, Vocabulary, RelationSymbol                  #import Formula and NamedState class from full module
        from Assignment import VariableAssignment

        def validate_input():
            """
            Determine if input is valid; raise an exception otherwise.
            """

            if not isinstance(f, Formula):                                                  #if f parameter is not of type Formula
                raise TypeError(                                                            #explicitly raise TypeError
                    "f parameter must be a Formula")
            
            if not isinstance(named_state, NamedState):                                    #if named_state parameter is not of type NamedState
                raise TypeError(                                                            #explicitly raise TypeError
                    "named_state parameter must be a NamedState")
            
            if not isinstance(X, VariableAssignment):                                                     #if X parameter is not of type dict
                raise TypeError(                                                            #explicitly raise TypeError
                    "X parameter must be of type VariableAssignment")
            
            if not isinstance(vocab, Vocabulary):                                           #if vocab parameter is not of type Vocabulary
                raise TypeError(                                                            #explicitly raise TypeError
                    "vocab parameter must be of type Vocabulary")

            ns_vocab = named_state.get_p().get_vocabulary()
            X_vocab = X.get_vocabulary()

            if ns_vocab == X_vocab == vocab:
                pass
            else:
                raise ValueError(
                    "vocabulary of constant assignment in named_state "
                    "parameter, vocabulary of X parameter and vocabulary "
                    "parameter must all be equal")

        def generate_value_sets(profile):
            """
            Generate all combinations of values that objects in profile 
            can take on, i.e., the cartesian product.
            """

            def break_down_tuples(lis):
                """
                Replace low-high tuples in lis parameter with all elements
                in their range.
                """

                def frange(x, y, jump):
                    """
                    Declare a generator that generates values in an 
                    inclusive range with a float step size.
                    """

                    while x <= y:                                                           #while low is less than high
                        yield x                                                             #yield x at current step
                        x += jump                                                           #increment x by step size

                tuples = []
                for i, item in reversed(list(enumerate(lis))):                              #for every item in lis parameter starting from the back
                    if isinstance(item, tuple):                                             #if the item is a low-high tuple
                        tuples.append(item)                                                 #save the tuple and delete it in lis
                        del lis[i]

                for tup in tuples:                                                          #for every low-high tuple formerly in lis
                    low = tup[0]
                    high = tup[1]

                    if isinstance(low, float) or isinstance(high, float):                   #if we need to use floats
                        lis.extend(list(frange(low, high, get_float_df())))
                    else:                                                                   #otherwise, we're using ints
                        lis.extend(list(range(low, high + 1)))

                return lis

            from itertools import product

            original_vals = copy.copy([named_state.get_ascription(tup) for tup in profile])            #get value set for each object

            point_flag = False
            for ascription in original_vals:
                for value in ascription:
                    if isinstance(value, Point):
                        point_flag = True
                        break

            if point_flag:                                                                  #encode_points will raise TypeError if an ascription wit ha Point object is mixed
                original_vals = encode_points(original_vals)                                #with a non-Point value to prevent binding problem

            value_sets = []                                                                 #declare an empty list to hold valueset without low-high tuples

            for ov in original_vals:                                                        #for each object's value set
                tupleless_value_set = break_down_tuples(copy.copy(ov))                      #get a copy of the object's value set with low-high tuples converted to values in their ranges
                value_sets.append(tupleless_value_set)                                      #store new value set within value_sets

            combos = list(product(*value_sets))                                             #compute all possible value set combinations

            return combos

        def get_relation_arguments(definition):
            """Return the arguments provided in Relation definition."""

            start_paren = definition.find('(')                                              #get index of starting parenthesis
            end_paren = definition.find(')')                                                #get index of ending parenthesis

            arg_string = definition[start_paren+1:end_paren]                                #get substring of relation definition with arguments

            return arg_string.split(',')                                                    #split the substring into the relation arguments

        def sub_value_set(value_set, relation_args, definition):
            """
            Return a copy of definition with relation arguments 
            substituted with their corresponding values in value set.
            """

            def reorder_value_set():
                """
                Reorder the value set in accordance with how the 
                relation_args were reordered.
                """
                
                pos = []
                for i, c_arg in enumerate(arg_copy):
                    for j, r_arg in enumerate(relation_args):
                        if c_arg == r_arg:
                            pos.append((i,j))

                pos.sort(key = lambda x : x[1])

                reordered_value_set = []
                for i in range(len(value_set)):
                    reordered_value_set.append(value_set[pos[i][0]])

                return reordered_value_set
            

            arg_copy = copy.copy(relation_args)

            relation_args.sort(key=len, reverse=True)                                       #sort relation args by descending length

            reordered_value_set = reorder_value_set()                                       #reorder the value set to match reordering in relation_args

            new_def = definition                                                            #copy definition into new string
            
            for i, r_arg in enumerate(relation_args):                                       #for each argument
                new_def = new_def.replace(r_arg, str(reordered_value_set[i]))               #replace all occurances of the argument wit hthe corresponding value set value

            return new_def

        def handle_is_on_line(profile):
            """
            Get truth value of expressions containing within operator.
            """

            def validate_is_on_line_profile(profile):
                """
                Raise a ValueError if ascriptions form profile don't 
                correspond to a Point and line segment.
                """

                ascriptions = [named_state.get_ascription(tup) for tup in profile]            #get value set for each object

                if len(ascriptions) != 2:
                    raise ValueError(
                        "profile for is_on_line must contain exactly two pairs")

                if len(ascriptions[0]) != 1:
                    raise ValueError(
                        "ascription of first profile pair for" +
                        " is_on_line must contain exactly one Point")

                if not isinstance(ascriptions[0][0], Point):
                    raise ValueError(
                        "ascription of first profile pair for" +
                        " is_on_line must contain exactly one Point")

                if len(ascriptions[1]) != 2:
                    raise ValueError(
                        "ascription of second profile pair for" +
                        " is_on_line must contain exactly two Points")

                if not isinstance(ascriptions[1][0], Point) or not isinstance(ascriptions[1][1], Point):
                    raise ValueError(
                        "ascription of first profile pair for" +
                        " is_on_line must contain exactly one Point")

                return ascriptions

            def is_on(ascriptions):
                "Return true iff point c intersects the line segment from a to b."
                # (or the degenerate case that all 3 points are coincident)
                
                ax, ay = ascriptions[1][0].get_coordinate()
                bx, by = ascriptions[1][1].get_coordinate()
                cx, cy = ascriptions[0][0].get_coordinate()
                
                #print 'is ' + str(c) + " on line segment from " + str(a) + " to " + str(b)
                
                return (collinear(ax, ay, bx, by, cx, cy)
                        and (within(ax, cx, bx) if ax != bx else 
                             within(ay, cy, by))) 

            def collinear(ax, ay, bx, by, cx, cy):
                "Return true iff a, b, and c all lie on the same line."
                return (bx - ax) * (cy - ay) == (cx - ax) * (by - ay)

            def within(p, q, r):
                "Return true iff q is between p and r (inclusive)."
                return p <= q <= r or r <= q <= p

            ascriptions = validate_is_on_line_profile(profile)
            #print "@@@" + str(ascriptions)
            return is_on(ascriptions)

        def handle_through_worldline(profile):
            """
            Handle Relations with definition in the following form:
            R2(p1,p2,l) <=> p1 = p2 through_worldline l
            where p1 and p2 are Points and l is a line segment represented
            by a 2-tuple of Points
            """

            #Create subprofiles to check if points are on line
            p1_on_l_profile = [profile[0], profile[2]]
            p2_on_l_profile = [profile[1], profile[2]]

            p1_on_l = handle_is_on_line(p1_on_l_profile)
            p2_on_l = handle_is_on_line(p2_on_l_profile)

            #if they're both on the same worldine, then observes holds
            both_on_same_worldline = p1_on_l and p2_on_l

            #Get the point objects for comparison
            ascriptions = [named_state.get_ascription(tup) for tup in profile]            #get value set for each object
            p1 = ascriptions[0]
            p2 = ascriptions[1]
            '''
            print "-"*40
            print ascriptions
            print p1 == p2
            print both_on_same_worldline
            print "-"*40
            print
            '''
            #if the p1 and p2 are the same location or both on the same worldline,
            #then p1 and p2 are observable from one another
            if p1 == p2 or both_on_same_worldline:
                return True
            else:
                return False

        def handle_meets(profile):
            """
            Determine if spacetime_position at profile[0] is on both worldlines
            m1 and m2 and therefore if m1 and m2 intersect at sp.
            """

            profile_1 = [profile[0], profile[1]]
            profile_2 = [profile[0], profile[2]]
            
            sp_on_m1 = handle_is_on_line(profile_1)
            sp_on_m2 = handle_is_on_line(profile_2)

            if sp_on_m1 and sp_on_m2:
                return True
            else:
                return False

        def handle_not_same_point(profile):
            """Handle when two points are being compared for inequality."""

            ascriptions = [named_state.get_ascription(tup) for tup in profile]

            if len(ascriptions) != 2:
                raise ValueError(
                    "only 2 points may be compared")

            if not isinstance(ascriptions[0][0], Point) or not isinstance(ascriptions[1][0], Point):
                raise TypeError(
                    "ascriptions must be of type Point")
            
            p1 = ascriptions[0][0]
            p2 = ascriptions[1][0]

            return p1 != p2

        def handle_clocks_unequal(profile):
            """
            Handle when we compare two spacetime clocks.

            clocks refers to 2nd element in spacetime_position tuple.
            """

            ascriptions = [named_state.get_ascription(tup) for tup in profile]

            if len(ascriptions) != 2:
                raise ValueError(
                    "only 2 points may be compared")

            if not isinstance(ascriptions[0][0], Point) or not isinstance(ascriptions[1][0], Point):
                raise TypeError(
                    "ascriptions must be of type Point")
            
            p1 = ascriptions[0][0]
            p2 = ascriptions[1][0]

            return p1.get_coordinate()[1] != p2.get_coordinate()[1]

        validate_input()

        #do an attribute interpretation from vocabulary to attribute structure

        if not interpretation_table:
            interpretation_table = get_attribute_interpretation(
                named_state.get_attribute_system().get_attribute_structure(),
                vocab)

        #we now have a fixed vocabulary, attribute structure, and attribute interpretation

        for entry in interpretation_table: 
            if entry[0].get_name() == f.get_name():                                         #get entry in interpretation table corresponding to f
                R_I = entry
                break
        else: 
            raise ValueError(f.get_name() + " must be in intepretation table")              #if intepretation table doesn't have relation, raise exception

        p = named_state.get_p()                                                             #save constant assignment of named_state in p 
        profile = list(R_I[3])                                                              #extract profile from interpretation_table
        terms = f.get_terms()                                                               #extract terms from formula
        astr_relation = named_state.\
                        get_attribute_system().\
                        get_attribute_structure().\
                        get_relation(int(R_I[2][1:]))
        definition = astr_relation.get_definition()                                         #get relation and definition of relation that will be computed

        if len(profile) != len(astr_relation.get_DR()):                                     #if relation we are trying to compute has an amount of arguments not equal to profile pairs
            raise ValueError(                                                               #raise ValueError, don't let a bug propogate
                    "number of profile pairs must be equal to the number "
                    "of arguments the relation takes"
                )

        #compiling profile into attribute object pairs that will be substituted into the expression

        profile_indicies = [pair[1] for pair in profile]                                    #extract j_i's from profile into list
        
        for index in profile_indicies:
            if index > len(terms): raise ValueError(                                        #check if each index is valid in respect to list of terms
                "each index corresponds to an index in formula's terms list; "              #i.e., j_x has corresponding (t^{p,X})_j_x
                "indicies may not exceed the amount of terms"
                ) 

        for i, pair in enumerate(profile):                                                  #for each pair in profile
            term = terms[pair[1] - 1]                                                       #grab formula term corresponding to the pair's index; shifted down 1 as indexing starts at 0 and not 1
            profile[i] = (pair[0], term)                                                    #rewrite that pair with the corresponding term instead of index

        for i, pair in enumerate(profile):                                                  #for each pair in profile
            defined_flag = False
            try: 
                obj = p.get_mapping()[pair[1]]                                                            #grab the object corresponding to the pair's term
                defined_flag = True                                                         #set flag to determine if formula can be computed
            except KeyError: pass
            
            if not defined_flag:
                try: 
                    obj = X.get_mapping()[pair[1]]                                                            #grab the object corresponding to the pair's term
                    defined_flag = True                                                         #set flag to determine if formula can be computed
                except KeyError: pass

            if not defined_flag:
                return "unknown"                                           #some term is not defined by either p or X so truth value is unknown

            profile[i] = (pair[0], obj)                                                     #rewrite that pair with the corresponding object instead of term

       
        relation_args = get_relation_arguments(definition)                                  #get the arguments provided in the relation definition


        #we now check the formula against each possible world within the state
        if 'is_on_line' in definition and 'and' in definition:
            return handle_meets(profile)
        elif 'is_on_line' in definition:
            return handle_is_on_line(profile)
        elif 'through_worldline' in definition:
            return handle_through_worldline(profile)
        elif 'not_same_point' in definition:
            return handle_not_same_point(profile)
        elif 'clocks_unequal' in definition:
            return handle_clocks_unequal(profile)
        else :

            #we now have a compiled profile; need to evaluate every possible world of the state

            value_sets = generate_value_sets(profile)                                       #generate all possible value_sets objects can take on

            truth_values = []

            for value_set in value_sets:                                                    #for each possible value set

                subbed_definition = sub_value_set(                                          #substitute relation argument in definition with their corresponding values in value set
                    value_set, relation_args, definition)

                rh_index = subbed_definition.find("<=> ") + 4                               #get index of where expression begins

                expr = subbed_definition[rh_index:]                                         #get expression from definition

                from truth_parser import LogicoMathematicalTruthParser 
                lmtp=LogicoMathematicalTruthParser()                                        #create a parser object for relation definition
                result=lmtp.eval(expr)                                                      #try to evaluate the logico-mathematical expression
                truth_values.append(result)                                                 #append the result of the evaulation if successful

            if all(truth_values):                                                           #if the formula holds in every world, return true
                return True
            elif not any(truth_values):                                                     #if the formula does not hold in any world, return False
                return False
            else:                                                                           #if the formula sometimes holds and sometimes doesn't, return unknown token
                return "unknown"









































































    def __str__(self):
        """Implement str(Formula)."""
        return self._name + '(' + ', '.join([str(t) for t in self._terms]) + ')'

    def __repr__(self):
        """Implement repr(Formula)."""
        return self.__str__()

def main():
    """Quick tests."""

    from Interval import Interval
    from Attribute import Attribute
    from Relation import Relation
    from AttributeStructure import AttributeStructure
    from AttributeSystem import AttributeSystem
    from AttributeInterpretation import AttributeInterpretation
    from ConstantAssignment import ConstantAssignment
    from NamedState import NamedState

    a = Attribute('hour', [Interval(0, 23)])
    a2 = Attribute('minute', [Interval(0, 59)])
    r_pm = Relation('R1(h1) <=> h1 > 11', ['hour'], 1)
    r_am = Relation('R2(h1) <=> h1 <= 11', ['hour'], 2)
    r_ahead = Relation('R3(h1,m1,h2,m2) <=> h1 > h2 or (h1 = h2 and m1 > m2)', ['hour', 'minute', 'hour', 'minute'], 3)
    r_behind = Relation('R4(h1,m1,h2,m2) <=> h1 <= h2 or (h1 = h2 and m1 < m2)', ['hour', 'minute', 'hour', 'minute'], 4)
    attribute_structure = AttributeStructure(a, a2, r_ahead, r_behind, r_pm, r_am)

    pm_rs = RelationSymbol('PM', 1)
    am_rs = RelationSymbol('AM', 1)
    ahead_rs = RelationSymbol('Ahead', 4)
    behind_rs = RelationSymbol('Behind', 4)
    vocabulary = Vocabulary(['C1', 'C2'], [pm_rs, am_rs, ahead_rs, behind_rs], ['V1', 'V2'])

    profiles = [
        [pm_rs, ('hour', 1)],
        [am_rs, ('hour', 1)],
        [ahead_rs, ('hour', 1), ('minute', 1), ('hour', 2), ('minute', 2)],
        [behind_rs, ('hour', 1), ('minute', 1), ('hour', 2), ('minute', 2)]]

    mapping = {pm_rs: 1, am_rs: 2, ahead_rs: 3, behind_rs: 4}

    ai = AttributeInterpretation(vocabulary, attribute_structure, mapping, profiles)

    objects = ['s1', 's2']
    attribute_system = AttributeSystem(attribute_structure, objects)
    p = ConstantAssignment(vocabulary, attribute_system, {'C1': 's1', 'C2': 's2'})
    NamedState(
        attribute_system,
        p, {('hour', 's1'): [9, 13], ('minute', 's1'): [12], ('hour', 's2'): [8], ('minute', 's2'): [27]})

if __name__ == "__main__":
    main()