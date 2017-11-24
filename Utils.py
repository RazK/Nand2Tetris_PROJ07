# COMMAND TYPES:
C_ARITHMETIC = "C_ARITHMETIC"
C_PUSH = "C_PUSH"
C_POP = "C_POP"
C_LABEL = "C_LABEL"
C_GOTO = "C_GOTO"
C_IF = "C_IF"
C_FUNCTION = "C_FUNCTION"
C_RETURN = "C_RETURN"
C_CALL = "C_CALL"

# COMMAND IDENTIFIERS:
COMMANDS = {
    "push": C_PUSH,
    "pop": C_POP,
    "goto": C_GOTO,
    "label": C_LABEL,
    "return": C_RETURN,
    "function": C_FUNCTION,
    "if-goto": C_IF,
    "call": C_CALL
}
COMMANDS_WITH_2_ARGS = [C_PUSH, C_POP, C_FUNCTION, C_CALL]

# MEMORY ALIASES:
SP = "R0"
LCL = "R1"
ARG = "R2"
THIS = "R3"
THAT = "R4"

# Segments Predefined Addresses
# TODO: RazK, Noy: Update segments with real values
SEGMENTS = {
    "argument": 0,
    "local": 0,
    "static": 0,
    "constant": 0,
    "this": 0,
    "that": 0,
    "pointer": 0,
    "temp": 5
}

# INSTRUCTIONS:
LOAD_A = "@"

# REGISTERS:
M_REG = "M"
A_REG = "A"
D_REG = "D"

# ARITHMETIC:
BINARY_ARITHMETIC = {
    "add": "+",
    "sub": "-",
    "and": "&",
    "or": "|"
}
UNARY_ARITHMETIC = {
    "neg": "!",
    "not": "-"
}
ASSIGN = "="
ADD = "+"
SUB = "-"
ONE = "1"
ZERO = "0"

# ERRORS MESSAGES:
WRONG_COMMAND_TYPE_MSG = "This method should get only 'C_PUSH' or 'C_POP' " \
                         "as command type."
NOT_AN_OPERATION_MSG = "Operation is not supported."
COMMAND_NOT_SUPPORTED_MSG = "Command is not supported."
ARG_ASKED_FOR_RETURN_MSG = "The return command has no arguments."
NO_SECOND_ARG_MSG = "Command has no second argument."

# MORE:
NEW_LINE = "\n"
SPACE = " "


def getAddress(segment, index):
    """
    Returns the absolute RAM address of the given segment + index.
    :param segment: Name of the desired segment (should be a key in the
                    SEGMENTS dict)
    :param index: Offset relative to the given segment.
    :return: Absolute RAM address of the given segment + index.
    """
    # TODO: RazK: Check parameters validity
    return str(SEGMENTS[segment] + index)

# INTERNAL CALCULATIONS:
TEMP = "temp"
ADDRESS_TEMP_0 = getAddress(TEMP, 0)
ADDRESS_TEMP_1 = getAddress(TEMP, 1)
