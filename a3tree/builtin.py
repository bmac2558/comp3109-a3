class MinNode(object):
    def __init__(self, vplnode, consts, local_vars):
        # avoid cyclical imports
        from a3tree.expr import ExprNode
        self.lexpr = ExprNode(vplnode.children[0], consts, local_vars)
        self.rexpr = ExprNode(vplnode.children[1], consts, local_vars)

    def validate(self):
        pass

    def optimise(self):
        pass

    def generate(self):
        yield 'min'

    def __repr__(self):
        return "(MIN {0} {1})".format(
                self.lexpr,
                self.rexpr,
                )
