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
    popq    %rbx            # restore reg %rbx
    leave                   # restore frame pointer
    ret                     # leave the function
"""

from a3tree.error import VPLParameterError
from a3tree.variable import VariableNode
from a3tree.statement import StatementNode
import build.VPLLexer as lex

class FunctionNode(object):
    """
    A function.
    
    Contains parameters, local variables, 'tmp' variables and statements.

    """
    def __init__(self, vplnode, consts):
        assert vplnode.type == lex.FUNCTION
        self.name = vplnode.children[0].text
        self.params = []
        self.local_vars = []
        self.named_vars = dict()
        self.tmp_vars = dict()
        used_names = set()

        if len(vplnode.children[1].children) > 5:
            raise VPLParameterError("VPL allows only 5 or fewer vector parameters.")

        # function parameters
        for i, param in enumerate(vplnode.children[1].children):
            if param.text in used_names:
                raise VPLParameterError("Declared parameters are not unique "
                                        "(duplicate '{0}').".format(param.text))
            used_names.add(param.text)

            self.named_vars[param.text] = VariableNode(param, param=i+1)
            self.params.append(self.named_vars[param.text])

        # local variables
        for var in vplnode.children[2].children:
            if var.text in used_names:
                raise VPLParameterError("Declared locals are not unique "
                                        "(duplicate '{0}').".format(var.text))
            used_names.add(var.text)

            self.named_vars[var.text] = VariableNode(var, idx=len(self.local_vars)+1)
            self.local_vars.append(self.named_vars[param.text])

        # statements, performin calculations
        self.statements = [StatementNode(s, consts, self.named_vars)
                for s in vplnode.children[3].children]

        # temporary '@tmp' variables
        # for holding intermidate results during calculations
        class DummyNode(object): pass
        num_tmp_vars = max(s.tmps_needed for s in self.statements)
        for i in xrange(num_tmp_vars):
            dummy = DummyNode()
            dummy.text = '@tmp_var_' + str(i)
            self.tmp_vars[i] = VariableNode(dummy, idx=self.num_locals+1)

    def validate(self):
        for statement in self.statements:
            statement.validate(self.named_vars, self.tmp_vars)

    @property
    def num_locals(self):
        """The number of variables on this function's stack."""
        return len(self.local_vars) + len(self.tmp_vars)

    def generate(self):
        # simply declare the function, allocate stack space for local and
        # 'tmp' varibles, output the statements in order and leave the func.
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
