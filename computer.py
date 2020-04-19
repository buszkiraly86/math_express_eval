import math
import time

operators = ["+", "-", "*", "/", "!", "^"]

class Expression:
    def __init__(self, parsed):
        pass

    def eval(self):
        return self.value

class NumberLiteral(Expression):
    def __init__(self, value):
        self.value = value
        pass

    def __str__(self):
        return str(self.value)

class Operation(Expression):
    def __init__(self, op, operands = []):
        self.op = op
        self.operands = operands
        self.value = None
        pass

    def __str__(self):
        return self.op

    def eval(self):
        if self.value:
            return self.value

        if self.op == "+":
            self.value = self.operands[0].eval() + self.operands[1].eval()
        elif self.op == "-":
            self.value = self.operands[0].eval() - self.operands[1].eval()
        elif self.op == "*":
            self.value = self.operands[0].eval() * self.operands[1].eval()
        elif self.op == "/":
            self.value = self.operands[0].eval() / self.operands[1].eval()
        elif self.op == "!":
            self.value = math.factorial(self.operands[0].eval())
        elif self.op == "^":
            self.value = self.operands[0].eval() ** self.operands[1].eval()

        return self.value

class NumberToken:
    def __init__(self, value):
        self.value = value

class OperatorToken:
    def __init__(self, op):
        self.op = op

class OpeningToken:
    def __init__(self):
        pass

class ClosingToken:
    def __init__(self):
        pass

class Lexer:
    def __init__(self):
        pass

    def getTokens(self, expression):
        expression = expression.replace(" " , "") 
        tokens = []
        currentToken = [] 
        state = None

        i = 0

        while i < len(expression):
            char = expression[i]

            if not state:
                if char.isdigit() or char == ".":
                    state = "number"
                elif char == "(":
                    tokens.append(OpeningToken())
                elif char == ")":
                    tokens.append(ClosingToken())
                elif char in operators:
                    tokens.append(OperatorToken(expression[i]))
                else:
                    raise Exception("syntax error: " + char + " at " + str(i))
            
            if state == "number":
                if char.isdigit() or char == ".":
                    currentToken.append(char)

                if not char.isdigit() and char != ".":
                    tokens.append(NumberToken(float(("".join(currentToken)))))
                    currentToken = []
                    state = None
                    i -= 1

            i += 1

        if len(currentToken):
            if state == "number":
                tokens.append(NumberToken(float("".join(currentToken))))

        return tokens

class Parser:
    def __init__(self):
        pass

    def parse(self, expression):
        out = []
        i = 0

        if len(expression) == 1 and type(expression[0]) == NumberToken:
            return NumberLiteral(expression[0].value)

        # parentheses
        while i < len(expression):
            token = expression[i]

            if type(token) == OpeningToken:
                closingTokenIndex = i + 1
                level = 1
                for j in range(i + 1, len(expression)):
                    if type(expression[j]) == OpeningToken:
                        level += 1
                    if type(expression[j]) == ClosingToken:
                        level -= 1

                        if not level:
                            closingTokenIndex = j
                            break

                out.append(self.parse(expression[i + 1: closingTokenIndex]))
                i = closingTokenIndex
            elif type(token) == NumberToken:
                out.append(NumberLiteral(token.value))
            elif type(token) == OperatorToken:
                out.append(token)

            i += 1

        # updating the list
        expression = out.copy()
        out = []

        # !
        opFound = True
        while opFound and len(expression):
            i = 0
            opFound = False
            while i < len(expression):
                token = expression[i]

                if not opFound and type(token) == OperatorToken and token.op in ["!"]:
                    out.pop()
                    out.append(Operation(token.op, [expression[i - 1]]))
                    opFound = True
                else:
                    out.append(token)

                i += 1

            expression = out.copy()
            out = []

        # ^ 
        opFound = True
        while opFound and len(expression):
            i = 0
            opFound = False
            while i < len(expression):
                token = expression[i]

                if not opFound and type(token) == OperatorToken and token.op in ["^"]:
                    out.pop()
                    out.append(Operation(token.op, [expression[i - 1], expression[i + 1]]))
                    opFound = True
                    i += 1
                else:
                    out.append(token)

                i += 1

            expression = out.copy()
            out = []

        # *, /
        opFound = True
        while opFound and len(expression):
            i = 0
            opFound = False
            while i < len(expression):
                token = expression[i]

                if not opFound and type(token) == OperatorToken and token.op in ["*", "/"]:
                    out.pop()
                    out.append(Operation(token.op, [expression[i - 1], expression[i + 1]]))
                    opFound = True
                    i += 1
                else:
                    out.append(token)

                i += 1

            expression = out.copy()
            out = []

        opFound = True
        while opFound and len(expression):
            i = 0
            opFound = False
            while i < len(expression):
                token = expression[i]

                if not opFound and type(token) == OperatorToken and token.op in ["+", "-"]:
                    out.pop()
                    out.append(Operation(token.op, [expression[i - 1], expression[i + 1]]))
                    opFound = True
                    i += 1
                else:
                    out.append(token)

                i += 1

            expression = out.copy()
            out = []

        return expression[0]

#expression = "1+(2+4)*5+5/6"
#expression = "10 + 9 / 2 + 3 * (2 + 8)"
#expression = "3 + 2 * (7 + 3 / (3 + 4))"
#expression = "0.7 * 44 + 0.7 * 63 + 95"
expression = "100 ^ 0.5"

parser = Parser()
lexer = Lexer()
tokens = lexer.getTokens(expression)
print(parser.parse(tokens).eval())
#exp = Expression(expression)
#parsed = parser.parse(expression)
#print(parsed)
#exp = Expression(parsed)
#print(exp.eval())
