from computer import Parser, Lexer

parser = Parser()
lexer = Lexer()

expressions = [
    ("1+(2+4)*5+5/6", 31.8333333333),
    ("10 + 9 / 2 + 3 * (2 + 8)", 44.5),
    ("3! + 2^2 * (7 + 3 / (3 + 4))", 35.7142857143),
    ("0.7 * 44 + 0.7 * 63 + 95", 169.9),
    ("100 ^ 0.5", 10),
    ("3!!", 720)
]

badExpressions = [
    "1 + 3 * (5",
    "1 ++ 5",
    "+"
]

for expression, value in expressions:
    tokens = lexer.getTokens(expression)
    evaluated = parser.parse(tokens).eval()
    print(evaluated, value)

for expression in badExpressions:
    try:
        print(expression)
        tokens = lexer.getTokens(expression)
        evaluated = parser.parse(tokens).eval()
        print("should have thrown an exception")
        exit(-1)
    except Exception as error:
        print(error)
