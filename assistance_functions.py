from __future__ import division
from pyparsing import (Literal,CaselessLiteral,Word,Combine,Group,Optional,
                       ZeroOrMore,Forward,nums,alphas,oneOf)
import math
import operator
import copy
import inspect
#from Point import Point
#from mapping import pygame_mapping

######################################################################################################################
#                                                  Debug functions                                                   #
######################################################################################################################

def get_caller():
    """return the caller """
    curframe = inspect.currentframe() 
    calframe = inspect.getouterframes(curframe, 2)
    return 'caller name:', calframe[2][3]

def write_debug():
    f = open('debug.txt', 'w')
    for line in debug:
        f.write(line)

debug = []

######################################################################################################################
#                                                     Globals                                                        #
######################################################################################################################

class Stack:
    """simple Stack class; used in parse only as of now."""

    def __init__(self):
        """Use a simple list for stack storage."""
        
        self.items = []

    def isEmpty(self):
        """Return boolean for whether or not stack is empty."""
        
        return self.items == []

    def push(self, item):
        """Push item parameter into the stack."""
        
        self.items.append(item)

    def pop(self):
        """Pop top element off of the stack."""

        return self.items.pop()

    def peek(self):
        """Return copy of top most stack element without removing it."""

        return self.items[len(self.items)-1]

    def size(self):
        """Return size of the stack as integer."""

        return len(self.items)


flat_flag = False

float_df = .001

def set_flat_flag(boolean):
    """Set flat parameter to flatten nested groups."""

    if not isinstance(boolean, bool):                                                   #if boolean parameter not a bool, raise TypeError
        raise TypeError(                                                                #explictly raise TypeError
            'boolean parameter must be of type bool'
            )
    global flat_flag                                                                    #bring global flag for flattening into local namespace
    flat_flag = boolean                                                                 #set it to boolean parameter

def get_flat_flag():
    """Return flat_flag."""

    global flat_flag
    return flat_flag

def set_float_df(flt):
    """Set float differential to for merging singles during parsing or get_set_theoretic_difference."""

    if not isinstance(flt, float):                                                      #if flt parameter not a float, raise TypeError
        raise TypeError(                                                                #explictly raise TypeError
            'flt parameter must be of type float'
            )
    
    if flt <= 0:                                                                        #if provided differential is less than or equal to 0
        raise ValueError(                                                               #explicitly raise ValueError
            'flt parameter must be positve'
            )

    global float_df                                                                     #bring global float differential float_df into local namespace
    float_df = flt                                                                      #set it to flt parameter

def get_float_df():
    """Return float_df."""

    global float_df
    return float_df

######################################################################################################################
#                                                  Vivd functions                                                    #
######################################################################################################################

def thinning(ns1, ns2):
    """if ns1 is obtainable from ns2 by thinning, return True and False otherwise; raise TypeError if either param is not a named state"""
    from vivid import NamedState
    if not isinstance(ns1, NamedState): 
        raise TypeError(str(ns1) + ' must be type NamedState')
    if not isinstance(ns2, NamedState): 
        raise TypeError(str(ns2) + ' must be type NamedState')
    if NamedState.is_extension(ns1, ns2): 
        return True
    else: 
        return False

def widening(ns1, ns2):
    """if ns2 is obtainable from ns1 by widening, return True and False otherwise; raise TypeError if either param is not a named state"""
    
    return thinning(ns2, ns1)                                                           #widening is converse of thinning, so pass thinning converse

def collapse(tuples):
    """functions to collapse overlaping tuples."""
    
    for i, t in enumerate(tuples):
        for j, t2 in enumerate(tuples):
            if t != t2:
                if t[0]  <  t2[0] and t[1]  <= t2[1] and t[1] >= t2[0]:         #if (t[)t2]
                    tuples.append((t[0], t2[1]))                                    #append collapsed representation of the two tuples to tuples, then start again via while True call
                    if i < j:                                                       #delete in correct order to not fuck iterator
                        del tuples[j]
                        del tuples[i]
                    if j < i:                                                       #delete in correct order to not fuck iterator
                        del tuples[i]
                        del tuples[j]
                    return True
                if t2[0] <= t[0]  and t[1]  <= t2[1]:                               #if (t2(t)t2)
                    del tuples[i]                                                   #delete t, start over
                    return True
                if t2[0] <= t[0]  and t2[1] <  t[1]  and t2[1] >= t[0]:         #if [t2(]t)
                    tuples.append((t2[0], t[1]))                                    #append collapsed representation of the two tuples to tuples, then start again via while True call
                    if i < j:                                                       #delete in correct order to not fuck iterator
                        del tuples[j]
                        del tuples[i]
                    if j < i:                                                       #delete in correct order to not fuck iterator
                        del tuples[i]
                        del tuples[j]
                    return True
                if t[0]  <  t2[0] and t2[1] <  t[1] :                               #if (t(t2)t)
                    del tuples[j]
                    return True
    return False

def nested_equivalence(g1, g2):
    """
    Return boolean for whether two nested groupings (NOTE: NESTED GROUPINGS MEANS PARSED LISTS ONLY) are equivalent 

    when elements are not in same order but in same level they are equvalent provided every element is accounted for
    note: this function can only handle wrapping in extra lists if shrink is turned on which it is by default;

    nested_equivalence(
        [[[[[80, 7, 900.0], 69], 23], 12, 3, 5], [[[55], 6009], 50], -11111, 0, 651, 900],
        [[[[55], 6009], 50], [[[[7, 80, 900.0], 69], 23], 12, 5, 3], 900, 0, 651, -11111]
    )
    evaluates to true, but

    nested_equivalence(
        [[[[[[80, 7, 900.0], 69], 23], 12, 3, 5], [[[55], 6009], 50], -11111, 0, 651, 900]],
        [[[[[55], 6009], 50], [[[[7, 80, 900.0], 69], 23], 12, 5, 3], 900, 0, 651, -11111]]
    )
    evaluates to false when shrink is turned off

    if shrink is on, both evaluate to true
    as does 
    nested_equivalence(
        parse(['{{{3}}}']),
        parse(['{3}'])
    )

    internal functions parse and is_subset operate with shrink turned off, 
    however shrink defaults to on so that calls to parse do not show buggy behavior as in the first example above
    p1 = parse('')

    NOTE: nested_equivalence is used in parse, is_subset, and get_set_theoretic_difference; in all cases it is turned OFF.
    """

    count = []

    def shrink_list(lis):
        """Return a shrunk copy of lis parameter; i.e., remove all encapsulating lists of length 1."""

        while type(lis) == list and len(lis) == 1 and type(lis[0]) == list:         #while lis parameter is a list of length 1
            lis = lis[0]                                                                #remove encapsulating list

        return lis

    def get_depth(l) :
        if isinstance(l, list):
            if l:
                return 1 + max(get_depth(item) for item in l)
            else:
                return 1
        else:
            return 0

    def get_list_count(lis):
        """Return an int representing the amount of sublists within lis parameter."""

        list_count = 0
        for element in lis:
            if type(element) == list:
                list_count += 1
        return list_count

    def compare(n1, n2):
        """
        Return boolean for whether or not n1 and n2 are deeply equivalent 

        Deeply equivalent can be understood as follows:
        if n1 and n2 have the same elements at each level as each other regardless of ordering
        outer variable count is used to keep track of how many top level base classes are matched. 
        As a consequence of forcing the lists to be same length before pairing i.e., 'if len(n1_lists) == len(n2_lists):', finding a match for i also finds j's match
        this means that we do not have to repeat the process with i and j in reversed.
        This algorithm is profoundly confusing; I arrived at the answer by accident, but I assure you it works.
        """

        def split_lists_from_nonlists(lis):
            """Split elements of list into lists and nonlists."""

            lists = []
            nonlists = []

            for element in lis:                                                         #for each element in n1
                if isinstance(element, list):                                           #if its a list, add to n1_lists
                    lists.append(element)
                else:                                                                   #otherwise, add to n1_non_lists
                    nonlists.append(element)

            return lists, nonlists

        n1_lists, n1_nonlists = split_lists_from_nonlists(n1)
        n2_lists, n2_nonlists = split_lists_from_nonlists(n2)

        if simple_compare(n1_nonlists, n2_nonlists):                                    #if non-sublist elements can be mapped to one another
            if n1_lists:                                                                #if there are still sublists, i.e., we need to recur again
                if len(n1_lists) == len(n2_lists):                                      #if those sublists are equal in length
                    for i in n1_lists:                                                  #for each sublist i in n1
                        for j in n2_lists:                                              #for each sublist j in n2
                            if compare(i, j):                                           #recur, trying to find a match for i with every possible pairing of sublists in n2
                                break                                                   #if a match was found, break as we no longer consider the rest of n2
            else:                                                                       #base case; no sublists left and non-sublist elements can be mapped to one another
                count.append(1)                                                         #increment count list; each entry corresponds to a top level sublist being matched
                #return True                                                             #return True to cut search space a little

    def simple_compare(n1, n2):
        """Return boolean for whether or not lists of depth 1 are equivalent."""

        def match_element(element, lis):
            """Return boolean for whether element parameter is contained in lis and deletes that item from lis if it is present."""

            for i, e in enumerate(lis):                                             #for each element e in lis,
                if e == element:                                                        #if i matches element parameter
                    del lis[i]                                                          #delete e from lis
                    return True
            return False


        c1 = copy.copy(n1)                                                              #create a copy of n1 to avoid pass by reference
        c2 = copy.copy(n2)                                                              #create a copy of n2 to avoid pass by reference
        c2_cpy = copy.copy(c2)                                                          #create extra copy of n2 as first will be modified
        
        for i in c1:                                                                    #for each element in n1
            if not match_element(i, c2):                                                #check if it has a match in n2 while deleting match from n2 if found
                return False                                                            #no match, not equivalent

        for j in c2_cpy:                                                                #for each element in n2
            if not match_element(j, c1):                                                #check if it has a match in n1 while deleting match from n1 if found
                return False                                                            #no match, not equivalent

        return True                                                                     #n1 and n2 are one-to-one, return True

    def split_singles(lis):
        """Split singles from lis parameter."""

        singles = []
        groups = []

        for item in lis:
            if isinstance(item, list):
                groups.append(item)
            else:
                singles.append(item)

        return groups, singles

    group1 = parse(copy.copy(g1))                                                       #create copy of parameters to avoid pass by reference
    group2 = parse(copy.copy(g2))                                                       #create copy of parameters to avoid pass by reference

    group1 = shrink_list(group1)                                                        #reassign group1 as a shrunk version of itself
    group2 = shrink_list(group2)                                                        #reassign group2 as a shrunk version of itself

    group1, singles1 = split_singles(group1)
    group2, singles2 = split_singles(group2)

    d1 = get_depth(group1)                                                              #get depth of the first list
    d2 = get_depth(group2)                                                              #get depth of the second list

    if d1 == d2:                                                                        #if the two lists have the same amount of levels
        if d1 == 1:                                                                     #if there are no sublists
            return simple_compare(singles1, singles2)                                       #do simple comparison

        #if not simple_compare(singles1, singles2) :
        #    return False        

        compare(group1, group2)                                                         #compare pushes entries into count representing number of total top level sublist matches

        g1_list_count = get_list_count(group1)                                          #get count of sublists in g1
        g2_list_count = get_list_count(group2)                                          #get count of sublists in g1

        #print str(g1_list_count) + '\t' + str(g2_list_count) + '\t' + str(count)

        #print g1
        #if len(g1) > 1 and count:
        #    del count[0]

        if len(count) == g1_list_count and g1_list_count == g2_list_count:              #if sublists match 1-to-1 in g1 and g2 and non sublists also match, i.e., they are deeply equivalent
            return True                                                                 #return True
        else:                                                                           #otherwise, not deeply equivalent
            return False                                                                #return False
    else:
        return False

def parse_int_float_string(possible_number):
    """Return int, float, or string depending on validity of possible_number parameter"""
    try:
        if '.' in possible_number:
            e_float = float(possible_number)                                    #int parsing failed, try to parse to float and return
            return e_float
        else:
            e_int = int(possible_number)                                            #try to parse element as an int and add return
            return e_int
        
    except ValueError:                                                                 #float parsing failed, return as string
        return possible_number          

def parse(set1):
    """
    Parse set1 paramter into a list of individual elements and low-high tuples

    parse considers the following types of individual element in the set1 paramter (of type list):
    individual elements,                                                            e.g. 'f', 1, 'word', 100, 12.34             ->      ['f', 1, 'word', 100, 12.34]
    a group of elements in set notation,                                            e.g. '{1, 2, 3, 7, 9, 'f', 12.34}'          ->      [1, 2, 3, 7, 9, 'f', 12.34]
    a group of elements in a tuple,                                                 e.g. '(1, 2, 3, 7, 9, 'f', 12.34)'          ->      [1, 2, 3, 7, 9, 'f', 12.34]
    a group of elements in brackets,                                                e.g. '[1, 2, 3, 7, 9, 'f', 12.34]'          ->      [1, 2, 3, 7, 9, 'f', 12.34]
    a string (note: commas in stirng are ignored; a string is a string),            e.g. 'fresh,yo'                             ->      ['fresh,yo']
    continuous ranges denoted by ellipses (note: this creates a low-high tuple),    e.g. '-12.3,...,10' or '15,...,90,...,2000' ->      [(-12.3, 10.0), (1, 2000)]
    boolean types,                                                                  e.g. True, False                            ->      [True, False]
    iterables (note: iterables are groups, however low-highs are auto parsed),      e.g. (1,2,3), [4,5,6], (1,90), (10,'f')     ->      [[1,2,3], [4,5,6], (1,90), [10, 'f']]

    parse supports arbitrarily nested groups e.g. '{-11111,0,{12,3,{23,{69,{80,7,900}}},5},651,900}', however, don't mix and match different grouping characters in same string
    (note: nested groups allow for duplicates, that is, you can have copies of the same nested group or multiple single elements on the same level provided they parse to the same output)

    Overlapping low-high tuples are collapsed and individual numbers are absorbed by low-high tuples when they fall within range.
    low-high tuples where low==high are converted to a single number
    if low or high is a float, by default the other will be converted to a float

    note: when flattening, if flattened list has a float with the same value as an int also in list, 
    whichever one comes 2nd is treated as a duplicate and deleted as flatten() casts list to built in python type set and back

    as of now, parse is used in the functions: 
    Attribute.set_possible_values(), 
    is_alternate_extension(),
    is_subset(),
    get_set_theoretic_difference(),
    State.set_ascription()

    input:
    set1: a list containing any combination of above types
    flat: a boolean to determine whether or not to flatten any nested groups
    
    exceptions will be raised in the following cases:
    set1 paramter is not a list,
    a grouping is invalidly formatted i.e., it is not a group of correctly formatted elements separated by single commas 
    starting with a single opening character and ending with that character's corresponding closing character
    (note:inner quotes are not supported as of now; grouping elements will try to be parsed to ints or floats and default to string if parsing fails),
    ellipses begin or end a potential low-high tuple string (note: this is for time being until infinite sets are figured out),
    a grouping that contains a subgroup with different grouping characters than the supergroup

    output:
    a list containing only single elements and low-high tuples.
    """

    #print get_caller()

    #handle exception case 1
    if not isinstance (set1, list):                                                 #if parse parameter is not of type list
        raise TypeError(                                                                #explicitly raise a TypeError
            'set1 parameter must be of type list'
            )

    def parse_element(e):
        """parse an individual element according to specifications laid out in parse docstring"""

        def is_iterable(iter_element):
            """Return boolean for whether or not iter_element parameter is an iterable"""
            
            if isinstance(iter_element, tuple):                                     #if iter_element parameter is a tuple
                if len(iter_element) == 2:
                    left_valid = type(iter_element[0]) == int or type(iter_element[0]) == float
                    right_valid = type(iter_element[1]) == int or type(iter_element[1]) == float 
                    if left_valid and right_valid:
                        return False
                return True                                                             #return True
            elif isinstance(iter_element, list):                                        #if iter_element parameter is a list
                return True                                                             #return True
            elif isinstance(iter_element, dict):                                        #if iter_element parameter is a dict
                raise TypeError(                                                        #raise TypeError; dicts not supported as elements
                    'elements of type dict are not supported'
                    )
            else:
                return False

        def iterable_to_grouping(iter_element):
            """Return list of iterable iter_element parameter"""

            if isinstance(iter_element, tuple):                                     #if iter_element parameter is a tuple
                return list(iter_element)                                               #return it as a list
            elif isinstance(iter_element, list):                                        #if iter_element parameter is a list
                return iter_element                                                     #return it as it is

        def is_low_high_tuple(tup):
            if isinstance(tup, tuple):                                          #if tup parameter is a tuple
                if len(tup) == 2:
                    left_valid = type(tup[0]) == int or type(tup[0]) == float
                    right_valid = type(tup[1]) == int or type(tup[1]) == float 
                    if left_valid and right_valid:
                        return True
            return False

        def enforce_low_high_tuple(tup):
            """Given a low-high tuple candidate, return it in correct order or as single"""

            float_flag = type(tup[0]) == float or type(tup[1]) == float                 #determine if either low or high is a float

            if tup[0] == tup[1]:                                                        #if low equals high
                if float_flag:                                                          #return single as a float if either low or high is a float
                    return float(tup[0])                                                #return as a single
                else:                                                                   
                    return tup[0]                                                       #simply return single
            if tup[0] < tup[1]:                                                     #if low is less than high
                if float_flag:                                                          #if either low or high is a float
                    return (float(tup[0]), float(tup[1]))                               #return as a single
                else:                                                                   #otherwise
                    return e                                                            #simply return
            if tup[0] > tup[1]:                                                     #if low is greater than high
                if float_flag:                                                          #if either low or high is a float
                    return (float(tup[1]), float(tup[0]))                               #return as floats in reversed order
                else:                                                                   #otherwise
                    return (tup[1], tup[0])                                             #return in reverse

        #handles exception cases 2, 4
        def is_grouping(s):
            """Return boolean for whether or not s parameter is a grouping."""
            
            def do_left_right_match(l, r):
                """Return boolean for whether left and right grouping chars match."""
                
                if l == '{':
                    if r == '}':
                        return True
                    else:
                        return False
                if l == '(':
                    if r == ')':
                        return True
                    else:
                        return False
                if l == '[':
                    if r == ']':
                        return True
                    else:
                        return False

            def is_inside_correctly_formatted(left, right, grouping):
                """Return boolean for whether or not grouping is formatted correctly inside of grouping characters."""

                def contains_other_grouping_chars(left, right, grouping_string):
                    """Return boolean for whether or not grouping_string parameter contains subgroup with different grouping characters than supergroup"""
                    
                    if left == '{' and right == '}':                                    #if left and right grouping chars in uspergroup are {}
                        if '(' in grouping_string or ')' in grouping_string\
                         or '[' in grouping_string or ']' in grouping_string:           #if other grouping characters are in string, return True
                            return True
                        else:                                                           #otherwise, return True
                            return False
                    elif left == '(' and right == ')':                                  #if left and right grouping chars in uspergroup are ()
                        if '{' in grouping_string or '}' in grouping_string\
                         or '[' in grouping_string or ']' in grouping_string:           #if other grouping characters are in string, return True
                            return True
                        else:                                                           #otherwise, return True
                            return False
                    elif left == '[' and right == ']':                                  #if left and right grouping chars in uspergroup are []
                        if '{' in grouping_string or '}' in grouping_string\
                         or '(' in grouping_string or ')' in grouping_string:           #if other grouping characters are in string, return True
                            return True
                        else:                                                           #otherwise, return True
                            return False
                    else:                                                               #left and right are mismatched, explicitly raise ValueError
                        raise ValueError(
                            'cannot have mismatched grouping ' +
                            'characters at begin and end of a grouping'
                            )

                group_elements = grouping.split(',')                                    #split grouping up by commas

                if '' in group_elements:                                                #if two commas are used in a row, incorrect formatting
                    return False                                                        #return False
                else:                                                                   #elements are separated by single commas, correct formatting
                    if not contains_other_grouping_chars(left, right, grouping):        #if subgroup in grouping does not have different grouping chars
                        return True                                                     #return True
                    else:                                                               #otheriwse return False
                        return False

            if not isinstance(s, str):                                              #a grouping has to be of type string
                return False
            
            left = s[0]                                                                 #get first character of string
            right = s[-1]                                                               #get last character of string

            left_cond = left == '{' or left == '(' or left == '['                       #check if first char is a left grouping char
            right_cond = right == '}' or right == ')' or right == ']'                   #check if last char is a right grouping char
            
            if left_cond and right_cond:                                                #if both first and last chars are grouping chars
                match = do_left_right_match(left, right)                                #check if they match
                if match == True:                                                       #if they do, return True
                    format_flag = is_inside_correctly_formatted(                        #determine if inside is correctly formatted
                        left,
                        right,
                        s[1:len(s)-1]
                        )
                    if format_flag:                                                 #if inside of grouping is correctly formatted
                        return True                                                     #return True
                    else:                                                               #inside of grouping is incorrectly formatted
                        raise ValueError(                                               #raise ValueError
                            'inside of grouping is incorrectly formatted'
                            )
                else:                                                                   #they don't match but grouping chars are used
                    raise ValueError(                                                   #raise ValueError
                        'cannot have a grouping with mismatched ' +
                        'grouping characters in element of input_list'
                        )
            
            return False                                                                #not a grouping if first and last chars aren't grouping chars, return False

        def parse_grouping(group_string):
            """Return a parsed grouping element as an int, float, or string."""

            def extract_subgroup(left, right, expr):
                """
                Return boolean for whether or not expr parameter is balanced, that is, whether opening and closing characters have same count.
                
                input:
                left: left grouping character
                right: right grouping character
                expr: expression to extract subgroups from

                output:
                a list of subgroups present in expr parameter
                """

                s = Stack()
                balanced = True
                index = 0

                subgroups = []
                build_str = ''

                while index < len(expr) and balanced:                                   #while index is less than length of expr and expr is balanced
                    symbol = expr[index]                                                #get char at index of expr
                    
                    if symbol != left and symbol != right:                          #if the symbol is neither opening or closing grouping char
                        build_str += symbol                                             #add it to the build string
                        index = index + 1                                               #increment index
                        continue                                                        #loop to next char

                    if symbol == left:                                                  #if symbol is opening grouping char
                        s.push(symbol)                                                  #push it into the stack
                        build_str += symbol                                             #also add it to build string
                    else:                                                               #not opening goruping char
                        if s.isEmpty():                                                 #if stack is empty
                            balanced = False                                            #expr is not balanced
                        else:                                                           #otherwise
                            build_str += right                                          #add closing grouping char to build string
                            s.pop()                                                     #pop opening character off of stack

                    if s.isEmpty():                                                     #if stack is empty at this point in expr, we may have a built subgroup
                        subg_index = build_str.find(left)                               #get starting index of subgroup
                        if subg_index != -1:                                            #if a subgroup is indeed present
                            subgroups.append(                                           #extract it and add to subgroups list
                                build_str[subg_index: len(build_str)]
                                )
                        build_str = ''                                                  #reset build string
                    index = index + 1                                                   #and increment index

                if balanced and s.isEmpty():                                            #if the expression is thus far balanced and the stack has been depleted, it is totally balanced
                    return subgroups                                                    #return the subgroups
                else:                                                                   #not a balanced expression, raise ValueError
                    raise ValueError(
                        'all grouping expressions must be balanced'
                        )

            grouping_left = group_string[0]                                             #get left grouping character
            grouping_right = group_string[len(group_string)-1]                          #get right grouping character
            trimmed_group_string = group_string[1:len(group_string)-1]                  #trim the group chars off of the string

            subgroups = extract_subgroup(                                               #extract subgroups from group_string
            grouping_left, 
            grouping_right, 
            trimmed_group_string
            ) 

            for subgroup in subgroups:                                                  #for every subgroup extracted from group_string
                temp_string = trimmed_group_string                                      #store temportary copy of trimmed string
                trimmed_group_string = trimmed_group_string.replace(                    #replace trimmed string with itself minus the subgroup
                    subgroup + ',',
                    ''
                    )
                if temp_string == trimmed_group_string:                                 #subgroup was adjacent to end of trimmed string and thus had no comma
                    trimmed_group_string = trimmed_group_string.replace(                #replace it with itself without subgroup and remove trailing comma for groupings split
                        subgroup,
                        '')[:-1]

            grouping_output = []                                                        #create list to store parsed elements of grouping

            for subgroup in subgroups:
                grouping_output.append(parse_grouping(subgroup))

            grouping = trimmed_group_string.split(',')                                  #split grouping string into constituent elements
            
            if '' in grouping:                                                          #if empty strings have been incurred after trimming (during nested singletons)
                grouping.remove('')                                                     #remove them

            for ge in grouping:                                                     #for each element of the grouping
                parsed_ge = parse_int_float_string(ge)                                  #parse element to int, float, or string
                grouping_output.append(parsed_ge)                                       #append parsed element to grouping output list      

            return grouping_output                                                      #return list containing all parsed elements

        #handles exception case 3
        def can_convert_to_low_high_tuple(s):
            """Return boolean for whether or not s parameter can be converted to low-high tuple"""

            def is_convertable(string):
                """Return boolean for whether or not string parameter contains an ellipsis"""

                def valid_numerics_and_ellipses(vne_string):
                    """Return whether or not vne_string parameter contains only numeric characters, commas, and ellipses in appropriate places"""

                    e_elements = vne_string.split(',')

                    start_ellipses = e_elements[0] == '...'                             #store if ellipses begin potential low-high tuple string
                    end_ellipses = e_elements[len(e_elements) - 1] == '...'             #store if ellipses begin potential low-high tuple string

                    if start_ellipses or end_ellipses:                              #if ellipses begin or end a low-high tuple string
                        raise ValueError(                                               #raise ValueError
                            'infinite sets not supported; ' + 
                            'ellipses cannot begin or end ' +
                            'a low-high tuple string'
                            )
                    for e_element in e_elements :                                       #for each element in e_elements
                        parsed_e_element = parse_int_float_string(e_element)            #parse e_element to int, float, or string
                        
                        is_int = type(parsed_e_element) == int                          #store condition for if parsed_e_element is an int
                        is_float = type(parsed_e_element) == float                      #store condition for if parsed_e_element is an float

                        if not is_int and not is_float:                             #if parsed_e_element is not an int or float
                            if parsed_e_element != '...':                               #parsed_e_element is a string; if it's not an ellipsis
                                return False                                            #return False

                    return True                                                         #elements all check out, return True

                if isinstance(string, str):                                         #if string parameter is a string
                    if '...' in string:                                             #if string contains an ellipsis
                        
                        format_flag = valid_numerics_and_ellipses(string)               #determine if string parameter contains
                        if format_flag:                                             #if string contains only numerics and ellipses all separated by commas
                            return True                                                 #return True
                        else:                                                           #otherwise, return False
                            return False
                    else:                                                               #string does not contain ellipsis
                        return False                                                    #return False

                #Note: returns None here which evaluates to False

            if is_convertable(s):                                                       #if s paramter is convertable to low-high tuple
                return True                                                             #return True
            else:                                                                       #s parameter is not convertable to low-high tuple
                return False                                                            #return False

        def convert_to_low_high_tuple(lh_string):
            """Return a low-high tuple converted from lh_string parameter"""

            lh_elements = lh_string.split(',')                                          #split lh_string into constituent elements
            
            ellipses_indicies = []
            for i in reversed(range(len(lh_elements))):                             #get indicies of ellipses greatest first
                if lh_elements[i] == '...':
                    ellipses_indicies.append(i)                                         #append index if it corresponds to an ellipses

            for i in ellipses_indicies:                                             #for each index corresponding to an ellipses
                del lh_elements[i]                                                      #delete ellipses element
            
            low = min(lh_elements)                                                      #get the smallest element for low-high tuple
            high = max(lh_elements)                                                     #get the highest element for low-high tuple


            float_flag = False
            if '.' in low or '.' in high:                                               #if low or high are a float, set float flag
                float_flag = True


            if float_flag:                                                              #if low or high is a float, cast both to float
                if float(low) == float(high):                                           #if low == high, return single number
                    return float(low)
                else:
                    if float(low) < float(high):                                        #this condition is for when both are negative
                        return (float(low), float(high))                                #return low-high float tuple
                    else:
                        return (float(high), float(low))                                #return low-high float tuple
            else:                                                                       #otherwise, cast both to ints
                if int(low) == int(high):                                               #if low == high, return single number
                    return int(low)
                else:
                    if int(low) < int(high):                                            #this condition is for when both are negative
                        return (int(low), int(high))                                    #return low-high int tuple
                    else:
                        return (int(high), int(low))                                    #return low-high int tuple

        iter_flag = is_iterable(e)                                                      #determine if element is an iterable

        if iter_flag:                                                                   #if element is an iterable
            return iterable_to_grouping(e)                                              #return it as a grouping

        tuple_flag = is_low_high_tuple(e)

        if tuple_flag:                                                                  #if it is potentially a low-high tuple
            return enforce_low_high_tuple(e)                                            #return it with correct formatting

        grouping_flag = is_grouping(e)                                                  #determine if element is a grouping
        
        if grouping_flag:                                                               #if element is a grouping
            return parse_grouping(e)                                                    #get the parsed group
        
        low_high_flag = can_convert_to_low_high_tuple(e)                                #determine if element can be converted to low-high tuple

        if low_high_flag:                                                               #if element is convertable to a low-high tuple 
            return convert_to_low_high_tuple(e)                                         #return low-high tuple conversion

        return e                                                                        #e is a single element, return it simply

    def separate_tuples(elements):
        """Return a list of tuples and a list of non-tuples from elements parameter."""

        tuples = []                                                                     #create a list for tuples
        non_tuples = []                                                                 #create a list for non-tuples

        for element in elements:                                                        #for each element in elements
            if isinstance(element, tuple):                                              #if that element is a tuple
                tuples.append(element)                                                  #append it to tuples list
            else:                                                                       #otherwise, append to non-tuples list
                non_tuples.append(element)

        return tuples, non_tuples                                                       #return the two lists

    def floatify(tuples):
        """Return low-high tuples without mismatched types; modifies tuples parameter in place."""

        for i, tup in enumerate(tuples):                                                #for each low-high tuple
            low_type = type(tup[0])                                                     #get type of low
            high_type = type(tup[1])                                                    #get type of high

            if low_type == float or high_type == float:                                 #if either low or high is a float
                tuples[i] = (float(tup[0]), float(tup[1]))                              #replace tup with copy where both low and high are floats

    def flatten(non_tuples):
        """Return a flattened non_tuples."""

        def flatten_list(lis):
            """Given a list, possibly nested to any level, return it flattened."""
            
            new_lis = []                                                                #create new list
            for item in lis:                                                            #for item in nth list
                if type(item) == type([]):                                              #if type of item is a list therefore possible to recur on
                    new_lis.extend(flatten_list(item))                                  #extend new list with the (n+1)th list
                else:                                                                   #not a list
                    new_lis.append(item)                                                #just add to new list
            return new_lis                                                              #return nth list

        list_non_tuples = []                                                            #creat list of lists, i.e., groupings in non_tuples
        single_non_tuples = []                                                          #create list of singles
        
        for non_tuple in non_tuples:                                                    #for every non-tuple
            if type(non_tuple) == list:                                                 #if its a list, add to list non-tuples
                list_non_tuples.append(non_tuple)
            else:                                                                       #not a list, has to be a single
                single_non_tuples.append(non_tuple)                                     #add to single non-tuples

        flat_non_tuples = list(                                                         #flatten the list non-tuples and remove duplicates
            set(flatten_list(list_non_tuples)))                       

        return flat_non_tuples + single_non_tuples                                      #join the singles with the flattened list elements

    def merge_singles(element):
        """
        function to merge single integers with tuples that either contain it or are 1 off on either the low or high
        e.g. if tuple x = (10, 50), and integer y = 9, 10-50, or 51, it will be merged
        """

        for i, x in enumerate(element):
            for j, y in enumerate(element):
                if isinstance(x, tuple) and isinstance(y, int):                         #dont have to check if i != j, if i == j cant be of differnet types
                    if x[0] <= y <= x[1]:                                               #if a single int is contained in a high-low tuple, remove it
                        del element[j]
                        return True
                    
                    if y == x[0] - 1:                                                   #if a single int equals 1 lower than a tuples low, combine them and delete old tuple and single
                        element.append((y, x[1]))
                        if i < j:
                            del element[j]
                            del element[i]
                        if j < i:
                            del element[i]
                            del element[j]
                        return True
                    
                    if y == x[1] + 1:                                                   #if a single int equals 1 higher than a tuples high, combine them and delete old tuple and single
                        element.append((x[0], y))
                        if i < j:
                            del element[j]
                            del element[i]
                        if j < i:
                            del element[i]
                            del element[j]
                        return True
                elif isinstance(x, tuple) and isinstance(y, float):                     #dont have to check if i != j, if i == j cant be of differnet types
                    
                    global float_df                                                     #bring float differential float_df into local namespace 

                    if x[0] - float_df <= y <= x[1] + float_df:                         #if a single int is contained in a high-low tuple, remove it
                        del element[j]
                        return True
                        
        return False

    def delete_duplicate_subgroups(subgroups):
        """Return boolean for whether or not a duplicate subgroup was successfully deleted from subgroups parameter"""

        for i, nt1 in enumerate(subgroups):
            for j, nt2 in enumerate(subgroups):
                if i != j:                                                              #if indicies aren't the same
                    if type(nt1) == type(nt2) and type(nt1) == list:                    #if both nt1 and nt2 are sublists
                        if nested_equivalence(nt1, nt2):                     #if they are deeply equivalent without shrinking
                            del subgroups[i]
                            return True
        return False

    input_list = copy.copy(set1)                                                        #create copy of input to avoid pass by reference
    output_list = []                                                                    #create empty output list

    for element in set1:                                                                #for each element in input_list
        parsed_element = parse_element(element)                                         #get its parsed equivalent
        output_list.append(parsed_element)                                              #and store it in output list

    tuples, non_tuples = separate_tuples(output_list)                                   #split low-high tuples from not low-high tuples

    while collapse(tuples): pass                                                        #collapse overlapping tuples

    floatify(tuples)                                                                    #take care of mismatched in/float low-high tuples

    global flat_flag                                                                    #bring global flat_flag into local namespace

    if flat_flag:                                                                       #if flat parameter is turned on
        non_tuples = flatten(non_tuples)                                                #flatten non-tuples
    else:                                                                               #flat parameter is off
        while delete_duplicate_subgroups(non_tuples): pass

    output_list = tuples + non_tuples                                                   #combine tuples and non-tuples back together

    while merge_singles(output_list): pass                                          #merge singles into low-high tuples

    return output_list                                                                  #send back parsed list

def is_proper_subset(set1, set2):
    """Return if set1 is a proper subset of set2, i.e., set1 is a subset of set2, but set2 is not a subset of set1."""

    if is_subset(set1, set2) and not is_subset(set2, set1):                         #if set1 subset set2 and set2 not subset set1
        return True
    else:                                                                               #otherwise, not proper subset
        return False

def is_subset(set1, set2):
    """
    Return boolean for whether or not set1 parameter is a subset of set2 parameter

    handles any set made of components handled by parse; i.e., subgroups, singles, and low-high tuples

    set1: the subset, type enforced as either list or dict
    set2: the superset; type enforced as either list or dict
    
    raises TypeError if both set1 and set2 parameters are not a lists or both are not dicts.
    """

    def is_dict_subset(dict1, dict2):
        """Return boolean for whether or not dict1 is a subset of dict2."""

        return all(item in dict2.items() for item in dict1.items())                     #convert key values to tupls and return true if all key value tuples in dict1 are in dict2

    def split_points(lis):
        """Return list of Point objects split off from lis parameter."""
        try:
            return [item for item in lis if isinstance(item, Point)]
        except NameError:
            return []

    def split_subgroups(lis):
        """Return list of subgroups split off from lis parameter."""

        return [item for item in lis if type(item) == list]                             #return list of all list elements

    def split_singles(lis):
        """Return list of singles split off from lis parameter."""

        try:
            #return list of all low-high tuples
            return [item for item in lis if type(item) != tuple and type(item) != list and not isinstance(item, Point)]
        except NameError:
            return [item for item in lis if type(item) != tuple and type(item) != list]

    def split_tuples(lis):
        """Return list of tuples split off from lis parameter."""

        return [item for item in lis if type(item) == tuple]                            #return list of all low-high tuples
    
    def is_points_subset(points1, points2):
        """
        Return boolean for whether or 
        not points1 is a subset of points2.
        """

        if not points1 and not points2:
            return True

        generic_dimensions1 = []
        generic_dimensions2 = []

        for point in points1:
            if point.is_generic():
                generic_dimensions1.append(point.get_dimension())

        for point in points2:
            if point.is_generic():
                generic_dimensions2.append(point.get_dimension())
            
        if [dim for dim in generic_dimensions1 if dim not in generic_dimensions2]:
            return False            

        unmatched_points = []

        for point in points1:
            if point.get_dimension() not in generic_dimensions2:
                unmatched_points.append(point)

        if not [point for point in unmatched_points if point not in points2]:                    #if there are no points in points1 not in points2, return True
            return True
        else:                                                                           #otherwise, return False
            return False

    def is_subgroup_subset(subgroup1, subgroup2):
        """Return boolean for whether or not subgroup1 is a subset of subgroup2."""

        for i in subgroup1:                                                         #for each subgroup i in subgroup1
            for j in subgroup2:                                                     #for each subgroup j in subgroup1
                if nested_equivalence(i, j):                                     #if i has a deep match in j without shrinking, terminate for else through break
                    break
            else:                                                                       #we are only here if a j was not found matching i, which means not a subset
                return False
        return True                                                                     #every i has a match, it is a subset

    def is_singles_subset(singles1, singles2, tuples2):
        """Return boolean for whether or not singles1 is a subset of a combination of singles2 and tuples2."""

        unmatched_singles = [                                                           #get the singles in singles1 not in singles2
        item for item in singles1 if item not in singles2
        ]

        for s in unmatched_singles:                                                 #for each unmatched single
            if not isinstance(s, int) and not isinstance(s, float):                     #if its not an int or float
                return False                                                            #it can't be below a low-high tuple, not a subset so return False
            else:
                for t in tuples2:                                                       #for every low-high tuple
                    if t[0] <= s <= t[1]:                                               #if s is contained between low-high tuple
                        break                                                           #break for else 
                else:                                                                   #s is not contained by any low-high tuple
                    return False                                                        #not a subset
        return True                                                                     #there's a match for every single

    def is_tuples_subset(tuples1, tuples2):
        """
        Return boolean for whether or not 
        tuples1 is a subset of tuples2.
        """

        for i in tuples1:                                                               #for each low-high tuple in tuples1
            for j in tuples2:                                                           #for each low-high tuple in tuples2
                if j[0] <= i[0] and i[1] <= j[1]:                                       #if i is contained within j (note: guarenteed for both tuples to be low-high tuples)
                    break                                                               #break for else as we found a match
            else:                                                                       #otherwise, no match for some low-high tuple
                return False                                                            #return False
        return True                                                                     #found a match for every low-high tuple, return True

        
    type1 = type(set1)                                                                  #get type of set1
    type2 = type(set2)                                                                  #get type of set2

    if type1 != list or type2 != list:                                                  #if both parameters aren't of type list
        if type1 != dict or type2 != dict:                                              #if they're both not of type dict
            raise TypeError(                                                            #raise TypeError
                'set1 and set 2 must both be either ' +
                'of type list or of type dict'
                )
    
    both_types = type1                                                                  #store shared type in a more intuitive name                                         

    if both_types == dict:                                                              #if we're processing dicts
        return is_dict_subset(set1, set2)                                               #prosses and return the boolean


    parsed_set1 = copy.copy(parse(set1))                                                #create a copy of a parsed set1    
    parsed_set2 = copy.copy(parse(set2))                                                #create a copy of a parsed set2 

    #handle trival cases 

    if not parsed_set1:                                                           #if set 1 is empty list, it is a subset
        return True
    if not set1 and not set2:                                               #if both sets are empty, it is a subset
        return True                                     
    if len(set1) > 0 and not set2:                                                #if set 2 is empty but set 1 is not, it is not a subset
        return False

    #split lists into their components

    points1 = split_points(parsed_set1)
    points2 = split_points(parsed_set2)
    subgroup1 = split_subgroups(parsed_set1)                                            #split subgroups off of first list
    subgroup2 = split_subgroups(parsed_set2)                                            #split subgroups off of second list
    singles1 = split_singles(parsed_set1)                                               #split singles off of first list
    singles2 = split_singles(parsed_set2)                                               #split singles off of second list
    tuples1 = split_tuples(parsed_set1)                                                 #split tuples off of first list
    tuples2 = split_tuples(parsed_set2)                                                 #split tuples off of second list

    #determine is_subset for respective components

    points_condition = is_points_subset(points1, points2)                               #determine if subgroup1 is a subset of subgroup2
    subgroup_condition = is_subgroup_subset(subgroup1, subgroup2)                       #determine if subgroup1 is a subset of subgroup2
    singles_condition = is_singles_subset(singles1, singles2, tuples2)                  #determine if singles1 is a subset of singles2
    tuples_condition = is_tuples_subset(tuples1, tuples2)                               #determine if tuples1 is a subset of tuples2

    if subgroup_condition and singles_condition and \
        tuples_condition and points_condition:                                          #if all components of set1 are subsets of their respective components in set2
        return True                                                                     #return True
    else:                                                                               #otherwise 
        return False                                                                    #return False   

def get_set_theoretic_difference(set1, set2):
    """get set1\set2, i.e. the elements in set1 not in set2, raise TypeError if not both lists."""
    
    if not isinstance(set1, list):                                                      #if set1 parameter is not a list
        raise TypeError(                                                                #raise TypeError
            'set1 parameter must be of type list'
            )
    if not isinstance(set2, list):                                                      #if set2 parameter is not a list
        raise TypeError(                                                                #raise TypeError
            'set2 parameter must be of type list'
            )

    def split_points(lis):
        """Return list of Point objects split off from lis parameter."""

        return [item for item in lis if isinstance(item, Point)]                        #return list of all list elements

    def split_subgroups(lis):
        """Return list of subgroups split off from lis parameter."""

        return [item for item in lis if type(item) == list]                             #return list of all list elements

    def split_singles(lis):
        """Return list of singles split off from lis parameter."""

        return [
        item for item in lis if type(item) != tuple and type(item) != list and not isinstance(item, Point)              #return list of all low-high tuples
        ]

    def split_tuples(lis):
        """Return list of tuples split off from lis parameter."""

        return [item for item in lis if type(item) == tuple]                            #return list of all low-high tuples
    
    def is_points_subset(points1, points2):
        """
        Return boolean for whether or 
        not points1 is a subset of points2.
        """

        generic_dimensions1 = []
        generic_dimensions2 = []

        for point in points1:
            if point.is_generic():
                generic_dimensions1.append(point.get_dimension())

        for point in points2:
            if point.is_generic():
                generic_dimensions2.append(point.get_dimension())
            
        if [dim for dim in generic_dimensions1 if dim not in generic_dimensions2]:
            return False            

        unmatched_points = []

        for point in points1:
            if point.get_dimension() not in generic_dimensions2:
                unmatched_points.append(point)

        if not [point for point in unmatched_points if point not in points2]:                    #if there are no points in points1 not in points2, return True
            return True
        else:                                                                           #otherwise, return False
            return False

    def is_subgroup_subset(subgroup1, subgroup2):
        """Return boolean for whether or not subgroup1 is a subset of subgroup2."""

        for i in subgroup1:                                                         #for each subgroup i in subgroup1
            for j in subgroup2:                                                     #for each subgroup j in subgroup1
                if nested_equivalence(i, j):                                     #if i has a deep match in j without shrinking, terminate for else through break
                    break
            else:                                                                       #we are only here if a j was not found matching i, which means not a subset
                return False
        return True                                                                     #every i has a match, it is a subset

    def is_singles_subset(singles1, singles2, tuples2):
        """Return boolean for whether or not singles1 is a subset of a combination of singles2 and tuples2."""

        unmatched_singles = [                                                           #get the singles in singles1 not in singles2
        item for item in singles1 if item not in singles2
        ]

        for s in unmatched_singles:                                                 #for each unmatched single
            if not isinstance(s, int) and not isinstance(s, float):                     #if its not an int or float
                return False                                                            #it can't be below a low-high tuple, not a subset so return False
            else:
                for t in tuples2:                                                       #for every low-high tuple
                    if t[0] <= s <= t[1]:                                               #if s is contained between low-high tuple
                        break                                                           #break for else 
                else:                                                                   #s is not contained by any low-high tuple
                    return False                                                        #not a subset
        return True                                                                     #there's a match for every single

    def is_tuples_subset(tuples1, tuples2, singles2):
        """Return boolean for whether or not tuples1 is a subset of tuples2 or singles2."""

        def check_length_optimizer(u_tuples, singles):
            """Return boolean for whether or not any unmatched tuple's range is greater than length of singles2"""

            for t in u_tuples:                                                          #for every unmatched tuple t
                float_flag = type(t[0]) == float or type(t[1]) == float                 #determine whether we're using floats
                if float_flag:                                                          #if t uses floats
                    global float_df                                                     #bring global float differential into local namespace
                    df = float_df                                                       #create a copy of it to save some line space

                    value_count = abs(t[1] - t[0]) / df                                 #get amount of elements in low-high tuple range
                    if value_count > len(singles):                                      #if there are more values in the low-high tuple's range than there are singles
                        return True                                                     #singles can't contain all values of low-high tuple, return True
                else:                                                                   #t uses ints
                    value_count = abs(t[1] - t[0])                                      #get amount of elements in low-high range
                    if value_count > len(singles):                                      #if there are more values in the low-high tuple's range than there are singles
                        return True                                                     #singles can't contain all values of low-high tuple, return True
            
            return False

        def generate_tuple_values(tup):
            """Return a list of all int or float values between low-high tuple inclusively."""

            def frange(x, y, jump):
                """Declare a generator that generates values in an inclusive range with a float step size."""

                while x <= y:                                                           #while low is less than high
                    yield x                                                             #yield x at current step
                    x += jump                                                           #increment x by step size

            float_flag = type(tup[0]) == float or type(tup[1]) == float                 #determine if we're generating float or int values

            gen_values = []                                                             #create an empty list to hold the values between low-high tuple

            if float_flag:                                                              #if we're doing floats
                global float_df                                                         #bring global float differential into local namespace
                df = float_df                                                           #create a copy of it to save some line space

                r = frange(tup[0], tup[1], df)                                          #create generator object to generate values within low-high tuple range with df step size 
                while True:                                                         #loop until we don't need to anymore
                    try:                                                                #try to generate the next value within low-high range
                        gen_values.append(r.next())                                     #and append it to gen_values list
                    except StopIteration:                                               #no more values within range
                        return gen_values                                               #return the generated values
            else:                                                                       #if we're using ints
                return [i for i in range(tup[0], tup[1] + 1)]                           #just return a list of the range built on the fly 

        unmatched_tuples = []                                                           #create empty list to store tuples in tuples1 not contained by tuples in tuples2

        for i in tuples1:                                                               #for each low-high tuple in tuples1
            for j in tuples2:                                                           #for each low-high tuple in tuples2
                if j[0] <= i[0] and i[1] <= j[1]:                                       #if i is contained within j (note: guarenteed for both tuples to be low-high tuples)
                    break                                                               #break for-else as we found a match
            else:                                                                       #otherwise, no match for some low-high tuple
                unmatched_tuples.append(i)
        
        ##############################################################################################################
        # NOTE: POSSIBLE BOTTLENECK BY generate_tuple_values(), UNCOMMENT FOLLOWING TWO LINES TO FOREGO              #
        #CHECKING EVERY VALUE IN LOW-HIGH TUPLE RANGE AGAINST SINGLES. IN THE UNCOMMENTED CASE, tuples1 IS A         #
        #SUBSET OF tuples2 ONLY IF EVERY TUPLE IN tuples1 IS CONTAINED BY A TUPLE IN tuples2 AND singles2 IS IGNORED #
        ##############################################################################################################
        #       return False                                                            #return False
        #return True                                                                    #found a match for every low-high tuple, return True

        if not unmatched_tuples:                                                  #if a match was found for every low-high tuple
            return True                                                                 #return True

        if check_length_optimizer(unmatched_tuples, singles2):                          #if some tuple's range has more values than singles2 has elements
            return False                                                                #singles does not contain the tuple, return False

        for t in unmatched_tuples:                                                      #for every unmatched tuple
            t_vals = generate_tuple_values(t)                                           #generate values between low and high inclusively
            
            unmatched_singles = [                                                       #get the singles in t_vals not in singles2
                item for item in t_vals if item not in singles2
            ]

            if len(unmatched_singles) > 0:                                              #if the tuple isn't contained in tuples2 and every value of the tuple isn't matched by a single
                return False                                                            #not a subset, return False

        return True                                                                     #every tuple is either contained by a tuple in tuples2 or
                                                                                        #every value the tuple takes on has a match in singles2, it is a subset
       
    def get_points_difference(points1, points2):
        """Return Point objects in points1 not in points2."""

        return [point for point in points1 if point not in points2]

    def get_subgroup_difference(subgroup1, subgroup2):
        """Return a list containing the subgroups in subgroup1 not in subgroup2"""
        
        subg_difference = []                                                            #create an empty list to hold subgroups in set1 not in set2

        for i in subgroup1:                                                         #for each subgroup i in set1
            for j in subgroup2:                                                     #for each subgroup j in set2
                if nested_equivalence(i, j):                                 #if i is deeply equivalent to j without shrinking, break from for-else loop
                    break
            else:                                                                       #i not equal to any subgroup j
                subg_difference.append(i)                                               #append it to difference

        return subg_difference                                                          #return subgroups in set1 not in set2

    def get_singles_difference(singles1, singles2, tuples2):
        """Return a list containing the singles in singles1 not in singles2 or encapsulated by low-high tuples in tuples2"""

        sing_difference = []                                                            #create an empty list to hold sinlges in set1 not in set2

        for i in singles1:                                                              #for each single i in set1
            for j in singles2:                                                          #for each single j in set2
                if i == j:                                                              #if i == j, break for-else
                    break
            else:                                                                       #i not equal to any single j in set2
                sing_difference.append(i)                                               #append it to difference

        final_difference = []                                                           #create an empty list to hold singles in set1 not in singles or between any low-high tuple in set2

        for i, single in reversed(list(enumerate(sing_difference))):                    #for every single i in set1 not found in singles in set2 in reversed order
            if type(single) != int and type(single) != float:                           #if that single is not a number
                final_difference.append(single)                                         #it can't be between a low-high tuple, append to final difference
                del sing_difference[i]                                                  #done processing it, remove from sing_difference

        for i in sing_difference:                                                       #for every single i in set1 without a match in the singles of set2
            for tup in tuples2:                                                     #for every low-high tuple tup in set2
                if tup[0] <= i <= tup[1]:                                               #if i is contained by a low-high tuple (also i is guarenteed to be a number from block above)
                    break                                                               #terminate for-else loop
            else:                                                                       #i not contained by any number, add to final difference
                final_difference.append(i)

        return final_difference                                                         #return subgroups in set1 not in set2       

    def get_tuples_difference(tuples1, tuples2, singles2):
        """
        Return a list containing the tuples in tuples1 not in tuples2

        There are 7 cases to consider before prettying up anything, using ( ) for t1 and [  ] for t2:

        case 1:     (   )   [   ]       t1 is entirely less than t2
        case 2: (   [   )   ]       t1 is paritally less than t2 
        case 3:     [   (   )   ]       t1 is contained by t2
        case 4: [   (   ]   )       t1 is partially greater than t2
        case 5: [   ]   (   )       t1 is entirely greater than t2
        case 6: (   [   ]   )       t1 contains t2
        case 7: (   ) = [   ]       t1 is the same tuple as t2

        """

        def split_tuples_by_singles(tup1, sing2):
            """
            Return a boolean for whether or not some tuple in tup1 can be split by some single in sing2.

            The idea is for each tuple, split if possible with a member of sing2 and return True. Do this until no more splits can be done and return False.
            """

            def use_floats(tup):
                """Return a boolean for whether or not tup pramaeter contains a float."""

                if type(tup[0]) == float or type(tup[1]) == float:                      #if either endpoint is a float
                    return True                                                         #return True
                else:                                                                   #otherwise, return False
                    return False

            global float_df                                                             #bring float differential float_df into local namespace
            df = float_df                                                               #set local copy to it to user float differential; defaults to .001

            for i, t in enumerate(tup1):                                                #for every tuple in tuple list
                for s in sing2:                                                     #for every single in sing2
                    if type(s) == int or type(s) == float:                              #if float is a number and therefore can possibly split a tuple
                        
                        float_flag = use_floats(t)                                      #determine whether to split by float or int
                        
                        if t[0] < s < t[1]:                                         #if the tuple contains the single exclusively
                            if float_flag:                                              #if we're using floats
                                tup1.append((t[0], s - df))                             #append new tuple from low to s - float_df 
                                tup1.append((s + df, t[1]))                             #append new tuple from s + float_df to high
                                del tup1[i]                                             #delete old tuple so we don't loop ad infinitum
                                return True                                             #return True
                            else:                                                       #if we're using ints
                                tup1.append((t[0], s - 1))                              #append new tuple from low to s - 1 
                                tup1.append((s + 1, t[1]))                              #append new tuple from s + 1 to high
                                del tup1[i]                                             #delete old tuple so we don't loop ad infinitum
                                return True                                             #return True
                        
                        if t[0] == s:                                                   #if the single is equal to the low
                            if float_flag:                                              #if we're using floats
                                tup1.append((s + df, t[1]))                             #append new tuple from s+ float_df to high
                                del tup1[i]                                             #delete old tuple so we don't loop ad infinitum
                                return True                                             #return True
                            else:                                                       #if we're using ints
                                tup1.append((s + 1, t[1]))                              #append new tuple from s + 1 to high
                                del tup1[i]                                             #delete old tuple s we don't loop ad infinitum
                                return True                                             #return True

                        if s == t[1]:                                                   #if the single is equal to the high
                            if float_flag:                                              #if we're using floats
                                tup1.append((t[0], s - df))                             #append new tuple from low to s - float_df
                                del tup1[i]                                             #delete old tuple so we don't loop ad infinitum
                                return True                                             #return True
                            else:                                                       #if we're using ints
                                tup1.append((t[0], s - 1))                              #append new tuple from low to s - 1
                                del tup1[i]                                             #delete old tuple s we don't loop ad infinitum
                                return True                                             #return True

            return False                                                                #no more tuples can be split, return False

        def forge(tup1, tup2):
            """
            Return a modified tup1 with a tuple split according to cases 2, 4, or 6

            the idea is to continually remove any overlapping elements of tuples in tup1 and tup2 until no more overlap.
            This is done through a line like:
            while forge(tup1, tup2): pass
            then extracting the final set theoretic difference tuples through a line like:
            for i in tup1: tuples_difference.append(i)

            df parameter is for differential to split float tuples according to e.g. given tuple (5, 10) and (6.0, 12); the split becomes (5.0, 5.999) with df = .001
            note: if a float is present in either tuple, any split tuples will be entirely float 
            """
            
            def is_float_tuple(t_f, t_s):
                """Return boolean for whether or not either tuple t_f or t_l contain a float"""

                if type(t_f[0]) == float or type(t_f) == float:                         #if either low or high is a float in first tuple
                    return True                                                             #return True
                if type(t_s[0]) == float or type(t_s) == float:                         #if either low or high is a float in second tuple
                    return True                                                             #return True

                return False                                                                #neither contain a tuple, return False

            global float_df                                                             #bring float differential float_df into local namespace
            df = float_df                                                               #set local copy to it to user float differential; defaults to .001

            for i, t in enumerate(tup1):
                for j, t2 in enumerate(tup2):
                    
                    float_flag = is_float_tuple(t, t2)

                    if t[0]  <  t2[0] and t[1]  <= t2[1] and t[1] >= t2[0]:             #if (t[)t2]
                        if float_flag:                                                  #if either t or t2 contain a float, use entirely floats
                            tup1.append((float(t[0]), float(t2[0]) - df))               #append the lower difference between t and t2 - 1 to tup1
                        else:                                                           #otherwise, they're guarenteed to use ints, don't need to explicitly cast
                            tup1.append((t[0], t2[0]-1))                                #append the lower difference between t and t2 - 1 to tup1
                        
                        del tup1[i]                                                     #delete original t from tup1, i.e. delete overlapping elements in lieu of append above
                        return True

                    if t2[0] <= t[0]  and t2[1] <  t[1]  and t2[1] >= t[0]:             #if [t2(]t)
                        if float_flag:                                                  #if either t or t2 contain a float, use entirely floats
                            tup1.append((float(t2[1]) + df, float(t[1])))               #append the higher difference between t2 + 1 and t to tup1
                        else:                                                           #otherwise, they're guarenteed to use ints, don't need to explicitly cast
                            tup1.append((t2[1] + 1, t[1]))                              #append the higher difference between t2 + 1 and t to tup1
                        del tup1[i]                                                     #delete original t from tup1, i.e. delete overlapping elements in lieu of append above
                        return True

                    else:
                        if t[0]  <  t2[0] and t2[1] <  t[1]:                            #if (t(t2)t)
                            if float_flag:                                              #if either t or t2 contain a float, use entirely floats
                                tup1.append((float(t[0]), float(t2[0]) - df))           #append the lower difference between t and t2 - 1 to tup1
                                tup1.append((float(t2[1]) + df, float(t[1])))           #append the higher difference between t2 + 1 and t to tup1  
                            else:                                                       #otherwise, they're guarenteed to use ints, don't need to explicitly cast
                                tup1.append((t[0], t2[0]-1))                            #append the lower difference between t and t2 - 1 to tup1
                                tup1.append((t2[1] + 1, t[1]))                          #append the higher difference between t2 + 1 and t to tup1
                            del tup1[i]
                            return True
            return False

        def remove_outliers(tup1, tup2, diff_list):
            """stub function to remove any extreme differences, i.e. any values below or above anything in tup2 after sorting."""

            def remove_front_outliers(tup1, tup2, diff_list):
                """remove those outliers in the front and append to differences."""

                for i, t in enumerate(tup1):
                    for j, t2 in enumerate(tup2):
                        if t[1]  <  t2[0]:                                                  #if (t)(t2)
                            diff_list.append(t)                                             #add t to difference list
                            del tup1[i]                                                     #delete t from tup1 as its done
                            return True                                                     #try again in case next tuple in tuple2 is also totally greater than t
                        else: 
                            return False                                                    #we are done

            def remove_back_outliers(tup1, tup2, diff_list):
                """remove those outliers in the back and append to differences."""

                for i, t in enumerate(reversed(tup1)):
                    for j, t2 in enumerate(reversed(tup2)):
                        if t2[1]  <  t[0]:                                                  #if (t2)(t)
                            diff_list.append(t)                                             #add t to difference list
                            del tup1[len(tup1) - i - 1]                                     #delete t from tup1 as its done
                            return True                                                     #try again in case next tuple in tuple2 is also totally greater than t
                        else: 
                            return False                                                    #we are done

            while remove_front_outliers(tup1, tup2, diff_list): pass                        #call as many times as needed
            while remove_back_outliers(tup1, tup2, diff_list): pass                         #call as many times as needed


        tup_list1 = copy.copy(tuples1)                                                  #create a copy of tuples1 to avoid pass by reference
        tup_list2 = copy.copy(tuples2)                                                  #create a copy of tuples2 to avoid pass by reference
        sing_list2 = copy.copy(singles2)                                                #create a copy of singles2 to avoid pass by reference

        tuples_difference = []                                                          #create a list to hold difference of tuples

        for i, t1 in reversed(list(enumerate(tup_list1))):                              #for each tuple t1 in tuples1, going backwards to remove in place
            for t2 in tup_list2:                                                        #for each tuple t2 in tuples2
                if t2[0] <= t1[0] and t1[1] <= t2[1]:                                   #if t1 is contained by t2; case 3
                    del tup_list1[i]
                    break                                                               #break from for-else
                elif t1 == t2:                                                          #if t1 is equal to some t2; case 7
                    del tup_list1[i]
                    break                                                               #break from for-else
            else:                                                                       #if t1 is not equal to any t2,
                pass


        while split_tuples_by_singles(tup_list1, sing_list2): pass                  #split any tuples in tup1 by any single between that tuples's low and high

        while collapse(tup_list1): pass
        while collapse(tup_list2): pass


        tup_list1.sort(key=lambda tup: tup[0])                                          # sorts tup_list1 in place
        tup_list2.sort(key=lambda tup: tup[0])                                          # sorts tup_list2 in place

        #handle cases 1 and 5

        remove_outliers(tup_list1, tup_list2, tuples_difference)                        #remove the outliers in tup_list1 and add to differences

        #handles cases 2, 4, and 6

        while forge(tup_list1, tup_list2): pass                                         #while we can forge new tuples from overlaps, keep updating tup_list1

        for i in tup_list1: tuples_difference.append(i)                             #append any leftover unique tuples to diff_list

        tuples_difference.sort(key=lambda tup: tup[0])                                  #sorts tupleS_difference in place
        while collapse(tuples_difference): pass                                         #collapse any overlapping tuples

        return tuples_difference                                                        #return set theoretic difference of tuples1 w.r.t. tuples2


    output = []                                                                         #create an empty list to store output in

    parsed_set1 = copy.copy(parse(set1))                                                #create a copy of a parsed set1
    parsed_set2 = copy.copy(parse(set2))                                                #create a copy of a parsed set2 

    #handle trival case 

    if is_subset(parsed_set1, parsed_set2):                                         #if set1 is a subset of set2, there's nothing in the difference
        return output

    #split lists into their components

    points1 = split_points(parsed_set1)
    points2 = split_points(parsed_set2)
    subgroup1 = split_subgroups(parsed_set1)                                            #split subgroups off of first list
    subgroup2 = split_subgroups(parsed_set2)                                            #split subgroups off of second list
    singles1 = split_singles(parsed_set1)                                               #split singles off of first list
    singles2 = split_singles(parsed_set2)                                               #split singles off of second list
    tuples1 = split_tuples(parsed_set1)                                                 #split tuples off of first list
    tuples2 = split_tuples(parsed_set2)                                                 #split tuples off of second list

    #determine is_subset for respective components

    points_condition = is_points_subset(points1, points2)
    subgroup_condition = is_subgroup_subset(subgroup1, subgroup2)                       #determine if subgroup1 is a subset of subgroup2
    singles_condition = is_singles_subset(singles1, singles2, tuples2)                  #determine if singles1 is a subset of singles2
    tuples_condition = is_tuples_subset(tuples1, tuples2, singles2)                     #determine if tuples1 is a subset of tuples2

    points_difference = []
    subgroup_difference = []                                                            #declare an empty list for the set theoretic difference of the subgroup components
    singles_difference = []                                                             #declare an empty list for the set theoretic difference of the singles components
    tuples_difference = []                                                              #declare an empty list for the set theoretic difference of the tuples components

    #get members of respective components not present in their counterparts

    if not points_condition:
        points_difference = get_points_difference(points1, points2)
    if not subgroup_condition:                                                          #if subgroups of set1 are not a subset of subgroups of set2
        subgroup_difference = get_subgroup_difference(subgroup1, subgroup2)             #there are subgroups in set1 not in set2, get them
    if not singles_condition:                                                           #if singles of set1 are not a subset of singless of set2
        singles_difference = get_singles_difference(singles1, singles2, tuples2)        #there are singles in set1 not in set2, get them
    if not tuples_condition:                                                            #if tuples of set1 are not a subset of tupless of set2
        tuples_difference = get_tuples_difference(tuples1, tuples2, singles2)           #there are tuples in set1 not in set2, get them

    output = points_difference + subgroup_difference + singles_difference + tuples_difference               #combine differences in respective components
    
    return parse(output)                                                                #return total set theoretic difference, parsed to merge singles

def encode_points(ascriptions):
    "Encode points into single float value."

    new_ascrs = []

    for ascription in ascriptions:
            
        new_ascr = []

        for point in ascription:
            if isinstance(point, Point):
                new_ascr.append(hash(point.get_coordinate()))
            else :
                raise TypeError(
                    'must all be points if point in ascription')

        new_ascrs.append(new_ascr)

    return new_ascrs

def get_attribute_interpretation(astr, vocab):
    """
    Form an attribute interpretation of Vocabulary vocab into an 
    AttributeStructure astr.
    
    To do this, we need to make a formal mapping that assigns, to each
    R within vocab._R of arity n, a relation R' in astr._relations()
    of arity m (called the realization of R) and a list of m pairs
    (where each pair is composed of a label and an integer between 1 
    and n w/ repeats possible) called the profile.

    input:
    astr: The AttributeStructure object containing the Relations R'
    vocab: Vocabulary from which the Relation Symbols R come from 

    output:
    table in form of 2D list. Each entry is composed of 4 columns;
    the name of R, n, the identifier of R' in astr, and the profile
    e.g. 
    [RelationSymbol('Ahead', 4), 4, 'R1', [('hour', 1), ('minute', 1), ('hour', 2), ('minute', 2)]]
    [RelationSymbol('Behind', 4), 4, 'R2', [('hour', 1), ('minute', 1), ('hour', 2), ('minute', 2)]]
    [RelationSymbol('PM', 1), 1, 'R3', [('hour', 1)]]
    corresponds to a vocab with 3 Relation symbols R, Ahead, Behind,
    and PM and a table which assigns to each of them a relation R' in
    astr (R1, R2, and R3 respectively) whose definitions are stored in
    astr and a profile for each of them.

    This output is used in assign_truth_value which takes a valid
    interpretation_table as part of its input. The interpretation_table
    will be used to determine truth value of formulae; as such each
    formula whose truth value is to be determined must have an entry in
    the table. Optionally, an explicitly created table by the user can
    be used to bypass this function and speed things up.
    
    """
    from vivid import AttributeStructure, Vocabulary

    if not isinstance(astr, AttributeStructure): 
        raise TypeError(
        'astr parameter must be of type AttributeStructure'
        )
    if not isinstance(vocab, Vocabulary): 
        raise TypeError(
        'vocab parameter must be of type Vocabulary'
        )

    def get_profile(R, R_prime):
        """
        Function to return profile of relation for interpretation

        input:
        R: Some RelationSymbol object
        R_prime: Some Relation object

        output: compiled profile of R.
        """

        from vivid import Relation, RelationSymbol

        if not isinstance(R, RelationSymbol):                                      #if R is not a RelationSymbol
            raise TypeError(                                                            #raise TypeError explicitly
                "name parameter must be of type RelationSymbol")
        if not isinstance(R_prime, Relation):                                           #if R' is not a Relation
            raise TypeError(                                                            #raise TypeError explicitly
                "R parameter must be of type Relation")

        profile=[]
            
        n = R.get_arity()                                                               #get arity of Relation Symbol R

        print ("Creating profile for relation " + R.get_name())
        for Ai in R_prime._DR:                                                      #for each attribute of the cartesian product the relation pertains to 
            while True:                                                             #while a valid index hasn't been selected
                try:                                                                    #try to get an index
                    
                    j_x = int(
                        raw_input("Enter positive j_x for " + Ai + ": "))               #try to get a j_x for profile pair

                    if not (1 <= j_x <= n):                                         #if 1 <= j_x <= n is not true; j_x shifted up 1 as indexing starts at 0 and not 1
                        warning =  "profile indicies j_x must be between 1 " +\
                                    "and arity of Relation Symbol " +\
                                    "n({arity}); try again".format(arity=n)             #print warning message and let user try again
                        print (warning)
                    else:                                                               #valid j_x input by user, proceed to j_(x+1)
                        break

                except ValueError:
                    print ("j_x must be an int; try again.")

            profile.append((Ai, j_x))
        return profile

    def relation_transformer(string_map):
        """
        Provide a transformer for pygame mapping output; always has
        access to vocab_rs and astr_rs even without parameter because
        of closure.
        """

        mapping = []

        for source, target in string_map.iteritems():                                   #for each source target pair

            for i, vocab_r in enumerate(vocab_rs):                                      #for each R in vocab
                if source == vocab_r.get_name():                                        #if we found R in vocab matching source
                    source_string = vocab_r                                             #store source index and break
                    break

            for subscript, relation in astr_rs.iteritems():                             #for every subscript:Relation pair in astr_rs dict
                if int(target[1:]) == subscript:                                        #if we found R in astr matching target
                    target_key = relation
                    break

            mapping.append((source_string, target_key))

        return mapping

    transformer = relation_transformer                                                  #create function object for relation transformer

    I_table = []
    vocab_rs = vocab.get_R()
    astr_rs = astr.get_relations()
    
    vocab_r_strings = [rs.get_name() for rs in vocab_rs]                                #build list of relations symbols in vocab as strings
    astr_r_strings = ['R' + str(subscript) for subscript in astr_rs]                    #build list of relations in astr as strings

    if len(vocab_rs) > len(astr_rs):                                                    #must ensure than there's at least one R' for every R for intepreting to work;
        raise ValueError(                                                               #don't let errors propogate
            'cardinality of relations in vocabulary must ' +
            'be smaller than or equal to cardinality of ' + 
            'relations in attribute structure'
            )


    m = pygame_mapping(vocab_r_strings, astr_r_strings, transformer)                #otherwise, use pygame mapping, transforming output with relation_transformer

    for (R, R_prime) in m:                                                              #for each source target match
        I_table.append(
            [R, R_prime.get_arity(), 'R'+str(R_prime.subscript),
            get_profile(R, R_prime)])                                                   #get profile(R', name of R, wether or not to make profile manually)
    
    return I_table

def assign_truth_value(f, named_state, X, vocab, interpretation_table=None):
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

######################################################################################################################
#                                             Non-Essential functions                                                #
######################################################################################################################

def Larger_than(A, B):
    if A > B: return True
    else: return False

def get_bounds(i_avg,j_avg):
    if 0 <= i_avg <= 0.025: bounds = [0,1]#[0,15] #0 <= i <= 15

    if 0.025 <= i_avg < 0.0333333333333: bounds = [0,1]#[15,30] #15 <= i < 30
    if 0.0333333333333 == i_avg: bounds = [1] #i == 30
    if 0.0333333333333 < i_avg <= 0.0681818181818: bounds = [1,2]#[30,45] #30 < i <= 45

    if 0.0681818181818 <= i_avg < 0.146666666667: bounds = [1,2]#[45,60] #45 <= i < 60
    if 0.146666666667 == i_avg: bounds = [2] #i == 60
    if 0.146666666667 < i_avg <= 0.263333333333: bounds = [2,3]#[60,75] #60 < i <= 75

    if 0.263333333333 <= i_avg < .375: bounds = [2,3]#[75,90] #75 <= i < 90
    if .375 == i_avg: bounds = [3] #i == 90
    if .375 < i_avg <= 0.53: bounds = [3,4]#[90,105] #90 < i <= 105

    if 0.53 <= i_avg < 0.643333333333: bounds = [3,4]#[105,120] #105 <= i < 120
    if 0.643333333333 == i_avg: bounds = [4] #i == 120
    if 0.643333333333 < i_avg <= .75: bounds = [4,5]#[120,135] #120 < i <= 135

    if 0.75 <= i_avg < 0.833333333333: bounds = [4,5]#[135,150] #135 <= i <= 150
    if 0.833333333333 == i_avg: bounds = [5] #i == 150
    if 0.833333333333 < i_avg <= 0.84: bounds = [5,6]#[150,160] #150 <= i <= 160

    if 0.84 <= i_avg < .85: bounds = [5,6]#[160,180] #160 <= i < 180
    if .85 == i_avg: bounds = [6] #i == 180

    if j_avg < 15.5 and len(bounds) == 1: bounds = [12-bounds[0]]
    if j_avg < 15.5 and len(bounds) > 1: bounds = [12-bounds[0], 12-bounds[1]]#[360-bounds[0],360-bounds[1]]
    return bounds

def check_ahead(h1,m1,h2,m2):
    if h1 > h2: return True
    if h1 == h2:
        if m1 > m2: return True
    return False
