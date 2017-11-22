from Utils import *


class Parser:
    def __init__(self, infile):
        """
        Opens the input file/stream and gets ready to parse it.
        :param filename: An open hack assembly file descriptor (reading only)
        """
        self.__file = open(infile, "r")
        self.__curr_command = "label END"

    def hasMoreCommands(self):
        """
        Are there more commands in the input?
        :return: boolean (True if more commands, False otherwise)
        """
        pass

    def advance(self):
        """
        Reads the next command from the input and makes it the current
        command.
        Should be called only if hasMoreCommands() is true.
        Initially there is no current command.
        """
        pass

    def commandType(self):
        """
        Returns the type of the current VM command.
        C_ARITHMETIC is returned for all the arithmetic commands.
        :return: type of the current VM command.
        """
        # Extracts the command's prefix:
        split_command = self.__curr_command.split(SPACE)
        command_prefix = split_command[0]

        # Classify the command:
        if command_prefix in COMMANDS:
            return COMMANDS[command_prefix]

        elif self.__curr_command in BINARY_ARITHMETIC \
                or self.__curr_command in UNARY_ARITHMETIC:
            return C_ARITHMETIC

        else:
            raise ValueError(NOT_AN_OPERATION_MSG)

    def arg1(self):
        """
        Returns the first argument of the current command.
        In the case of C_ARITHMETIC, the command itself (add, sub, etc.) is
        returned
        Should not be called if the current command is C_RETURN.
        :return: string (Type of the current command)
        """
        if self.commandType() is C_RETURN:
            raise ValueError(ARG_ASKED_FOR_RETURN_MSG)

        elif self.commandType() is C_ARITHMETIC:
            return self.__curr_command

        # Else, return the first argument of the command:
        slice_command = self.__curr_command.split(SPACE)
        first_arg = slice_command[1]
        return first_arg

    def arg2(self):
        """
        Returns the second argument of the current command.
        Should be called only if the current command is C_PUSH, C_POP,
        C_FUNCTION, or C_CALL.
        :return: Second argument of the current command
        """

        # Tests if the command has a second argument:
        if self.commandType() not in [C_PUSH, C_POP, C_FUNCTION, C_CALL]:
            raise ValueError(NO_SECOND_ARG_MSG)

        # Extracts the second argument:
        slice_command = self.__curr_command.split(SPACE)
        second_arg = slice_command[2]
        return second_arg



def main():
    """
    Tests for the Parser module
    """
    parsi = Parser("C:/Users/Noy/Desktop/project7/Nand2Tetris_PROJ07/file.vm.txt")
    print(parsi.arg2())


if __name__ == "__main__":
    main()
