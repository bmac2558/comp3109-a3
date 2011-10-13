from a3tree.builtin import MinNode
from a3tree.util import MOVQ_RAX_R10
from a3tree.util import MOVQ_RAX_R11
from a3tree.util import assign_op
from a3tree.variable import ConstNode
from a3tree.variable import VariableNode

import build.VPLLexer as lex

# NB: Each node must place its result in %rax during generate()

class ExprNode(object):
    def __init__(self, vplnode, consts, local_vars):
        # collapse the syntax tree to the next action node
        while vplnode.type not in (lex.EXPRMIN, lex.PLUS, lex.MINUS, lex.MULT,
                                   lex.DIVIDE, lex.ID, lex.NUM):
            assert len(vplnode.children) == 1, "Oops, I made a bad assumption"
            vplnode = vplnode.children[0]

        if vplnode.type == lex.ID:
            self.loperand = local_vars[vplnode.text]
            self.roperand = self.operator = None
            self.is_const = False
            self.chain_depth = 1

        elif vplnode.type == lex.NUM:
            self.loperand = ConstNode(vplnode, consts)
            self.roperand = self.operator = None
            self.is_const = True
            self.chain_depth = 1

        else:
            if vplnode.type == lex.PLUS:
                self.operator = '+'
            elif vplnode.type == lex.MINUS:
                self.operator = '-'
            elif vplnode.type == lex.MULT:
                self.operator = '*'
            elif vplnode.type == lex.DIVIDE:
                self.operator = '/'
            else:
                self.operator = 'MIN'

            self.loperand = ExprNode(vplnode.children[0], consts, local_vars)
            self.roperand = ExprNode(vplnode.children[1], consts, local_vars)
            self.is_const = False
            self.chain_depth = max(self.loperand.chain_depth,
                                   self.roperand.chain_depth) + 1

    def validate(self):
        pass

    def optimise(self):
        pass

    def generate(self):
        for line in self.loperand.generate():
            yield line

        if self.roperand is not None:
            yield MOVQ_RAX_R10

            for line in self.roperand.generate():
                yield line
            yield MOVQ_RAX_R11

            yield assign_op(
                    self.operator,
                    operand1_const=self.loperand.is_const,
                    operand2_const=self.roperand.is_const,
                    )

    def __repr__(self):
        if self.operator is None:
            return repr(self.loperand)
        return "({0} {1} {2})".format(
                self.operator,
                self.loperand,
                self.roperand,
                )
