grammar VPL;

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

start	:	m EOF;

m   :	f m
    |
    ;

f   : 	FUNC ID p d s END
    ;

p   :	LBRA l RBRA
    ;
    
l   :	ID
    |	ID COMMA l
    ;

d   :	VAR l SCOL
    |	
    ;

s   :	(ID EQUAL e) (SCOL s)*
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
    

ID  :	('a'..'z'|'A'..'Z'|'_') ('a'..'z'|'A'..'Z'|'0'..'9'|'_')*
    ;

NUM :	('0'..'9')+(\'.'('0'..'9')+)?
    ;