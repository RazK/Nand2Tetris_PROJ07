@256
D=A
@R0
M=D
@Sys.0_RETURN_HERE
D=A
@R0
A=M
M=D
@R0
M=M+1
@R1
D=M
@R0
A=M
M=D
@R0
M=M+1
@R2
D=M
@R0
A=M
M=D
@R0
M=M+1
@3
D=M
@R0
A=M
M=D
@R0
M=M+1
@R4
D=M
@R0
A=M
M=D
@R0
M=M+1
@R0
D=M
@R0
A=M
M=D
@R0
M=M+1
// __writePush
// __saveValueInTemp
@5
D=A
@5
M=D
@5
D=M
@R0
A=M
M=D
@R0
M=M+1
// writeArithmetic
// __writeBinary
@R0
M=M-1
A=M
D=M
A=A-1
M=M-D
// __writePop
// __writeLoadAddress
@R2
D=A
@5
M=D
@R0
M=M-1
A=M
D=M
@5
A=M
M=D
@R0
D=M
@R1
M=D
@Sys.init
D;JMP
(Sys.0_RETURN_HERE)
// FILE: C:\Users\Noy\Desktop\project7\Nand2Tetris_PROJ07\File.vm
// push constant 1
// __writePush
// __saveValueInTemp
@1

D=A
@5
M=D
@5
D=M
@R0
A=M
M=D
@R0
M=M+1
// push constant 2
// __writePush
// __saveValueInTemp
@2

D=A
@5
M=D
@5
D=M
@R0
A=M
M=D
@R0
M=M+1
// push constant 3
// __writePush
// __saveValueInTemp
@3

D=A
@5
M=D
@5
D=M
@R0
A=M
M=D
@R0
M=M+1
// call file.noy 3
@File.1_RETURN_HERE
D=A
@R0
A=M
M=D
@R0
M=M+1
@R1
D=M
@R0
A=M
M=D
@R0
M=M+1
@R2
D=M
@R0
A=M
M=D
@R0
M=M+1
@3
D=M
@R0
A=M
M=D
@R0
M=M+1
@R4
D=M
@R0
A=M
M=D
@R0
M=M+1
@R0
D=M
@R0
A=M
M=D
@R0
M=M+1
// __writePush
// __saveValueInTemp
@8
D=A
@5
M=D
@5
D=M
@R0
A=M
M=D
@R0
M=M+1
// writeArithmetic
// __writeBinary
@R0
M=M-1
A=M
D=M
A=A-1
M=M-D
// __writePop
// __writeLoadAddress
@R2
D=A
@5
M=D
@R0
M=M-1
A=M
D=M
@5
A=M
M=D
@R0
D=M
@R1
M=D
@file.noy
D;JMP
(File.1_RETURN_HERE)
// push constant 444
// __writePush
// __saveValueInTemp
@444

D=A
@5
M=D
@5
D=M
@R0
A=M
M=D
@R0
M=M+1
// goto END // skip noy definition
@init$END
D;JMP
// function file.noy 3
(file.noy)
D=0
@R0
A=M
M=D
@R0
M=M+1
D=0
@R0
A=M
M=D
@R0
M=M+1
D=0
@R0
A=M
M=D
@R0
M=M+1
// push constant 666
// __writePush
// __saveValueInTemp
@666

D=A
@5
M=D
@5
D=M
@R0
A=M
M=D
@R0
M=M+1
// return
@R1
D=M
@FRAME
M=D
@FRAME
D=M
@R0
A=M
M=D
@R0
M=M+1
// __writePush
// __saveValueInTemp
@5
D=A
@5
M=D
@5
D=M
@R0
A=M
M=D
@R0
M=M+1
// writeArithmetic
// __writeBinary
@R0
M=M-1
A=M
D=M
A=A-1
M=M-D
// POP DREG
@R0
M=M-1
A=M
D=M
// POP DREG finish
A=D
D=M
@RET
M=D
// OOOPPPPOOO
// POP DREG
@R0
M=M-1
A=M
D=M
// POP DREG finish
@R2
A=M
M=D
// OOOPPPPOOO out madafaka
@R2
D=M+1
@R0
M=D
@FRAME
A=M
A=A-1
D=A
@5
M=D
A=D
D=M
@THAT
M=D
@5
A=M
A=A-1
D=A
@5
M=D
A=D
D=M
@THIS
M=D
@5
A=M
A=A-1
D=A
@5
M=D
A=D
D=M
@ARG
M=D
@5
A=M
A=A-1
D=A
@5
M=D
A=D
D=M
@LCL
M=D
@5
A=M
@RET
A=M
D;JMP
// label END
(File.END)
