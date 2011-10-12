FUNCTION_HEAD = """
.text
.global {0}
.type {0}, @function
.p2align 4,,15

{0}:
    # save current frame pointer onto the stack
    pushq   %rbp

    # set frame pointer
    movq    %rsp, %rbp

    # save callee-saved registers that are used on the stack
    # (potentially rbp, rbx and r12 - r15)
    pushq   %rbx
"""

LOCAL_MEMALLOC = """
    # allocate memory for local variables
    # allocate {0} local variables
    movq    %rdi, %rax    # NB: %rdi holds the first arg, ie. the number of vectors
    imulq   $4, %rax, %rax
    addq    $16, %rax
    imulq   ${0}, %rax, %rax
    subq    %rax, %rsp
    andq    $-16, %rsp
"""

FUNCTION_FOOT = """
    # function epilog
    popq    %rbx    # restore reg %rbx
    leave           # restore frame pointer
    ret             # leave the function
"""

from a3tree.variable import VariableNode
from a3tree.statement import StatementNode
import build.VPLLexer as lex

class FunctionNode(object):
    def __init__(self, vplnode):
        assert vplnode.type == lex.FUNCTION
        self.name = vplnode.children[0].text
        self.params = [VariableNode(p) for p in vplnode.children[1].children]
        self.localvars = [VariableNode(v) for v in vplnode.children[2].children]
        self.statements = [StatementNode(s) for s in vplnode.children[3].children]

    def validate(self):
        pass

    def optimise(self):
        pass

    def generate(self):
        yield FUNCTION_HEAD.format(self.name)
        yield LOCAL_MEMALLOC.format(len(self.localvars))
        for statement in self.statements:
            for line in statement,generate():
                yield line
        yield FUNCTION_FOOT

    def __repr__(self):
        return "(FUNCTION:{0} (PARAMS {1}) (LOCALS {2}) (STATEMENTS {3}))".format(
                self.name,
                ' '.join(map(repr, self.params)),
                ' '.join(map(repr, self.localvars)),
                ' '.join(map(repr, self.statements)),
                )
