import cfg
import re
import errors
import checks

def find_bugs(graph: cfg.CFG, graph_with_strings: cfg.CFG, *declared):
    """
    Can currently find defined but unused variables, variables that are used but not defined, invalid use
    of python reserved keywords and unreachable code after (break, continue and return statements).
    """
    if not graph.constructed and not graph_with_strings.constructed: return
    
    defs = dict()   # All definitions in the graph and if it was used or not
    current_defs = dict()   # All definitions until the line of code we reached
    if declared:
        declared = [i.split('=')[0].strip() for i in declared[0].split(',')]
        for variable in declared:
            defs[variable] = [False, graph.root]
            current_defs[variable] = 0
    stack = []
    current = [graph.root, graph_with_strings.root]
    visited_set_to = list(current[0].children.values())[0].visited     # To know if edge is visited

    stack.append(current)
    while len(stack) > 0:
        current: cfg.Node = stack.pop()
        current_with_string = current[1]
        current = current[0]
        code = current.code
        is_break_or_continue = True if current.code in ['break', 'continue'] else False
        is_return = True if current.code == 'return' or current.code[:7] == 'return ' else False

        # If in an iteration, we return to line that is before the line we were using in the last iteration
        # we delete all definitions after the current line from the current_defs dict.
        to_pop = [i for i, j in current_defs.items() if j > current.id]
        for i in to_pop:
            current_defs.pop(i)

        # Find defs
        if current.node_type == 'normal':
            x = code.split('=')
            if len(x) > 1:
                if x[1] != '' and x[0][-1] not in ['!', '<', '>']:
                    x[1] = x[1].strip()
                    if x[1] not in ['True', 'False', 'None'] and checks.checkReservedKeyword(x[1]):
                        raise errors.InvalidUseOfReservedKeywordException(f"Cannot use '{x[1].strip()}' as a variable name.")
                    # if line was (ex. counter += 1) or (ex. x //= 2)
                    if x[0][-1] in ['+', '-', '/', '*', '%', '^']:
                        x[0] = x[0][:-1]
                        if x[0][-1] in ['*', '/']: x[0] = x[0][:-1]
                    line_defs = x[0].split(',')     # In case (ex. x, y = 2, 3)
                    for i in line_defs:
                        if not checks.checkReservedKeyword(i.strip()):
                            if defs.get(i.strip()) is None: defs[i.strip()] = [False, current]
                            if current_defs.get(i.strip()) is None: current_defs[i.strip()] = current.id
                        else:
                            raise errors.InvalidUseOfReservedKeywordException(f"Cannot use '{i.strip()}' as a variable name.")
        elif current.node_type == 'for':
            x = code.split(' in ')
            line_defs = x[0][4:].split(',')
            for i in line_defs:
                if not checks.checkReservedKeyword(i.strip()):
                    if defs.get(i.strip()) is None: defs[i.strip()] = [False, current]
                    if current_defs.get(i.strip()) is None: current_defs[i.strip()] = current.id
                else:
                    raise errors.InvalidUseOfReservedKeywordException(f"Cannot use '{i.strip()}' as a variable name.")
                        
        # Find uses
        if current.node_type not in ['def', 'else'] and current.code not in ['Start', 'End']:
            # Make sure we don't interpret a def as a use
            code_splitted = code.split('=')
            if len(code_splitted) > 1:
                if code_splitted[1] != '' and code_splitted[0][-1] not in ['!', '<', '>']:
                    code = '='.join(code_splitted[1:])

            # Use regular expressions to find all variables in the line
            used_variables = re.findall('[a-zA-Z_][a-zA-Z0-9_]*[^a-zA-Z0-9_(]', code + ' ')
            for i in range(len(used_variables)):
                if i != 0:
                    # For cases like (ex. current.children) we only take node as the used variable
                    if used_variables[i-1] + used_variables[i] in code: continue
                used_variables[i] = used_variables[i][:-1]
                # Make sure that the variables we got are not python reserved keywords
                if not checks.checkReservedKeyword(used_variables[i]):
                    if current_defs.get(used_variables[i]) is None:
                        raise errors.NonDeclaredVariableException(
                            f'Variable "{used_variables[i]}" is used in "{current_with_string.code}" but may not be declared.')
                    elif (defs[used_variables[i]][1].findCommonConditions(current.conditions_to_reach) 
                          != defs[used_variables[i]][1].conditions_to_reach):
                        raise errors.NonDeclaredVariableException(
                            f'Variable "{used_variables[i]}" is used in "{current_with_string.code}" but may not be declared.')
                    else:
                        defs[used_variables[i]][0] = True

        # Find used functions
        used_functions = re.findall('[\.a-zA-Z_][a-zA-Z0-9_]*[(]', code)
        for i in used_functions:
            if i[0] == '.': continue
            i = i[:-1]
            if graph.child_graphs.get(i) is None and not checks.checkBuiltInFunction(i):
                raise errors.FunctionNotFoundException(
                    f'Function "{i}" is used in "{current_with_string.code}" but may not be defined or is used out of scope.')
            else:
                # TODO
                pass
                
                    

        for i, j in list(zip(list(current.children.keys()), list(current_with_string.children.keys()))):
            if is_break_or_continue or (is_return and not (len(current.children) == 1
                and list(current.children.keys())[0].code == 'End')):
                err = f"{j.code} is never going to be executed after {current_with_string.code}"
                raise errors.UnReachableCodeException(err)
            
            if current.children[i].visited == visited_set_to:
                current.children[i].visited += 1
                current.children[i].visited %= 2
                current_with_string.children[j].visited += 1
                current_with_string.children[j].visited %= 2
                stack.append([i, j])
    
    err = ''
    for i, j in defs.items():
        if not j[0]:
            err += f'\n"{i}" was never used'
    if err: raise errors.DeclaredButNeverUsedException(err)
    return list(defs.keys())


def duplicate_finder(code='buggy.py'):
    with open(code, 'r') as code_file:
        code_lines = [line.strip().replace("'", '"') for line in code_file]
    code_lines_clone = code_lines[:]
    ignored_duplicates = ['else:', '"""', '']
    duplicates = []
    while True:
        duplicated = False
        for line in code_lines_clone:
            if line not in ignored_duplicates and code_lines_clone.count(line) > 2:
                duplicated = True
                indices = [index+1 for index in [i for i, x in enumerate(code_lines) if x == line]]
                temp = [line]
                temp.extend([indices])
                duplicates.append(temp)
                print("code : ", line, 'duplicated at lines :  ',  end='')
                for index in indices:
                    print(index, ' ', end='')
                print()
                for i in range(code_lines_clone.count(line)):
                    code_lines_clone.remove(line)
                break
        if not duplicated:
            break
    print(duplicates)
    dup = []
    for i in range(len(duplicates)):
        clone = [x+1 for x in duplicates[i][1][:]]
        for j in range(i+1, len(duplicates)):
            if duplicates[j][1] == clone:
                dup.append([duplicates[i], duplicates[j]])
    for d in dup:
        print(d)


# def find_duplicates(code):
#     code = code.split('\n')
#     code_lines = [line.strip().replace("'", '"') for line in code if not checks.checkUnwantedLine(line)]
#     final_duplicates = dict()
#     counter = 1
#     duplicates = dict()
#     for line in code_lines:
#         if duplicates.get(line) is None: duplicates[line] = [counter]
#         else: duplicates[line].append(counter)
#         counter += 1

if __name__ == '__main__':
    # with open('buggy.py', 'r') as code_file:
    # code = cr.refactor_find_syntax_errors(code_file.read(), 4)
    duplicate_finder()

