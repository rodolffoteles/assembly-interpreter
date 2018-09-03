ld reg2, mem2 
ld reg3, mem3
add reg0, reg2, reg3
addi reg2, reg2, 5
str mem2, reg0
jeq reg2, reg3, 0
addi reg3, reg3, 1
eof