from computer import Parser, Lexer
import math

parser = Parser()
lexer = Lexer()

expressions = [
    ("a = 3", 3),
    ("b = 10", 10),
    ("1+(2+4)*5+5/6", 31.8333333333),
    ("10 + 9 / 2 + 3 * (2 + 8)", 44.5),
    ("a! + 2^2 * (7 + 3 / (-3 + 4))", 46),
    ("0.7 * 44 + 0.7 * 63 + 95", 169.9),
    ("100 ^ 0.5", 10),
    ("3!!", 720),
    ("a * b", 30),
    ("30 - b", 20),
    ("b^a", 1000),
    ("a", 3),
    ("a = b", 10),
    ("a", 10),
    ("-5", -5),
    ("-2*(-5)", 10),
    ("-2*(-5) - 6", 4),
    ("3*(-5 + 7)", 6)
]

badExpressions = [
    "1 + 3 * (5",
    "1 ++ 5",
    "+",
    "3 = 5"
]

for expression, expected in expressions:
    try:
        tokens = lexer.getTokens(expression)
        evaluated = parser.parse(tokens).eval()
        close = math.isclose(evaluated, expected)
        if not close:
            print(expression, "evaluation incorrect, expected: ", expected, " got: ", evaluated)
            exit(-1)
    except Exception as e:
        print(expression)
        raise e

for expression in badExpressions:
    try:
        tokens = lexer.getTokens(expression)
        evaluated = parser.parse(tokens).eval()
        print(expression, " should have thrown an exception")
        exit(-1)
    except Exception as error:
        pass

while True:
    expression = input(">>>")

    if expression == "exit":
        break
    else:
        tokens = lexer.getTokens(expression)
        evaluated = parser.parse(tokens).eval()
        print(evaluated)
