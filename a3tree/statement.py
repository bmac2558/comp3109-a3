from a3tree.expr import ExprNode
from a3tree.variable import VariableNode

class StatementNode(object):
    def __init__(self, vplnode):
        self.var = VariableNode(vplnode.children[0])
        self.expr = ExprNode(vplnode.children[1])

    def validate(self):
        pass

    def optimise(self):
        pass

    def generate(self):
        yield "Assign to {0} the value of {1}".format(
                self.var.name,
                repr(self.expr))

    def __repr__(self):
        return "(ASSIGN {0} {1})".format(
                self.var,
                self.expr,
                )
