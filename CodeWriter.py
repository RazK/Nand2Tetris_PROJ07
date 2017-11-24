from Utils import *


class CodeWriter:
    def __init__(self, outfile):
        """
        Open the output file/stream and gets ready to write into it.
        """
        self.__output = outfile

    def set_file_name(self, file_name):
        # TODO: RazK, Noy: Decide on a naming convention for methods,
        # either 'someFuncDoesWhat' or 'some_func_does_what', and refactor all
        # code to stick with it.
        """
        Informs the code writer that the translation of a new VM file
        is started.
        :param file_name: The name of the output file.
        """
        pass

    def __writeLine(self, line):
        """
        Writes the given line to the output file, terminated by newline.
        :param line: Line to write to the output file.
        """
        self.__output.write("{}\n".format(line))

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

    def __writePushPop(self, command, segment, index):
        """
        Writes the assembly code that is the translation of the given
        command, where the command is either C_PUSH or C_POP.
        :param command: either C_PUSH or C_POP
        :param segment: either ARG, THAT, THIS,
        :param index:
        """
        # Get address to Push/Pop
        address = getAddress(segment, index)

        # Write the appropriate command
        if command == C_PUSH:
            self.__writePush(address)
        elif command == C_POP:
            self.__writePop(address)
        else:
            raise ValueError(WRONG_COMMAND_TYPE_MSG)

    def __handle_binary(self, operation):
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

    def __handle_unary(self, operation):
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

    def __handle_jumps(self, operation):
        """
        Translates the operations: x=y, x>y, x<y to assembly, and writs
        to the output file.
        :param operation: eq, gt, lt.
        :return:
        """
        # TODO: Noy: Ask Raz.
        pass

    def write_arithmetic(self, command):
        """
        Writes the assembly code that is the translation of the given
        arithmetic command.
        :param command: The arithmetic command to be translated.
        """

        if command in BINARY_ARITHMETIC:
            self.__handle_binary(BINARY_ARITHMETIC.get(command))

        elif command in UNARY_ARITHMETIC:
            self.__handle_unary(UNARY_ARITHMETIC.get(command))

        # TODO: Noy: to add something for < > =

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
        gustav.write_arithmetic("neg")
        # gustav.writePushPop("C_POP", "static", 17)


if __name__ == "__main__":
    main()
