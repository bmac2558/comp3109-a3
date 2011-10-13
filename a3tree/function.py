from a3tree.variable import VariableNode
from a3tree.statement import StatementNode

import build.VPLLexer as lex

FUNCTION_HEAD = """
.text
.global {name}
.type {name}, @function
.p2align 4,,15

{name}:
    # save current frame pointer onto the stack
    pushq   %rbp

    # set frame pointer
    movq    %rsp, %rbp

    # save callee-saved registers that are used on the stack
    # (potentially rbx and r12 - r15)
    pushq   %rbx
    pushq   %r12            # NB: not sure if this impacts location calculations
"""

LOCAL_MEMALLOC = """
    # allocate memory for local variables
    # allocate {num} local variables
    movq    %rdi, %rax      # NB: %rdi holds the first arg, ie. the size of the vectors
    imulq   $4, %rax, %rax
    addq    $16, %rax
    imulq   ${num}, %rax, %rax
    subq    %rax, %rsp
    andq    $-16, %rsp
"""

FUNCTION_FOOT = """
    # function epilog
    popq    %r12            # restore reg %r12
    popq    %rbx            # restore reg %rbx
    leave                   # restore frame pointer
    ret                     # leave the function
"""

from a3tree.variable import VariableNode
from a3tree.statement import StatementNode
import build.VPLLexer as lex

class FunctionNode(object):
    def __init__(self, vplnode, consts):
        assert vplnode.type == lex.FUNCTION
        self.name = vplnode.children[0].text
        self.num_locals = 0
        self.params = []
        self.variables = []
        self.local_vars = dict()
        self.tmp_vars = dict()

        for i, param in enumerate(vplnode.children[1].children):
            self.local_vars[param.text] = VariableNode(param, param=i+1)
            self.params.append(param)

        for var in vplnode.children[2].children:
            self.local_vars[var.text] = VariableNode(var, idx=self.num_locals+1)
            self.variables.append(var)
            self.num_locals += 1

        self.statements = [StatementNode(s, consts, self.local_vars)
                for s in vplnode.children[3].children]

        class DummyNode(object): pass
        num_tmp_vars = max(s.tmps_needed for s in self.statements)
        print "num_tmp_vars:", num_tmp_vars
        for i in xrange(num_tmp_vars):
            dummy = DummyNode()
            dummy.text = 'tmp_var_' + str(i)
            self.tmp_vars[i] = VariableNode(dummy, idx=self.num_locals+1)
            self.num_locals += 1

    def validate(self):
        for statement in self.statements:
            statement.validate(self.local_vars, self.tmp_vars)

    def optimise(self):
        pass

    def generate(self):
        yield FUNCTION_HEAD.format(name=self.name)
        if self.num_locals:
            yield LOCAL_MEMALLOC.format(num=self.num_locals)
        for statement in self.statements:
            for line in statement.generate():
                yield line
        yield FUNCTION_FOOT

    def __repr__(self):
        return "(FUNCTION:{0} (PARAMS {1}) (LOCALS {2}) (STATEMENTS {3}))".format(
                self.name,
                ' '.join(map(repr, self.params)),
                ' '.join(map(repr, self.local_vars)),
                ' '.join(map(repr, self.statements)),
                )
