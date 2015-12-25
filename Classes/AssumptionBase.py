"""AssumptionBase class."""

from Formula import Formula


class AssumptionBase(object):
    """
    Assumption base object.

    Essentially this class is a container for a finite set of Formulae
    over the same Vocabulary.
    """

    def __init__(self, *formulae):
        """Construct an AssumptionBase object."""
        self._formulae = []

        if formulae:
            # Ensure all optional positional args are of type Formula.
            for f in formulae:
                if not hasattr(f, "_is_Formula"):
                    raise TypeError(
                        "all arguments passed to constructor must be a "
                        "Formula object")

            # check for same vocabulary condition and add formula to list
            vocabulary = formulae[0]._vocabulary
            names = [f._name for f in formulae]

            if len(names) != len(set(names)):
                raise ValueError("Duplicate Formula names not permitted")

            for f in formulae:
                if vocabulary != f._vocabulary:
                    raise ValueError(
                        "all formulae provided to constructor must share the "
                        "same Vocabulary")

                # ensure no duplicates
                if f not in self._formulae:
                    self._formulae.append(f)
        else:
            raise ValueError("AssumptionBase cannot be empty")

        self._formulae = sorted(self._formulae, key=lambda x: x._name)
        self._vocabulary = self._formulae[0]._vocabulary
        self._is_AssumptionBase = True

    def __eq__(self, other):
        """Implement != operator for AssumptionBase objects."""
        if not hasattr(other, "_is_AssumptionBase"):
            raise TypeError(
                "Can only compare an AssumptionBase object with "
                "another AssumptionBase object")

        # Cardinalities must be the same.
        if len(self._formulae) != len(other._formulae):
            return False

        # check if each formula in self has a match in other.
        intersection = set(self._formulae) & set(other._formulae)
        union = set(self._formulae) | set(other._formulae)
        return intersection == union

    def __ne__(self, other):
        """Implement != operator for AssumptionBase objects."""
        return not self.__eq__(other)

    def __add__(self, other):
        """Implement + operator for AssumptionBase."""
        from copy import deepcopy
        self_copy = deepcopy(self)

        # Handle adding an AssumptionBase
        if hasattr(other, "_is_AssumptionBase"):
            # Edge cases
            if len(self) == 0:
                return deepcopy(other)
            if len(other) == 0:
                return self_copy

            names = [formula._name for formula in self._formulae]
            vocabulary = self._formulae[0]._vocabulary

            for other_formula in other:
                if other_formula._vocabulary != vocabulary:
                    raise ValueError(
                        "Cannot add AssumptionBase's with different "
                        "Vocabulary's")
                if other_formula._name in names:
                    raise ValueError("Duplicate Formula objects not permitted")

                self_copy._formulae.append(deepcopy(other_formula))

            return self_copy

        # Handle adding a Formula
        if hasattr(other, "_is_Formula"):
            # Edge cases
            if len(self) == 0:
                return AssumptionBase(*deepcopy([other]))

            names = [formula._name for formula in self._formulae]
            vocabulary = self._formulae[0]._vocabulary

            if other._vocabulary != vocabulary:
                raise ValueError(
                    "Cannot add Formula's with different Vocabulary's")
            if other._name in names:
                raise ValueError("Duplicate Formula objects not permitted")

            self_copy._formulae.append(deepcopy(other))

            return self_copy

        raise TypeError(
            "Only Formula and AssumptionBase objects can be added to an "
            "AssumptionBase")

    def __iadd__(self, other):
        """Implement += for AssumptionBase object."""
        return self + other

    def __str__(self):
        """Implement str(AssumptionBase)."""
        return 'AB(' + ', '.join([str(f) for f in self._formulae]) + ')'

    def __repr__(self):
        """Implement str(AssumptionBase)."""
        return self.__str__()

    def __len__(self):
        """Implement len(AssumptionBase)."""
        return len(self._formulae)

    def __getitem__(self, key):
        """Implement indexing for AssumptionBase object."""
        if hasattr(key, "_is_Formula"):
            for i, formula in enumerate(self._formulae):
                if key == formula:
                    return self._formulae[i]
            raise KeyError("Formula not found")

        if type(key) == str:
            for i, name in enumerate([f._name for f in self._formulae]):
                if key == name:
                    return self._formulae[i]
            raise KeyError("Formula not found")

        if type(key) == int:
            try:
                return self._formulae[key]
            except IndexError:
                raise IndexError(
                    str(key) + " not a valid index in AssumptionBase")

        raise TypeError("Invalid key type")

    def __iter__(self):
        """Add an interator to the class for easy formula access."""
        for formula in self._formulae:
            yield formula

    def __contains__(self, item):
        """Implement 'in' and 'not in' operator for AssumptionBase."""
        # Handle if item provided is a string; assume it's a Formula name
        if type(item) == str:
            names = [f._name for f in self._formulae]
            if item in names:
                return True

        # Handle if Formula object is provided
        if hasattr(item, "_is_Formula"):
            for formula in self._formulae:
                if item == formula:
                    return True

        return False

    def __deepcopy__(self, memo):
        """Implement copy.deepcopy for AssumptionBase."""
        from copy import deepcopy
        return AssumptionBase(*deepcopy(self._formulae))


def main():
    """Quick tests."""
    from RelationSymbol import RelationSymbol
    from Vocabulary import Vocabulary

    ahead_rs = RelationSymbol('Ahead', 4)
    behind_rs = RelationSymbol('Behind', 4)
    pm_rs = RelationSymbol('PM', 1)
    vocabulary = Vocabulary(
        ['C1', 'C2'], [ahead_rs, behind_rs, pm_rs], ['V1', 'V2'])

    f1 = Formula(vocabulary, 'Ahead', 'C1', 'V1')
    f2 = Formula(vocabulary, 'Behind', 'C1')

    a = AssumptionBase(f1, f2)
    a2 = AssumptionBase(f2, f1)

    print a2

if __name__ == "__main__":
    main()
