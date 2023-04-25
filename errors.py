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