def t_norms(norm_type):
    if norm_type == "min":
        return lambda a, b: min(a, b)
    elif norm_type == "prod":
        return lambda a, b: a * b
    elif norm_type == "lukasiewicz":
        return lambda a, b: max(0, a + b - 1)
    elif norm_type == "drastic":
        return lambda a, b: b if a == 1 else a if b == 1 else 0
    else:
        raise ValueError(f"Unknown t-norm type: {norm_type}")
