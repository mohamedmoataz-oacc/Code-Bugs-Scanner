def checkReservedKeyword(word):
    keywords = (
        'False', 'def', 'if', 'raise', 'None', 'del', 'import', 'return', 'True', 'elif', 'async', 'await',
        'in', 'try', 'and', 'else', 'is', 'while', 'as', 'except', 'lambda', 'with', 'assert', 'finally',
        'nonlocal', 'yield', 'break', 'for', 'not', 'class', 'from', 'or', 'continue', 'global', 'pass'
    )
    if word in keywords: return True
    return False