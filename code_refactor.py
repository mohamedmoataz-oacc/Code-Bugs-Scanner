import time
def refactor_find_syntax_errors(code, indentation):
    stack = []
    braces, matches = ['(', '{', '['], [')', '}', ']']
    new_code = ''
    code_without_strings = ''
    current_line = 1
    in_string = False
    comment = False
    string_info = [None, None] # [type (' or "), start_line]
    indents = 0         # How much indentation is at the start of this line
    last = False        # If the last character was a line break or not. A space doesn't count
    semicolon_num = 0   # ex. "\n    foo", if the pointer is at f, then last will still be True

    print('Refactoring code...')
    time.sleep(1)
    print('Checking for syntax errors (opened brackets, non-closed strings)')
    time.sleep(2)
    for i in range(len(code)):  # iterates over every character in code
        if not in_string and code[i] == '#':  # Determines if this line is a comment  
            comment = True
        
        if not comment:
            if code[i-1] == '\n':
                last = True
                indents = 0
            if last and code[i] == ' ': indents += 1
            elif last and code[i] != ' ': last = False

            if code[i] == '"' or code[i] == "'":    # If we are inside a string
                if string_info[0] is None:  # If we are starting a string
                    in_string = True
                    if code[i-1] == code[i] and code[i-2] == code[i]:   # For triple quotes strings
                        string_info[0] = code[i] * 3
                    else: string_info[0] = code[i]
                    string_info[1] = current_line
                else:   # If we are ending a string
                    if code[i] == string_info[0][0] and (len(string_info[0]) == 1 or
                        (len(string_info[0]) == 3 and code[i-1] == code[i] and code[i-2] == code[i])):
                        in_string = False
                        string_info[0], string_info[1] = None, None

            if i == len(code) - 1 and in_string:
                raise SyntaxError(f"String opened in line {string_info[1]} was not closed.")
            elif code[i] == '\n' and in_string and len(string_info[0]) == 1:
                raise SyntaxError(f"String opened in line {string_info[1]} was not closed.")

            if code[i] in braces and not in_string:     # When a bracket is opened
                stack.append((code[i], current_line))
            elif code[i] in matches and not in_string:  # When a closing bracket is found
                match = stack.pop()
                if matches.index(code[i]) != braces.index(match[0]):
                    raise SyntaxError(f"Line {match[1]}: '{match[0]}' was closed using a false bracket '{code[i]}'.")
            if i == len(code) - 1 and len(stack) > 0:
                # If we reach end of code and there are brackets that are still opened
                err = ''
                for bracket in stack:
                    err += f"\nLine {bracket[1]}: '{bracket[0]}' has no matching bracket."
                raise SyntaxError(err)

            # Replace any semicolon that is not in a string with a new line
            if code[i] == ';' and not in_string:
                new_code += '\n'
                code_without_strings += '\n'
                semicolon_num += 1
            elif code[i] == '\n' and ((in_string and len(string_info[0]) == 3) or len(stack) > 0):
                new_code += ' '
            elif (code[i] != '\n' and code[i] != '"' and code[i] != "'" and code[i-1] == ':' and code[i] not in matches 
                  and not in_string and len(stack) == 0):
                # Used in cases when there is no line break after if statement.
                # ex. if x > 3: print("foo bar")
                # But not in cases like ex. fromto[0:9]
                new_code += '\n'
                code_without_strings += '\n'
                new_code += ' ' * (indents + indentation)
                code_without_strings += ' ' * (indents + indentation)
                if code[i] != ' ':
                    new_code += code[i]
                    code_without_strings += code[i]
            else:
                new_code += code[i]
                if not in_string or code[i] == string_info[0][0]: code_without_strings += code[i]

        if comment and code[i] == '\n': # Detects when a comment ends
            comment = False
            new_code += '\n'
            code_without_strings += '\n'
        
        if code[i] == '\n': current_line += 1
    # print(i == len(code) - 1, stack)
    return [new_code, semicolon_num, code_without_strings]
