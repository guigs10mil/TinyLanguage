from tokenizer import Tokenizer
import prepro
from node import *

class Parser:
    tokens: Tokenizer = None

    @staticmethod
    def parseBlock():
        res = Statment("Block", [])

        while (Parser.tokens.actual.type != "EOF"
                and Parser.tokens.actual.type != "ELSEIF"
                and Parser.tokens.actual.type != "ELSE"
                and Parser.tokens.actual.type != "END"):
            res.children.append(Parser.parseCommand())

        return res

    @staticmethod
    def parseProgram():
        res = Statment("Program", [])

        if (Parser.tokens.position == -1):
            Parser.tokens.selectNext()

        while (Parser.tokens.actual.type != "EOF"):
            if (Parser.tokens.actual.type == "FUNCTION"):
                Parser.tokens.selectNext()
                if (Parser.tokens.actual.type == "IDENT"):
                    identifier = Parser.tokens.actual
                    func = FuncDec(identifier, None, [])
                    Parser.tokens.selectNext()
                    if (Parser.tokens.actual.type == "POPEN"):
                        Parser.tokens.selectNext()

                        ## ARGUMENTOS
                        if (Parser.tokens.actual.type == "IDENT"):
                            identifier = Parser.tokens.actual
                            Parser.tokens.selectNext()
                            if (Parser.tokens.actual.type == "TYPEDEF"):
                                Parser.tokens.selectNext()
                            else:
                                raise ValueError("No TYPEDEF (::) found in function declaration. Found " + Parser.tokens.actual.type + " instead.")

                            if (Parser.tokens.actual.type == "TYPEINT"):
                                func.children.append((identifier, IntVal(None)))
                            elif (Parser.tokens.actual.type == "TYPEBOOL"):
                                func.children.append((identifier, BoolVal(None)))
                            elif (Parser.tokens.actual.type == "TYPESTRING"):
                                func.children.append((identifier, StrVal(None)))
                            else:
                                raise ValueError("No value type found in function declaration. Found " + Parser.tokens.actual.type + " instead.")
                            Parser.tokens.selectNext()

                            while (Parser.tokens.actual.type == "COMMA"):
                                Parser.tokens.selectNext()
                                
                                if (Parser.tokens.actual.type == "IDENT"):
                                    identifier = Parser.tokens.actual
                                    Parser.tokens.selectNext()
                                    if (Parser.tokens.actual.type == "TYPEDEF"):
                                        Parser.tokens.selectNext()
                                    else:
                                        raise ValueError("No TYPEDEF (::) found in function declaration. Found " + Parser.tokens.actual.type + " instead.")

                                    if (Parser.tokens.actual.type == "TYPEINT"):
                                        func.children.append((identifier, IntVal(None)))
                                    elif (Parser.tokens.actual.type == "TYPEBOOL"):
                                        func.children.append((identifier, BoolVal(None)))
                                    elif (Parser.tokens.actual.type == "TYPESTRING"):
                                        func.children.append((identifier, StrVal(None)))
                                    else:
                                        raise ValueError("No value type found in function declaration. Found " + Parser.tokens.actual.type + " instead.")
                                    Parser.tokens.selectNext()


                        if (Parser.tokens.actual.type == "PCLOSE"):
                            Parser.tokens.selectNext()
                            if (Parser.tokens.actual.type == "TYPEDEF"):
                                Parser.tokens.selectNext()
                            else:
                                raise ValueError("No TYPEDEF (::) found in function declaration. Found " + Parser.tokens.actual.type + " instead.")

                            if (Parser.tokens.actual.type == "TYPEINT"):
                                func.returnType = "Int"
                            elif (Parser.tokens.actual.type == "TYPEBOOL"):
                                func.returnType = "Bool"
                            elif (Parser.tokens.actual.type == "TYPESTRING"):
                                func.returnType = "String"
                            else:
                                raise ValueError("No value type found in function declaration. Found " + Parser.tokens.actual.type + " instead.")

                            Parser.tokens.selectNext()

                            if (Parser.tokens.actual.type == "LBREAK"):
                                Parser.tokens.selectNext()
                            else:
                                raise ValueError("No line break found in function declaration. Found " + Parser.tokens.actual.type + " instead.")

                            func.children.append(Parser.parseBlock())

                            if (Parser.tokens.actual.type == "END"):
                                Parser.tokens.selectNext()
                            else:
                                raise ValueError("No end of while found in function declaration. Found " + Parser.tokens.actual.type + " instead.")
                                
                            if (Parser.tokens.actual.type == "LBREAK"):
                                Parser.tokens.selectNext()
                                res.children.append(func)
                            else:
                                raise ValueError("No line break found in function declaration. Found " + Parser.tokens.actual.type + " instead.")
                            

                        else:
                            raise ValueError("Closing parenteses not found in function declaration. Found " + Parser.tokens.actual.type + " instead.")
                    
                    else:
                        raise ValueError("Invalid token in function declaration: " + Parser.tokens.actual.type)
                else:
                    raise ValueError("No identifier found in function declaration. Found " + Parser.tokens.actual.type + " instead.")
            else:
                res.children.append(Parser.parseCommand())

        return res

    @staticmethod
    def parseCommand():

        res = None

        if (Parser.tokens.actual.type == "IDENT"):
            identifier = Parser.tokens.actual
            Parser.tokens.selectNext()
            if (Parser.tokens.actual.type == "EQUAL"):
                Parser.tokens.selectNext()
                if (Parser.tokens.actual.type == "READLINE"):
                    Parser.tokens.selectNext()
                    if (Parser.tokens.actual.type == "POPEN"):
                        Parser.tokens.selectNext()
                        if (Parser.tokens.actual.type == "PCLOSE"):
                            Parser.tokens.selectNext()
                        else:
                            raise ValueError("Closing parenteses not found. Found " + Parser.tokens.actual.type + " instead.")
                    else:
                        raise ValueError("Opening parenteses not found. Found " + Parser.tokens.actual.type + " instead.")

                    res = Assignment("=", [identifier, Readline(None)])
                
                else:
                    res = Assignment("=", [identifier, Parser.parseRelExpression()])

            elif (Parser.tokens.actual.type == "POPEN"):
                res = FuncCall(identifier.value, [])
                Parser.tokens.selectNext()

                if (Parser.tokens.actual.type != "PCLOSE"):
                    res.children.append(Parser.parseRelExpression())

                    while (Parser.tokens.actual.type == "COMMA"):
                        Parser.tokens.selectNext()
                        res.children.append(Parser.parseRelExpression())

                if (Parser.tokens.actual.type == "PCLOSE"):
                    Parser.tokens.selectNext()
                else:
                    raise ValueError("Closing parenteses not found. Found " + Parser.tokens.actual.type + " instead.")
            
            else:
                raise ValueError("Invalid token after identifier: " + Parser.tokens.actual.type)

            if (Parser.tokens.actual.type == "LBREAK"):
                Parser.tokens.selectNext()
                return res
            else:
                raise ValueError("No line break found. Found " + Parser.tokens.actual.type + " instead.")

        elif (Parser.tokens.actual.type == "PRINT"):
            Parser.tokens.selectNext()
            if (Parser.tokens.actual.type == "POPEN"):
                Parser.tokens.selectNext()
                res = Print("println", [Parser.parseRelExpression()])
                if (Parser.tokens.actual.type == "PCLOSE"):
                    Parser.tokens.selectNext()
                else:
                    raise ValueError("Closing parenteses not found. Found " + Parser.tokens.actual.type + " instead.")
            
            else:
                raise ValueError("Invalid token in PRINT: " + Parser.tokens.actual.type)
                
            if (Parser.tokens.actual.type == "LBREAK"):
                Parser.tokens.selectNext()
                return res
            else:
                raise ValueError("No line break found. Found " + Parser.tokens.actual.type + " instead.")

        elif (Parser.tokens.actual.type == "WHILE"):
            Parser.tokens.selectNext()
            res = While("while", [Parser.parseRelExpression()])

            if (Parser.tokens.actual.type == "LBREAK"):
                Parser.tokens.selectNext()
            else:
                raise ValueError("No line break found after while. Found " + Parser.tokens.actual.type + " instead.")

            res.children.append(Parser.parseBlock())

            if (Parser.tokens.actual.type == "END"):
                Parser.tokens.selectNext()
            else:
                raise ValueError("No end of while found. Found " + Parser.tokens.actual.type + " instead.")
                
            if (Parser.tokens.actual.type == "LBREAK"):
                Parser.tokens.selectNext()
                return res
            else:
                raise ValueError("No line break found. Found " + Parser.tokens.actual.type + " instead.")
        
        elif (Parser.tokens.actual.type == "IF"):
            Parser.tokens.selectNext()
            res = If("if", [Parser.parseRelExpression()])

            previousIf = res

            if (Parser.tokens.actual.type == "LBREAK"):
                Parser.tokens.selectNext()
            else:
                raise ValueError("No line break found after if. Found " + Parser.tokens.actual.type + " instead.")

            res.children.append(Parser.parseBlock())

            while (Parser.tokens.actual.type == "ELSEIF"):
                Parser.tokens.selectNext()
                tmpIf = If("if", [Parser.parseRelExpression()])
                
                previousIf.children.append(tmpIf)
                previousIf = tmpIf

                if (Parser.tokens.actual.type == "LBREAK"):
                    Parser.tokens.selectNext()
                else:
                    raise ValueError("No line break found after elseif. Found " + Parser.tokens.actual.type + " instead.")

                previousIf.children.append(Parser.parseBlock())

            if (Parser.tokens.actual.type == "ELSE"):
                Parser.tokens.selectNext()
                if (Parser.tokens.actual.type == "LBREAK"):
                    Parser.tokens.selectNext()
                else:
                    raise ValueError("No line break found after else. Found " + Parser.tokens.actual.type + " instead.")

                previousIf.children.append(Parser.parseBlock())


            if (Parser.tokens.actual.type == "END"):
                Parser.tokens.selectNext()
            else:
                raise ValueError("No end of if found. Found " + Parser.tokens.actual.type + " instead.")
                
            if (Parser.tokens.actual.type == "LBREAK"):
                Parser.tokens.selectNext()
                return res
            else:
                raise ValueError("No line break found. Found " + Parser.tokens.actual.type + " instead.")

        elif (Parser.tokens.actual.type == "LOCAL"):
            Parser.tokens.selectNext()
            if (Parser.tokens.actual.type == "IDENT"):
                identifier = Parser.tokens.actual
                Parser.tokens.selectNext()
                if (Parser.tokens.actual.type == "TYPEDEF"):
                    Parser.tokens.selectNext()
                    if (Parser.tokens.actual.type == "TYPEINT"):
                        res = Assignment("=", [identifier, IntVal(None)])
                    elif (Parser.tokens.actual.type == "TYPEBOOL"):
                        res = Assignment("=", [identifier, BoolVal(None)])
                    elif (Parser.tokens.actual.type == "TYPESTRING"):
                        res = Assignment("=", [identifier, StrVal(None)])
                    else:
                        raise ValueError("No value type found. Found " + Parser.tokens.actual.type + " instead.")

                    Parser.tokens.selectNext()

                else:
                    raise ValueError("No TYPEDEF (::) found. Found " + Parser.tokens.actual.type + " instead.")
            else:
                raise ValueError("No identifier found. Found " + Parser.tokens.actual.type + " instead.")

            if (Parser.tokens.actual.type == "LBREAK"):
                Parser.tokens.selectNext()
                return res
            else:
                raise ValueError("No line break found. Found " + Parser.tokens.actual.type + " instead.")

        elif (Parser.tokens.actual.type == "RETURN"):
            Parser.tokens.selectNext()
            res = Return("return", [Parser.parseRelExpression()])

            if (Parser.tokens.actual.type == "LBREAK"):
                Parser.tokens.selectNext()
                return res
            else:
                raise ValueError("No line break found. Found " + Parser.tokens.actual.type + " instead.")

        elif (Parser.tokens.actual.type == "LBREAK"):
            Parser.tokens.selectNext()
            res = NoOp("NoOp")
            return res

        else:
            raise ValueError("Invalid token in parse command: " + Parser.tokens.actual.type)

        
    @staticmethod
    def parseRelExpression():
        # consome os tokens do Tokenizer e analisa se a sintaxe está aderente à gramática proposta. retorna o resultado da expressão analisada

        res = Parser.parseExpression()

        while Parser.tokens.actual.type == "EQUALS" or Parser.tokens.actual.type == "GREATER" or Parser.tokens.actual.type == "LESSTHAN":
            if (Parser.tokens.actual.type == "EQUALS"):
                Parser.tokens.selectNext()
                res = BinOp("==", [res, Parser.parseExpression()])

            elif (Parser.tokens.actual.type == "GREATER"):
                Parser.tokens.selectNext()
                res = BinOp(">", [res, Parser.parseExpression()])

            elif (Parser.tokens.actual.type == "LESSTHAN"):
                Parser.tokens.selectNext()
                res = BinOp("<", [res, Parser.parseExpression()])

        return res
    
    @staticmethod
    def parseExpression():
        # consome os tokens do Tokenizer e analisa se a sintaxe está aderente à gramática proposta. retorna o resultado da expressão analisada

        res = Parser.parseTerm()

        while Parser.tokens.actual.type == "PLUS" or Parser.tokens.actual.type == "MINUS" or Parser.tokens.actual.type == "OR":
            if (Parser.tokens.actual.type == "PLUS"):
                Parser.tokens.selectNext()
                res = BinOp("+", [res, Parser.parseTerm()])

            elif (Parser.tokens.actual.type == "MINUS"):
                Parser.tokens.selectNext()
                res = BinOp("-", [res, Parser.parseTerm()])

            elif (Parser.tokens.actual.type == "OR"):
                Parser.tokens.selectNext()
                res = BinOp("||", [res, Parser.parseTerm()])

        return res

    @staticmethod
    def parseTerm():
        # consome os tokens do Tokenizer e analisa se a sintaxe está aderente à gramática proposta. retorna o resultado da expressão analisada

        res = Parser.parseFactor()

        while Parser.tokens.actual.type == "MULTI" or Parser.tokens.actual.type == "DIV" or Parser.tokens.actual.type == "AND":
            if (Parser.tokens.actual.type == "MULTI"):
                Parser.tokens.selectNext()
                res = BinOp("*", [res, Parser.parseFactor()])

            elif (Parser.tokens.actual.type == "DIV"):
                Parser.tokens.selectNext()
                res = BinOp("/", [res, Parser.parseFactor()])

            elif (Parser.tokens.actual.type == "AND"):
                Parser.tokens.selectNext()
                res = BinOp("&&", [res, Parser.parseFactor()])

        return res

    @staticmethod
    def parseFactor():
        # consome os tokens do Tokenizer e analisa se a sintaxe está aderente à gramática proposta. retorna o resultado da expressão analisada

        res = None

        if (Parser.tokens.actual.type == "INT"):
            res = IntVal(int(Parser.tokens.actual.value))
            Parser.tokens.selectNext()

        elif (Parser.tokens.actual.type == "BOOL"):
            res = BoolVal(True if Parser.tokens.actual.value == "T" else False)
            Parser.tokens.selectNext()

        elif (Parser.tokens.actual.type == "STRING"):
            res = StrVal(Parser.tokens.actual.value)
            Parser.tokens.selectNext()

        elif (Parser.tokens.actual.type == "NOT"):
            Parser.tokens.selectNext()
            res = UnOp("!", [Parser.parseFactor()])

        elif (Parser.tokens.actual.type == "PLUS"):
            Parser.tokens.selectNext()
            res = UnOp("+", [Parser.parseFactor()])

        elif (Parser.tokens.actual.type == "MINUS"):
            Parser.tokens.selectNext()
            res = UnOp("-", [Parser.parseFactor()])

        elif (Parser.tokens.actual.type == "IDENT"):
            identifier = Parser.tokens.actual.value
            Parser.tokens.selectNext()

            if (Parser.tokens.actual.type == "POPEN"):
                res = FuncCall(identifier, [])
                Parser.tokens.selectNext()

                if (Parser.tokens.actual.type != "PCLOSE"):
                    res.children.append(Parser.parseRelExpression())

                    while (Parser.tokens.actual.type == "COMMA"):
                        Parser.tokens.selectNext()
                        res.children.append(Parser.parseRelExpression())

                if (Parser.tokens.actual.type == "PCLOSE"):
                    Parser.tokens.selectNext()
                else:
                    raise ValueError("Closing parenteses not found in function call")
            
            else:
                res = Identifier(identifier)

        elif (Parser.tokens.actual.type == "POPEN"):
            Parser.tokens.selectNext()
            res = Parser.parseRelExpression()
            if (Parser.tokens.actual.type == "PCLOSE"):
                Parser.tokens.selectNext()
            else:
                raise ValueError("Closing parenteses not found")
        
        else:
            raise ValueError("Invalid token in FACTOR: " + Parser.tokens.actual.type)

        return res

    @staticmethod
    def run(code):
        # recebe o código fonte como argumento, inicializa um objeto Tokenizador e retorna o resultado do parseExpression(). Esse método será chamado pelo main().

        Parser.tokens = Tokenizer(prepro.PrePro.filter(code))
        res = Parser.parseProgram()

        if (Parser.tokens.actual.type != "EOF"):
            raise ValueError("Finished parsing but EOF wasn't reached. Found " + Parser.tokens.actual.type + " instead.")

        table = SymbolTable()

        return res.evaluate(table)