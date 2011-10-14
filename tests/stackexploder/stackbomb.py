import sys
file = './stackbomb.vpl'
f = open(file, 'w')
alphabet = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z']
f.write('func stackbomb(a)\n')
for a in alphabet:
    if a == 'f':
        f.write('a == aaa\n')
        f.write('end')
        break
    for b in alphabet:
        if b == 'o':
            break
        for c in alphabet:
            if c == 'e':
                break
            f.write('var ' + a + b + c +';\n')
