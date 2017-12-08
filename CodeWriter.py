from Utils import *

STATIC_VAR_NAME = "var"
NAME_INDEX = 0
LABEL_INDEX = 1
SYS_INIT = "Sys.init"
SYS_NUM_ARG = 0


class CodeWriter:
    def __init__(self, outfile):
        """
        Open the output file/stream and gets ready to write into it.
        """
        self.__output = outfile
        self.__stackSize = 0
        self.__unique_id = 0
        self.__current_file_name = None
        self.__current_func_name = None
        self.__nowDeclaringFunction = False

    def setFileName(self, file_name):
        # TODO: RazK, Noy: Decide on a naming convention for methods,
        # either 'someFuncDoesWhat' or 'some_func_does_what', and refactor all
        # code to stick with it.
        """
        Informs the code writer that the translation of a new VM file
        is started.
        :param file_name: The name of the output file.
        """
        self.__current_file_name = file_name

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

    def __writePush(self, vm_segment_name, index):
        """
        Writes the assembly code that pushes the value at the given segment
        with the given index to the top of the stack .
        :param vm_segment_name: segment name in vm language
        :param index: offset within the segment
        Example:
            LCL      = [ 1 ]
            RAM[LCL] = [300]
            RAM[300] = [xxx]
            writePushSegmentAddress(VM_LCL_SEG)
            --> pushes xxx, since RAM[RAM[LCL]] = RAM[RAM[1]] = RAM[300] = xxx
        """
        # Write comment in output
        self.writeComment("__writePush")

        # Prevent stack overflows
        if (self.__stackSize >= STACK_SIZE):
            raise OverflowError("Push operation will result in stack "
                                "overflow!")
        # Emulate memory address for constant using temp
        if vm_segment_name in [VM_CONSTANT_SEG]:
            self.__saveValueInTemp(index)
            # refer segment + index to the emulated memory
            self.__writeLine(LOAD_A + TEMP_0_ADDRESS)

        elif vm_segment_name in [VM_TEMP_SEG, VM_POINTER_SEG]:
            # Statically find address
            seg_addr = VM_SEGMENT_2_ADDRESS[vm_segment_name]
            self.__writeLine(LOAD_A + str(int(seg_addr) + int(index)))

        elif vm_segment_name in [VM_STATIC_SEG]:
            self.__writeLine(LOAD_A +
                             self.__appendFilenameToText(str(index)))

        else:
            # Load A with the specified address
            self.__writeLoadAddress(vm_segment_name, index)

        # Fetch the value at the specified address
        self.__writeLine(D_REG + ASSIGN + M_REG)

        # Enters the extracted value to the stack:
        self.__writeLine(LOAD_A + SP_SEG_ALIAS)
        self.__writeLine(A_REG + ASSIGN + M_REG)
        self.__writeLine(M_REG + ASSIGN + D_REG)

        # Increments SP:
        self.__writeLine(LOAD_A + SP_SEG_ALIAS)
        self.__writeLine(M_REG + ASSIGN + M_REG + ADD + ONE)
        self.__stackSize += 1

    def __writePop(self, vm_segment_name, index):
        """
        Writes the assembly code that pops the value at the top of the stack to
        the given segment at the given index.
        :param vm_segment_name: segment name in vm language
        :param index: offset within the segment
        """
        # Write comment in output
        self.writeComment("__writePop")

        # Prevent stack underflows
        if (self.__stackSize <= 0):
            raise OverflowError("Pop operation will result in stack "
                                "underflow!")

        if vm_segment_name in [VM_CONSTANT_SEG]:
            # Can't pop to constant segment
            raise ValueError(POP_FROM_CONSTANT_MSG)

        # Save pop destination address in A
        elif vm_segment_name in [VM_TEMP_SEG, VM_POINTER_SEG]:
            # Statically find address
            seg_addr = VM_SEGMENT_2_ADDRESS[vm_segment_name]
            self.__writeLine(LOAD_A + str(int(seg_addr) + int(index)))

        elif vm_segment_name in [VM_STATIC_SEG]:
            self.__writeLine(LOAD_A +
                             self.__appendFilenameToText(str(index)))

        else:
            # Dynamically resolve address
            self.__writeLoadAddress(vm_segment_name, index)

        # Keep destination in temp
        self.__writeLine(D_REG + ASSIGN + A_REG)
        self.__writeLine(LOAD_A + TEMP_SEG_ADDRESS)
        self.__writeLine(M_REG + ASSIGN + D_REG)

        # Decrements SP and extracts the topmost value of the stack to D:
        self.__writeLine(LOAD_A + SP_SEG_ALIAS)
        self.__writeLine(M_REG + ASSIGN + M_REG + SUB + ONE)
        self.__writeLine(A_REG + ASSIGN + M_REG)
        self.__writeLine(D_REG + ASSIGN + M_REG)
        self.__stackSize -= 1

        # Write the popped value (in D) to the destination (in temp)
        self.__writeLine(LOAD_A + TEMP_SEG_ADDRESS)
        self.__writeLine(A_REG + ASSIGN + M_REG)
        self.__writeLine(M_REG + ASSIGN + D_REG)

    def writeComment(self, comment):
        """
        Writes a comment line to the assembly.
        :param comment: comment to write to the assembly.
        """
        self.__writeLine("// {}".format(comment))

    def writePushPop(self, operation, vm_segment_name, index):
        """
        Writes the assembly code that is the translation of the given
        operation, where the operation is either C_PUSH or C_POP.
        :param operation: either C_PUSH or C_POP
        :param vm_segment_name: either ARG, THAT, THIS, LCL,
        :param index: The index of the wanted register in the segment.
        """

        # Write the appropriate command
        if operation == C_PUSH:
            self.__writePush(vm_segment_name, index)
        elif operation == C_POP:
            self.__writePop(vm_segment_name, index)
        else:
            raise ValueError(WRONG_COMMAND_TYPE_MSG)

    def __writeBinary(self, operation):
        """
        Translates the operations: x+y, x-y, x&y, x|y to assembly, and writs
        to the output file.
        :param operation: add , sub , or, and  operation in assembly.
        """
        # Write comment in output
        self.writeComment("__writeBinary")

        # Does the calculation on the stack :)
        self.__writeLine(LOAD_A + SP_SEG_ALIAS)
        self.__writeLine(M_REG + ASSIGN + M_REG + SUB + ONE)
        self.__writeLine(A_REG + ASSIGN + M_REG)
        self.__writeLine(D_REG + ASSIGN + M_REG)
        self.__writeLine(A_REG + ASSIGN + A_REG + SUB + ONE)
        self.__writeLine(M_REG + ASSIGN + M_REG + operation + D_REG)

    def __writeUnary(self, operation):
        """
        Translates the operations: -x, !x to assembly, and writs
        to the output file.
        :param operation: Either not or neg in assembly.
        """
        # Write comment in output
        self.writeComment("__writeUnary")

        # Manipulate directly on the stack (omg):
        self.__writeLine(LOAD_A + SP_SEG_ALIAS)
        self.__writeLine(M_REG + ASSIGN + M_REG + NEG_ONE)
        self.__writeLine(A_REG + ASSIGN + M_REG)
        self.__writeLine(M_REG + ASSIGN + operation + M_REG)
        self.__writeLine(LOAD_A + SP_SEG_ALIAS)
        self.__writeLine(M_REG + ASSIGN + M_REG + ADD + ONE)

    def __uniqueLabel(self, label):
        """
        Adds a unique id to the given label to prevent collisions with other
        labels carrying the same name.
        Example:
            __uniqueLabel("TRUE") --> "TRUE_1"
        :param label: label to localize
        :return: Given label with a unique identifier.
        """
        unique_label = "{}{}{}".format(label, UNIQUE_DELIMITER,
                                       self.__unique_id)
        self.__unique_id += 1
        return unique_label

    def __appendFilenameToText(self, text):
        """
        Appends the name of the current file before the given variable's name.
        Example:
            Filename = "Foo.vm"
            __appendFilenameToText("bar") --> "Foo.bar"
        :param text:
        :return: the name of the variable appended with the current filename.
        """
        # Extract the filename without the extension
        base = self.__current_file_name.split(EXTENSION_DELIMITER)[0]
        return "{}{}{}".format(base, LABEL_DELIMITER, text)

    def __appendFuncDollarToText(self, text):
        """
        Appends the name of the current function + $ before the given
        text.
        Example:
            Function = "sys.bar"
            __appendFilenameToText("CYBER") --> "sys.bar$CYBER"
        :param text: inner label
        :return: the name of the variable appended with the current
        filename.function
        """
        func = self.__current_func_name
        return "{}{}{}".format(func, INNER_LABEL_DELIMITER, text)

    def __isNegative(self):
        """
        Compares the value in a cell pointed by A to 0 and keeps the result in
        temp 0.
        The result should be 1 if negative and 0 otherwise.
        """

    def __writeComparative(self, operation, overflowSafe=False):
        """
        Translates the operations: x=y, x>y, x<y to assembly, and writes
        to the output file.
        :param operation: eq, gt, lt.
        """
        # Write comment in output
        self.writeComment("__writeComparative")

        # Subtracting the values in the two topmost cells:
        self.__writeBinary(SUB)

        # Keeps the result in Temp 0 segment:
        self.__writePop(VM_TEMP_SEG, INDEX_0)

        # Initializes Temp 1 to be 0:
        self.__writeLine(LOAD_A + TEMP_1_ADDRESS)
        self.__writeLine(M_REG + ASSIGN + ZERO)

        # Initializes D with the Subtraction result:
        self.__writeLine(LOAD_A + TEMP_0_ADDRESS)
        self.__writeLine(D_REG + ASSIGN + M_REG)

        # If the comparision result is T, changes temp 1 to "-1":
        TRUE_LABEL = self.__uniqueLabel(TRUE_ADDRESS)
        self.__writeLine(LOAD_A + TRUE_LABEL)
        self.__writeLine(operation)

        # Else, it remains "0":
        FALSE_LABEL = self.__uniqueLabel(FALSE_ADDRESS)
        self.__writeLine(LOAD_A + FALSE_LABEL)
        self.__writeLine(A_JUMP)
        self.__writeLine(declareLabel(TRUE_LABEL))
        self.__writeLine(LOAD_A + TEMP_1_ADDRESS)
        self.__writeLine(M_REG + ASSIGN + NEG_ONE)
        self.__writeLine(declareLabel(FALSE_LABEL))

        # Pushes the result back to the stack:
        self.__writePush(VM_TEMP_SEG, INDEX_1)

    def writeArithmetic(self, operation):
        """
        Writes the assembly code that is the translation of the given
        arithmetic operation.
        :param operation: The arithmetic command to be translated.
        """
        # Write comment in output
        self.writeComment("writeArithmetic")

        if operation in ARITHMETIC_BINARY:
            self.__writeBinary(operation)

        elif operation in ARITHMETIC_UNARY:
            self.__writeUnary(operation)

        elif operation in ARITHMETIC_COMPARE:
            self.__writeComparative(operation)

        else:
            raise ValueError(NOT_AN_OPERATION_MSG)

    def __saveValueInTemp(self, value):
        """
        Saves the given value in the temp register.
        :param value: Numeric value to save in the temp register
        """

        # Write comment in output
        self.writeComment("__saveValueInTemp")

        safe_value = str(value)
        self.__writeLine(LOAD_A + safe_value)
        self.__writeLine(D_REG + ASSIGN + A_REG)
        self.__writeLine(LOAD_A + TEMP_0_ADDRESS)
        self.__writeLine(M_REG + ASSIGN + D_REG)
        pass

    def __writeLoadAddress(self, vm_segment_name, index):
        """
        Writes the address specified by the given segment with the given
        offset to the A register.
        Notice! D_REG is used here and values it held before the call are LOST!
        :param vm_segment_name: Name of the desired segment (should be a key
        in the SEGMENTS dict)
        :param index: Offset relative to the given segment.
        """
        # Write comment in output
        self.writeComment("__writeLoadAddress")

        # TODO: RazK: Check parameters validity
        # Load A reg with the specified segment address
        self.__writeLine(LOAD_A + VM_SEGMENT_2_ADDRESS[vm_segment_name])

        # Add offset if exists
        if (index != 0):
            self.__writeLine(D_REG + ASSIGN + M_REG)
            self.__writeLine(LOAD_A + str(index).strip("\n"))
            self.__writeLine(A_REG + ASSIGN + D_REG + ADD + A_REG)

    def writeInit(self):
        """
        Writes the assembly code that effects the VM initialization
        (also called bootstrap code).
        This code should be placed in the ROM beginning in address 0x0000.
        """

        # Initializes the stack base to be 256:
        self.__writeLine(LOAD_A + STACK_STANDARD_BASE)
        self.__writeLine(D_REG + ASSIGN + A_REG)
        self.__writeLine(LOAD_A + SP_SEG_ALIAS)
        self.__writeLine(M_REG + ASSIGN + D_REG)

        # Calls sys.init:
        self.writeCall(SYS_INIT, SYS_NUM_ARG)

    def __writeLoadLabel(self, label):
        """
        Loads the given label in correct file-appending mode
        Example:
            (Not in function)
            __writeLoadLabel("CYBER") --> @CYBER
            (In function Foo in file Xxx)
            __writeLoadLabel("CYBER") --> Xxx.Foo@CYBER
        """
        dest = label
        if (self.__current_func_name != None):
            dest = self.__appendFuncDollarToText(label)
        self.__writeLine(LOAD_A + dest)

    def writeLabel(self, label):
        """
        Writes the assembly code that is the translation of the given
        label command.
        Appends the label to filename
        Example:
            FuncName: foo.bar
            Label CYBER --> (foo.bar$CYBER)
        :param label: label name to declare
        """
        dest = label
        if (self.__current_func_name != None):
            dest = self.__appendFuncDollarToText(label)
        self.__writeLine(declareLabel(dest))

    def writeGoto(self, label):
        """
        Writes the assembly code that is the translation of the given goto
        command.
        :param label: The place that we are going to jump to,
                                    assuming it exists.
        """
        self.__writeLoadLabel(label)
        self.__writeLine(A_JUMP)

    def writeIf(self, label):
        """
        Writes the assembly code that is the translation of the given
        if-goto command
        :param label:   label to jump if the value at the top of the stack is
                        zero.
        """
        # Pops the value from the top of the stack and compares it to zero
        self.__writePop(VM_TEMP_SEG, INDEX_0)  # Pop --> temp
        self.__writeLine(LOAD_A + TEMP_SEG_ADDRESS)  # @temp
        self.__writeLine(D_REG + ASSIGN + M_REG)  # D = RAM[temp]
        self.__writeLoadLabel(label)
        self.__writeLine(A_NE)  # Jump if D != 0

    def __writePushSegmentAddress(self, segmentName):
        """
        writes the assembly code that pushes the address of the given
        segment to the stack.
        :param segmentName:
        :return:
        Example:
            LCL      = [ 1 ]
            RAM[LCL] = [300]
            writePushSegmentAddress(VM_LCL_SEG)
            --> pushes [300], because RAM[LCL] = 300
        """
        if segmentName not in {VM_THAT_SEG, VM_THIS_SEG, VM_LCL_SEG,
                               VM_ARG_SEG}:
            raise ValueError("Segment not supported")

        segmentAddress = VM_SEGMENT_2_ADDRESS[segmentName]
        self.__writeLine(LOAD_A + segmentAddress)  # @SEG
        self.__writeLine(D_REG + ASSIGN + M_REG)  # @D = RAM[SEG]
        self.__writePushDREG()

    def __writePopSegmentAddress(self, segmentName):
        """
        writes the assembly code that pushes the address of the given
        segment to the stack.
        :param segmentName:
        :return:
        Example:
            LCL      = [ 1 ]
            RAM[LCL] = [300]
            writePushSegmentAddress(VM_LCL_SEG)
            --> pushes [300], because RAM[LCL] = 300
        """
        if segmentName not in {VM_THAT_SEG, VM_THIS_SEG, VM_LCL_SEG,
                               VM_ARG_SEG}:
            raise ValueError("Segment not supported")
        segmentAddress = VM_SEGMENT_2_ADDRESS[segmentName]
        self.__writePopDREG()  # D=STACK[top]
        self.__writeLine(LOAD_A + segmentAddress)  # @SEG
        self.__writeLine(M_REG + ASSIGN + D_REG)  # RAM[SEG]=D

    def __writePushDREG(self):
        """
        Pushes the value in D_REG to the stack
        """
        self.__writeLine(LOAD_A + SP_SEG_ALIAS)  # @SP
        self.__writeLine(A_REG + ASSIGN + M_REG)  # A=M
        self.__writeLine(M_REG + ASSIGN + D_REG)  # M=D
        self.__writeLine(LOAD_A + SP_SEG_ALIAS)  # @SP
        self.__writeLine(M_REG + ASSIGN + M_REG + ADD + ONE)  # SP=SP+1
        self.__stackSize += 1

    def __writePopDREG(self):
        """
        Pops the value from the stack to D_REG
        """
        self.writeComment("POP DREG")
        self.__writeLine(LOAD_A + SP_SEG_ALIAS)  # @SP
        self.__writeLine(M_REG + ASSIGN + M_REG + SUB + ONE)  # SP=SP-1
        self.__writeLine(A_REG + ASSIGN + M_REG)  # A=M
        self.__writeLine(D_REG + ASSIGN + M_REG)  # D=M
        self.writeComment("POP DREG finish")
        self.__stackSize -= 1

    def writeCall(self, fileAppendedFuncName, numArgs):
        """
        Writes the assembly code that is the translation of the given Call
        command.
        :param fileAppendedFuncName: filename-attached-label of the function to
                                     call
        :param numArgs: number of arguments in the stack before the function
                        was called
        """
        # Push return address
        unique_label = self.__uniqueLabel(RETURN_LABEL)
        self.__writeLoadLabel(unique_label)
        self.__writeLine(D_REG + ASSIGN + A_REG)  # D=A
        self.__writePushDREG()

        # Push LCL
        self.__writePushSegmentAddress(VM_LCL_SEG)

        # Push ARG
        self.__writePushSegmentAddress(VM_ARG_SEG)

        # Push THIS
        self.__writePushSegmentAddress(VM_THIS_SEG)

        # Push THAT
        self.__writePushSegmentAddress(VM_THAT_SEG)

        # ARG = SP-(n+5)
        # Push SP
        self.__writeLine(LOAD_A + SP_SEG_ALIAS)
        self.__writeLine(D_REG + ASSIGN + M_REG)
        self.__writePushDREG()
        # Push n+5
        self.__writePush(VM_CONSTANT_SEG, (int(numArgs) +
                                           NUM_OF_PUSHED_SEGMENTS))
        # sub
        self.writeArithmetic(A_SUB)
        # pop --> ARG
        self.__writePop(VM_ARG_SEG, INDEX_0)
        # LCL = SP
        self.__writeLine(LOAD_A + SP_SEG_ALIAS)
        self.__writeLine(D_REG + ASSIGN + M_REG)
        self.__writeLine(LOAD_A + LCL_SEG_ALIAS)
        self.__writeLine(M_REG + ASSIGN + D_REG)
        # goto f
        self.__writeLine(LOAD_A + fileAppendedFuncName)
        self.__writeLine(A_JUMP)

        # Label return address after method call
        self.writeLabel(unique_label)

    def StripFileName(self, file_appended_label):
        """
        returns the label following the file prefix.
        Example:
        file.SomeLabel --> SomeLabel
        :param file_appended_label:
        :return: label without prefix
        """
        return file_appended_label.split(LABEL_DELIMITER)[1]

    def saveAToTemp(self):
        """
        Saves The contentnts of the A register to Temp0
        """
        self.__writeLine(D_REG + ASSIGN + A_REG)
        self.__writeLine(LOAD_A + TEMP_0_ADDRESS)
        self.__writeLine(M_REG + ASSIGN + D_REG)
        self.__writeLine(A_REG + ASSIGN + D_REG)

    def loadAFromTemp(self):
        """
        Loads the current value in temp0 to A.
        """
        self.__writeLine(LOAD_A + TEMP_0_ADDRESS)
        self.__writeLine(A_REG + ASSIGN + M_REG)

    def __restorSegment(self, vm_seg_name):
        """
        Restores the relevant segment to it's previous state before the call.
        """
        self.__writeLine(A_REG + ASSIGN + A_REG + NEG_ONE)
        self.saveAToTemp()
        self.__writeLine(D_REG + ASSIGN + M_REG)
        self.__writeLine(LOAD_A + vm_seg_name)
        self.__writeLine(M_REG + ASSIGN + D_REG)
        self.loadAFromTemp()

    def writeReturn(self):
        """
        Writes the assembly code that is the slation of the given Return
        command.
        """
        # FRAME = LCL
        self.__writeLine(LOAD_A + LCL_SEG_ALIAS)  # @LCL
        self.__writeLine(D_REG + ASSIGN + M_REG)  # D=M
        self.__writeLine(LOAD_A + VAR_FRAME)  # @FRAME
        self.__writeLine(M_REG + ASSIGN + D_REG)  # M=D

        # RET = *(*FRAME-5)
        # Push FRAME
        self.__writeLine(LOAD_A + VAR_FRAME)  # A = FRAME
        self.__writeLine(D_REG + ASSIGN + M_REG)  # D = *FRAME
        self.__writePushDREG()  # Push(*FRAME)
        # Push 5
        self.__writePush(VM_CONSTANT_SEG, NUM_OF_PUSHED_SEGMENTS)
        # sub
        self.writeArithmetic(A_SUB)

        #  pop (*FRAME-5) --> D_REG
        self.__writePopDREG()
        #  RET = *(*FRAME-5)
        self.__writeLine(A_REG + ASSIGN + D_REG)  # A =  (*FRAME-5)
        self.__writeLine(D_REG + ASSIGN + M_REG)  # D = *(*FRAME-5)
        self.__writeLine(LOAD_A + VAR_RET)
        self.__writeLine(M_REG + ASSIGN + D_REG)  # *RET = *(*FRAME-5)

        # *ARG = pop()
        self.writeComment("OOOPPPPOOO")
        self.__writePopDREG()  # D = pop()
        self.__writeLine(LOAD_A + ARG_SEG_ALIAS)  # A =  ARG
        self.__writeLine(A_REG + ASSIGN + M_REG)  # A = *ARG
        self.__writeLine(M_REG + ASSIGN + D_REG)  # *ARG = D
        self.writeComment("OOOPPPPOOO out madafaka")

        # SP = ARG + 1
        self.__writeLine(LOAD_A + ARG_SEG_ALIAS)  # @ARG
        self.__writeLine(D_REG + ASSIGN + M_REG + ADD + ONE)  # D=M+1
        self.__writeLine(LOAD_A + SP_SEG_ALIAS)  # @SP
        self.__writeLine(M_REG + ASSIGN + D_REG)  # M=D

        # Restores the values of THIS, THAT, ARG, LCL:
        self.__writeLine(LOAD_A + VAR_FRAME)
        self.__writeLine(A_REG + ASSIGN + M_REG)

        self.__restorSegment(ASM_THAT_SEG)
        self.__restorSegment(ASM_THIS_SEG)
        self.__restorSegment(ASM_ARG_SEG)
        self.__restorSegment(ASM_LOCAL_SEG)

        self.__writeLine(LOAD_A + VAR_RET)
        self.__writeLine(A_REG + ASSIGN + M_REG)
        self.__writeLine(A_JUMP)

        # THAT = *(FRAME-1)
        # self.__writeLine(LOAD_A + VAR_FRAME)                    # A=  FRAME
        # self.__writeLine(A_REG + ASSIGN + M_REG + SUB + ONE)    # A= (*FRAME-1)
        # self.__writeLine(D_REG + ASSIGN + M_REG)                # D=*(*FRAME-1)
        # self.__writeLine(LOAD_A + THAT_SEG_ALIAS)               # A=THAT
        # self.__writeLine(M_REG + ASSIGN + D_REG)




        # THIS = *(FRAM-2)

    def writeFunction(self, functionName, numLocals):
        """
        Writes the assembly code that is the trans. of the given Function
        command.
        :param functionName: NON file-appended name of the function to declare
        :param numLocals:   number of arguments pushed to the stack before
                            calling this function
        """
        self.__current_func_name = functionName
        self.__writeLine(declareLabel(functionName))
        for local in range(int(numLocals)):
            self.__writeLine(D_REG + ASSIGN + ZERO)
            self.__writePushDREG()

    def labelWize(self, label):
        """
        If no current function: label
        If current function but not declaring function: file.function$label
        If current function and declaring function: file.label
        :param label:
        :return: decorated label acording to current state
        """


def main():
    """
    Tests for the CodeWriter module
    """
    with open("file.asm", "w+") as f:
        gustav = CodeWriter(f)
        gustav.writeInit()
        # gustav.writePushPop("C_POP", "static", 17)


if __name__ == "__main__":
    main()
