from cfg import CFG
from bug_finder import find_bugs
from code_refactor import refactor_find_syntax_errors

def scanCodeGraphs(root: CFG, string_root: CFG):
    queue = [(root, string_root, '')]

    while queue:
        current: tuple(CFG) = queue.pop(0)
        current[0].construct_graph()
        current[0].printCFG()
        print('----------------------------------------')
        current[1].construct_graph()
        if current[2] == '': find_bugs(current[0], current[1])
        else: find_bugs(current[0], current[1], current[2])

        for i in current[0].child_graphs.keys():
            queue.append((current[0].child_graphs[i][0], current[1].child_graphs[i][0], current[0].child_graphs[i][1]))

    print('Scan succeeded. No bugs detected.')

if __name__ == '__main__':
    with open('buggy.py', 'r') as code_file: code = refactor_find_syntax_errors(code_file.read(), 4)
    strings_graph = CFG(code[0], 4)
    graph = CFG(code[2], 4, debug=True)
    scanCodeGraphs(graph, strings_graph)
