import os
import sys
from CodeWriter import CodeWriter
from Parser import Parser
from Utils import *

VM_EXTENSION = ".vm"
ASM_EXTENSION = ".asm"
#DEFAULT_VM_FILE = "C:\\Users\\Noy\\Desktop\\nand2tetris\\projects\\07\\StackArithmetic\\SimpleAdd\\SimpleAdd.vm"
DEFAULT_VM_FILE = "..\\..\\StackArithmetic\\SimpleAdd"
# "#"test\\underflow.vm"
DEFAULT_VM_DIR = "..\\..\\MemoryAccess\\BasicTest"

def main(path):
    """
    Translate the vm file (or files) in the given path into .asm assembly
    files to be assembled by the assembler.
    """
    # Collect all .vm files to assemble
    sources = None
    base = os.path.splitext(path)[0]

    # Path is a single vm file?
    if os.path.isfile(path):
        if not path.endswith(VM_EXTENSION):
            raise FileNotFoundError("Invalid extension '{}' for virtual  "
                                    "machine file (expected '{}')"
                                    .format(path, VM_EXTENSION))
        sources = [path]

    # Path is a directory with vm files?
    elif os.path.isdir(path):
        sources = [os.path.join(path, f) for f in os.listdir(path) if
                   f.endswith(VM_EXTENSION)]
        foldername = os.path.basename(os.path.normpath(base))
        base = os.path.join(base, foldername)

    if sources == None:
        raise FileNotFoundError("No {} files found to translate!"
                                .format(VM_EXTENSION))

    output = base + ASM_EXTENSION

    # Assemble all files
    translate(sources, output)


def translate(sources, output):
    """
    Translate the file specified by filename into a binary
    .hack file to be executed on the Hack computer.
    """

    # Open the output for writing
    with open(output, 'w') as out:
        writer = CodeWriter(out)

        # Parse each source and translate to it the output
        for sourcefile in sources:

            # Open source for translation, output file for writing
            with open(sourcefile, 'r') as source:
                parser = Parser(source)
                writer.setFileName(os.path.basename(sourcefile))
                writer.writeComment("FILE: {}".format(sourcefile))

                # Parse each command line in the source and translate
                while (parser.hasMoreCommands()):

                    # Write comment of current command
                    writer.writeComment(
                        parser.getCurrCommand().strip(NEW_LINE))

                    # Parse command
                    operation = parser.getOperation()

                    if operation in C_OPERATIONS_PUSH_POP:
                        segment = parser.arg1()
                        index = parser.arg2()
                        writer.writePushPop(operation, segment, index)

                    elif operation in A_OPERATIONS_ANY:
                        writer.writeArithmetic(operation)
                    parser.advance()

            # Flush translation to file
            out.flush()

if (__name__ == "__main__"):
    if len(sys.argv) > 1:
        main(sys.argv[1])
    else:
        main(DEFAULT_VM_FILE)
