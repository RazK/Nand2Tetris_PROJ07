import os
import sys
from src.Nand2Tetris_PROJ07.CodeWriter import CodeWriter
from src.Nand2Tetris_PROJ07.Parser import Parser
from src.Nand2Tetris_PROJ07.Utils import *

VM_EXTENSION = ".vm"
ASM_EXTENSION = ".asm"
DEFAULT_VM_FILE = "test\\foo.vm"
DEFAULT_VM_DIR = "..\\..\\MemoryAccess\\BasicTest"

def main(path):
    """
    Translate the vm file (or files) in the given path into .asm assembly
    files to be assembled by the assembler.
    """
    # Collect all .vm files to assemble
    sources = None

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

    if sources == None:
        raise FileNotFoundError("No .asm files found to assemble!")

    base = os.path.splitext(path)[0]
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
                writer.writeComment(sourcefile)

                # Parse each command line in the source and translate
                while (parser.hasMoreCommands()):
                    operation = parser.getOperation()

                    if operation in OPERATIONS_PUSH_POP:
                        segment = parser.arg1()
                        index = parser.arg2()
                        writer.writePushPop(operation, segment, index)

                    elif operation in OPERATIONS_ARITHMETIC:
                        writer.writeArithmetic(operation)
                    parser.advance()

            # Flush translation to file
            out.flush()

if (__name__ == "__main__"):
    if len(sys.argv) > 1:
        main(sys.argv[1])
    else:
        main(DEFAULT_VM_DIR)
