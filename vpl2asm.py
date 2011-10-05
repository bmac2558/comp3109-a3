#!/usr/bin/env python
import sys
import antlr3
from build.VPLLexer import VPLLexer
from build.VPLParser import VPLParser

char_stream = antlr3.ANTLRInputStream(sys.stdin)
lexer = VPLLexer(char_stream)
tokens = antlr3.CommonTokenStream(lexer)
parser = VPLParser(tokens)
root = parser.start()

print>>sys.stderr, root.tree.toStringTree()
