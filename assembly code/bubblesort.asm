# Sorts a given array through bubble sort
#
# To function correctly the data must be arranged so that
# the first memory position contains the array size and the 
# rest the arrays values. The sorted array is overwritten
# on these original values.

        li reg0, 0                  # reg0 = 0
        ld reg1, 0(reg0)            # reg1 = array size
while:  li reg2, 1                  # reg2 is the index i
        li reg8, 0                  # reg8 is the switch counter 
for:    ld reg3, 0(reg2)            # load array[i] and array[i+1]
        ld reg4, 1(reg2)       
        slt reg5, reg4, reg3        # if it's ordered skip the switch
        beq reg5, reg0, cont
        str reg4, 0(reg2)           # swith the values and increment reg8
        str reg3, 1(reg2) 
        addi reg8, reg8, 1
cont:   addi reg2, reg2, 1          # increment index and check if occured switches
        slt reg5, reg2, reg1
        bne reg5, reg0, for
        bne reg8, reg0, while