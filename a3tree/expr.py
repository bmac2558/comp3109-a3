from a3tree.error import VPLUnboundNameError
from a3tree.util import MOVQ_RAX_R10
from a3tree.util import MOVQ_RAX_R11
from a3tree.util import assign
from a3tree.util import assign_op
from a3tree.variable import ConstNode
from a3tree.variable import VariableNode

import build.VPLLexer as lex

# NB: Each node must place its result in %rax during generate()

class ExprNode(object):
    """
    A node in a binary tree representation of an evaluatable expression.

    Has a temporary variable that it uses to store intermediate results; its
    left (first) operand uses the same variable, while its right (second)
    operand uses the next temporary variable on the stack.  This means that
    expressions that are heavily nested to the left require fewer temporary
    variables.

    """
    def __init__(self, vplnode, consts, named_vars, tmp_var_idx):
        # collapse the syntax tree to the next action node
        while vplnode.type not in (lex.EXPRMIN, lex.PLUS, lex.MINUS, lex.MULT,
                                   lex.DIVIDE, lex.ID, lex.NUM):
            assert len(vplnode.children) == 1, "Oops, I made a bad assumption"
            vplnode = vplnode.children[0]

        if vplnode.type == lex.ID:
            if vplnode.text in named_vars:
                self.loperand = named_vars[vplnode.text]
            else:
                raise VPLUnboundNameError("variable " + vplnode.text + " used before declaration.")
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

            self.tmp_var_idx = tmp_var_idx
            self.loperand = ExprNode(vplnode.children[0], consts, named_vars,
                                     tmp_var_idx)
            self.roperand = ExprNode(vplnode.children[1], consts, named_vars,
                                     tmp_var_idx + 1)
            self.is_const = False
            self.chain_depth = max(self.loperand.chain_depth,
                                   self.roperand.chain_depth) + 1

    def validate(self, named_vars, tmp_vars):
        if self.operator is not None:
            self.tmp_var = tmp_vars[self.tmp_var_idx]

        self.loperand.validate(named_vars, tmp_vars)

        if self.operator is not None:
            self.roperand.validate(named_vars, tmp_vars)

    def generate(self):
        # evaluate left operand
        for line in self.loperand.generate():
            yield line

        if self.roperand is not None:
            # save left operand to temporary variable
            # NB: this is (probably) unnecessary of loperand is an ExprNode
            yield MOVQ_RAX_R10
            for line in self.tmp_var.generate():
                yield line
            yield assign('%r10', '%rax')

            # evaluate right operand
            for line in self.roperand.generate():
                yield line
            yield MOVQ_RAX_R11

            # load temporary variable holding loperand's result
            for line in self.tmp_var.generate():
                yield line
            yield MOVQ_RAX_R10

            # assign (operator loperand roperand) to temporary variable
            yield assign_op(
                    self.operator,
                    operand1_const=self.loperand.is_const,
                    operand2_const=self.roperand.is_const,
                    )

            # always leave %rax pointing to the result
            # vebose for clarity
            for line in self.tmp_var.generate():
                yield line

    def __repr__(self):
        if self.operator is None:
            return repr(self.loperand)
        return "({0} {1} {2})".format(
                self.operator,
                self.loperand,
                self.roperand,
                )
