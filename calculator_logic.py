def evaluate_expression(expr):
    try:
        result = eval(expr)
        return str(result)
    except Exception as e:
        return "Error"
