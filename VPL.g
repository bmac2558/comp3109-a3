grammar VPL;

options {language=Python;}

tokens {
    FUNC = 'func';
    END = 'end';
    LBRA = '(';
    RBRA = ')';
    COMMA = ',';
    VAR = 'var';
    SCOL = ';';
    COL = ':';
    EQUAL = '=';
    PLUS = '+';
    MINUS = '-';
    MULT = '*';
    DIVIDE = '/';
    MIN = 'min';
}

@members {
    funcnames = set()
    memory = dict()
}

start	:	m EOF;

m   :	f m
    {
        print """
        .text
        .global {0}
        .type {0}, @function
        .p2align 4,,15

        {0}:
            # save current frame pointer onto the stack
            pushq   \%rbp

            # set frame pointer
            movq    \%rsp, \%rbp

            # save callee-saved registers that are used on the stack
            # (potentially rbp, rbx and r12 - r15)
            pushq   \%rbx

            # allocate memory for local variables
            # allocate {1} local variables
            movq    \%rdi, \%rax    # NB: \%rdi holds the first arg, ie. the number of vectors
            imulq   $4, \%rax, \%rax
            addq    $16, \%rax
            imulq   ${1}, \%rax, \%rax
            subq    \%rax, \%rsp
            andq    $-16, \%rsp

            # function body

            # function epilog
            popq    \%rbx    # restore reg \%rbx
            leave           # restore frame pointer
            ret             # leave the function
        """.format($f.name, $f.num_vars)
    }
    |
    ;

f returns [name, num_vars] :
        FUNC ID p d s END
        {
        if $ID.text in self.funcnames:
            raise NameError("Duplicate function name '{0}'!".format($ID.text))
        self.funcnames.add($ID.text)
        $name = $ID.text
        $num_vars = 1
        }
    ;

p   :	LBRA l RBRA
    ;

l   :	ID
    |	ID COMMA l
    ;

d   :	VAR l SCOL
    |
    ;

s   :	ID EQUAL e (SCOL s)?
    |
    ;

e   :	e2 (PLUS e | MINUS e)?
    ;

e2  :	e3 (MULT e2 | DIVIDE e2)?
    ;

e3  :	MIN LBRA e COMMA e RBRA
    |	LBRA e RBRA
    |	ID
    |	NUM
    ;


ID  :	    ('a'..'z'|'A'..'Z'|'_') ('a'..'z'|'A'..'Z'|'0'..'9'|'_')* ;

NUM :	    ('0'..'9')+ ('.'('0'..'9')+)? ;

WS  :       ( ' ' | '\t' | '\n' | '\r' | '\u000C' )+ { $channel = HIDDEN; } ;
