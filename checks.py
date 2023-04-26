def checkReservedKeyword(word):
    keywords = (
        'False', 'def', 'if', 'raise', 'None', 'del', 'import', 'return', 'True', 'elif', 'async', 'await',
        'in', 'try', 'and', 'else', 'is', 'while', 'as', 'except', 'lambda', 'with', 'assert', 'finally',
        'nonlocal', 'yield', 'break', 'for', 'not', 'class', 'from', 'or', 'continue', 'global', 'pass'
    )
    if word in keywords: return True
    return False

def checkUnwantedLine(line):
        if len(line.strip()) == 0: return True # If the line was empty
        # If line is a string that is not used.
        elif ((line.strip().startswith("'") and line.strip().endswith("'")) or 
                (line.strip().startswith('"') and line.strip().endswith('"'))): return True
        else: return False