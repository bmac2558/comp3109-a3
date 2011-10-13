from a3tree.builtin import MinNode
from a3tree.variable import ConstNode
from a3tree.variable import VariableNode

import build.VPLLexer as lex

MOVQ_RAX = """
    movq    %rax, {dst}
"""
MOVQ_RAX_R10 = MOVQ_RAX.format(dst='%r10')
MOVQ_RAX_R11 = MOVQ_RAX.format(dst='%r11')

ASSIGN_OPR = """
    # perform (%r10) {operation} (%r11) and store result at (%rax)
    movq    %rdi, %rbx      # load vector length into counter %rbx
    shrq    $2, %rbx        # divide counter reg by 4
                            # (per loop iteration 4 floats)
    jz      .loop_end{idx}      # check whether number is equal to zero

    .loop_begin{idx}:

        movaps  (%r10), %xmm0   # load first operand into %xmm0
        movaps  (%r11), %xmm1   # load second operand into %xmm1

        # perform operation
        {operation}   %xmm0, %xmm1

        movaps  %xmm1, (%rax)   # store result

        # increment pointers (by 4 x float)
{op1_type}{op2_type}
        addq    $16, %rax

        decq    %rbx            # decrement counter
        jnz     .loop_begin{idx}    # jump to loop header if counter is not zero

    .loop_end{idx}:
"""

OPERATOR_INSTRUCTION = {
        '+': 'addps',
        '-': 'subps',
        '*': 'mulps',
        '/': 'divps',
        }

CONST = 0
VAR = 1

OPERAND_TYPE = {
        (CONST, 1): '',
        (CONST, 2): '',
        (VAR, 1): """\
        addq    $16, %r10       # increment operand 1 pointer by (4 x float)
""",
        (VAR, 2): """\
        addq    $16, %r11       # increment operand 2 pointer by (4 x float)
""",
        }



# NB: Each node must place its result in %rax during generate()

class ExprNode(object):
    def __init__(self, vplnode, consts, local_vars):
        self.loperand = Expr2Node(vplnode, consts, local_vars)
        if vplnode.type in (lex.PLUS, lex.MINUS):
            if vplnode.type == lex.PLUS:
                self.operator = '+'
            else:
                self.operator = '-'
            self.roperand = ExprNode(vplnode.children[1], consts, local_vars)
            self.type = VAR
        else:
            self.operator = self.roperand = None
            self.type = self.loperand.type

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

            yield ASSIGN_OPR.format(
                    idx='0',  # FIXME
                    operation=OPERATOR_INSTRUCTION[self.operator],
                    op1_type=OPERAND_TYPE[self.loperand.type, 1],
                    op2_type=OPERAND_TYPE[self.roperand.type, 2],
                    )

    def __repr__(self):
        if self.operator is None:
            return repr(self.loperand)
        return "({0} {1} {2})".format(
                self.operator,
                self.loperand,
                self.roperand,
                )

class Expr2Node(object):
    def __init__(self, vplnode, consts, local_vars):
        self.loperand = Expr3Node(vplnode, consts, local_vars)
        if vplnode.type in (lex.MULT, lex.DIVIDE):
            if vplnode.type == lex.MULT:
                self.operator = '*'
            else:
                self.operator = '/'
            self.roperand = Expr2Node(vplnode.children[1], consts, local_vars)
            self.type = VAR
        else:
            self.operator = self.roperand = None
            self.type = self.loperand.type

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

            yield ASSIGN_OPR.format(
                    idx='0',  # FIXME
                    operation=OPERATOR_INSTRUCTION[self.operator],
                    op1_type=OPERAND_TYPE[self.loperand.type, 1],
                    op2_type=OPERAND_TYPE[self.roperand.type, 2],
                    )

    def __repr__(self):
        if self.operator is None:
            return repr(self.loperand)
        return "({0} {1} {2})".format(
                self.operator,
                self.loperand,
                self.roperand,
                )

class Expr3Node(object):
    def __init__(self, vplnode, consts, local_vars):
        if vplnode.type == lex.EXPRMIN:
            self.me = MinNode(vplnode, consts, local_vars)
            self.type = VAR
        elif vplnode.type == lex.ID:
            self.me = local_vars[vplnode.text]
            self.type = VAR
        elif vplnode.type == lex.NUM:
            self.me = ConstNode(vplnode, consts)
            self.type = CONST
        else:
            self.me = ExprNode(vplnode.children[0], consts, local_vars)
            self.type = self.me.type

    def validate(self):
        pass

    def optimise(self):
        pass

    def generate(self):
        for line in self.me.generate():
            yield line

    def __repr__(self):
        return repr(self.me)
