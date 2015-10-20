"""State object."""

#from assistance_functions import *
from copy import deepcopy
from ValueSet import ValueSet
from AttributeSystem import AttributeSystem
from AttributeSystem import AttributeStructure
from AttributeSystem import Attribute, Relation 

class State(object): 
    """
    Class for a state of an AttributeSystem
        
    attribute_system:       copy of Attriute system from which the state came;
                            stored as an AttributeSystem.
    ascriptions:            dictionary of attribute-object pair keys with
                            Attribute value sets as values.
    """

    def __init__(self, attribute_system, **ascriptions):
        """Return an initialized State object."""

        if not hasattr(attribute_system, "_is_AttributeSystem"):
            raise TypeError(
                "asys parameter must be of type AttributeSystem")

        self._attribute_system = deepcopy(attribute_system)
        self._ascriptions = {}
        self._is_state = True
        
        #Initialize the state as empty
        for Ai in self._attribute_system._attribute_structure._attributes:
            for s_i in self._attribute_system._objects:
                self._ascriptions[(Ai._label, s_i)] = deepcopy(Ai._value_set)

        #Set any ascriptions provided to constructor
        for ao_pair, valueset in ascriptions.iteritems():
            self.set_ascription(ao_pair, valueset)

        #break references by copying ascriptions
        self._ascriptions = deepcopy(self._ascriptions)

    def __eq__(self, other):
        """
        Return a boolean for whether or not self and other 
        State objects are equal.
        """

        #if AttributeSystems aren't the same, then States can't be
        if self._attribute_system != other_get_attribute_system:
            return False

        #if Attribute-object pairs are not the same, unequal
        if set(self._ascriptions.keys()) != set(other._ascriptions.keys()):
            return False
        #ValueSet is unordered, simple equality works for testing
        for ao_pair in self._ascriptions.keys():
            if self._ascriptions[ao_pair] != other._ascriptions[ao_pair]:
                return False

        return True
    
    def __ne__(self, other):
        """Implement != for State object."""
        
        return not self.__eq__(other)

    def __deepcopy__(self):
        """
        Implement copy.deepcopy for State object. 
        
        Constructor copies implicitly so just return new object.
        """
        
        return State(self._attribute_system, self._ascriptions)

    def set_ascription(self, ao_pair, new_valueset):
        """
        Set an ascription ao_pair (label,obj) value set to v.

        Raise TypeError if v parameter is not a list
        Raise ValueError if v parameter is not subset of valueset.
        Raise KeyError if ao_pair parameter not in ascriptions, 
        """
        
        new_values = None
        #Enforce new_value_set as a list, set, or ValueSet
        if isinstance(new_valueset, list) or isinstance(new_valueset, set):
            new_values = ValueSet(new_valueset)
        elif hasattr(new_value_set, "_is_ValueSet"):
            new_values = deepcopy(new_valueset)
        else:
            raise TypeError(
                "Ascription values must be of type list, set, or ValueSet")
        
        #ensure non-empty Ascriptions
        if not new_values:
            raise ValueError("Ascriptions must be non-empty.")

        #
        if ao_pair in self._ascriptions.keys():
            label, obj = ao_pair
            #Get ValueSet of Attribute with provided label in ao_pair
            attribute = self._attribute_system._attribute_structure[label]
            possible_values = attribute._value_set

            #If new value_set provided is a subset of the possible value_set of
            #the Attribute
            if new_values <= possible_values:
                self._ascriptions[ao_pair] = new_values
            else:
                raise ValueError(
                    str(new_values) + ' is not a subset of ' + 
                    str(possible_values))
        else:
            raise KeyError(
                str(ao_pair) + ' not in ascriptions')
    
    def __getitem__(self, key):
        """Implement indexing for State."""
        #if key is a string (i.e., label), return copy of list of ValueSets
        if type(key) == str:
            #get labels of all ascriptions
            labels = self._attribute_system._attribute_structure.get_labels()
            if key not in labels:
                raise KeyError(
                    key + " is not a valid Attribute label.")
            #extract objects
            objects = self._attribute_system._objects
            #get ascription ValueSets li(sj) with li = key 
            ascription_i = [self._ascriptions[(key, obj)] for obj in objects]
            return ascription_i
        #if key is an attribute-object pair return that li(sj)
        elif type(key) == tuple:
            if len(key) != 2:
                raise TypeError(
                    "key must be string or 2-tuple (attribute-object pair)")
            try:
                return self._ascriptions[key]
            except KeyError:
                raise KeyError(
                    str(key) + " not a valid key.")
        else:
            raise TypeError(
                "Only Attribute label strings and attribute-object "
                "2-tuples are valid keys")

    def is_valuation(self, label):
        """
        Determine if value set of ascription li is a valuation.

        raise KeyError of key parameter is not a valid ascription key.
        """

        #get list of li(sj) ValueSets with label provided 
        valuesets = self[label]
        #try to look up the valueset of given ao_pair
        for valueset in valuesets:
            if len(valueset) == 1:
                #if the only element in ValueSet is an Interval, ValueSet is
                #not a valuation
                if hasattr(valueset[0], "_is_Interval"):
                    return False
            else:
                return False
        return True

    def is_world(self):
        """Returns True if this State is a world; false otherwise."""
        for label in self._attribute_system._attribute_structure.get_labels():
            if not self.is_valuation(label):
                return False
        return True

    def is_extension(self, other):
        """
        Return a boolean for whether or not this State object is an 
        extension of other State object.

        raise TypeError if other parameter is not of Type State
        """

        if not isinstance(other, State):                                                #if other parameter is not a state
            raise TypeError(                                                            #explicitly raise a ValueError
                'other parameter must be of Type state')

        self_keys = self.get_ascription_keys()                                          #get a copy of this State's ascription keys
        other_keys = other.get_ascription_keys()                                        #get a copy of other State's ascription keys

        if self_keys == other_keys:                                                     #if the ascription keys for this State and the other State are the same
            for i in range(len(self_keys)):                                             #for each ascription key
                self_key = self_keys[i]                                                 
                other_key = other_keys[i]                                               #get copy of keys
                
                self_value_set = self.get_ascription(self_key)                          #get value set of the ascription in this State
                other_value_set = other.get_ascription(other_key)                       #get value set of the ascription in other State

                if not is_subset(self_value_set, other_value_set):                      #if this value set is not a subset of other value set
                    return False                                                        #not an extension, return False
        else: 
            return False                                                                #ascription keys aren't the same, not an extension of s
        
        return True                                                                     #every ascription in this State is a subset of the ascription in other State, it is an extension

    def is_proper_extension(self, other):
        """
        Return a boolean for whether or not this State object is a
        proper extension of other State object.

        raise TypeError if other parameter is not of Type State
        """

        so_extension = self.is_extension(other)                                         #determine if this State is an extension of other State
        os_extension = other.is_extension(self)                                         #determine if other State is an extension of this State

        if so_extension and not os_extension:                                           #if this State is an extension of other State but other State is not an extension of this State
            return True                                                                 #it is a proper extension, return True
        else:                                                                           #otherwise, return False
            return False

    def get_worlds(self):
        """
        Return a list of all possible worlds derivable from this 
        NamedState object.
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

        #get all ascriptions of this NamedState.
        ascriptions = copy.copy(
            [item for item in self.get_ascriptions().items()])

        value_sets = []
        labels = []

        #break down low-high tuples to get discrete version of all
        #possible values in each ascriptions value set.
        for (label, value_set) in ascriptions:
            tupleless_value_set = break_down_tuples(copy.copy(value_set))
            value_sets.append(tupleless_value_set)
            labels.append(label)

        combos = list(product(*value_sets))

        worlds = []

        #create each possible world from this NamedState and 
        #return them in a list.
        for values in combos:
            world = State(self.get_attribute_system())
            for i, label in enumerate(labels):
                world.set_ascription(label, [values[i]])
            worlds.append(world)

        return worlds

    def is_alternate_extension(self, s_prime, *states):
        """
        Determine if s_prime is an alternate extension of this State
        w.r.t. states s1,...,sm provided by optional positional
        arguments in states parameter.
        """

        if not isinstance(s_prime, State):
            raise TypeError(
                "s_prime parameter must be of type State.")

        #generate all alternate extensions of this State
        alternate_extensions = self.get_alternate_extensions(*states)

        #check if s_prime is within list of all alternate extensions
        for alternate_extension in alternate_extensions:
            if s_prime == alternate_extension:
                return True
        return False

    def get_alternate_extensions(self, *states):
        """
        Return all alternate extensions of this State object with
        respect to States s1,...,sm within the states parameter.

        Raise ValueError if state parameter is empty.
        Raise TypeError if any item in states parameter is not of
        type State.
        Raise ValueError if any of the states s1,...,sm is not a
        proper extenstion of this State object.
        """

        def get_properly_spanning_lists():
            """
            Return those lists that properly span s1,...,sm
            w.r.t. this State.

            This function is based on the algorithm found in the paper;
            as such, it follows its steps extremely closely.
            """

            #create filtered table of all proper subset ascriptions among all
            #the states; this is step 1 of the algorithm outlined in the paper.
            table = []
            for state in states:
                row = []
                for (label, value_set) in state.get_ascriptions().items():
                    if is_proper_subset(
                        state.get_ascription(label),
                        self.get_ascription(label)):
                        row.append([label, value_set])
                table.append(row)
            
            #make all possible spanning lists from filtered table
            #this is step 2 of the algorithm outlined in the paper.
            from itertools import product, combinations
            spanning_tuples = list(product(*table))
            spanning_lists = [list(tup) for tup in spanning_tuples]

            #we now proceed to step 3 of the algorithm outlined in the paper
            #by filtering out the non-properly spanning lists.
            for sl_index, spanning_list in reversed(
                list(enumerate(spanning_lists))):
                non_spanning_flag = False
                #try every sublist with a length greater than 1 as 1 is already
                #ensured not to be properly spanning by virtue of step 2.
                for i in range(2, len(spanning_list)+1):
                    sublists = list(combinations(spanning_list, i))
                    
                    for sublist in sublists:
                        
                        #check if sublist labels are homogeneous, i.e., 
                        #if a.o. pairs are all equal in sublist
                        labels = [ao_pair[0] for ao_pair in sublist]
                        if labels.count(labels[0]) == len(labels):
                            
                            #sublist is homogeneous so merge the value sets 
                            #of the a.o. pairs
                            value_sets = [ao_pair[1] for ao_pair in sublist]
                            #flatten value sets into signle merged list
                            merged_value_set = [
                                item for sublist in value_sets
                                for item in sublist]
                            
                            #determine if ascription in self is equal to union
                            #of merged ascriptions in sublist
                            equal_cond_1 = is_subset(
                                self.get_ascription(ao_pair[0]), 
                                merged_value_set)
                            equal_cond_2 = is_subset(
                                merged_value_set, 
                                self.get_ascription(ao_pair[0]))
                            
                            if equal_cond_1 and equal_cond_2:
                                non_spanning_flag = True
                                break
                    if non_spanning_flag:
                        break
                #if non-spannig flag was tripped, erase current spanning list
                #from the set of spanning lists; we're going in reverse so we
                #can do this in one pass
                if non_spanning_flag:
                    del spanning_lists[sl_index]

            return spanning_lists

        def make_ascriptions(proper_spanning_list):
            """
            Take the union of all sets of equal a.o. pairs and return
            a dictionary of the ascriptions with their value sets.
            """

            def delete_duplicates(value_set):
                """
                Delete duplicates in a value_set.

                Cannot use standard list(set(...)) as objects and nested
                lists may be elements in value_set.
                """

                del_indicies = []
                for i, v1 in enumerate(value_set):
                   for j, v2 in enumerate(value_set):
                       if i != j:
                           if isinstance(v1, list) and isinstance(v2, list):
                               if nested_equivalence(v1, v2):
                                   del value_set[i]
                                   return True
                           if v1 == v2:
                               del value_set[i]
                               return True
                return False

            #Make a default dict with empty list as default value so value sets
            #can be extended when there are multiple a.o. pair copies in
            #proper_spanning_list 
            from collections import defaultdict
            ascriptions = defaultdict(lambda: [])
            for (ao_pair, value_set) in proper_spanning_list:
                ascriptions[ao_pair].extend(value_set)
            
            #There could be duplicates in ascriptions from extending lists;
            #delete any duplicates that might be in ascriptions. 
            for (ao_pair, value_set) in ascriptions.items():
                 value_set = ascriptions[ao_pair]
                 while delete_duplicates(value_set): pass

            #cast back to a regular dict and return
            return dict(ascriptions)

        def make_alternate_extension(proper_spanning_list):
            """
            Make an alternate extension from a single properly spanning list.
            """

            #First make a new copy of this State and create the ascriptions
            #available from the properly spanning list
            ae = State(self.get_attribute_system(), self.get_ascriptions())
            ascriptions = make_ascriptions(proper_spanning_list)

            #for each ascription, complement it w.r.t. the original ascription
            #and replace the original ascription with the complement
            for (label, value_set) in ascriptions.items():
                complement_value_set = get_set_theoretic_difference(
                    ae.get_ascription(label), value_set)
                ae.set_ascription(label, complement_value_set)
            
            return ae

        #check for exceptions first
        
        if not states:
            raise ValueError(
                "at least one State object must be provided as an argument")

        for state in states:
            if not isinstance(state, State):
                raise TypeError(
                    "all optional positional arguments must be of type State.")

        for state in states:
            if not state.is_proper_extension(self):
                raise ValueError(
                    "all states provided must be proper "
                    "subsets of this State object.")

        proper_spanning_lists = get_properly_spanning_lists()
        
        alternate_extensions = []
        for psl in proper_spanning_lists:
            ae = make_alternate_extension(psl)
            alternate_extensions.append(ae)

        return alternate_extensions

    def __str__(self):
        s = ''
        for delta_i in sorted(self._ascriptions.keys(), key=lambda tup: tup[1]): 
            #s += delta_i[0] + '(' + delta_i[1] + '): ' + str(self._ascriptions[delta_i]) + '\n'                #used for debugging; shows in list for and not notation
            s += delta_i[0] + '(' + delta_i[1] + '): {' + str(self._ascriptions[delta_i])[1:-1] + '}' + '\n'
        return s[:-1]

def main():
    """."""
    a, b, c = Attribute("a", ["A", 1]), Attribute("b", ["B", 2]), Attribute("c", ["C", 3])
    r = Relation("R1(a,b) <=> ", ["a", "b"], 1)

    a = AttributeStructure(a, b, c, r)
    o = ['o3', 'o1']

    asys = AttributeSystem(a, o)
    s = State(asys)
    s.set_ascription(('a', 'o3'), [1])
    s.set_ascription(('a', 'o1'), ['A'])
    #print s['a']
    #print s.is_valuation('a')


if __name__ == "__main__":
    main()