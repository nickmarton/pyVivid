"""truth_value_parser module."""

from __future__ import division
from pyparsing import (Literal, CaselessLiteral, Word, Combine, Group,
                       Optional, ZeroOrMore, Forward, nums, alphas, oneOf)
import math
import operator

# BNF:
# expop       ::   '^'
# multop      ::   '*' | '/'
# addop       ::   '+' | '-'
# relop       ::   '=' | '>' | '<' | '<=' | '>='
# negop       ::   '!'
# logop       ::   'and' | 'or'
# integer     ::   ['+' | '-'] '0'..'9'+
# atom        ::   PI | E | True | False | real | fn '(' expr ')' | '(' expr ')'
# factor      ::   atom [ expop factor ]*
# term        ::   factor [ multop factor ]*
# expr        ::   term [ addop term ]*
# relation    ::   expr [relop expr]*
# negation    ::   [negop]* + relation
# sentence    ::   negation [logop negation]*


class TruthValueParser(object):
    """
    TruthValueParser class. TruthValueParser provides parsing functionality for
    entirely mathematical/logical strings.

    :ivar _is_Parser: An identifier to use in place of ``type`` or \
    ``isinstance``.
    """

    negations = []

    def __init__(self):
        """
        Construct a TruthValueParser object.
        """

        point = Literal(".")
        e = CaselessLiteral("E")
        fnumber = Combine(Word("+-" + nums, nums) +
                          Optional(point + Optional(Word(nums))) +
                          Optional(e + Word("+-" + nums, nums)))
        ident = Word(alphas, alphas + nums + "_$")

        true = Literal("True")
        false = Literal("False")
        andop = CaselessLiteral("and")
        orop = CaselessLiteral("or")
        negop = Literal("!")
        eop = Literal("=")
        gop = Literal(">")
        lop = Literal("<")
        geop = Literal(">=")
        leop = Literal("<=")
        plus = Literal("+")
        minus = Literal("-")
        mult = Literal("*")
        div = Literal("/")
        lpar = Literal("(").suppress()
        rpar = Literal(")").suppress()
        logop = andop | orop
        relop = eop | geop | leop | gop | lop
        addop = plus | minus
        multop = mult | div
        expop = Literal("^")
        pi = CaselessLiteral("PI")
        sentence = Forward()
        atom = (
            (Optional(oneOf("- +")) +
                (pi | e | true | false | fnumber | ident + lpar + sentence + rpar).setParseAction(self.pushFirst)) |
            Optional(oneOf("- +")) + Group(lpar + sentence + rpar)).setParseAction(self.pushUMinus)
        # by defining exponentiation as "atom [ ^ factor ]..." instead of
        # "atom [ ^ atom ]...", we get right-to-left exponents, instead of
        # left-to-right that is, 2^3^2 = 2^(3^2), not (2^3)^2.
        factor = Forward()
        factor << atom + ZeroOrMore((expop + factor).setParseAction(
            self.pushFirst))

        term = factor + ZeroOrMore((multop + factor).setParseAction(
            self.pushFirst))
        expr = Group(term + ZeroOrMore((addop + term).setParseAction(
            self.pushFirst)))

        relation = Group(expr + ZeroOrMore((relop + expr).setParseAction(
            self.pushRel)))

        negation = ZeroOrMore(negop.setParseAction(self.pushNeg)) + relation

        sentence << Group(negation + ZeroOrMore(
            (logop + negation).setParseAction(self.pushFirst)))

        self.bnf = sentence

        # map operator symbols to corresponding arithmetic operations
        epsilon = 1e-12
        self.opn = {"+": operator.add,
                    "-": operator.sub,
                    "*": operator.mul,
                    "/": operator.truediv,
                    "^": operator.pow}

        self.fn = {"sin": math.sin,
                   "cos": math.cos,
                   "tan": math.tan,
                   "abs": abs,
                   "trunc": lambda a: int(a),
                   "round": round,
                   "sgn": lambda a: abs(a) > epsilon and cmp(a, 0) or 0}

        self.rel = {"=": operator.eq,
                    ">": operator.gt,
                    "<": operator.lt,
                    ">=": operator.ge,
                    "<=": operator.le}

        self.neg = {"!": lambda a: False if a is True else True}

        self.log = {"and": all,
                    "or": any}

        self._is_Parser = True

    def __call__(self, *args):
        """
        Call TruthValueParser object (e.g., ``TruthValueParser(expression)``).
        """

        return self._eval(*args)

    def pushFirst(self, strg, loc, toks):
        """Push first token onto the stack."""
        self.exprStack.append(toks[0])

    def pushUMinus(self, strg, loc, toks):
        """Push unary minus operator onto the stack."""
        if toks and toks[0] == '-':
            self.exprStack.append('unary -')

    def pushNeg(self, strg, loc, toks):
        "Push a negation into negation list."
        self.negations.append(toks[0])

    def pushRel(self, strg, loc, toks):
        """Push relational operator onto stach and possible negations."""
        self.exprStack.append(toks[0])
        if self.negations:
            for i in range(len(self.negations)):
                self.exprStack.append("!")
            self.negations = []

    def evaluate_stack(self, s):
        """Evaluate internal stack of parse object."""
        op = s.pop()
        if op == 'unary -':
            return -self.evaluate_stack(s)
        if op in "+-*/^":
            op2 = self.evaluate_stack(s)
            op1 = self.evaluate_stack(s)
            return self.opn[op](op1, op2)
        elif op in "<=>=":
            op2 = self.evaluate_stack(s)
            op1 = self.evaluate_stack(s)
            return self.rel[op](float(op1), float(op2))
        elif op in "!":
            op = self.evaluate_stack(s)
            return self.neg["!"](op)
        elif op in "andor":
            op2 = self.evaluate_stack(s)
            op1 = self.evaluate_stack(s)
            return self.log[op]([op1, op2])
        elif op == "True":
            return True
        elif op == "False":
            return False
        elif op == "PI":
            return math.pi  # 3.1415926535
        elif op == "E":
            return math.e  # 2.718281828
        elif op in self.fn:
            return self.fn[op](self.evaluate_stack(s))
        elif op[0].isalpha():
            return 0
        else:
            return float(op)

    def _eval(self, string):
        """
        Try to evaluate given string in ``string`` parameter.
        (e.g.,"``(4 < 5 * cos(2 * PI) and 4*e^3 > 3 *(3 + 3))and!(2 < 3)``").

        :param string: The expression to evaluate.
        :type  string: ``str``
        """

        self.exprStack = []
        parseAll = True
        results = self.bnf.parseString(string, parseAll)
        val = self.evaluate_stack(self.exprStack[:])
        return val


def main():
    import time
    start_time = time.time()

    lmtp = TruthValueParser()
    # result = lmtp(
    # '(!!(((-cos(2*pi) + 44^2) + (-cos(2*pi) + 44^2) ^ 1.5) > 1) and !!True) or 7>5^2')
    expression = '(4<5 * cos(2 * PI) and 4*e^3 > 3 * 3 *(3+3))and!!(2 < 3)'
    print expression
    result = lmtp(expression)
    print result

    end_time = time.time()

    print
    print str(end_time - start_time) + " seconds"

if __name__ == "__main__":
    main()
