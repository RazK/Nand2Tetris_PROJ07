from Utils import *


class CodeWriter:
    def __init__(self, outfile):
        """
        Open the output file/stream and gets ready to write into it.
        """
        self.__output = outfile

    def set_file_name(self, file_name):
        """
        Informs the code writer that the translation of a new VM file
        is started.
        :param file_name: The name of the output file.
        """
        pass

    # For write_arithmetic's usage:

    def __writePushPop(self, command, segment, index):
        """
        Writes the assembly code that is the translation of the given
        command, where the command is either C_PUSH or C_POP.
        :param command: either C_PUSH or C_POP
        :param segment: either ARG, THAT, THIS,
        :param index:
        """

        add_base_index = SEGMENTS.get(segment) + index

        if command == C_PUSH:

            # Writes the translation into the output file:
            self.__output.write(A_INST_PREFIX + str(add_base_index) + NEW_LINE)
            self.__output.write(D_REG + EQUAL + M_REG + NEW_LINE)

            # Enters the extracted value to the stack:
            self.__output.write(A_INST_PREFIX + SP + NEW_LINE)
            self.__output.write(A_REG + EQUAL + M_REG + NEW_LINE)
            self.__output.write(M_REG + EQUAL + D_REG + NEW_LINE)

            # Increments SP:
            self.__output.write(A_INST_PREFIX + SP + NEW_LINE)
            self.__output.write(M_REG + EQUAL + M_REG + ADD + ONE + NEW_LINE)

        elif command == C_POP:

            # Decrements SP and extracts the topmost value of the stack:
            self.__output.write(A_INST_PREFIX + SP + NEW_LINE)
            self.__output.write(M_REG + EQUAL + M_REG + SUB + ONE + NEW_LINE)
            self.__output.write(A_REG + EQUAL + M_REG + NEW_LINE)
            self.__output.write(D_REG + EQUAL + M_REG + NEW_LINE)

            # Writes the extracted value to the wanted segment:
            self.__output.write(A_INST_PREFIX + str(add_base_index) + NEW_LINE)
            self.__output.write(M_REG + EQUAL + D_REG + NEW_LINE)

        else:
            raise ValueError(WRONG_COMMAND_TYPE_MSG)

    def __handle_binary(self, operation):
        """
        Translates the operations: x+y, x-y, x&y, x|y to assembly, and writs
        to the output file.
        :param operation: add , sub , or, and  operation in assembly.
        """

        # Pops two values from the stack and saves them in the temp segment:
        self.__writePushPop(C_POP, TEMP, TEMP_0)
        self.__writePushPop(C_POP, TEMP, TEMP_1)

        # Does the calculation :)
        self.__output.write(
            A_INST_PREFIX + str(SEGMENTS.get(TEMP) + TEMP_0) + NEW_LINE)
        self.__output.write(D_REG + EQUAL + M_REG + NEW_LINE)
        self.__output.write(
            A_INST_PREFIX + str(SEGMENTS.get(TEMP) + TEMP_1) + NEW_LINE)
        self.__output.write(
            M_REG + EQUAL + D_REG + operation + M_REG + NEW_LINE)

        # Pushes the result back to the topmost cell in the stack:
        self.__writePushPop(C_PUSH, TEMP, TEMP_1)

    def __handle_unary(self, operation):
        """
        Translates the operations: -x, !x to assembly, and writs
        to the output file.
        :param operation: Either not or neg in assembly.
        """

        # Extracts the value in the topmost stack cell and keeps it in temp.
        self.__writePushPop(C_POP, TEMP, TEMP_0)

        # Does the calculation:
        self.__output.write(
            A_INST_PREFIX + str(SEGMENTS.get(TEMP) + TEMP_0) + NEW_LINE)
        self.__output.write(M_REG + EQUAL + operation + M_REG + NEW_LINE)

        # Pushes the result back to the stack:
        self.__writePushPop(C_PUSH, TEMP, TEMP_0)

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
            raise ValueError(NOT_AN_OPPERATION_MSG)

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
