import pdb
import sys

import antlr3

import a3tree
from build.VPLLexer import VPLLexer
from build.VPLParser import VPLParser

# hack to make print statements work more like expected
stdout = sys.stdout
sys.stdout = sys.stderr

if sys.argv[1] in ('-h', '--help'):
    print "usage: {0} [vpl-file]".format(sys.argv[0])

if len(sys.argv) > 1:
    source = open(sys.argv[1], 'rU')
else:
    source = sys.stdin

char_stream = antlr3.ANTLRInputStream(source)
lexer = VPLLexer(char_stream)
tokens = antlr3.CommonTokenStream(lexer)
parser = VPLParser(tokens)
root = parser.start()

print root.tree.toStringTree()

prog = a3tree.ProgramNode(root.tree)

print prog
###pdb.set_trace()
