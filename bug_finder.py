# import code_refactor as cr
import cfg
import re
import errors


def find_unused_variables(graph: cfg.CFG):
    if not graph.constructed: return
    
    defs = dict()
    stack = []
    current = graph.root
    visited_set_to = list(current.children.values())[0].visited
    stack.append(current)
    while len(stack) > 0:
        node = stack.pop()
        print(node.code)

        # Find defs
        if node.node_type == 'normal':
            x = node.code.split('=')
            if len(x) > 1:
                if x[1] != '' and x[0][-1] != '!':
                    if x[0][-1] in ['+', '-', '/', '*', '%', '^']:
                        x[0] = x[0][:-1]
                        if x[0][-1] in ['*', '/']: x[0] = x[0][:-1]
                    line_defs = x[0].split(',')
                    dss = ''
                    for i in line_defs:
                        defs[i.strip()] = False
                        dss += i.strip() + ', '
                    # print(dss, end= ' | ')
        elif node.node_type == 'for':
            defs[node.code.split(' ')[1]] = False
        
        # Find uses
        if node.node_type not in ['def', 'else']:
            code = node.code
            code_splitted = code.split('=')
            if len(code_splitted) > 1:
                if code_splitted[1] != '': code = '='.join(code_splitted[1:])
            used_variables = re.findall('[a-zA-Z_][a-zA-Z0-9_]*[^a-zA-Z0-9_(.]', code)
            # print(used_variables, end=' | ')
            uss = ''
            for i in range(len(used_variables)):
                if i != 0:
                    if used_variables[i-1] + used_variables[i] in code: continue
                used_variables[i] = used_variables[i][:-1]
                if not checkReservedKeyword(used_variables[i]):
                    try:
                        defs[used_variables[i]] = True
                        uss += used_variables[i] + ', '
                    except KeyError:
                        raise errors.NonDeclaredVariableException(
                            f"Variable {used_variables[i]} was used in {node.code} but was not declared.")
            # print(uss)

        for i in node.children.keys():
            if node.children[i].visited == visited_set_to:
                node.children[i].visited += 1
                node.children[i].visited %= 2
                stack.append(i)
    return defs

def checkReservedKeyword(word):
    keywords = (
        'False', 'def', 'if', 'raise', 'None', 'del', 'import', 'return', 'True', 'elif',
        'in', 'try', 'and', 'else', 'is', 'while', 'as', 'except', 'lambda', 'with', 'assert', 'finally',
        'nonlocal', 'yield', 'break', 'for', 'not', 'class', 'from', 'or', 'continue', 'global', 'pass'
    )
    if word in keywords: return True
    return False

def duplicate_finder(code):
    code_lines = [line.replace(' ', '') for line in code[0].split('\n')]
    semi = code[1]

    itr = 1
    for line in code_lines:
        print(itr, line)
        itr += 1

    duplicated_lines = []

    while True:
        for i in range(len(code_lines)):
            if code_lines[i] != '':
                if code_lines.count(code_lines[i]) > 1:
                    indices = [i for i, x in enumerate(code_lines) if x == code_lines[i]]
                    print(i + 1, indices)

        break

    # for i in range(len(code_lines)):
    #     if code_lines[i] != '' and code_lines[i] != 'else':
    #         if code_lines.count(code_lines[i]) > 1:
    #             duplicated_indices = [i+1-semi]
    #             for j in range(i, len(code_lines)-1):
    #                 if code_lines[i] == code_lines[j+1]:
    #                     duplicated_indices.append(j+2-semi)
    #             duplicated_lines.append(duplicated_indices)
    # print(duplicated_lines)


# if __name__ == '__main__':
#     with open('buggy.py', 'r') as code_file:
#         # code = cr.refactor_find_syntax_errors(code_file.read(), 4)
#         duplicate_finder(code)
