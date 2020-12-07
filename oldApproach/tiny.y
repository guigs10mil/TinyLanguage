%{
  // Codigo baseado no site https://aquamentus.com/flex_bison.html. Acessado dia 25/10/2020.

  #include <cstdio>
  #include <iostream>
  using namespace std;

  // stuff from flex that bison needs to know about:
  extern int yylex();
  extern int yyparse();
  extern FILE *yyin;
  extern int line_num;
 
  void yyerror(const char *s);
%}

%error-verbose

%union {
  int ival;
  char *sval;
}

// define the constant-string tokens:
%token INT_TYPE BOOL_TYPE
%token IF ELSE
%token WHILE
%token PRINT
%token RETURN

%token OPEN_P CLOSE_P OPEN_B CLOSE_B COMMA EQUAL COLON SEMI_COLON

%token AND OR EQUALS PLUS MINUS TIMES DIVIDED GREATER LESS_THAN NOT

// define the "terminal symbol" token types I'm going to use (in CAPS
// by convention), and associate each with a field of the union:
%token <ival> INT
%token <sval> IDENTIFIER

%type <sval> type

%%
// the first rule defined is the highest-level rule, which in our
// case is just the concept of a whole "tiny file":
program:
  commands
  ;
commands:
  commands command
  | command
  ;
command:
  function                                              { cout << "Ran function" << endl; }
  | declaration                                         { cout << "Ran declaration" << endl; }
  ;
function:
  type IDENTIFIER OPEN_P arguments CLOSE_P block 
  | type IDENTIFIER OPEN_P CLOSE_P block
  ;
arguments:
  arguments COMMA argument
  | argument
  ;
argument:
  type identifier
  ;
type:
  INT_TYPE { cout << "Identifier type int" << endl; }
  | BOOL_TYPE { cout << "Identifier type bool" << endl; }
  ;
block:
  OPEN_B statments CLOSE_B
  ;
statments:
  statments statment
  | statment
  ;
statment:
  declaration
  | attribution
  | print
  | if
  | while
  | RETURN OPEN_P condition CLOSE_P SEMI_COLON { 
      cout << "returning " << endl;
    }
  ;
declaration:
  type IDENTIFIER SEMI_COLON  {
    cout << "declaring variable " << endl;
  }
  | type IDENTIFIER EQUAL expression SEMI_COLON {
    cout << "declaring variable " << endl;
  } 
  ;
attribution:
  IDENTIFIER EQUAL expression SEMI_COLON {
    cout << "variable attribution " << endl;
  }
  ;
print:
  PRINT OPEN_P expression CLOSE_P SEMI_COLON {
    cout << "Print" << endl;
  }
  ;
if:
  IF OPEN_P condition CLOSE_P block ELSE block
  | IF OPEN_P condition CLOSE_P block
  ;
while:
  WHILE OPEN_P condition CLOSE_P block {
    cout << "while" << endl;
  }
  ;
condition:
  condition and_or expression
  | condition comparative_operators expression
  | expression
  ;
expression:
  expression plus_minus term
  | term
  ;
term:
  term multiplication_division factor
  | factor
  ;
factor:
  INT
  | plus_minus factor
  | NOT factor
  | OPEN_P expression CLOSE_P
  | identifier
  ;
identifier:
  IDENTIFIER
  ;
plus_minus:
  PLUS
  | MINUS
  ;
multiplication_division:
  TIMES
  | DIVIDED
  ;
and_or:
  AND
  | OR
  ;
comparative_operators:
  EQUALS
  | GREATER
  | LESS_THAN
  ;
%%

int main(int, char**) {
  // open a file handle to a particular file:
  FILE *myfile = fopen("in.tiny", "r");
  // make sure it's valid:
  if (!myfile) {
    cout << "I can't open in.tiny!" << endl;
    return -1;
  }
  // set lex to read from it instead of defaulting to STDIN:
  yyin = myfile;

  // parse through the input until there is no more:
  do {
    yyparse();
  } while (!feof(yyin));
  cout << "FINISHED" << endl;
}

void yyerror(const char *s) {
  cout << "EEK, parse error on line " << line_num << "!  Message: " << s << endl;
  // might as well halt now:
  exit(-1);
}