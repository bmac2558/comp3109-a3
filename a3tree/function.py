FUNCTION_HEAD = """
.text
.global {0}
.type {0}, @function
.p2align 4,,15

{0}:
    # save current frame pointer onto the stack
    pushq   \%rbp

    # set frame pointer
    movq    \%rsp, \%rbp

    # save callee-saved registers that are used on the stack
    # (potentially rbp, rbx and r12 - r15)
    pushq   \%rbx
"""

LOCAL_MEMALLOC = """
    # allocate memory for local variables
    # allocate {1} local variables
    movq    \%rdi, \%rax    # NB: \%rdi holds the first arg, ie. the number of vectors
    imulq   $4, \%rax, \%rax
    addq    $16, \%rax
    imulq   ${1}, \%rax, \%rax
    subq    \%rax, \%rsp
    andq    $-16, \%rsp
"""

FUNCTION_FOOT = """
    # function epilog
    popq    \%rbx    # restore reg \%rbx
    leave           # restore frame pointer
    ret             # leave the function
"""

class FunctionNode(object):
    def __init__(self, vplnode):
        self.name = vplnode.children[0].text
        self.params = []
        self.localvars = []
        self.statements = []

    def validate(self):
        pass

    def optimise(self):
        pass

    def generate(self):
        pass

    def __repr__(self):
        return "(FUNCTION:{0} ...)".format(self.name)
