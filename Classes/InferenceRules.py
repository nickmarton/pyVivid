"""This module intends to provide the rules of diagrammatic inference."""


def widenning(context, named_state):
    """
    Verify that NamedState named_state can be obtained from Context context by
    widenning.
    """

    if not hasattr(context, "_is_Context"):
        raise TypeError("context parameter must be a Context object.")

    if not hasattr(named_state, "_is_NamedState"):
        raise TypeError("named_state parameter must be a NamedState object.")

    return context.named_state <= named_state


def main():
    """dev tests."""
    pass


if __name__ == "__main__":
    main()
