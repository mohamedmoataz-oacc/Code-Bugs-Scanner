# # Program to display the Fibonacci's) sequence up to n-th term
# nterms = int(input("How many terms? "))
 
# # first two terms
# n1, n2 = 0, 1
# count = True == False
# # if count == 0:
# # print('hi')

 
# if nterms > 4:
#     e1 = 99
#     # elif count < 3:
#     #     print('hi')
#     # else:
#     #     print('hello')
#     def justAFunction(x):
#         print('that contains')
#         if x == 'ok':
#             print("and that's it")
#             return 'flag{hdj}'
#         return x
 
#     e2 = 555
# elif nterms > 6:
#     used_but_undefined = 0
 
#     def noHorayFunction():
#         print('that contains')
 
#         def append():
#             print("and that's it")
#     HorayFunction(90)
# else:
#         xx = 99


# i = []
# i.append(9)
# while i < 5:
#     e6 = 5
#     zz = 5
#     # if xx == i:
#     #     break
#     #     print('anything')
#     e6 = e6 + 1
#     i += 1
# # print(zz)

# for i, j in [[1,'hi'], [4,'hello']]:
#     print(i,j)


def calculate_grade(grades):
    output = list()
    for grade in grades:
        if grade >= 0 and grade <= 100:
            if grade <= 59: output.append('F')
            elif grade <= 69: output.append('D')
            elif grade <= 79: output.append('C')
            elif grade <= 89: output.append('B')
            else: output.append('A')
    return output
    print('a bug')

# grade = 78;output = []
# if True:
#     if grade >= 0 and grade <= 100:
#         if grade <= 59: output.append('F')
#         elif grade <= 69: output.append('D')
#         elif grade <= 79: output.append('C')
#         elif grade <= 89: output.append('B')
#         else: output.append('A')
# print(output)