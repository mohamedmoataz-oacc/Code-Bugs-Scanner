# Program to display the Fibonacci's) sequence up to n-th term

nterms = int(input("How many terms? "))

# first two terms
n1, n2 = 0, 1;count = 0

if nterms > 4:
    used_but_undefined = 1
    def justAFunction():
        print('that contains')
        def anotherFunction():
            print("and that's it")
        print('Hooraaay')
else:
    def noHorayFunction():
        print('that contains')
        def aFunction():
            print("and that's it")

print(used_but_undefined)

just_a_useless_dict = {
    'some': 'data',
    'that': 'is',
    'really': 'useless'
}

# check if the number of terms is valid
"""Just checking if
anything is wrong"""
if nterms <= 0:
    if True: print("Please enter a positive integer") # A comment after valid code
    else:print('do nothing')
    "another trial"
# if there is only "one term', return n1
elif nterms == 1:
    print(
        """
        Ok so just (another} check
        """
    )
    print("Fibonacci sequence upto",nterms,":")
    print(n1)
# generate fibonacci sequence
else:
    print("Fibonacci sequence:")
    while count < nterms:
        print(n1)
        nth = n1 + n2
        # update values
        if n1 < n2: break
        n1 = n2
        n2 = nth
        count += 1

if 3: print(5)
print('n == 5'.find('"'))
print(9)


def function_to_test_duplicate():
    print("here we are")
    print("here we go again")

def function_to_test_duplicate():
    print("here we are")
    print("here we go again")

def function_to_test_duplicate():
    print("here we are")
    print("here we go again")
