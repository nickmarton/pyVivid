"""State class."""

from AttributeSystem import Attribute, Relation
from AttributeSystem import AttributeStructure
from AttributeSystem import AttributeSystem

class State(object): 
    """
    Class for a state of an AttributeSystem
        
    asys: copy of Attriute system from which the state came; 
    stored as an AttributeSystem
    ascriptions: dictionary of attribute-object pair keys with 
    corresponding ascription value sets as values
    """

    def __init__(self, asys, ascriptions=None):
        """
        Return an initialized State object.

        Raise TypeError if asys parameter is not of type 
        AttributeSystem.
        Raise TypeError if ascriptions parameter is None or not of type
        dict.
        """

        if not isinstance(asys, AttributeSystem):                                       #if asys parameter is not of type AttributeSystem
            raise TypeError(                                                            #explicitly raise TypeError
                "asys parameter must be of type AttributeSystem")

        self._attribute_system = asys                                                   #give state copy of Attributesystem for covenience
        self._ascriptions = {}                                                          #init ascriptions to dictionary
        
        for A_i in self._attribute_system._attribute_structure.get_attributes():        #for every Attribute in the system
            l_i, v_i = A_i.get_label(), A_i.get_possible_values()                       #get the label and possible values of it
            for s_i in self._attribute_system.get_objects():                            #for all objects in system
                self._ascriptions[(l_i, s_i)] = v_i                                     #init ascription with label object pair as key and value set as value

        if ascriptions:
            if not isinstance(ascriptions, dict):
                raise TypeError(
                    "ascriptions parameter must be of type dict.")

            for label, value_set in ascriptions.items():
                self.set_ascription(label, value_set)

    def __eq__(self, other):
        """
        Return a boolean for whether or not self and other 
        State objects are equal.
        """

        if self.get_attribute_system() != other.get_attribute_system():                 #if AttributeSystems aren't the same, then States can't be
            return False
        
        for k, v in self.get_ascriptions().iteritems():                                 #for each key value pair in ascriptions
            if k not in other.get_ascriptions():                                        #if label object pair isn't a key in other
                return False
            else:
                pq_cond = is_subset(v, other.get_ascriptions()[k])
                qp_cond = is_subset(other.get_ascriptions()[k], v)
                if not pq_cond or not qp_cond:                                     #if label object pair is a key but value sets are different
                    return False
        return True
    
    def __ne__(self, other):
        """
        Return a boolean for whether or not self and other 
        State objects are equal.
        """
        
        if self.get_attribute_system() != other.get_attribute_system():                 #if AttributeSystems aren't the same, then States can't be
            return True
        
        for k, v in self.get_ascriptions().iteritems():                                 #for each key value pair in ascriptions
            if k not in other.get_ascriptions():                                        #if label object pair isn't a key in other
                return True
            else:
                pq_cond = is_subset(v, other.get_ascriptions()[k])
                qp_cond = is_subset(other.get_ascriptions()[k], v)
                if not pq_cond or not qp_cond:                                     #if label object pair is a key but value sets are different
                    return True
        return False

    def deep_copy(self):
        """Provide a deep_copy of this State object."""
        import copy

        attribute_system_copy = self._attribute_system.deep_copy()
        ascriptions_copy = copy.copy(self._ascriptions)

        return State(attribute_system_copy, ascriptions_copy)

    def get_attribute_system(self): 
        """Return the underlying AttributeSystem of this State."""

        return self._attribute_system
    
    def get_ascriptions(self): 
        """Return the ascriptions of this State."""

        return self._ascriptions
    
    def get_ascription_keys(self):
        """get the label, object pairs of ascriptions of this State."""

        return self._ascriptions.keys()

    def set_ascription(self, key, v):
        """
        Set an ascription key (label,obj) value set to v;

        raise TypeError if v parameter is not a list
        raise KeyError if key parameter not in ascriptions, 
        raise ValueError if v parameter is not subset of valueset.
        """
        
        if not isinstance(v, list):                                                     #if v parameter is not of type list
            raise TypeError(                                                            #explicitly raise TypeError
                'v parameter must be of type list') 
        
        if key in self._ascriptions:                                                    #if key parameter is a valid key in this State's ascriptions
            
            possible_values = self.get_attribute_system()\
                                .get_attribute_structure()\
                                    .get_attribute(key[0])\
                                        .get_possible_values()                          #get possible values Attribute with label provided in key can take on
            

            if is_subset(parse(v), possible_values):                                    #if the value set is a subset of the value set currently in the ascription
                self._ascriptions[key] = copy.copy(parse(v))                            #replace the old value set with v parameter 
            else:                                                                       #v parameter is not a subset of current value set
                raise ValueError(                                                       #explicitly raise ValueError
                    'v parameter is not a subset of ' + str(
                        self._ascriptions[key]))
        else:                                                                           #key parameter is not a valid ascription key
            raise KeyError(                                                             #explicitly raise KeyError
                str(key) + ' not in ascriptions')
    
    def get_ascription(self, key):
        """
        Return the value set of the ascription with key parameter;

        raise KeyError if key parameter is not a valid ascription key.
        """

        if key in self._ascriptions:                                                    #if key parameter is a valid ascription key
            return self._ascriptions[key]
        else:                                                                           #otherwise,
            raise KeyError(                                                             #explicitly raise KeyError
                str(key) + ' is not a valid ascription key')

    def is_valuation(self, key):
        """
        Determine if value set of ascription key matching key parameter
        is a valuation; 

        raise KeyError of key parameter is not a valid ascription key.
        """
        
        if not key in self.get_ascriptions():                                           #if key parameter is not a valid ascription key
            raise KeyError(                                                             #explicitly raise KeyError
                key + " is not a valid key")
        else:                                                                           #key parameter is a valid ascription key
            value_set = self._ascriptions[key]                                          #get a copy of value set at that ascription key
        

        length_condition = len(value_set) == 1                                          #determine if there's only one element in value set                             
        if length_condition:
            if isinstance(value_set[0], tuple):                                         #if sole element is a low-high tuple
                return False                                                            #ascription is not a valuation
            else:                                                                       #otherwise, ascription is a valuation
                return True
        else:                                                                           #more than 1 element in value set so ascription is not a valuation
            return False

    def is_world(self):
        """Returns True if this State is a world; false otherwise."""

        for key in self.get_ascription_keys():                                          #for every ascription key
            if not self.is_valuation(key):                                              #if the value set of a particular ascription is not a valuation
                return False                                                            #this State is not a world, return False
        return True                                                                     #all ascriptions are valuations, this State is a world

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
    """Main method; quick testing."""

    a, b, c = Attribute("a", []), Attribute("b", []), Attribute("c", [])
    r = Relation("R1(a,b) <=> ", ["a", "b"])

    a = AttributeStructure(a, b, c, r)
    o = ['o1', 'o2']

    asys = AttributeSystem(a, o)
    s = State(asys)

if __name__ == "__main__":
    main()
