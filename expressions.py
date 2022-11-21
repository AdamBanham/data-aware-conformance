"""
Example of using pyparsing for expressions can be found here:
https://github.com/pyparsing/pyparsing/blob/master/examples/eval_arith.py

The following is adapted to suit Petri net with Data that are generated from
ProM and stored in this repo in the 'models' directory.
"""

from pyparsing import (
    Word,
    nums,
    alphas,
    Combine,
    oneOf,
    opAssoc,
    infixNotation,
    Literal,
)

from typing import Any,Set
from copy import deepcopy,copy

class EvalLiteral:
    "Class to evaluate a parsed literal"

    def __init__(self):
        self.value = None

    def eval(self):
        return eval( self.value.replace('&#34;',"'"))

    def __call__(self, tokens) -> Any:
        self.value = tokens[0]
        return copy(self)

class EvalVariable:
    "Class to evaluate a parsed variable"

    def __init__(self, state_space):
        self.value = None
        self._observed_variables = set()
        self._set_state_space(state_space)

    def _set_state_space(self, space):
        self._state_space = space 

    def eval(self, dryrun=False):
        if (dryrun):
            self._observed_variables.add(self.value)
            return
        if self.value in self._state_space:
            return self._state_space[self.value]
        raise ValueError(f"Undefined variable :: {self.value}")

    def seen_variables(self) -> Set:
        return self._observed_variables
    
    def __call__(self, tokens) -> Any:
        self.value = tokens[0]
        self.eval(dryrun=True)
        return copy(self)



class EvalConstant:
    "Class to evaluate a parsed numeric constant"

    def __init__(self):
        self.value = None

    def eval(self):
        if self.value == 'true':
            return True 
        elif self.value == 'false':
            return False
        return float(self.value)

    def __call__(self, tokens) -> Any:
        self.value = tokens[0]
        return copy(self)


class EvalComparisonOp:
    "Class to evaluate comparison expressions"
    opMap = {
        "&lt;" : lambda a, b: a < b,
        "&lt;=" : lambda a,b: a <= b,
        "&gt;" : lambda a, b: a > b,
        "&gt;=" : lambda a,b: a >= b,
        "==": lambda a, b: a == b,
        '&amp;&amp;': lambda a,b: a and b,
        "<" : lambda a, b: a < b,
        "<=" : lambda a,b: a <= b,
        ">" : lambda a, b: a > b,
        ">=" : lambda a,b: a >= b,
        '&&': lambda a,b: a and b,
    }

    def __init__(self):
        self.value = None

    def eval(self):
        val1 = self.value[0].eval()
        for op, val in self.operatorOperands(self.value[1:]):
            fn = EvalComparisonOp.opMap[op]
            val2 = val.eval()
            if not fn(val1, val2):
                break
            val1 = val2
        else:
            return True
        return False

    def operatorOperands(self,tokenlist):
        "generator to extract operators and operands in pairs"
        it = iter(tokenlist)
        while 1:
            try:
                yield (next(it), next(it))
            except StopIteration:
                break

    def __call__(self, tokens) -> Any:
        self.value = tokens[0]
        return copy(self)


class ExpressionParser():
    "A parser for guards associated with Petri net with Data"

    def __init__(self, state_space, exp:str) -> None:
        self._space = state_space
        self._org_exp = exp
        self._create_instances()
        self._create_operand()
        self._expr_form()
        self._parse()

    def _create_instances(self) -> None:
        self._constant = EvalConstant()
        self._literal = EvalLiteral()
        self._variable = EvalVariable(self._space)
        self._comparison = EvalComparisonOp()

    def _create_operand(self) -> None:
        # operand for parser
        booleans = Literal("true") | Literal('false')
        integer = Word(nums)
        real = Combine(Word(nums) + "." + Word(nums))
        values = booleans | real | integer 
        values.setParseAction(self._constant)

        literal = Combine('&#34;' + Word(alphas) + '&#34;')
        literal = literal | Combine('"' + Word(alphas) + '"')
        literal.setParseAction(self._literal)

        variable = Combine(Word(alphas,exact=1) + Word(alphas + nums))
        variable.setParseAction(self._variable)

        self._operand = values | literal | variable

    def _expr_form(self) -> None:
        comparisonop = oneOf("&lt;= <= &gt;= >= &lt; < &gt; > == &amp;&amp; &&")
        self._expr = infixNotation(
            self._operand,
            [
                (comparisonop, 2, opAssoc.LEFT, self._comparison),
            ],
        )

    def _parse(self):
        self._result = self._expr.parseString(self._org_exp)[0]

    def get_observed_vars(self):
        return self._variable.seen_variables()

    def change_state_space(self, state_space):
        self._space = state_space
        self._create_instances()
        self._create_operand()
        self._expr_form()
        self._parse()

    def result(self):
        return self._result.eval()
    
    

rules = [ 
    "true",
    "false",
    "((d1&gt;5)&amp;&amp;(d1&lt;=7))",
    "(d1&lt;=5)",
    "(d1&gt;7)",
    "(d10==&#34;apple&#34;)",
    "(d11&lt;10)",
    "((d10==&#34;apple&#34;)&amp;&amp;(d1&gt;9))",
    "(d1&gt;4)",
    "(d11&lt;10)",
    "(d1&gt;=8)",
    "(d3==&#34;AA&#34;)",
    """(d3=="AA")"""
]

vars_ = {
    "d1" : 10,
    "d2" : 5,
    "d3" : 'AA',
    "d4" : 5,
    "d5" : 5,
    "d6" : 10,
    "d10" : 'apple',
    "d11" : 5
}

def test():
    # define tests from given rules
    tests = []
    for t in rules:
        t_orig = t
        t = t.replace("true", "True")
        t = t.replace("false", "False")
        t = t.replace("&#34;", "'")
        t = t.replace("&lt;=", "<=")
        t = t.replace("&gt;", ">")
        t = t.replace("&lt;", "<")
        t = t.replace("&gt;=", ">=")
        t = t.replace("&amp;&amp;", " and ")
        tests.append((t_orig, eval(t, vars_)))

    # copy vars_ to EvalConstant lookup dict
    failed = 0
    for test, expected in tests:
        parser = ExpressionParser(vars_,test)
        print("saw the following variables :: ", parser.get_observed_vars())
        parsedvalue = parser.result()
        print(test, "|| expected :: " , expected, " && saw :: " , parsedvalue)
        if abs(parsedvalue - expected) > 1e-6:
            print("<<< FAIL")
            failed += 1
        else:
            print("")

    print("")
    if failed:
        raise Exception("could not parse")

if __name__ == "__main__":
    test()