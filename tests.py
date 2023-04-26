import unittest
from cfg import CFG
import errors
from bug_finder import find_bugs
from code_refactor import refactor_find_syntax_errors

class TestBugFindingMethods(unittest.TestCase):

    def test_find_bugs(self):
        test1 = """
x=1
y=2
print(x,y,z)
"""
        test1 = refactor_find_syntax_errors(test1, 4)[2]
        cg = CFG(test1, 4)
        cg.construct_graph()
        self.assertRaises(errors.NonDeclaredVariableException, find_bugs, cg)

if __name__ == '__main__':
    unittest.main()