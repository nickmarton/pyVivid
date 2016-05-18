import vivid


def main():

    # Define Attributes, Relations and AttributeStructure
    spacetime_loc = vivid.Attribute("spacetime_loc",
                                    [vivid.Point("x", "x")])
    speed = vivid.Attribute("speed", [vivid.Interval(0.0, 1.0)])
    worldline = vivid.Attribute('worldline',
                                [vivid.LineSegment(vivid.Point('x', 'x'),
                                                   vivid.Point('x', 'x'))])

    R1 = vivid.Relation(
        "R1(sp, w1, w2) <=> meets(sp, w1, w2)",
        ["spacetime_loc", "worldline", "worldline"], subscript=1)

    R2 = vivid.Relation("R2(v) <=> v = 1", ["speed"], subscript=2)

    R3 = vivid.Relation("R3(sp1, sp2) <=> not_same_point(sp1, sp2)",
                        ["spacetime_loc", "spacetime_loc"], subscript=3)

    R4 = vivid.Relation("R4(v1, v2) <=> v1 = v2",
                        ["speed", "speed"], subscript=4)

    R5 = vivid.Relation("R5(sp1, sp2) <=> clocks_unequal(sp1, sp2)",
                        ["spacetime_loc", "spacetime_loc"], subscript=5)

    attribute_structure = vivid.AttributeStructure(
        spacetime_loc, worldline, speed, R1, R2, R3, R4, R5)

    print "Creating Attribute Structure:"
    print attribute_structure
    print

    # define Vocabulary
    meets = vivid.RelationSymbol("meets", 3)
    speed_of_light = vivid.RelationSymbol("speed_of_light", 1)
    not_same_spacetime_location = vivid.RelationSymbol("not_same_spacetime", 2)
    in_same_frame = vivid.RelationSymbol("in_same_frame", 2)
    clocks_unequal = vivid.RelationSymbol("clocks_unequal", 2)

    vocabulary = vivid.Vocabulary(
        ["m1", "m2", "m3", "m4"],
        [meets, speed_of_light, not_same_spacetime_location,
         in_same_frame, clocks_unequal],
        [])

    print "Creating Vocabulary:"
    print vocabulary
    print

    # define AttributeInterpretation
    profiles = [
        [meets, ("spacetime_loc", 1), ("worldline", 2), ("worldline", 3)],
        [speed_of_light, ("speed", 1)],
        [not_same_spacetime_location, ("spacetime_loc", 1),
         ("spacetime_loc", 2)],
        [in_same_frame, ("speed", 1), ("speed", 2)],
        [clocks_unequal, ("spacetime_loc", 1), ("spacetime_loc", 2)]]

    attribute_interpretation = vivid.AttributeInterpretation(
        vocabulary, attribute_structure,
        {meets: 1, speed_of_light: 2, not_same_spacetime_location: 3,
         in_same_frame: 4, clocks_unequal: 5},
        profiles)

    print "Creating Attribute Interpretation:"
    print attribute_interpretation
    print

    # Create all the positions and lines ahead of time
    m1_segment = vivid.LineSegment(vivid.Point(0.0, 0.0), vivid.Point(0.0, 0.0))
    m2_segment = vivid.LineSegment(vivid.Point(-1.0, -2.0), vivid.Point(3.0, 6.0))
    m3_segment = vivid.LineSegment(vivid.Point(0.0, -2.0), vivid.Point(4.0, 6.0))
    m4_segment = vivid.LineSegment(vivid.Point(1.0, -2.0), vivid.Point(5.0, 6.0))
    c1_segment = vivid.LineSegment(vivid.Point(-2.0, -2.0), vivid.Point(6.0, 6.0))
    c2_segment = vivid.LineSegment(vivid.Point(0.0, 4.0), vivid.Point(6.0, -2.0))
    i1_pos = vivid.Point(0.0, 0.0)
    p_pos = vivid.Point(2.0, 2.0)
    q_pos = vivid.Point(2.6666666667, 1.3333333333)
    i2_pos = vivid.Point(2.6666666667, 1.3333333333)
    q_prime_pos = vivid.Point(2.0, 0.0)

    # Create initial named state delta 0
    objects = ["m1", "m2", "m3", "m4"]
    attribute_system = vivid.AttributeSystem(attribute_structure, objects)

    print "Creating Attribute System:"
    print attribute_system
    print

    const_mapping = {"m1": "m1", "m2": "m2", "m3": "m3", "m4": "m4"}
    p = vivid.ConstantAssignment(vocabulary, attribute_system, const_mapping)

    ascr = {
        ("worldline", "m1"): [m1_segment], ("speed", "m1"): [0.0],
        ("worldline", "m2"): [m2_segment], ("speed", "m2"): [1.0],
        ("worldline", "m3"): [m3_segment], ("speed", "m3"): [1.0],
        ("worldline", "m4"): [m4_segment], ("speed", "m4"): [1.0]}

    delta_0 = vivid.NamedState(attribute_system, p, ascr)

    delta_0.add_object("i1", {("spacetime_loc", "i1"): [i1_pos]},
                       constant_symbol="i1")

    print "Creating Initial named state delta 0:"
    # print delta_0
    print

    delta_1 = vivid.diagram_reiteration(
        vivid.Context(vivid.AssumptionBase(vocabulary), delta_0))

    print "Creating named state delta 1:"
    # print delta_1
    print

    meets_i1_m1_m2 = vivid.Formula(vocabulary, "meets", "i1", "m1", "m2")
    same_frame_v1_v2 = vivid.Formula(vocabulary, "in_same_frame", "m1", "m2")
    same_frame_v2_v3 = vivid.Formula(vocabulary, "in_same_frame", "m2", "m3")
    same_frame_v2_v4 = vivid.Formula(vocabulary, "in_same_frame", "m2", "m4")
    same_frame_v3_v4 = vivid.Formula(vocabulary, "in_same_frame", "m3", "m4")

    delta_1_context = vivid.Context(vivid.AssumptionBase(vocabulary), delta_1)

    print "Verifying first set of observations:"
    assert (vivid.observe(delta_1_context, meets_i1_m1_m2,
                          attribute_interpretation) and
            not vivid.observe(delta_1_context, same_frame_v1_v2,
                              attribute_interpretation))

    assert vivid.observe(delta_1_context, same_frame_v2_v3,
                         attribute_interpretation)

    assert vivid.observe(delta_1_context, same_frame_v2_v4,
                         attribute_interpretation)

    assert vivid.observe(delta_1_context, same_frame_v3_v4,
                         attribute_interpretation)

    print "True"
    print

    # Add p and c1 to the diagram
    delta_1.add_object("p", {("spacetime_loc", "p"): [p_pos]},
                       constant_symbol="p")
    delta_1.add_object("c1", {("worldline", "c1"): [c1_segment],
                              ("speed", "c1"): [1.0]},
                       constant_symbol="c1")
    delta_2 = vivid.diagram_reiteration(
        vivid.Context(vivid.AssumptionBase(vocabulary), delta_1))

    print "Creating named state delta 2:"
    # print delta_2
    print

    meets_p_c1_m3 = vivid.Formula(vocabulary, 'meets', 'p', 'c1', 'm3')
    speed_of_light_c1 = vivid.Formula(vocabulary, 'speed_of_light', 'c1')

    delta_2_context = vivid.Context(vivid.AssumptionBase(vocabulary), delta_2)

    print "Verifying second set of observations:"
    assert (vivid.observe(delta_2_context, meets_p_c1_m3,
                          attribute_interpretation) and
            vivid.observe(delta_2_context, speed_of_light_c1,
                          attribute_interpretation))
    print "True"
    print

    print "Asserting thinning can derive delta 3 from delta 2, then creating delta 3:"
    assert vivid.thinning(delta_2_context, delta_2)
    print "True"
    print

    delta_3 = vivid.diagram_reiteration(delta_2_context)

    delta_3.add_object("c2", {('worldline', 'c2'): [c2_segment],
                              ("speed", "c2"): [1.0]},
                       constant_symbol="c2")
    delta_3.add_object("i2", {("spacetime_loc", "i2"): [i2_pos]},
                       constant_symbol="i2")
    delta_3.add_object("q", {("spacetime_loc", "q"): [q_pos]},
                       constant_symbol="q")
    delta_3.add_object("q_prime", {("spacetime_loc", "q_prime"): [q_prime_pos]},
                       constant_symbol="q_prime")

    delta_4 = vivid.diagram_reiteration(vivid.Context(vivid.AssumptionBase(vocabulary), delta_3))

    print "Creating named state delta 4:"
    # print delta_4
    print

    meets_q_c2_m4 = vivid.Formula(vocabulary, 'meets', 'q', 'c2', 'm4')
    speed_of_light_c2 = vivid.Formula(vocabulary, 'speed_of_light', 'c2')

    delta_4_context = vivid.Context(vivid.AssumptionBase(vocabulary), delta_4)

    print "Verifying third set of observations:"
    assert (vivid.observe(delta_4_context, meets_q_c2_m4,
                          attribute_interpretation) and
            vivid.observe(delta_4_context, speed_of_light_c2,
                          attribute_interpretation))
    print "True"
    print

    print "Asserting thinning can derive delta 5 from delta 4, then creating delta 5:"
    assert vivid.thinning(delta_4_context, delta_4)
    print "True"
    print

    delta_5 = vivid.diagram_reiteration(delta_4_context)

    meets_i1_m2_c1 = vivid.Formula(vocabulary, 'meets', 'i1', 'm2', 'c1')
    meets_p_c1_c2 = vivid.Formula(vocabulary, 'meets', 'p', 'c1', 'c2')
    meets_i2_c2_m4 = vivid.Formula(vocabulary, 'meets', 'i2', 'c2', 'm4')
    not_same_spacetime_loc_q_qprime = vivid.Formula(vocabulary, 'not_same_spacetime', 'q', 'q_prime')
    not_same_spacetime_loc_p_q = vivid.Formula(vocabulary, 'not_same_spacetime', 'p', 'q')
    clocks_unequal_i1_i2 = vivid.Formula(vocabulary, 'clocks_unequal', 'i1', 'i2')

    delta_5_context = vivid.Context(vivid.AssumptionBase(vocabulary), delta_5)

    print "Verifying fourth set of observations:"
    assert vivid.observe(delta_5_context, not_same_spacetime_loc_q_qprime,
                         attribute_interpretation)

    assert vivid.observe(delta_5_context, not_same_spacetime_loc_p_q,
                         attribute_interpretation)
    o_meets_i1_m2_c1 = vivid.observe(delta_5_context, meets_i1_m2_c1,
                                     attribute_interpretation)

    o_meets_p_c1_c2 = vivid.observe(delta_5_context, meets_p_c1_c2,
                                    attribute_interpretation)

    o_meets_i2_c2_m4 = vivid.observe(delta_5_context, meets_i2_c2_m4,
                                     attribute_interpretation)

    o_speed_of_light_c1 = vivid.observe(delta_5_context, speed_of_light_c1,
                                        attribute_interpretation)

    o_speed_of_light_c2 = vivid.observe(delta_5_context, speed_of_light_c2,
                                        attribute_interpretation)
    assert (meets_i1_m2_c1 and meets_p_c1_c2 and meets_i2_c2_m4 and
            o_speed_of_light_c1 and o_speed_of_light_c2)

    o_clocks_unequal_i1_i2 = vivid.observe(
        delta_5_context, clocks_unequal_i1_i2, attribute_interpretation)
    assert o_clocks_unequal_i1_i2
    print "True"
    print

    meets_p_m2_m4 = vivid.Formula(vocabulary, 'meets', 'p', 'm2', 'm4')

    o_meets_p_m2_m4 = vivid.observe(delta_5_context, meets_p_m2_m4,
                                    attribute_interpretation)
    o_same_frame_v2_v4 = vivid.observe(delta_5_context, same_frame_v2_v4,
                                       attribute_interpretation)

    print "verifying disjunction:"
    disjunct = (o_same_frame_v2_v4 or
                (o_meets_p_m2_m4 and not o_same_frame_v2_v4) or
                (o_meets_i1_m2_c1 and o_meets_p_c1_c2 and o_meets_i2_c2_m4 and
                 o_speed_of_light_c1 and o_speed_of_light_c2))
    assert disjunct
    print "True"
    print

    print "verifying clocks are out of sync:"
    out_of_sync = o_clocks_unequal_i1_i2 and disjunct
    assert out_of_sync
    print "True"
    print

    print "PROOF COMPLETE"

if __name__ == "__main__":
    main()
