# Calculates the mean of a given list of numbers
#
# To function correctly the data must be arranged so that
# the first memory position contains the array size and the 
# rest the arrays values. The mean is be stored next to the
# last array number.
        
        li reg0, 0
        ld reg1, 0(reg0)        # reg1 = array length
        li reg2, 0              # reg2 = 0
        li reg4, 0              # reg4 = 0
        
loop:   addi reg2, reg2, 1      # reg2++
        ld reg3, 0(reg2), 0     # load array[reg2]
        add reg4, reg4, reg3    # reg4 += reg3
        subi reg1, reg1, 1      # reg1--
        slt reg5, reg0, reg1    # if reg1 > 0: reg5 = 1
        bne reg5, reg0, loop    # if reg5 != 0 jump loop

        ld reg1, 0(reg0)        # reg1 = array length
        mov reg3, reg1          # reg3 = array length + 1
        addi reg3, reg3, 1      
        div reg2, reg4, reg1    # reg2 = reg4/reg1
        str reg2, 0(reg3)       # mem(reg3) = reg2