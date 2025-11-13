

def t_norms(norm_type):
    if norm_type == "min":
        def t_norm(a, b):
            return min(a, b)
    elif norm_type == "prod":
        def t_norm(a, b):
            return a * b
    elif norm_type == "lukasiewicz":
        def t_norm(a, b):
            return max(0, a + b - 1)
    elif norm_type == "drastic":
        def t_norm(a, b):
            if a == 1:
                return b
            elif b == 1:
                return a
            else:
                return 0
    else:
        raise ValueError(f"Unknown t-norm type: {norm_type}")