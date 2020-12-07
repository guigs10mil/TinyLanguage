class SymbolTable:
    functions = {}

    def __init__(self):
        self.table = {"return": None}

    def getter(self, key):
        if key in self.table:
            return self.table[key]
        else:
            raise ValueError("Getter did not find the given variable: " + key)

    def setter(self, key, value):
        if key == "return":
            self.table[key] = value
            return
        if key in SymbolTable.functions:
            raise ValueError("Variable already declared as a function")
        if value[1] == None:
            self.table[key] = value
            return
        if key in self.table:
            if value[0] != self.table[key][0]:
                raise ValueError("Variable type does not match the Symbol Table: " + value[0] + " != " + self.table[key][0])
            self.table[key] = value
        else:
            raise ValueError("Variable " + key + " of type " + value[0] + " was not declared")