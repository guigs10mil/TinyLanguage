/* A Bison parser, made by GNU Bison 2.3.  */

/* Skeleton interface for Bison's Yacc-like parsers in C

   Copyright (C) 1984, 1989, 1990, 2000, 2001, 2002, 2003, 2004, 2005, 2006
   Free Software Foundation, Inc.

   This program is free software; you can redistribute it and/or modify
   it under the terms of the GNU General Public License as published by
   the Free Software Foundation; either version 2, or (at your option)
   any later version.

   This program is distributed in the hope that it will be useful,
   but WITHOUT ANY WARRANTY; without even the implied warranty of
   MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
   GNU General Public License for more details.

   You should have received a copy of the GNU General Public License
   along with this program; if not, write to the Free Software
   Foundation, Inc., 51 Franklin Street, Fifth Floor,
   Boston, MA 02110-1301, USA.  */

/* As a special exception, you may create a larger work that contains
   part or all of the Bison parser skeleton and distribute that work
   under terms of your choice, so long as that work isn't itself a
   parser generator using the skeleton or a modified version thereof
   as a parser skeleton.  Alternatively, if you modify or redistribute
   the parser skeleton itself, you may (at your option) remove this
   special exception, which will cause the skeleton and the resulting
   Bison output files to be licensed under the GNU General Public
   License without this special exception.

   This special exception was added by the Free Software Foundation in
   version 2.2 of Bison.  */

/* Tokens.  */
#ifndef YYTOKENTYPE
# define YYTOKENTYPE
   /* Put the tokens into the symbol table, so that GDB and other debuggers
      know about them.  */
   enum yytokentype {
     INT_TYPE = 258,
     BOOL_TYPE = 259,
     IF = 260,
     ELSE = 261,
     WHILE = 262,
     PRINT = 263,
     RETURN = 264,
     OPEN_P = 265,
     CLOSE_P = 266,
     OPEN_B = 267,
     CLOSE_B = 268,
     COMMA = 269,
     EQUAL = 270,
     COLON = 271,
     SEMI_COLON = 272,
     AND = 273,
     OR = 274,
     EQUALS = 275,
     PLUS = 276,
     MINUS = 277,
     TIMES = 278,
     DIVIDED = 279,
     GREATER = 280,
     LESS_THAN = 281,
     NOT = 282,
     INT = 283,
     IDENTIFIER = 284
   };
#endif
/* Tokens.  */
#define INT_TYPE 258
#define BOOL_TYPE 259
#define IF 260
#define ELSE 261
#define WHILE 262
#define PRINT 263
#define RETURN 264
#define OPEN_P 265
#define CLOSE_P 266
#define OPEN_B 267
#define CLOSE_B 268
#define COMMA 269
#define EQUAL 270
#define COLON 271
#define SEMI_COLON 272
#define AND 273
#define OR 274
#define EQUALS 275
#define PLUS 276
#define MINUS 277
#define TIMES 278
#define DIVIDED 279
#define GREATER 280
#define LESS_THAN 281
#define NOT 282
#define INT 283
#define IDENTIFIER 284




#if ! defined YYSTYPE && ! defined YYSTYPE_IS_DECLARED
typedef union YYSTYPE
#line 17 "tiny.y"
{
  int ival;
  char *sval;
}
/* Line 1529 of yacc.c.  */
#line 112 "tiny.tab.h"
	YYSTYPE;
# define yystype YYSTYPE /* obsolescent; will be withdrawn */
# define YYSTYPE_IS_DECLARED 1
# define YYSTYPE_IS_TRIVIAL 1
#endif

extern YYSTYPE yylval;

