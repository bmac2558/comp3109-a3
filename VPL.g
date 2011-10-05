grammar VPL;

options {
    language=Python;
    output=AST;
}

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

    PROGRAM;
    FUNCTION;
    PARAMS;
    LOCALS;
    STATEMENTS;
    ASSIGN;
    EXPRMIN;
    SUBEXPR;
}

start :	f* EOF
        -> ^(PROGRAM f*)
    ;

f   :
        FUNC
        ID
        p
        d
        ss
        END
        -> ^(FUNCTION ID p d ss)
    ;

p   :	LBRA l RBRA
        -> ^(PARAMS l*)
    ;

l   :	ID (COMMA! ID)*
    ;

d   :	(VAR l SCOL)*
        -> ^(LOCALS l*)
    ;

ss  :   (s (SCOL s)* )?
        -> ^(STATEMENTS s*)
    ;

s   :	ID EQUAL e*
        -> ^(ASSIGN ID e*)
    ;

plus_or_minus : PLUS | MINUS ;
e   :	e2 (plus_or_minus^ e)?
    ;

mult_or_div : MULT | DIVIDE ;
e2  :	e3 (mult_or_div^ e2)?
    ;

e3  :	MIN LBRA e COMMA e RBRA
        -> ^(EXPRMIN e*)
    |	LBRA e RBRA
        -> ^(SUBEXPR e)
    |	ID
    |	NUM
    ;


ID  :	    ('a'..'z'|'A'..'Z'|'_') ('a'..'z'|'A'..'Z'|'0'..'9'|'_')* ;

NUM :	    ('0'..'9')+ ('.'('0'..'9')+)? ;

WS  :       ( ' ' | '\t' | '\n' | '\r' | '\u000C' )+ { $channel = HIDDEN; } ;
