# Command Types

C_ARITHMETIC = "C_ARITHMETIC"
C_PUSH = "C_PUSH"
C_POP = "C_POP"
C_LABEL = "C_LABEL"
C_GOTO = "C_GOTO"
C_IF = "C_IF"
C_FUNCTION = "C_FUNCTION"
C_RETURN = "C_RETURN"
C_CALL = "C_CALL"

SP = "R0"
LCL = "R1"
ARG = "R2"
THIS = "R3"
THAT = "R4"

SEGMENTS = {
    "argument": 0,
    "local": 0,
    "static": 0,
    "constant": 0,
    "this": 0,
    "that": 0,
    "pointer": 0,
    "temp": 0
}

# INSTRUCTIONS
A_INST_PREFIX = "@"

# REGISTERS
M_REG = "M"
A_REG = "A"
D_REG = "D"

# ARITHMETIC:
EQUAL = "="
ADD = "+"
SUB = "-"
ONE = "1"
ZERO = "0"

# MORE:
NEW_LINE = "\n"
