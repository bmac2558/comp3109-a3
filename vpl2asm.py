#All local variables stored on the stack begin at where they are declared
#+1, the first item on the stack is an empty allocation of memory for
#intermediate calculations

import pdb
import sys
import antlr3
import a3tree
from build.VPLLexer import VPLLexer
from build.VPLParser import VPLParser

args_reg = {1:'%rdi', 2:'%rsi', 3:'%rdx', 4:'%rcx', 5:'%r8', 6:'%r9'}
parameters = []
local_vars = []
inter_vars = [1]
constants = []
temp_use = []
operators = {'+':'add', '-':'sub', '*':'mul', '/':'div', 'EXPRMIN':'min'}


def compile(node):
    if node.toString() in parameters:
        print '\tmovq\t' + args_reg[parameters.index(node.toString()) + 1] + ', %rax'
        print '#move %r10 to first unused temp variable'
        print '\taddq\t%rdi, %r10'
        print '\timulq\t$4, %r10, %r10'
        print '\taddq\t$16, %r10'
        print '\timulq\t$' + str(len(local_vars) + temp_use.index(False) + 1) + ', %r10, %r10'
        print '\tsubq\t%rbp, %r10'
        print '\tnegq\t%r10'
        print '\tandq\t$-16, %r10'
        print '\tmovq\t$rdi, $rdx'
        print '\tshrl\t$2, %rbx'
        print '\tjz\t.loop_end<var>'
        temp_use[temp_use.index(False)] = True
    elif node.toString() in local_vars:
        print '#move %rax to local_var'
        print '\taddq\t%rdi, %rax'
        print '\timulq\t$4, %rax, %rax'
        print '\taddq\t$16, %rax'
        print '\timulq\t$' + str(local_vars.index(node.toString()) + 1) + ', %rax, %rax'
        print '\tsubq\t%rbp, %rax'
        print '\tnegq\t%rax'
        print '\tandq\t$-16, %rax'
        print '#move %r10 to first unused temp variable'
        print '\taddq\t%rdi, %r10'
        print '\timulq\t$4, %r10, %r10'
        print '\taddq\t$16, %r10'
        print '\timulq\t$' + str(len(local_vars) + temp_use.index(False) + 1) + ', %r10, %r10'
        print '\tsubq\t%rbp, %r10'
        print '\tnegq\t%r10'
        print '\tandq\t$-16, %r10'
        print '\tmovq\t$rdi, $rdx'
        print '\tshrl\t$2, %rbx'
        print '\tjz\t.loop_end<var>'
        temp_use[temp_use.index(False)] = True
    elif node.toString() in ['+', '-', '*', '/', 'EXPRMIN']:
        compile(node.children[0])
        compile(node.children[1])
        print '#move %rax to local_var'
        print '\taddq\t%rdi, %rax'
        print '\timulq\t$4, %rax, %rax'
        print '\taddq\t$16, %rax'
        if False in temp_use:
            print '\timulq\t$' + str(len(local_vars) + temp_use.index(False) + 1) + ', %rax, %rax'
            temp_use[temp_use.index(False)-1] = False
        else:
            print '\timulq\t$' + str(len(local_vars) + len(temp_use)) + ', %rax, %rax'
            temp_use[-1] = False
        print '\tsubq\t%rbp, %rax'
        print '\tnegq\t%rax'
        print '\tandq\t$-16, %rax'
        print '#move %r10 to first unused temp variable'
        print '\taddq\t%rdi, %r10'
        print '\timulq\t$4, %r10, %r10'
        print '\taddq\t$16, %r10'
        print '\timulq\t$' + str(len(local_vars) + temp_use.index(False) + 1) + ', %r10, %r10'
        print '\tsubq\t%rbp, %r10'
        print '\tnegq\t%r10'
        print '\tandq\t$-16, %r10'
        print '\tmovq\t%r10, %r11'
        print '\tmovq\t$rdi, $rdx'
        print '\tshrl\t$2, %rbx'
        print '\tjz\t.loop_end<' + operators[node.toString()] + '>'
    else:
        print '\tleaq\t.const<' + node.toString() + '>, %rax'
        print '\tmove %r10 to first available temp'
        print '\taddq\t%rdi, %r10'
        print '\timulq\t$4, %r10, %r10'
        print '\taddq\t$16, %r10'        
        print '\timulq\t$' + str(len(local_vars) + temp_use.index(False) + 1) + ', %r10, %r10'
        print '\tsubq\t%rbp, %r10'
        print '\tnegq\t%r10'
        print '\tandq\t$-16, %r10'
        print '\tmovq\t$rdi, $rdx'
        print '\tshrl\t$2, %rbx'
        print '\tjz\t.loop_end<const>'
        temp_use[temp_use.index(False)] = True
        if node.toString() not in constants:
            constants.append(node.toString())

def local_var_to_register(n, destreg):
    print '\tmovq\t%rdi, ' + destreg
    print '\timulq\t$4, ' + destreg + ', ' + destreg
    print '\taddq\t$16, ' + destreg
    print '\timulq\t$' + str(n) + ', ' + destreg + ', ' + destreg
    print '\tsubq\t%rbp, ' + destreg
    print '\tnegq\t' + destreg
    print '\tandq\t$-16, ' + destreg

def create_const(x):
    print '.data'
    print '.align 16'
    print '.const<' + x + '>:'
    print '\t.float <' + x + '>'
    print '\t.float <' + x + '>'
    print '\t.float <' + x + '>'
    print '\t.float <' + x + '>'
    print

def print_loops():
    print '.loop_begin<const>:'
    print
    print '\tmovaps\t(%rax), %xmm0'
    print '\tmovaps\t%xmm0, (%r10)'
    print '\taddq\t$16, %r10'
    print '\tdecq\t%rbx'
    print '\tjnz\t.loop_begin'
    print
    print '.loop_end<const>'
    print
    print '.loop_begin<var>:'
    print
    print '\tmovaps\t(%rax), %xmm0'
    print '\tmovaps\t%xmm0, (%r10)'
    print '\taddq\t$16, %rax'
    print '\taddq\t$16, %r10'
    print '\tdecq\t%rbx'
    print '\tjnz\t.loop_begin'
    print
    print '.loop_end<var>'
    for j in ['addps', 'subps', 'divps', 'mulps', 'minps']:
        print
        print '.loop_begin<' + j[:3] + '>:'
        print
        print '\tmovaps\t(%rax), %xmm0'
        print '\tmovaps\t(%r10), %xmm1'
        print '\t' + j + '\t%xmm0, %xmm1'
        print '\tmovaps\t%xmm1, (%r11)'
        print '\taddq\t$16, %rax'
        print '\taddq\t$16, %r10'
        print '\taddq\t$16, %r11'
        print '\tdecq\t%rbx'
        print '\tjnz\t.loopbegin<' + j[:3] +  '>'
        print
        print '.loopend<' + j[:3] + '>'

def search(op_set, root):
    if root.toString() in op_set:
        return True
    elif len(root.children) == 0:
        return False
    else:
        return ((search(op_set, root.children[0]) or (search(op_set, root.children[1]))))

def count_ops(set1, set2, root):
    var1 = False
    var2 = False
    if root.toString() in set1:
        var1 = search(set2, root.children[0])
        var2 = search(set2, root.children[1])
    elif root.toString() in set2:
        var1 = search(set1, root.children[0])
        var2 = search(set1, root.children[1])
    if var1 and var2:
        return 1 + count_ops(set1, set2, root.children[0]) + count_ops(set1, set2, root.children[1])
    elif (var1 == True) and (var2 == False):
        return count_ops(set1,set2, root.children[0])
    elif (var1 == False) and (var2 == True):
        return count_ops(set1, set2, root.children[1])
    else:
        return 0

def add_inter_vars(root):
    set1 = ['EXPRMIN', '+', '-']
    set2 = ['EXPRMIN', '*', '/']
    return max(count_ops(set1, set2, root), 1)

def evaluate(ast_node):
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
        print '\tpushq\t%rbp'
        print '\tmovq\t%rsp, %rbp'
        print '\tpushq\t%rbx'
        for node in ast_node.children[1:]:
            evaluate(node)
        print '\tpopq\t%rbx'
        print '\tleave'
        print '\tret'
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
        print '#assigning memory for local variables'
        print '\tmovq\t%rdi, %rax'
        print '\timulq\t$4, %rax, %rax'
        print '\taddq\t$16, %rax, %rax'
        print '\timulq\t$' + str(len(local_vars)) + ', %rax, %rax'
        print '\tsubq\t%rax, %rsp'
        print '\tandq\t%-16, %rsp'
        return
    elif ast_node.toString() == 'STATEMENTS': 
        for node in ast_node.children: 
            a = add_inter_vars(node.children[1])
            if a + 1 > inter_vars[0]:
                inter_vars[0] = a + 5     
        print '#creating space for temporaries'
        print '\tmovq\t%rdi, %rax'
        print '\timulq\t$' + str(inter_vars[0]) + ', %rax'
        print '\tsubq\t%rax, %rsp'
        for k in range(inter_vars[0]):
            temp_use.append(False)
        for j in ast_node.children:
            evaluate(j)
    elif ast_node.toString() == 'ASSIGN':
        compile(ast_node.children[1])
        if ast_node.children[0].toString() in parameters:
            print '\tmovq\t' + args_reg[parameters.index(ast_node.children[0].toString()) + 1] + ', %r10'
            print '#move %rax to last used temp variable'
            print '\taddq\t%rax, %rax'
            print '\timulq\t$4, %rax, %rax'
            print '\taddq\t$16, %rax'
            print '\timulq\t$' + str(len(local_vars) + temp_use.index(False)) + ', %rax, %rax'
            print '\tsubq\t%rbp, %rax'
            print '\tnegq\t%rax'
            print '\tandq\t$-16, %rax'
            print '\tmovq\t$rdi, $rdx'
            print '\tshrl\t$2, %rbx'
            print '\tjz\t.loop_end<var>'
            temp_use[temp_use.index(True)] = False
        if ast_node.children[0].toString() in local_vars:
            print '#move %r10 to local_var'
            print 'addq\t%rdi, %r10'
            print 'imulq\t$4, %r10, %r10'
            print 'addq\t$16, %r10'
            print 'imulq\t$' + str(local_vars.index(ast_node.children[0].toString()) + 1) + ', %rax, %rax'
            print 'subq\t%rbp, %r10'
            print 'negq\t%r10'
            print 'andq\t$-16, %r10'
            print '#move %rax to last used temp variable'
            print 'addq\t%rdi, %rax'
            print 'imulq\t$4, %rax, %rax'
            print 'addq\t$16, %rax'
            print 'imulq\t$' + str(len(local_vars) + temp_use.index(False)) + ', %r10, %r10'
            print 'subq\t%rbp, %rax'
            print 'negq\t%rax'
            print 'andq\t$-16, %rax'
            print 'movq\t$rdi, $rdx'
            print 'shrl\t$2, %rbx'
            print 'jz\t.loop_end<var>'
            temp_use[temp_use.index(False)] = True
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

prog = a3tree.ProgramNode(root.tree)
evaluate(root.tree)
print
for const in constants:
    print create_const(const)
print_loops()

#pdb.set_trace()
sys.exit(0)
