%{
  #include "tiny.tab.h"
  int line_num = 1;
%}
%option noyywrap
%%
"int"             { return INT_TYPE; }
"bool"            { return BOOL_TYPE; }
"if"              { return IF; }
"else"            { return ELSE; }
"print"           { return PRINT; }
"while"           { return WHILE; }
"return"          { return RETURN; }
"("               { return OPEN_P; }
")"               { return CLOSE_P; }
"{"								{ return OPEN_B; }
"}"			  				{ return CLOSE_B; }
","               { return COMMA; }
"="               { return EQUAL; }
":"               { return COLON; }
";"               { return SEMI_COLON; }
"&&"              { return AND; }
"=="              { return EQUALS; }
"||"              { return OR; }
"+"               { return PLUS; }
"-"               { return MINUS; }
"*"               { return TIMES; }
"/"               { return DIVIDED; }
">"               { return GREATER; }
"<"               { return LESS_THAN; }
"!"               { return NOT; }
[0-9]+            { yylval.ival = atoi(yytext); return INT; }
[a-zA-Z][_a-zA-Z0-9]*      {
  yylval.sval = strdup(yytext);
  return IDENTIFIER;
}
[ \t\r\v\f]       ;
\n                { ++line_num; }
.                 ;
%%