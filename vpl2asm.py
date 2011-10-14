import pdb
import sys
import antlr3
import a3tree
from build.VPLLexer import VPLLexer
from build.VPLParser import VPLParser

# hack to make print statements work more like expected
stdout = sys.stdout
sys.stdout = sys.stderr

if len(sys.argv) > 1:
    if sys.argv[1] in ('-h', '--help'):
        print "usage: {0} [vpl-file]".format(sys.argv[0])
        sys.exit(0)
    else:
        source = open(sys.argv[1], 'rU')
else:
    source = sys.stdin

char_stream = antlr3.ANTLRInputStream(source)
lexer = VPLLexer(char_stream)
tokens = antlr3.CommonTokenStream(lexer)
parser = VPLParser(tokens)
root = parser.start()

print root.tree.toStringTree()
print

if '<mismatched' in root.tree.toStringTree():
    raise RuntimeError("Probable syntax error: AST tree did not generate cleanly; check ANTLR.")

prog = a3tree.ProgramNode(root.tree)
print prog
print

for line in prog.generate():
    print>>stdout, line
print

#pdb.set_trace()
