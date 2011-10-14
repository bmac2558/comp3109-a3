import string
import sys

f = open('stackbomb.vpl', 'w')
f.write('func stackbomb(a)\nvar ')
alphabet = string.lowercase
for a in alphabet:
    if a == 'f':
        f.write('zzzz;\n')
        f.write('    _cad = 40;\n')
        f.write('    a = a + _cad\n')
        f.write('end')
        break
    for b in alphabet:
        if b == 'o':
            break
        for c in alphabet:
            if c == 'e':
                break
            f.write('_' + a + b + c + ',\n')
