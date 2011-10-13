#All local variables stored on the stack begin at where they are declared
#+1, the first item on the stack is an empty allocation of memory for
#intermediate calculations

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

#size = contents of address1
#size+3 & -4
#size*4
#(%register) is use the value register points at
#&register is use the value of the register

#adding to dem spaces allocted for variables
#for val in range(len(ast_node.children)-1):
#    print 'addq\t%rdi, %rax, %rax'
#    print 'movq\t$'  str(assigned_value) + ', (%rax)'

def calculations(output_reg, func_node):
    0 == 0

def evaluate(ast_node):
    print ast_node.toString()
    if ast_node.toString() == 'PROGRAM':
        evaluate(ast_node.children[0])
    elif ast_node.toString() == 'FUNCTION':
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
    elif ast_node.toString() == 'PARAMS':
        for node in ast_node.children:
            if node.toString() in parameters:
                #raise error and exit
                0 == 0
            else:
              parameters.append(str(node.toString()))
        return
    elif ast_node.toString() == 'LOCALS':
        for node in ast_node.children:
            if node.toString() in local_vars:
                #raise error and exit
                0 == 0
            else:
                local_vars.append(str(node.toString()))
        #assigning memory for local variables and intermediate
        #calculation storage.
        print 'movq\t%rdi, %rax'
        print 'imulq\t$4, %rax, %rax'
        print 'addq\t$16, %rax, %rax'
        print 'imulq\t$' + str(len(local_vars) + 1) + ', %rax, %rax'
        print 'subq\t%rax, %rsp'
        print 'andq\t%-16, %rsp'

        #assigning values to said assigned memory
        print 'movq\t%rsp, %rax'
        #for val in range(len(ast_node.children)-1):
        #    print 'addq\t%rdi, %rax, %rax'
        #    print 'movq\t$' + str(assigned_value) + ', (%rax)'
        return
    elif ast_node.toString() == 'STATEMENTS':
        for node in ast_node.children:
            evaluate(node)
    elif ast_node.toString() == 'ASSIGN':
        print ast_node.toStringTree()
        if ast_node.children[0].toString() in parameters:
            calculations(args_reg.get(parameters.index(ast_node.children[0].toString())+2), ast_node.children[1])
        elif ast_node.children[0].toString() in local_vars:
            0 == 0
        else:
            print 'welp you screwed up!'
    else:
        print 'This is a huge error, what the hell?!'

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

prog = a3tree.ProgramNode(root.tree)
print prog
print

for line in prog.generate():
    print line
print

evaluate(root.tree)

#pdb.set_trace()
