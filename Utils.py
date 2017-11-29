##################
# CODE OPERATIONS
##################

# OPERATIONS TYPES:
C_ARITHMETIC = "C_ARITHMETIC"
C_PUSH = "C_PUSH"
C_POP = "C_POP"
C_LABEL = "C_LABEL"
C_GOTO = "C_GOTO"
C_IF = "C_IF"
C_FUNCTION = "C_FUNCTION"
C_RETURN = "C_RETURN"
C_CALL = "C_CALL"

# OPERATION WITH 2 ARGUMENTS:
C_OPERATIONS_BINARY = [C_PUSH, C_POP, C_FUNCTION, C_CALL]

# PUSH POP OPERATIONS:
C_OPERATIONS_PUSH_POP = [C_PUSH, C_POP]

# CODE OPERATION IDENTIFIERS:
C_OPERATIONS = {
    "push": C_PUSH,
    "pop": C_POP,
    "goto": C_GOTO,
    "label": C_LABEL,
    "return": C_RETURN,
    "function": C_FUNCTION,
    "if-goto": C_IF,
    "call": C_CALL
}

########################
# ARITHMETIC OPERATIONS
########################

# OPERATION TYPES:
A_ADD = "+"
A_SUB = "-"
A_AND = "&"
A_OR = "|"
A_NEG = " -" # Important! should be different than '-', collides with A_SUB!
A_NOT = "!"
A_EQ = "D;JEQ"
A_LT = "D;JLT"
A_GT = "D;JGT"

# OPERATIONS WITH 2 ARGS:
A_OPERATIONS_BINARY = [A_ADD, A_SUB, A_AND, A_OR]

# OPERATIONS WITH 1 ARG:
A_OPERATIONS_UNARY = [A_NEG, A_NOT]

# OPERATIONS WITH NO ARGS
A_OPERATIONS_COMPARE = [A_EQ, A_LT, A_GT]

A_OPERATIONS = {
    "add": A_ADD,
    "sub": A_SUB,
    "and": A_AND,
    "or": A_OR,
    "neg": A_NEG,
    "not": A_NOT,
    "eq": A_EQ,
    "lt": A_LT,
    "gt": A_GT
}

A_OPERATIONS_ANY = A_OPERATIONS.values()

#########
# MEMORY
#########

# MEMORY ALIASES
SP = "R0"
LCL_SEG_ADDR = "R1"
ARG_SEG_ADDR = "R2"
THIS_SEG_ADDR = "3"
THAT_SEG_ADDR = "R4"
TEMP_SEG_ADDR = "5"
TEMP_0 = "5"
TEMP_1 = "6"
TEMP_2 = "7"
TEMP_3 = "8"
TEMP_4 = "9"
TEMP_5 = "10"
CONSTANT_SEG_ADDR = TEMP_SEG_ADDR
POINTER_SEG_ADDR = THIS_SEG_ADDR
# TODO: RazK: fix real value for STATIC
STATIC_SEG_ADDR = "Ben El" # LOL

CONSTANT_SEG_NAME = "constant"
TEMP_SEG_NAME = "temp"
POINTER_SEG_NAME = "pointer"
ARG_SEG_NAME = "argument"
LCL_SEG_NAME = "local"
STATIC_SEG_NAME = "static"
THIS_SEG_NAME = "this"
THAT_SEG_NAME = "that"

# SEGMENTS PREDEFINED ADDRESSES
SEGMENTS_NAME_TO_ADDR = {
    ARG_SEG_NAME : ARG_SEG_ADDR,
    LCL_SEG_NAME : LCL_SEG_ADDR,
    STATIC_SEG_NAME : STATIC_SEG_ADDR,
    CONSTANT_SEG_NAME : CONSTANT_SEG_ADDR,
    THIS_SEG_NAME : THIS_SEG_ADDR,
    THAT_SEG_NAME : THAT_SEG_ADDR,
    POINTER_SEG_NAME : POINTER_SEG_ADDR,  # Memory Segments Mapping (Book page 118)
    TEMP_SEG_NAME : TEMP_SEG_ADDR,
}
INDEX_0 = 0
INDEX_1 = 1
INDEX_2 = 2

# STACK
STACK_START_ADDRESS = 256
STACK_END_ADDRESS = 2047
STACK_SIZE = STACK_END_ADDRESS - STACK_START_ADDRESS + 1


# INTERNAL CALCULATIONS:
DEFAULT_COMMAND = None

############
# ASM CODE
############

# INSTRUCTIONS:
LOAD_A = "@"

# REGISTERS:
M_REG = "M"
A_REG = "A"
D_REG = "D"

# OPERATORS:
ASSIGN = "="
ADD = "+"
SUB = "-"
ONE = "1"
NEG_ONE = "-1"
ZERO = "0"

# MORE:
NEW_LINE = "\n"
SPACE = " "
TAB = "\t"
COMMENT_PREFIX = "//"
EOF = ""
EMPTY_LINE = ''

# CONDITIONS:
TRUE_ADDRESS = "TRUE"
FALSE_ADDRESS = "FALSE"
TRUE_TAG = "(TRUE)"
FALSE_TAG = "(FALSE)"
JUMP = "D;JMP"

def declareLabel(label):
    """
    Returns a label definition line which can be written to the output.
    Example:
        label = "foo" --> returns "(foo)"
    :param label: label to get declaration for
    :return: label within parenthesis according to declaration format.
    """
    return "({})".format(label)

SIZEOF_WORD = 15 # bits

def twosComplement(num):
    """
    Returns the number in it's two's complement (always positive)
    representation.
    :param num: number to complement.
    :return: The number complemented to a positive representation.
    """
    bin_complement = bin(int(num) & int("1" * SIZEOF_WORD, 2))[2:]
    str_complement = ("{0:0>%s}" % (SIZEOF_WORD)).format(bin_complement)
    return str(int(str_complement, 2))

#################
# ERROR MESSAGES
#################

WRONG_COMMAND_TYPE_MSG = "This method should get only 'C_PUSH' or 'C_POP' " \
                         "as command type."
NOT_AN_OPERATION_MSG = "Operation is not supported."
COMMAND_NOT_SUPPORTED_MSG = "Command is not supported."
ARG_ASKED_FOR_RETURN_MSG = "The return command has no arguments."
NO_SECOND_ARG_MSG = "Command has no second argument."
POP_FROM_CONSTANT_MSG = "Popping to the constant segment is not supported."
