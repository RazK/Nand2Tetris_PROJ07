from Utils import *


class CodeWriter:
    def __init__(self, outfile):
        """
        Open the output file/stream and gets ready to write into it.
        """
        self.__output = outfile
        self.__stackSize = 0
        self.__unique_id = 0


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
        if (self.__stackSize >= STACK_SIZE):
            raise OverflowError("Push operation will result in stack "
                                "overflow!")
        # Writes the translation into the output file:
        self.__writeLine(LOAD_A + address.strip())
        self.__writeLine(D_REG + ASSIGN + M_REG)

        # Enters the extracted value to the stack:
        self.__writeLine(LOAD_A + SP)
        self.__writeLine(A_REG + ASSIGN + M_REG)
        self.__writeLine(M_REG + ASSIGN + D_REG)

        # Increments SP:
        self.__writeLine(LOAD_A + SP)
        self.__writeLine(M_REG + ASSIGN + M_REG + ADD + ONE)
        self.__stackSize += 1

    def __writePop(self, address):
        """
        Writes the assembly code that is the translation of the given pop
        command.
        :param segment: either ARG, THAT, THIS,
        :param index: index relative to the segment.
        """
        if (self.__stackSize <= 0):
            raise OverflowError("Pop operation will result in stack "
                                "underflow!")

        # Decrements SP and extracts the topmost value of the stack:
        self.__writeLine(LOAD_A + SP)
        self.__writeLine(M_REG + ASSIGN + M_REG + SUB + ONE)
        self.__writeLine(A_REG + ASSIGN + M_REG)
        self.__writeLine(D_REG + ASSIGN + M_REG)
        self.__stackSize -= 1

        # Writes the extracted value to the wanted segment:
        self.__writeLine(LOAD_A + address.strip())
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

        # Get physical address to Push/Pop
        if segment != CONSTANT_SEG_NAME:
            address = getAddress(segment, int(index))
        # Emulate addresses for constants using TEMP_0 register
        else:
            self.__saveValueInTemp(index)
            address = ADDRESS_TEMP_0

        # Write the appropriate command
        if operation == C_PUSH:
            self.__writePush(address)
        elif operation == C_POP:
            if segment == CONSTANT_SEG_NAME:
                # Can't pop to constant segment
                raise ValueError(POP_FROM_CONSTANT_MSG)
            self.__writePop(address)
        else:
            raise ValueError(WRONG_COMMAND_TYPE_MSG)

    def __writeBinary(self, operation):
        """
        Translates the operations: x+y, x-y, x&y, x|y to assembly, and writs
        to the output file.
        :param operation: add , sub , or, and  operation in assembly.
        """

        # Pops x and y from the stack and saves them in the temp
        # segment:
        self.__writePop(ADDRESS_TEMP_1)
        self.__writePop(ADDRESS_TEMP_0)

        # Does the calculation :)
        self.__writeLine(LOAD_A + ADDRESS_TEMP_0)
        self.__writeLine(D_REG + ASSIGN + M_REG)
        self.__writeLine(LOAD_A + ADDRESS_TEMP_1)
        self.__writeLine(M_REG + ASSIGN + D_REG + operation + M_REG)

        # Pushes the result back to the topmost cell in the stack:
        self.__writePush(ADDRESS_TEMP_1)

    def __writeUnary(self, operation):
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

    def __uniqueLabel(self, label):
        """
        Adds a unique id to the given label to prevent collisions with other
        labels carrying the same name.
        Example:
            localizeLabel("TRUE") --> "TRUE_1"
        :param label: label to localize
        :return: Given label with a unique identifier.
        """
        unique_label = "{}_{}".format(self.__unique_id, label)
        self.__unique_id += 1
        return unique_label

    def __writeComparative(self, operation):
        """
        Translates the operations: x=y, x>y, x<y to assembly, and writes
        to the output file.
        :param operation: eq, gt, lt.
        """
        # TODO: RazK: Prevent integer overflow/underflow
        # Subtracting the values in the two topmost cells:
        self.__writeBinary(SUB)

        # Keeps the result in Temp 0 segment:
        self.__writePop(ADDRESS_TEMP_0)

        # Initializes Temp 1 to be 0:
        self.__writeLine(LOAD_A + ADDRESS_TEMP_1)
        self.__writeLine(M_REG + ASSIGN + ZERO)

        # Initializes D with the Subtraction result:
        self.__writeLine(LOAD_A + ADDRESS_TEMP_0)
        self.__writeLine(D_REG + ASSIGN + M_REG)

        # If the comparision result is T, changes temp 1 to "-1":
        TRUE_LABEL = self.__uniqueLabel(TRUE_ADDRESS)
        self.__writeLine(LOAD_A + TRUE_LABEL)
        self.__writeLine(operation)

        # Else, it remains "0":
        FALSE_LABEL = self.__uniqueLabel(FALSE_ADDRESS)
        self.__writeLine(LOAD_A + FALSE_LABEL)
        self.__writeLine(JUMP)
        self.__writeLine(declareLabel(TRUE_LABEL))
        self.__writeLine(LOAD_A + ADDRESS_TEMP_1)
        self.__writeLine(M_REG + ASSIGN + NEG_ONE)
        self.__writeLine(declareLabel(FALSE_LABEL))

        # Pushes the result back to the stack:
        self.__writePush(ADDRESS_TEMP_1)

    def writeArithmetic(self, operation):
        """
        Writes the assembly code that is the translation of the given
        arithmetic operation.
        :param operation: The arithmetic command to be translated.
        """
        if operation in A_OPERATIONS:
            operation_asm = A_OPERATIONS.get(operation)

            if operation_asm in A_OPERATIONS_BINARY:
                self.__writeBinary(operation_asm)

            elif operation_asm in A_OPERATIONS_UNARY:
                self.__writeUnary(operation_asm)

            elif operation_asm in A_OPERATIONS_COMPARE:
                self.__writeComparative(operation_asm)

        else:
            raise ValueError(NOT_AN_OPERATION_MSG)

    def __saveValueInTemp(self, value):
        """
        Saves the given value in the temp register.
        :param value: Numeric value to save in the temp register
        """
        safe_value = twosComplement(value)
        self.__writeLine(LOAD_A + safe_value)
        self.__writeLine(D_REG + ASSIGN + A_REG)
        self.__writeLine(LOAD_A + ADDRESS_TEMP_0)
        self.__writeLine(M_REG + ASSIGN + D_REG)
        pass


def main():
    """
    Tests for the CodeWriter module
    """
    with open("file.asm", "w+") as f:
        gustav = CodeWriter(f)
        gustav.writePushPop(C_PUSH, CONSTANT_SEG_NAME, 5)
        gustav.writePushPop(C_PUSH, CONSTANT_SEG_NAME, 3)
        gustav.writeArithmetic("lt")
        # gustav.writePushPop("C_POP", "static", 17)


if __name__ == "__main__":
    main()
