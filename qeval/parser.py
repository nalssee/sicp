import re

__all__ = ["parse"]


def tokenize(expr):
    regex = re.compile("""(
    .|                        # dot
    \(|                       # left paren
    \)|                       # right paren
    [\w.?!+-></=*+]+|         # identifier
    ".*?"|                    # string
    )
    """, re.VERBOSE)
    return (x for x in re.findall(regex, expr) if x != '')


def parse(expr):
    reader = token_reader()
    reader.send(None)
    try:
        for token in tokenize(expr):
            reader.send(token)
    except StopIteration as e:
        return e.value


def token_reader():
    """Consume tokens to construct a lisp expression
    """
    token = yield
    if token == '(':
        p_expr = []
        while True:
            exp1 = yield from token_reader()
            if exp1 == ')':
                break
            p_expr.append(exp1)
        return p_expr
    # handle dot
    # I know this is incomplete, just don't be too smart
    elif token == ".":
        exp1 = yield from token_reader()
        return ['dot', exp1]
    return atom(token)


def atom(token):
    try:
        return int(token)
    except ValueError:
        try:
            return float(token)
        except ValueError:
            return token