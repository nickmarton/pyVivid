#Vivid

Vivid is an implementation of the theoretical framework described in the paper [here][paper] (built entirely in python 2.7).
Vivid provides a framework to combine two different forms of reasoning; the first of which being traditional symbolic logic and the second being so called "diagrammatic" logic. More specifically, Vivid allows one to combine the reasoning processes used by people when reasoning about diagrams (e.g. a driver knows both the meaning of and how to identify a stop sign without any formal deduction) with traditional logic (e.g. first-order logic, propositional logic etc.) to produce succinct yet powerfully explanatory proofs. Vivid can also deal with reasoning over incomplete information (e.g. in the case of a partially filled in diagram). The full framework is not available publicly yet because of pending papers; please contact me to learn more.

[paper]: http://citeseerx.ist.psu.edu/viewdoc/download?doi=10.1.1.466.4004&rep=rep1&type=pdf

#TODO
* Finish NamedState refactoring
    * is_named_entailment
    * satisfies_context
* Finish NamedState unit tests
* Vocabulary mutability needs to propogate to all references of the Vocabulary object
* assign truth value needs to support more than just simple logic-math expressions