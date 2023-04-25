# import code_refactor as cr
import cfg
import re
import errors
import checks

def find_unused_variables(graph: cfg.CFG):
    if not graph.constructed: return
    
    defs = dict()   # All definitions in the graph and if it was used or not
    current_defs = dict()   # All definitions until the line of code we reached
    stack = []
    current = graph.root
    visited_set_to = list(current.children.values())[0].visited     # To know if edge is visited

    stack.append(current)
    while len(stack) > 0:
        node: cfg.Node = stack.pop()

        # If in an iteration, we return to line that is before the line we were using in the last iteration
        # we delete all definitions after the current line from the current_defs dict.
        to_pop = [i for i, j in current_defs.items() if j > node.id]
        if to_pop:
            print('Popping:', to_pop)
        for i in to_pop:
            current_defs.pop(i)

        # Find defs
        if node.node_type == 'normal':
            x = node.code.split('=')
            if len(x) > 1:
                if x[1] != '' and x[0][-1] != '!':
                    # if line was (ex. counter += 1) or (ex. x //= 2)
                    if x[0][-1] in ['+', '-', '/', '*', '%', '^']:
                        x[0] = x[0][:-1]
                        if x[0][-1] in ['*', '/']: x[0] = x[0][:-1]
                    line_defs = x[0].split(',')     # In case (ex. x, y = 2, 3)
                    for i in line_defs:
                        if not checks.checkReservedKeyword(i.strip()):
                            if defs.get(i.strip()) is None: defs[i.strip()] = False
                            if current_defs.get(i.strip()) is None: current_defs[i.strip()] = node.id
                        else:
                            raise errors.InvalidUseOfReservedKeywordException(f"Cannot use {i.strip()} as a variable name.")
        
        # Find uses
        if node.node_type not in ['def', 'else'] and node.code not in ['Start', 'End']:
            code = node.code
            # Make sure we don't interpret a def as a use
            code_splitted = code.split('=')
            if len(code_splitted) > 1:
                if code_splitted[1] != '': code = '='.join(code_splitted[1:])

            # Use regular expressions to find all variables in the line
            used_variables = re.findall('[a-zA-Z_][a-zA-Z0-9_]*[^a-zA-Z0-9_(.]', code + ' ')
            for i in range(len(used_variables)):
                if i != 0:
                    # For cases like (ex. node.children) we only take node as the used variable
                    if used_variables[i-1] + used_variables[i] in code: continue
                used_variables[i] = used_variables[i][:-1]
                # Make sure that the variables we got are not python reserved keywords
                if not checks.checkReservedKeyword(used_variables[i]):
                    if current_defs.get(used_variables[i]) is None:
                        raise errors.NonDeclaredVariableException(
                            f'Variable "{used_variables[i]}" was used in "{node.code}" but may not be declared.')
                    else:
                        defs[used_variables[i]] = True

        for i in node.children.keys():
            if node.children[i].visited == visited_set_to:
                node.children[i].visited += 1
                node.children[i].visited %= 2
                stack.append(i)
    
    err = ''
    for i, j in defs.items():
        if not j:
            err += f'\n"{i}" was never used'
    if err:
        raise errors.DeclaredButNeverUsedException(err)
    return defs


def duplicate_finder(code='buggy.py'):
    with open(code, 'r') as code_file:
        code_lines = [line.strip().replace("'", '"') for line in code_file]
    code_lines_clone = code_lines[:]
    ignored_duplicates = ['else:', '"""', '']
    while True:
        duplicated = False
        for line in code_lines_clone:
            if line not in ignored_duplicates and code_lines_clone.count(line) > 2:
                duplicated = True
                indices = [index+1 for index in [i for i, x in enumerate(code_lines) if x == line]]
                print("code : ", line, 'duplicated at lines :  ',  end='')
                for index in indices:
                    print(index, ' ', end='')
                print()
                for i in range(code_lines_clone.count(line)):
                    code_lines_clone.remove(line)
                break
        if not duplicated:
            break



if __name__ == '__main__':
    # with open('buggy.py', 'r') as code_file:
    # code = cr.refactor_find_syntax_errors(code_file.read(), 4)
    duplicate_finder()

