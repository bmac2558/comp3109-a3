from a3tree.error import VPLSyntaxError
from a3tree.expr import ExprNode
from a3tree.variable import VariableNode

ASSIGN = """
    # copy vector from %rax to %r10
    movq    %rdi, %rbx      # load vector length into counter %rbx
    shrl    $2, %rbx        # divide counter reg by 4
                            # (per loop iteration 4 floats)
    jz      .loop_end<X>    # check whether number is equal to zero

    .loop_begin<X>:

        movaps  (%rax), %xmm0   # load source into %xmm0
        movaps  %xmm0, (%r10)   # store %xmm0
{type}
        addq    $16, %r10       # increment destination pointer by (4 x float)

        decq    %rbx            # decrement counter
        jnz     .loop_begin<X>  # jump to loop header if counter is not zero

    .loop_end<X>:
"""

CONST = ""
VAR = """
        addq    $16, %rax       # increment source pointer by (4 x float)
"""

class StatementNode(object):
    def __init__(self, vplnode, consts, local_vars):
        name = vplnode.children[0].text
        try:
            self.var = local_vars[name]
        except NameError:
            raise VPLSyntaxError("Undeclared variable '{0}'".format(name))
        self.expr = ExprNode(vplnode.children[1], consts, local_vars)

    def validate(self):
        pass

    def optimise(self):
        pass

    def generate(self):
        yield "# assign to {0} the value of {1}".format(
                self.var.name,
                repr(self.expr))
        for line in self.expr.generate():
            yield line
        for line in self.var.generate(load_to='%r10'):
            yield line
        yield ASSIGN.format(type=VAR)  # FIXME?

    def __repr__(self):
        return "(ASSIGN {0} {1})".format(
                self.var,
                self.expr,
                )
