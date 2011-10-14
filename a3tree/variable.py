from a3tree.error import VPLSyntaxError

import build.VPLLexer as lex

ARG_REGISTERS = ['%rdi', '%rsi', '%rdx', '%rcx', '%r8', '%r9']

LOAD_CONST = """
    # load constant '{value}'
    leaq    .const{idx}, {to}
"""

LOAD_REG = """
    # load function param '{name}'
    movq    {from_}, {to}
"""

LOAD_VAR = """
    # load variable: place address of var #{idx} ('{name}') into {to}
    movq    %rdi, {to}
    imulq   $4, {to}, {to}
    addq    $16, {to}
    imulq   ${idx}, {to}, {to}
    subq    %rbp, {to}
    negq    {to}
    andq    $-16, {to}
"""

class VariableNode(object):
    """
    A variable; may be named or a "tmp"; may be a parameter or a local.

    Has either a local stack index `idx` or a parameter index `param`.
    `param` may be from 1 to 5
    `idx` may be 1 or greater

    Will always have a `name` attribute, but this is only meaningful for
    local stack variable, not 'tmp' shadow variables.

    """
    def __init__(self, vplnode, idx=0, param=0):
        if not (idx or param) or (idx and param):
            raise ValueError("Must pass only one of idx or param.")
        assert param <= 5, "May only have 5 or fewer vector parameters."
        self.name = vplnode.text
        self.idx = idx
        self.param = param

    def validate(self, named_vars, tmp_vars):
        pass

    def generate(self, load_to=''):
        # load into a register
        if not load_to.startswith('%'):
            load_to = '%rax'

        if self.param:
            yield LOAD_REG.format(
                    from_=ARG_REGISTERS[self.param], to=load_to,
                    name=self.name)
        else:
            yield LOAD_VAR.format(
                    idx=self.idx, name=self.name, to=load_to)

    @property
    def type(self):
        if self.idx:
            return 'VAR'
        return 'PARAM'

    def __repr__(self):
        return "(VAR:{0})".format(
                self.name,
                )

class ConstNode(object):
    """A constant: nice and simple."""

    def __init__(self, vplnode, consts):
        self.value = int(vplnode.text)
        if self.value not in consts:
            consts[self.value] = len(consts)
        self.idx = consts[self.value]

    def validate(self, named_vars, tmp_vars):
        pass

    def generate(self, load_to=''):
        # load into a register
        if not load_to.startswith('%'):
            load_to = '%rax'  # src

        yield LOAD_CONST.format(idx=self.idx, to=load_to, value=self.value)

    def __repr__(self):
        return "(NUM:{0})".format(
                self.value,
                )
