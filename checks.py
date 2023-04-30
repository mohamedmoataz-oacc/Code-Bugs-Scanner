def checkReservedKeyword(word):
    keywords = (
        'False', 'def', 'if', 'raise', 'None', 'del', 'import', 'return', 'True', 'elif', 'async', 'await',
        'in', 'try', 'and', 'else', 'is', 'while', 'as', 'except', 'lambda', 'with', 'assert', 'finally',
        'nonlocal', 'yield', 'break', 'for', 'not', 'class', 'from', 'or', 'continue', 'global', 'pass'
    )
    if word in keywords: return True
    return False

def checkBuiltInFunction(name):
    funcs = ["abs", "aiter", "all", "any", "anext", "ascii", "bin", "bool", "breakpoint", "bytearray",
            "bytes", "callable", "chr", "classmethod", "compile", "complex", "delattr", "dict", "dir",
            "divmod", "enumerate", "eval", "exec", "filter", "float", "format", "frozenset", "getattr",
            "globals", "hasattr", "hash", "help", "hex", "id", "input", "int", "isinstance", "issubclass",
            "iter", "len", "list", "locals", "map", "max", "memoryview", "min", "next", "object", "oct",
            "open", "ord", "pow", "print", "property", "range",  "repr", "reversed", "round", "set", "zip",
            "setattr", "slice", "sorted", "staticmethod", "str", "sum", "super", "tuple", "type", "vars",
    ]
    if name in funcs: return True
    else: return False

def checkUnwantedLine(line):
        if len(line.strip()) == 0: return True # If the line was empty
        # If line is a string that is not used.
        elif ((line.strip().startswith("'") and line.strip().endswith("'")) or 
                (line.strip().startswith('"') and line.strip().endswith('"'))): return True
        else: return False