import math

operators = ["+", "-", "*", "/", "!", "^", "="]
context = {}

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

class Variable(Expression):
    def __init__(self, name):
        self.name = name
        pass

    def __str__(self):
        return self.name + " " + str(self.value)

    def eval(self):
        return context[self.name]

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

class VariableToken:
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
                elif char.isalpha():
                    state = "variable"

            if state == "number":
                if char.isdigit() or char == ".":
                    currentToken.append(char)

                if not char.isdigit() and char != ".":
                    tokens.append(NumberToken(float(("".join(currentToken)))))
                    currentToken = []
                    state = None
                    i -= 1

            if state == "variable":
                if char.isalpha():
                    currentToken.append(char)

                if not char.isalpha():
                    tokens.append(VariableToken(("".join(currentToken))))
                    currentToken = []
                    state = None
                    i -= 1

            i += 1

        if len(currentToken):
            if state == "number":
                tokens.append(NumberToken(float("".join(currentToken))))
            elif state == "variable":
                tokens.append(VariableToken("".join(currentToken)))

        # handling negative numbers
        processedTokens = []
        i = 0
        while i < len(tokens):
            token = tokens[i]
            if type(token) == OperatorToken and token.op == "-" and i < len(tokens) - 1 and type(tokens[i + 1]) == NumberToken and (i == 0 or type(tokens[i - 1]) == OpeningToken):
                tokens[i + 1].value *= -1
                processedTokens.append(tokens[i + 1])
                i += 1
            else:
                processedTokens.append(token)

            i += 1

        return processedTokens

class Parser:
    def __init__(self):
        pass

    def process(self, expression, operators, adder):
        i = 0
        out = []

        while i < len(expression):
            token = expression[i]

            if type(token) == OperatorToken and token.op in operators:
                prev = out.pop()
                nextExpression = None
                if i + 1 < len(expression):
                    nextExpression = expression[i + 1]
                newItem = adder(token.op, prev, nextExpression)
                out.append(newItem)
                if newItem.op != "!":
                    i += 1
            else:
                out.append(token)

            i += 1

        return out

    def parse(self, expression):
        out = []
        i = 0

        # handling single number
        if len(expression) == 1 and type(expression[0]) == NumberToken:
            return NumberLiteral(expression[0].value)

        # =
        if len(expression) > 2 and type(expression[0]) == VariableToken and expression[1].op == "=":
            context[expression[0].value] = self.parse(expression[2:])
            return context[expression[0].value]

        # parentheses
        while i < len(expression):
            token = expression[i]

            if type(token) == OpeningToken:
                closingTokenIndex = next((len(expression) - 1- i for i, e in enumerate(reversed(expression)) if type(e) == ClosingToken), None)
                out.append(self.parse(expression[i + 1: closingTokenIndex]))
                i = closingTokenIndex
            else:
                out.append(token)

            i += 1

        expression = out.copy()
        out = []

        # transforming tokens to literals
        for token in expression:
            if type(token) == NumberToken:
                out.append(NumberLiteral(token.value))
            elif type(token) == VariableToken:
                if token.value not in context:
                    raise Exception("undeclared variable")
                out.append(NumberLiteral(context[token.value].eval()))
            else:
                out.append(token)

        # updating the list
        expression = out.copy()

        # !
        expression = self.process(expression, ["!"], lambda op, x, y: Operation(op, [x, y]))

        # ^ 
        expression = self.process(expression, ["^"], lambda op, x, y: Operation(op, [x, y]))

        # *, /
        expression = self.process(expression, ["*", "/"], lambda op, x, y: Operation(op, [x, y]))

        # +, -
        expression = self.process(expression, ["+", "-"], lambda op, x, y: Operation(op, [x, y]))

        if len(expression) > 1:
            raise Exception("invalid exception")

        return expression[0]
