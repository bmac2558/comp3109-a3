from a3tree import FunctionNode, VPLSyntaxError

class ProgramNode(object):
    def __init__(self, vplprog):
        self.functions = []
        funcnames = set()

        for child in vplprog.children:
            func = FunctionNode(child)

            if func.name in funcnames:
                raise VPLSyntaxError("Duplicate function name '{0}'".format(func.name))

            funcnames.add(func.name)
            self.functions.append(func)

    def validate(self):
        # should this be in the constructor?
        for func in self.functions:
            func.validate()

    def generate(self):
        for func in self.functions:
            for line in func.generate():
                yield line

    def __repr__(self):
        return "(PROGRAM {0})".format(
                ' '.join(map(repr, self.functions)))
