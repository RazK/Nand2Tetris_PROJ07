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


class Parser:
    def __init__(self, vm_file):
        """
        Opens the input file/stream and gets ready to parse it.
        :param filename: An open hack assembly file descriptor (reading only)
        """
        pass

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
        pass

    def arg1(self):
        """
        Returns the first argument of the current command.
        In the case of C_ARITHMETIC, the command itself (add, sub, etc.) is
        returned.
        Should not be called if the current command is C_RETURN.
        :return: string (Type of the current command)
        """
        pass

    def arg2(self):
        """
        Returns the second argument of the current command.
        Should be called only if the current command is C_PUSH, C_POP,
        C_FUNCTION, or C_CALL.
        :return: Second argument of the current command
        """
        pass


def main():
    """
    Tests for the Parser module
    """
    pass

if __name__ == "__main__":
    main()