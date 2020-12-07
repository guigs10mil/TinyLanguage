from symboltable import SymbolTable

class Node:
    def __init__(self, value, children = None):
        self.value = value
        self.children = children

    def evaluate(self, table: SymbolTable) -> int:
        return 0

class BinOp(Node):
    def evaluate(self, table: SymbolTable):
        child0 = self.children[0].evaluate(table)
        child1 = self.children[1].evaluate(table)

        if (child0[0] == "String" or child1[0] == "String"):
            if self.value == "*":
                if child0[0] == "Bool":
                    return ("String", str(child0[1]).lower() + str(child1[1]))
                if child1[0] == "Bool":
                    return ("String", str(child0[1]) + str(child1[1]).lower())
                
                return ("String", str(child0[1]) + str(child1[1]))

            elif self.value == "==" and child0[0] == "String" and child1[0] == "String":
                return ("Bool", bool(child0[1] == child1[1]))

            else:
                raise ValueError("BinOp invalid string operation: " + str(child0[1]) + " " + self.value + " " + str(child1[1]))

        if self.value == "+":
            return ("Int", int(child0[1] + child1[1]))
        if self.value == "-":
            return ("Int", int(child0[1] - child1[1]))
        if self.value == "*":
            return ("Int", int(child0[1] * child1[1]))
        if self.value == "/":
            return ("Int", int(child0[1] / child1[1]))
        if self.value == "&&":
            return ("Bool", bool(child0[1] and child1[1]))
        if self.value == "||":
            return ("Bool", bool(child0[1] or child1[1]))
        if self.value == "==":
            return ("Bool", bool(child0[1] == child1[1]))
        if self.value == ">":
            return ("Bool", bool(child0[1] > child1[1]))
        if self.value == "<":
            return ("Bool", bool(child0[1] < child1[1]))

class UnOp(Node):
    def evaluate(self, table: SymbolTable):
        child0 = self.children[0].evaluate(table)

        if (child0[0] == "String"):
            raise ValueError("UnOp cannot work with strings: " + child0[1])

        if self.value == "+":
            return child0
        if self.value == "-":
            return ("Int", -child0[1])
        if self.value == "!":
            return ("Bool", bool(not child0[1]))

class Identifier(Node):
    def evaluate(self, table: SymbolTable):
        return table.getter(self.value)

class Assignment(Node):
    def evaluate(self, table: SymbolTable):
        table.setter(self.children[0].value, self.children[1].evaluate(table))
        
class Statment(Node):
    def evaluate(self, table: SymbolTable):
        for i in self.children:
            i.evaluate(table)
            if table.getter("return") != None:
                break

class Print(Node):
    def evaluate(self, table: SymbolTable):
        print(self.children[0].evaluate(table)[1])

class Readline(Node):
    def evaluate(self, table: SymbolTable):
        return ("Int", int(input()))

class While(Node):
    def evaluate(self, table: SymbolTable):
        condition = self.children[0].evaluate(table)
        if condition[0] != "Bool":
            raise ValueError("'While' cannot accept strings as conditions: " + condition[0])

        while self.children[0].evaluate(table)[1]:
            self.children[1].evaluate(table)

class If(Node):
    def evaluate(self, table: SymbolTable):
        condition = self.children[0].evaluate(table)
        if condition[0] == "String":
            raise ValueError("'If' cannot accept strings as conditions: " + condition[0])

        if condition[1]:
            return self.children[1].evaluate(table)
        else:
            if len(self.children) > 2:
                return self.children[2].evaluate(table)

class Else(Node):
    def evaluate(self, table: SymbolTable):
        return self.children[0].evaluate(table)

class FuncDec(Node):
    def __init__(self, value, returnType, children = None):
        self.value = value
        self.type = returnType
        self.children = children

    def evaluate(self, table: SymbolTable):
        if self.value.value in SymbolTable.functions:
            raise ValueError("The function " + self.value.value + " was already declared")
        SymbolTable.functions[self.value.value] = (self.type, self)

class FuncCall(Node):
    def evaluate(self, table: SymbolTable):
        if self.value not in SymbolTable.functions:
            raise ValueError("The function " + self.value + " wasn't declared")
        n, dec = SymbolTable.functions[self.value]
        st = SymbolTable()
        # st.table = table.table

        if len(self.children) + 1 != len(dec.children):
            raise ValueError("Not enough arguments in function call: " + self.value)

        for i in range(len(self.children)):
            c1 = self.children[i].evaluate(table)
            c2 = dec.children[i][1].evaluate(table)
            if c1[0] == c2[0]:
                st.setter(dec.children[i][0].value, c2)
                st.setter(dec.children[i][0].value, c1)
            else:
                raise ValueError("Function call '" + self.value + "' has the wrong type for argument " + str(i) + ": " + c1[0] + " != " + c2[0])

        dec.children[-1].evaluate(st)

        if st.getter("return") != None:
            ret = st.getter("return")
            if ret[0] == dec.returnType:
                return ret
            else:
                raise ValueError("Return type is not the same as the Declaration type: " + ret[0] + " != " + dec.returnType)

class Return(Node):
    def evaluate(self, table: SymbolTable):
        table.setter("return", self.children[0].evaluate(table))

class IntVal(Node):
    def evaluate(self, table: SymbolTable):
        return ("Int", self.value)

class BoolVal(Node):
    def evaluate(self, table: SymbolTable):
        return ("Bool", self.value)

class StrVal(Node):
    def evaluate(self, table: SymbolTable):
        return ("String", self.value)

class NoOp(Node):
    def evaluate(self, table: SymbolTable) -> int:
        return 0