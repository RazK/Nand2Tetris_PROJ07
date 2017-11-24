from src.Nand2Tetris_PROJ07.Utils import *

# Comand Structure: OPERATION [ARG1] [ARG2]
# Examples:
#   add             (OPERATION = "add",   ARG1 = "",      ARG2 = "")
#   goto loop       (OPERATION = "goto",  ARG1 = "loop",  ARG2 = "")
#   push local 3    (OPERATION = "push",  ARG1 = "local", ARG2 = "3")

OPERATION = 0
ARG1 = 1
ARG2 = 2


class Parser:
    def __init__(self, infile):
        """
        Gets ready to parse the infile.
        :param infile: An open hack assembly file descriptor (reading only)
        """
        self.__file = infile
        self.__curr_command = DEFAULT_COMMAND
        self.__next_command = self.__file.readline()
        self.advance()

    def __shouldSkipLine(self):
        """
        Returns if the current line should be skipped, either because it's a
        comment line (starts with '//') or because it only contained tabs
        and spaces.
        :return: True if line should be skipped, False otherwise
        """
        # TODO: RazK: test this
        stripped = self.__curr_command.strip(SPACE + TAB)
        return stripped == NEW_LINE or stripped.startswith(COMMENT_PREFIX)

    def hasMoreCommands(self):
        """
        Are there more commands in the input?
        :return: boolean (True if more commands, False otherwise)
        """
        return self.__curr_command != EOF

    def advance(self):
        """
        Reads the next command from the input and makes it the current
        command.
        Should be called only if hasMoreCommands() is true.
        Initially there is no current command.
        """
        do = True
        while (do):
            self.__curr_command = self.__next_command
            self.__next_command = self.__file.readline()

            # Skip empty lines and comments
            do = (self.hasMoreCommands() and self.__shouldSkipLine())

            # TODO: RazK: Add mechanism to count instructions for jumps and
            # labels

    def getOperation(self):
        """
        Returns the type of the current VM command (the operation).
        C_ARITHMETIC is returned for all the arithmetic commands.
        :return: operation - type of the current VM command.
        """
        # Extracts the operation part of the command:
        op = self.__curr_command.split(SPACE)[OPERATION].strip()

        # Classify the command:
        if op in C_OPERATIONS:
            return C_OPERATIONS[op]

        elif op in OPERATIONS_ARITHMETIC:
            return C_ARITHMETIC

        else:
            raise ValueError(NOT_AN_OPERATION_MSG)

    def arg1(self):
        """
        Returns the first argument of the current command.
        In the case of C_ARITHMETIC, the command itself (add, sub, etc.) is
        returned.
        Should not be called if the current command is C_RETURN.
        :return: string (Type of the current command)
        """
        if self.getOperation() is C_RETURN:
            raise ValueError(ARG_ASKED_FOR_RETURN_MSG)

        elif self.getOperation() is C_ARITHMETIC:
            return self.__curr_command

        # Else, return the first argument of the command:
        return self.__curr_command.split(SPACE)[ARG1]

    def arg2(self):
        """
        Returns the second argument of the current command.
        Should be called only if the current command is C_PUSH, C_POP,
        C_FUNCTION, or C_CALL.
        :return: Second argument of the current command
        """

        # Tests if the command has a second argument:
        if self.getOperation() not in OPERATIONS_WITH_2_ARGS:
            raise ValueError(NO_SECOND_ARG_MSG)

        # Extracts the second argument:
        #TODO: RazK: What if the command can have 2 arguments but only has
        # 1? for example: 'push 1' doesn't have a second argument but I
        # think it's valid
        return self.__curr_command.split(SPACE)[ARG2]


def main():
    """
    Tests for the Parser module
    """
    parsi = Parser(
        "C:/Users/Noy/Desktop/project7/Nand2Tetris_PROJ07/file.vm.txt")
    print(parsi.hasMoreCommands())
    print(parsi.hasMoreCommands())


if __name__ == "__main__":
    main()
