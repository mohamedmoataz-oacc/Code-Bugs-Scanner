import code_refactor as cr
import cfg


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
