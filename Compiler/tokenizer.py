from tokenMaker import Token

class Tokenizer:
    def __init__(self, origin):
        self.origin = origin
        self.position = -1
        self.actual = None
        self.operators = ["+", "-", "*", "/", "(", ")", ">", "<", "!"]
        self.operatorTypes = ["PLUS", "MINUS", "MULTI", "DIV", "POPEN", "PCLOSE", "GREATER", "LESSTHAN", "NOT"]
        self.names = ["p", "w", "i", "ei", "e", "rl", "ed", "T", "F", "l", "I", "B", "S", "f", "r"]
        self.namesTypes = ["PRINT", "WHILE", "IF", "ELSEIF", "ELSE", "READLINE", "END", "BOOL", "BOOL", "LOCAL", "TYPEINT", "TYPEBOOL", "TYPESTRING", "FUNCTION", "RETURN"]
    
    def selectNext(self):
        # lê o próximo token e atualiza o atributo atual

        if (self.position) + 1 >= len(self.origin):
            self.actual = Token("EOF", "")
            return

        self.position += 1
        tk = self.origin[self.position]

        while tk == " ":
            if (self.position) + 1 >= len(self.origin):
                self.actual = Token("EOF", "")
                return
            self.position += 1
            tk = self.origin[self.position]

        if (tk in self.operators):
            self.actual = Token(
                self.operatorTypes[self.operators.index(tk)],
                tk)
            return

        elif (tk == "="):
            if (self.origin[self.position + 1] == "="):
                self.actual = Token("EQUALS", "==")
                self.position += 1
            else:
                self.actual = Token("EQUAL", tk)
            return

        elif (tk == "|"):
            if (self.origin[self.position + 1] == "|"):
                self.actual = Token("OR", "||")
                self.position += 1
            else:
                raise ValueError("Invalid OR token")
            return

        elif (tk == "&"):
            if (self.origin[self.position + 1] == "&"):
                self.actual = Token("AND", "&&")
                self.position += 1
            else:
                raise ValueError("Invalid AND token")
            return

        elif (tk == ":"):
            self.actual = Token("TYPEDEF", tk)
            return
        
        elif (tk == ","):
            self.actual = Token("COMMA", tk)
            return

        elif (tk == "\n"):
            self.actual = Token("LBREAK", tk)
            return

        elif (tk == "\""):
            tk = ""
            while (len(self.origin) > self.position + 1 and self.origin[self.position + 1] != "\""):
                tk += self.origin[self.position + 1]
                self.position += 1

            if (self.origin[self.position + 1] == "\""):
                self.position += 1
                self.actual = Token("STRING", tk)
            else:
                raise ValueError("Invalid STRING token: closing quotes not found.")
            return

        elif (tk.isnumeric()):
            while (len(self.origin) > self.position + 1 and self.origin[self.position + 1].isnumeric()):
                tk += self.origin[self.position + 1]
                self.position += 1

            self.actual = Token("INT", tk)
            return

        elif (tk.isalpha()):
            while (len(self.origin) > self.position + 1 and (self.origin[self.position + 1].isnumeric() or self.origin[self.position + 1].isalpha() or self.origin[self.position + 1] == "_")):
                tk += self.origin[self.position + 1]
                self.position += 1

            if (tk not in self.names):
                self.actual = Token("IDENT", tk)
                return

            i = self.names.index(tk)
            self.actual = Token(self.namesTypes[i], tk)
            return
            

        
        else:
            raise ValueError("Invalid token")

