import vivid


def main():
    """Simple toy proof."""
    hours = vivid.Attribute("hours", [vivid.Interval(0, 23)])
    minutes = vivid.Attribute("minutes", [vivid.Interval(0, 59)])
    R3 = vivid.Relation('R3(h1,m1,h2,m2) <=> h1 > h2 or (h1 = h2 and m1 > m2)',
                        ['hours', 'minutes', 'hours', 'minutes'], 3)

    attribute_structure = vivid.AttributeStructure(
        hours, minutes, R3)

    print "Creating Attribute Structure:"
    print attribute_structure
    print

    Ahead = vivid.RelationSymbol("Ahead", 2)

    vocabulary = vivid.Vocabulary(['c1', 'c2'], [Ahead], [])

    print "Creating Vocabulary:"
    print vocabulary
    print

    profiles = [
        [Ahead, ('hours', 1), ('minutes', 1), ('hours', 2), ('minutes', 2)]]

    attribute_interpretation = vivid.AttributeInterpretation(
        vocabulary, attribute_structure, {Ahead: 3}, profiles)

    print "Creating Attribute Interpretation:"
    print attribute_interpretation
    print

    attribute_system = vivid.AttributeSystem(attribute_structure, ['s1', 's2'])

    print "Creating Attribute System:"
    print attribute_system
    print

    p = vivid.ConstantAssignment(vocabulary, attribute_system,
                                 {'c1': 's1', 'c2': 's2'})

    ascriptions = {("hours", "s1"): [4, 5, 6], ("minutes", "s1"): [28],
                   ("hours", "s2"): [5], ("minutes", "s2"): [45]}
    named_state = vivid.NamedState(attribute_system, p, ascriptions)

    print "Creating Named State:"
    print named_state
    print

    refined_ascriptions = {("hours", "s1"): [6], ("minutes", "s1"): [28],
                           ("hours", "s2"): [5], ("minutes", "s2"): [45]}
    refined_named_state = vivid.NamedState(attribute_system, p,
                                           refined_ascriptions)

    print "Attempting to refine to Named State via thinning:"
    print refined_named_state
    print

    ahead_formula = vivid.Formula(vocabulary, "Ahead", "c1", "c2")
    context = vivid.Context(vivid.AssumptionBase(ahead_formula), named_state)

    print "Does thinning hold?:"
    print vivid.thinning(context,
                         refined_named_state,
                         vivid.AssumptionBase(ahead_formula),
                         attribute_interpretation)

if __name__ == "__main__":
    main()
