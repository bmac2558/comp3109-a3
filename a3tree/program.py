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

    def __repr__(self):
        ret = "(PROGRAM "
        ret += ' '.join(repr(f) for f in self.functions)
        return ret + ')'
