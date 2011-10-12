from a3tree.builtin import MinNode
from a3tree.variable import get_varnode
from a3tree.variable import VariableNode
import build.VPLLexer as lex

class ExprNode(object):
    def __init__(self, vplnode):
        self.loperand = Expr2Node(vplnode)
        if vplnode.type in (lex.PLUS, lex.MINUS):
            if vplnode.type == lex.PLUS:
                self.operator = '+'
            else:
                self.operator = '-'
            self.roperand = ExprNode(vplnode.children[1])
        else:
            self.operator = self.roperand = None

    def validate(self):
        pass

    def optimise(self):
        pass

    def generate(self):
        yield 'expr1'

    def __repr__(self):
        if self.operator is None:
            return repr(self.loperand)
        return "({0} {1} {2})".format(
                self.operator,
                self.loperand,
                self.roperand,
                )

class Expr2Node(object):
    def __init__(self, vplnode):
        self.loperand = Expr3Node(vplnode)
        if vplnode.type in (lex.MULT, lex.DIVIDE):
            if vplnode.type == lex.MULT:
                self.operator = '*'
            else:
                self.operator = '/'
            self.roperand = Expr2Node(vplnode.children[1])
        else:
            self.operator = self.roperand = None

    def validate(self):
        pass

    def optimise(self):
        pass

    def generate(self):
        yield 'expr2'

    def __repr__(self):
        if self.operator is None:
            return repr(self.loperand)
        return "({0} {1} {2})".format(
                self.operator,
                self.loperand,
                self.roperand,
                )

class Expr3Node(object):
    def __init__(self, vplnode):
        if vplnode.type == lex.EXPRMIN:
            self.me = MinNode(vplnode)
        elif vplnode.type == lex.ID:
            self.me = get_varnode(vplnode)
        elif vplnode.type == lex.NUM:
            self.me = get_varnode(vplnode)
        else:
            self.me = ExprNode(vplnode.children[0])

    def validate(self):
        pass

    def optimise(self):
        pass

    def generate(self):
        yield 'expr3'

    def __repr__(self):
        return repr(self.me)
