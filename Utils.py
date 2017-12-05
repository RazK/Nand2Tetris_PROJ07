##################
# CODE OPERATIONS
##################

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

# COMMANDS WITH 2 ARGS:
COMMANDS_BINARY = [C_PUSH, C_POP, C_FUNCTION, C_CALL]

# COMMANDS PUSH POP:
COMMANDS_PUSH_POP = [C_PUSH, C_POP]

# VM OPERATIONS TO COMMANDS DICTIONARY:
VM_OPERATIONS_2_COMMANDS = {
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

# ARITHMETIC TYPES:
A_ADD = "+"
A_SUB = "-"
A_AND = "&"
A_OR = "|"
A_NEG = " -" # Important! should be different than '-', collides with A_SUB!
A_NOT = "!"
A_EQ = "D;JEQ"
A_LT = "D;JLT"
A_GT = "D;JGT"

# ARITHMETIC WITH 2 ARGS:
ARITHMETIC_BINARY = [A_ADD, A_SUB, A_AND, A_OR]

# ARITHMETIC WITH 1 ARG:
ARITHMETIC_UNARY = [A_NEG, A_NOT]

# ARITHMETIC WITH NO ARGS
ARITHMETIC_COMPARE = [A_EQ, A_LT, A_GT]

VM_OPERATIONS_2_ARITHMETIC = {
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

ARITHMETIC_ANY = VM_OPERATIONS_2_ARITHMETIC.values()

#########
# MEMORY
#########

# MEMORY ALIASES
SP = "R0"
LCL_SEG_ALIAS = "R1"
ARG_SEG_ALIAS = "R2"
THIS_SEG_ADRESS = "3"
THAT_SEG_ALIAS = "R4"
TEMP_SEG_ADDRESS = "5"
TEMP_0_ADDRESS = "5"
TEMP_1_ADDRESS = "6"
CONSTANT_SEG_ALIAS = TEMP_SEG_ADDRESS
POINTER_SEG_ALIAS = THIS_SEG_ADRESS
# TODO: RazK: fix real value for STATIC
STATIC_SEG_ADDR = "Ben El" # LOL

VM_CONSTANT_SEG = "constant"
VM_TEMP_SEG = "temp"
VM_POINTER_SEG = "pointer"
VM_ARG_SEG = "argument"
VM_LCL_SEG = "local"
VM_STATIC_SEG = "static"
VM_THIS_SEG = "this"
VM_THAT_SEG = "that"

# SEGMENTS PREDEFINED ADDRESSES
VM_SEGMENT_2_ADDRESS = {
    VM_ARG_SEG : ARG_SEG_ALIAS,
    VM_LCL_SEG : LCL_SEG_ALIAS,
    VM_STATIC_SEG : STATIC_SEG_ADDR,
    VM_CONSTANT_SEG : CONSTANT_SEG_ALIAS,
    VM_THIS_SEG : THIS_SEG_ADRESS,
    VM_THAT_SEG : THAT_SEG_ALIAS,
    VM_POINTER_SEG : POINTER_SEG_ALIAS,  # Memory Segments Mapping (Book page 118)
    VM_TEMP_SEG : TEMP_SEG_ADDRESS,
}
INDEX_0 = 0
INDEX_1 = 1

# STACK
STACK_STANDARD_BASE = 256
STACK_START_ADDRESS = STACK_STANDARD_BASE
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

# DELIMETERS
LABEL_DELIMITER = "$"
VARIABEL_DELIMITER = "."
EXTENSION_DELIMITER = "."
UNIQUE_DELIMITER = "_"

# MORE:"
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
UNDEFINED_JUMP_DESTINATION_MSG = "The jump destination must be in the " \
                                 "current function"
