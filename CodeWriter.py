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

    def write_arithmetics(self, command):
        """
        Writes the assembly code that is the translation of the given
        arithmetic command.
        :param command: The arithmetic command to be translated.
        """
        pass

    def writePushPop(self, command, segment, index):
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
            self.__output.write(M_REG + EQUAL + D_REG + NEW_LINE)

            # Increments SP:
            self.__output.write(M_REG + EQUAL + M_REG + ADD + ONE + NEW_LINE)

        elif command == C_POP:

            # Decrements SP and extracts the topmost value of the stack
            self.__output.write(A_INST_PREFIX + SP + NEW_LINE)
            self.__output.write(M_REG + EQUAL + M_REG + SUB + ONE + NEW_LINE)
            self.__output.write(D_REG + EQUAL + M_REG + NEW_LINE)

            # Writes the extracted value to the wanted segment:
            self.__output.write(A_INST_PREFIX + str(add_base_index) + NEW_LINE)
            self.__output.write(M_REG + EQUAL + D_REG + NEW_LINE)

        else:
            raise ValueError(WRONG_COMMAND_TYPE_MSG)

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
    with open("file", "w+") as f:
        gustav = CodeWriter(f)
        gustav.writePushPop("C_PO", "static", 17)


if __name__ == "__main__":
    main()
