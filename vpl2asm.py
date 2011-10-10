import pdb
import sys
import antlr3
import a3tree
import re
from build.VPLLexer import VPLLexer
from build.VPLParser import VPLParser

args_reg = {1:'%rdi', 2:'%rsi', 3:'%rdx', 4:'%rcx', 5:'%r8', 6:'%r9'}
parameters = []
local_vars = []
id_reg_ex = re.compile('([a-zA-Z_])([a-zA-Z0-9_])*')
num_reg_ex = re.compile('([0-9])+ (.([0-9])+)?')

def evaluate(ast_node):
    if ast_node.toString() == 'PROGRAM':
        evaluate(ast_node.children[0])
    if ast_node.toString() == 'FUNCTION':
        name = ast_node.children[0].toString()
        print '.text'
        print '.global ' +  name
        print '.type ' + name + ', @function'
        print '.p2align 4,,15'
        print
        print name + ':'
        print 'pushq\t%rbp'
        print 'movq\t%rsp, %rbp'
        print 'pushq\t%rbx'
        for node in ast_node.children:
            evaluate(node)
        print 'popq\t%rbx'
        print 'leave'
        print 'ret'
    if ast_node.toString() == 'PARAMS':
        for node in ast_node.children:
            if node.toString() in parameters:
                #raise error and exit
                0 == 0
            else:
                parameters.append(node.toString)
        return
    if ast_node.toString() == 'LOCALS':
        for node in ast_node.children:
            if node.toString() in local_vars:
                #raise error and exit
                0 == 0
            else:
                local_vars.append(node.toString)
        print 'movq\t%rdi, %rax'
        print 'imulq\t$4, %rax, %rax'
        print 'addq\t$16, %rax, %rax'
        print 'imulq\t$' + str(len(local_vars)) + ', %rax, %rax'
        print 'subq\t%rax, %rsp'
        print 'andq\t%-16, %rsp'
        return
    if ast_node.toString() == 'STATEMENTS':
        #Do This
        0 == 0
    if ast_node.toString() == 'ASSIGN':
        #Do This
        0 == 0
    if ast_node.toString() == 'EXPRMIN':
        #Do This
        0 == 0
    poss_id = id_reg_ex.match(ast_node.toString())
    """if poss_id.group() == ast_node.toString():
        if ast_node.toString() in parameters:"""

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

prog = a3tree.ProgramNode(root.tree)
evaluate(root.tree)

#pdb.set_trace()
sys.exit(0)
