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
        
        ordered_set_terms = []
        for t in terms:
            if t not in ordered_set_terms:
                ordered_set_terms.append(t)

        from copy import deepcopy
        self._vocabulary = deepcopy(vocabulary)
        self._name = deepcopy(name)
        self._terms = ordered_set_terms
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

        def get_relation_arguments(definition):
            """Return the arguments provided in Relation definition."""

            start_paren = definition.find('(')
            end_paren = definition.find(')')

            arg_string = definition[start_paren+1:end_paren]
            return arg_string.split(',') 

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

        
        for entry in attribute_interpretation:
            if entry[0]._name == self._name:
                R_I = entry
                break
        else: 
            raise ValueError(f._name + " must be in intepretation table")

        p = named_state._p
        profile = list(R_I[3])
        terms = self._terms
        relation = named_state._attribute_system._attribute_structure[int(R_I[2][1:])]

        if len(profile) != len(relation._DR):
            raise ValueError(
                    "number of profile pairs must be equal to the number "
                    "of arguments the relation takes")

        #compiling profile into attribute object pairs that will be substituted into the expression

        #check if each index is valid in respect to list of terms
        #i.e., j_x has corresponding (t^{p,X})_{j_x}
        for index in [pair[1] for pair in profile]:
            if index > len(terms): raise ValueError(
                "each index corresponds to an index in formula's terms list; "
                "indicies may not exceed the amount of terms") 

        #for each pair in profile grab formula term corresponding to the
        #pair's index; shifted down 1 as indexing starts at 0 and not 1 then
        #rewrite that pair with the corresponding term instead of index
        for i, pair in enumerate(profile):
            term = terms[pair[1] - 1]
            profile[i] = (pair[0], term)

        #Replace Vocabulary C and V's with their respective objects
        #according to p and X
        for i, pair in enumerate(profile):
            try: 
                obj = p._mapping[pair[1]]
            except KeyError:
                try:
                    obj = X._mapping[pair[1]]
                except KeyError:
                    return "unknown"

            profile[i] = (pair[0], obj)


        relation_args = get_relation_arguments(relation._definition)
        worlds = named_state.get_worlds()

        #sort by longest arguments firsts so we can ensure unambiguous
        #replacement when swapping in the valuations associated with the
        #ao_pairs from each world into the relation definition
        relation_args, profile = (list(t) for t in zip(
                *sorted(zip(relation_args, profile), key=lambda x: len(x[0]),
                reverse=True)))

        truth_values = []
        for world in worlds:
            #break reference from Relation
            definition = str(relation._definition)
            #zip arguments in Relation and valuations together
            valuations = [world._ascriptions[ao_pair] for ao_pair in profile]
            substitutions = zip(relation_args, valuations)

            for substitution in substitutions:
                pattern, valueset = substitution
                #we're swapping in a valuation valueset so just shed the prefix
                #'V(' and suffix ')'
                value = str(valueset)[2:-1]
                definition = definition.replace(pattern, value)
            
            from TruthValueParser import TruthValueParser 
            lmtp=TruthValueParser()
            #trim the LHS of the definition to create evaluatable expression
            expression = definition[definition.find(" <=> ")+5:]
            result=lmtp.eval(expression)
            truth_values.append(result)

        if all(truth_values):
            return True
        elif not any(truth_values):
            return False
        else:
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
    from VariableAssignment import VariableAssignment
    from NamedState import NamedState

    a = Attribute('hour', [Interval(0, 23)])
    a2 = Attribute('minute', [Interval(0, 59)])
    r_pm = Relation('R1(h1) <=> h1 > 11', ['hour'], 1)
    r_am = Relation('R2(h1) <=> h1 <= 11', ['hour'], 2)
    r_ahead = Relation('R3(h1,m1,hhh2,mm2) <=> h1 > hhh2 or (h1 = hhh2 and m1 > mm2)', ['hour', 'minute', 'hour', 'minute'], 3)
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
    ns = NamedState(attribute_system, p, {('hour', 's1'): [9, 13], ('minute', 's1'): [12], ('hour', 's2'): [8], ('minute', 's2'): [27]})

    f = Formula(vocabulary, 'Ahead', 'C1', 'C2')
    print f.assign_truth_value(
        ai, ns, VariableAssignment(vocabulary, attribute_system, {}, dummy=True))

if __name__ == "__main__":
    main()