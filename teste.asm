ld mem1, reg2 
ld mem2, reg3
add reg0, reg2, reg3
addi reg2, reg2, 5
str mem1, reg0
beq reg2, reg3, 0
addi reg3, reg3, 1
eof