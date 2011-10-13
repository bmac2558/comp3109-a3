from a3tree import FunctionNode, VPLSyntaxError

CONSTS_HEADER = """
.data
.align 16"""

CONST = """
.const{idx}
    .float {value}
    .float {value}
    .float {value}
    .float {value}
"""

class ProgramNode(object):
    def __init__(self, vplprog):
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
        # should this be in the constructor?
        for func in self.functions:
            func.validate()
        self.validated = True

    def generate(self):
        if not self.validated:
            self.validate()

        for func in self.functions:
            for line in func.generate():
                yield line
        if self.consts:
            yield CONSTS_HEADER
        for value, idx in self.consts.iteritems():
            yield CONST.format(idx=idx, value=value)

    def __repr__(self):
        return "(PROGRAM {0})".format(
                ' '.join(map(repr, self.functions)))
