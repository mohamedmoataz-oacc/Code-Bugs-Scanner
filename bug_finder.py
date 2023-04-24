import code_refactor as cr
import cfg


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


if __name__ == '__main__':
    with open('buggy.py', 'r') as code_file:
        code = cr.refactor_find_syntax_errors(code_file.read(), 4)
        duplicate_finder(code)
