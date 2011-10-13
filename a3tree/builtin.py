class MinNode(object):
    def __init__(self, vplnode, consts, local_vars):
        # avoid cyclical imports
        from a3tree.expr import ExprNode
        self.lexpr = ExprNode(vplnode.children[0], consts, local_vars)
        self.rexpr = ExprNode(vplnode.children[1], consts, local_vars)

        self.chain_depth = max(self.lexpr.chain_depth,
                               self.rexpr.chain_depth) + 1

    def validate(self):
        pass

    def optimise(self):
        pass

    def generate(self):
        from a3tree.expr import ASSIGN_OPR
        from a3tree.expr import CONST
        from a3tree.expr import OPERAND_TYPE
        from a3tree.expr import MOVQ_RAX_R10
        from a3tree.expr import MOVQ_RAX_R11
        from a3tree.expr import VAR

        for line in self.lexpr.generate():
            yield line

        if self.rexpr is not None:
            yield MOVQ_RAX_R10

            for line in self.rexpr.generate():
                yield line
            yield MOVQ_RAX_R11

        yield ASSIGN_OPR.format(
                idx='0',  # FIXME
                operation='minps',
                op1_type=OPERAND_TYPE[self.lexpr.type, 1],
                op2_type=OPERAND_TYPE[self.rexpr.type, 2],
                )

    def __repr__(self):
        return "(MIN {0} {1})".format(
                self.lexpr,
                self.rexpr,
                )
