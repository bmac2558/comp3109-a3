from a3tree import FunctionNode, VPLSyntaxError

CONSTS_HEADER = """
.data
.align 16"""

CONST = """
.const{idx}:
    .float {value}
    .float {value}
    .float {value}
    .float {value}
"""

class ProgramNode(object):
    """Root node of an a3tree; models a full VPL program."""

    def __init__(self, vplprog):
        """Create a VPL a3tree from a VPL ANTLR AST root `vplprog`."""

        self.validated = False
        self.consts = dict()
        self.functions = []
        funcnames = set()

        for child in vplprog.children:
            func = FunctionNode(child, self.consts)

            if func.name in funcnames:
                raise VPLSyntaxError("Duplicate function name '{0}'".format(func.name))

            funcnames.add(func.name)
            self.functions.append(func)

    def validate(self):
        """Performs validation and set-up tasks needing a fully built tree."""
        # should this just be folded into the constructor for ProgramNode?
        for func in self.functions:
            func.validate()
        self.validated = True

    def generate(self):
        """Generator yielding lines of asm code."""

        if not self.validated:
            self.validate()

        # output all the functions
        for func in self.functions:
            for line in func.generate():
                yield line

        # then the footer with the constants
        if self.consts:
            yield CONSTS_HEADER
        for value, idx in self.consts.iteritems():
            yield CONST.format(idx=idx, value=value)

    def __repr__(self):
        return "(PROGRAM {0})".format(
                ' '.join(map(repr, self.functions)))
