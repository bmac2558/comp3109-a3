import build.VPLLexer as lex

def get_varnode(vplnode):
    if vplnode.type == lex.NUM:
        return NumNode(vplnode)
    else:
        return VariableNode(vplnode)

class VariableNode(object):
    def __init__(self, vplnode):
        self.name = vplnode.text

    def validate(self):
        pass

    def optimise(self):
        pass

    def generate(self):
        yield self.name

    def __repr__(self):
        return "(VAR:{0})".format(
                self.name,
                )

class NumNode(object):
    def __init__(self, vplnode):
        self.value = int(vplnode.text)

    def validate(self):
        pass

    def optimise(self):
        pass

    def generate(self):
        yield self.name

    def __repr__(self):
        return "(NUM:{0})".format(
                self.value,
                )
