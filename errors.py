class NonDeclaredVariableException(Exception):
    """
    When a variable is used but was not declared.
    """
    pass

class DeclaredButNeverUsedException(Exception):
    """
    When a variable is declared but was not used.
    """
    pass

class InvalidUseOfReservedKeywordException(Exception):
    """
    When a reserved keyword is used as a variable or a function's name.
    """
    pass

class UnReachableCodeException(Exception):
    """
    When a line of code is after break, continue or return so it is never going to be executed.
    """
    pass

class FunctionNotFoundException(Exception):
    """
    A function is used but not defined.
    """
    pass

class InvalidBlockException(Exception):
    """
    Entered a block without a valid block initializer (if, for, while, ...).
    """
    pass