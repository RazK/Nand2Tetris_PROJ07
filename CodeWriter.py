from Utils import *


class CodeWriter:
    def __init__(self, outfile):
        """
        Open the output file/stream and gets ready to write into it.
        """
        pass

    def writeArithmetic(self, command):
        """
        Writes the assembly code that is the translation of the given
        arithmetic command.
        :param command: String (the VM arithmetic command)
        """
        pass

    def writePushPop(self, command, segment, index):
        """
        Writes the assembly code that us the translation of the given
        command, where the command is either C_PUSH or C_POP.
        :param command: either C_PUSH or C_POP
        :param segment: either ARG, THAT, THIS,
        :param index:
        :return:
        """
        if command == C_PUSH:
            pass
            # TODO: Noy: Implement + Test
        elif command == C_POP:
            pass
            # TODO: Noy: Implement _ Test
        else:
            pass
            # TODO: Raise exception? Or just do nothing

    def close(self):
        """
        Closes the output file/stream.
        """
        pass
