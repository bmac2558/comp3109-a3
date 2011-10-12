class MinNode(object):
    def __init__(self, vplnode):
        # avoid cyclical imports
        from a3tree.expr import ExprNode
        self.lexpr = ExprNode(vplnode.children[0])
        self.rexpr = ExprNode(vplnode.children[1])

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
