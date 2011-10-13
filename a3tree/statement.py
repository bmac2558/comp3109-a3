from a3tree.error import VPLSyntaxError
from a3tree.expr import ExprNode
from a3tree.util import MOVQ_RAX_R10
from a3tree.util import assign
from a3tree.variable import VariableNode

class StatementNode(object):
    def __init__(self, vplnode, consts, local_vars):
        name = vplnode.children[0].text
        try:
            self.var = local_vars[name]
        except NameError:
            raise VPLSyntaxError("Undeclared variable '{0}'".format(name))
        self.expr = ExprNode(vplnode.children[1], consts, local_vars, 0)

        # naive tmps_needed solution
        max_depth = self.expr.chain_depth
        self.tmps_needed = int(max_depth)

    def validate(self, local_vars, tmp_vars):
        self.var.validate(local_vars, tmp_vars)
        self.expr.validate(local_vars, tmp_vars)

    def optimise(self):
        pass

    def generate(self):
        yield "# assign to {0} the value of {1}".format(
                self.var.name,
                repr(self.expr))
        for line in self.expr.generate():
            yield line
        yield MOVQ_RAX_R10
        for line in self.var.generate(load_to='%rax'):
            yield line
        yield assign('%r10', '%rax')

    def __repr__(self):
        return "(ASSIGN {0} {1})".format(
                self.var,
                self.expr,
                )
