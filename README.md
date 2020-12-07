# TinyLanguage
A language for those who have no time to waste. Only short names allowed.

Tiny Language is a compact variation of Julia, where all reserved names are compressed to one or two characters.

![DiagramaSintatico](https://github.com/guigs10mil/TinyLanguage/blob/master/DiagramaSintatico.png?raw=true)

### EBNF
PROGRAM = { COMMAND | FUNCTION } ;

BLOCK = { COMMAND } ;

COMMAND = ( ASSIGNMENT | PRINT | WHILE | IF | LOCAL | RETURN | FUNCALL ), "\n" | "\n" ;

FUNCTION = "f", IDENTIFIER, "(", [ IDENTIFIER, ":", "TYPE", { ",", IDENTIFIER, ":", "TYPE" } ], ")", ":", TYPE, "\n", BLOCK, "ed" ;

LOCAL = "l", IDENTIFIER, ":", "TYPE" ;

ASSIGNMENT = IDENTIFIER, "=", ( REL_EXPRESSION | "readline", "(", ")" ) ;

PRINT = "p", "(", REL_EXPRESSION, ")" ;

WHILE = "w", REL_EXPRESSION, "\n", BLOCK, "ed" ;

IF = "i", REL_EXPRESSION, "\n", BLOCK, { ELSEIF }, [ ELSE ], "ed" ;

ELSEIF = "ei", REL_EXPRESSION, "\n", BLOCK ;

ELSE = "e", "\n", BLOCK ;

RETURN = "r", REL_EXPRESSION ;

REL_EXPRESSION = EXPRESSION, { ( "==" | ">" | "<" ), EXPRESION } ;

EXPRESSION = TERM, { ( "+" | "-" | "||" ), TERM } ;

TERM = FACTOR, { ( "*" | "/" | "&&" ), FACTOR } ;

FACTOR = NUMBER | BOOLEAN | STRING | ( ( "+" | "-" | "!" ), FACTOR ) | ( "(", REL_EXPRESSION, ")" ) | IDENTIFIER | FUNCALL ;

FUNCALL = IDENTIFIER, "(", [ REL_EXPRESSION, { ",", REL_EXPRESSION } ] , ")" ;

TYPE = "I", "B", "S" ;

BOOLEAN = "T" | "F" ;

STRING = "'", {.*?}, "'" ;

IDENTIFIER = CHARACTER, { CHARACTER | DIGIT | "_" } ;

CHARACTER = "a" | ... | "z" | "A" | ... | "Z" ;

NUMBER = DIGIT, { DIGIT } ;

DIGIT = "0" | "1" | ... | "9" ;
