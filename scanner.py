import time
from cfg import CFG
import errors
from bug_finder import find_bugs, duplicate_finder
from code_refactor import refactor_find_syntax_errors

def scanCodeGraphs(root: CFG, string_root: CFG):
    queue = [(root, string_root, '', 'Root')]
    all_defs = dict()

    while queue:
        current: tuple(CFG) = queue.pop(0)
        print(current[3], 'code parsed:')
        print('       ---------')
        current[0].construct_graph()
        print(f'\n\n\n{current[3]}\'s Control Flow Graph:')
        print('       ---------')
        current[0].printCFG()
        print('--------------------------------------------------------------------------')
        current[1].construct_graph()
        if current[2] == '': all_defs.update(find_bugs(current[0], current[1]))
        else: all_defs.update(find_bugs(current[0], current[1], current[2]))

        for i in current[0].child_graphs.keys():
            queue.append((current[0].child_graphs[i][0], current[1].child_graphs[i][0], current[0].child_graphs[i][1], i))

    err = ''
    for i, j in all_defs.items():
        if not j[0]:
            err += f'\n"{i}" was never used'
    if err: raise errors.DeclaredButNeverUsedException(err)

    for i, j in graph.child_graphs.items():
        if not j[2]:
            err += f'\n"{i}" was never used'
    if err: raise errors.DeclaredButNeverUsedException(err)
    print('Scan succeeded. No bugs detected.')

if __name__ == '__main__':
    file_name = 'buggy.py'
    with open(file_name, 'r') as code_file:
        code = refactor_find_syntax_errors(code_file.read(), 4)
    
    print('Checking for:\n1- Invalid use of python reserved keywords.')
    print('2- Indentation Errors.')
    print('3- Invalid code blocks.')
    print('4- Used but undeclared variables.')
    print('5- Functions used in code but were not defined.')
    print('6- Unreachable code.')
    print('7- Variables that were declared but never used.')
    print('8- Duplicates in code. (Not clean code!)')
    time.sleep(2)
    print('----------------------------------------')
    print('Results:')
    print('----------------------------------------')
    
    strings_graph = CFG(code[0], 4)
    graph = CFG(code[2], 4, debug=True)
    scanCodeGraphs(graph, strings_graph)
    print('----------------------------------------')
    print('Checking for duplicated code lines...')
    time.sleep(2)
    duplicate_finder(file_name)
