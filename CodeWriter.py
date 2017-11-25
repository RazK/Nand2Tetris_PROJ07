from Utils import *

CONSTANT_SEG_NAME = "constant"

class CodeWriter:
    def __init__(self, outfile):
        """
        Open the output file/stream and gets ready to write into it.
        """
        self.__output = outfile

    def setFileName(self, file_name):
        # TODO: RazK, Noy: Decide on a naming convention for methods,
        # either 'someFuncDoesWhat' or 'some_func_does_what', and refactor all
        # code to stick with it.
        """
        Informs the code writer that the translation of a new VM file
        is started.
        :param file_name: The name of the output file.
        """
        pass

    def __writeLine(self, line, comment_suffix=None):
        """
        Writes the given line to the output file, terminated by newline.
        :param line: Line to write to the output file.
        """
        if comment_suffix != None:
            suffix = " // {}".format(comment_suffix)
        else:
            suffix = ''
        self.__output.write("{}{}\n".format(line, suffix))

    def __writePush(self, address):
        """
        Writes the assembly code that is the translation of the given push
        command.
        :param segment: either ARG, THAT, THIS,
        :param index: index relative to the segment.
        """
        # Writes the translation into the output file:
        self.__writeLine(LOAD_A + address)
        self.__writeLine(D_REG + ASSIGN + M_REG)

        # Enters the extracted value to the stack:
        self.__writeLine(LOAD_A + SP)
        self.__writeLine(A_REG + ASSIGN + M_REG)
        self.__writeLine(M_REG + ASSIGN + D_REG)

        # Increments SP:
        self.__writeLine(LOAD_A + SP)
        self.__writeLine(M_REG + ASSIGN + M_REG + ADD + ONE)

    def __writePop(self, address):
        """
        Writes the assembly code that is the translation of the given pop
        command.
        :param segment: either ARG, THAT, THIS,
        :param index: index relative to the segment.
        """
        # Decrements SP and extracts the topmost value of the stack:
        self.__writeLine(LOAD_A + SP)
        self.__writeLine(M_REG + ASSIGN + M_REG + SUB + ONE)
        self.__writeLine(A_REG + ASSIGN + M_REG)
        self.__writeLine(D_REG + ASSIGN + M_REG)

        # Writes the extracted value to the wanted segment:
        self.__writeLine(LOAD_A + address)
        self.__writeLine(M_REG + ASSIGN + D_REG)

    def writeComment(self, comment):
        """
        Writes a comment line to the assembly.
        :param comment: comment to write to the assembly.
        """
        self.__writeLine("// {}".format(comment))

    def writePushPop(self, operation, segment, index):
        """
        Writes the assembly code that is the translation of the given
        operation, where the operation is either C_PUSH or C_POP.
        :param operation: either C_PUSH or C_POP
        :param segment: either ARG, THAT, THIS,
        :param index:
        """
        # Get address to Push/Pop
        address = getAddress(segment, int(index.strip()))

        # Write the appropriate command
        if operation == C_PUSH:
            self.__writePush(address)
        elif operation == C_POP:
            # TODO: RazK: Probably there's a better place in Utils to define
            # 'CONSTANT_SEG_NAME'
            if segment == CONSTANT_SEG_NAME:
                # Can't pop to constant segment
                raise ValueError(POP_FROM_CONSTANT_MSG)
            self.__writePop(address)
        else:
            raise ValueError(WRONG_COMMAND_TYPE_MSG)

    def __handleBinary(self, operation):
        """
        Translates the operations: x+y, x-y, x&y, x|y to assembly, and writs
        to the output file.
        :param operation: add , sub , or, and  operation in assembly.
        """

        # Pops x and y from the stack and saves them in the temp
        # segment:
        self.__writePop(ADDRESS_TEMP_0)
        self.__writePop(ADDRESS_TEMP_1)

        # Does the calculation :)
        self.__writeLine(LOAD_A + ADDRESS_TEMP_0)
        self.__writeLine(D_REG + ASSIGN + M_REG)
        self.__writeLine(LOAD_A + ADDRESS_TEMP_1)
        self.__writeLine(M_REG + ASSIGN + D_REG + operation + M_REG)

        # Pushes the result back to the topmost cell in the stack:
        self.__writePush(ADDRESS_TEMP_1)

    def __handleUnary(self, operation):
        """
        Translates the operations: -x, !x to assembly, and writs
        to the output file.
        :param operation: Either not or neg in assembly.
        """

        # Extracts the value in the topmost stack cell and keeps it in temp.
        self.__writePop(ADDRESS_TEMP_0)

        # Does the calculation:
        self.__writeLine(LOAD_A + ADDRESS_TEMP_0)
        self.__writeLine(M_REG + ASSIGN + operation + M_REG)

        # Pushes the result back to the stack:
        self.__writePush(ADDRESS_TEMP_0)

    def __handleComparative(self, operation):
        """
        Translates the operations: x=y, x>y, x<y to assembly, and writs
        to the output file.
        :param operation: eq, gt, lt.
        :return:
        """
        # todo: Noy: handle <, >.

        # Subtracting the values in the two topmost cells:
        self.__handleBinary(SUB)

        # Keeps the result in Temp 0 segment:
        self.__writePop(ADDRESS_TEMP_0)

        # Initializes Temp 1 to be 0:
        self.__writeLine(LOAD_A + ADDRESS_TEMP_1)
        self.__writeLine(M_REG + ASSIGN + ZERO)

        # Initializes D with the Subtraction result:
        self.__writeLine(LOAD_A + ADDRESS_TEMP_0)
        self.__writeLine(D_REG + ASSIGN + M_REG)

        # If the comparision result is T, changes temp 1 to "-1":
        self.__writeLine(LOAD_A + TRUE_ADDRESS)
        self.__writeLine(operation)

        # Else, it remains "0":
        self.__writeLine(LOAD_A + FALSE_ADDRESS)
        self.__writeLine(JUMP)
        self.__writeLine(TRUE_TAG)
        self.__writeLine(LOAD_A + ADDRESS_TEMP_1)
        self.__writeLine(M_REG + ASSIGN + NEG_ONE)
        self.__writeLine(FALSE_TAG)

        # Pushes the result back to the stack:
        self.__writePush(ADDRESS_TEMP_1)


    def writeArithmetic(self, operation):
        """
        Writes the assembly code that is the translation of the given
        arithmetic operation.
        :param operation: The arithmetic command to be translated.
        """

        if operation in OPERATIONS_ARITHMETIC_BINARY:
            self.__handleBinary(OPERATIONS_ARITHMETIC_BINARY[operation])

        elif operation in OPERATIONS_ARITHMETIC_UNARY:
            self.__handleUnary(OPERATIONS_ARITHMETIC_UNARY[operation])

        elif operation in OPERATIONS_ARITHMETIC_COMPARE:
            self.__handleComparative(OPERATIONS_ARITHMETIC_COMPARE[operation])

        else:
            raise ValueError(NOT_AN_OPERATION_MSG)

    def close(self):
        """
        Closes the output file
        :return:
        """
        pass


def main():
    """
    Tests for the CodeWriter module
    """
    with open("file.asm", "w+") as f:
        gustav = CodeWriter(f)
        gustav.writeArithmetic("eq")
        # gustav.writePushPop("C_POP", "static", 17)


if __name__ == "__main__":
    main()
