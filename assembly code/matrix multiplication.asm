# Multiplicates two matrix A and B
#
# To function correctly the first for four memory position must
# contain respectively the number of rows and columns of matrix A and
# the number of rows and columns of matrix B. In the rest of the data 
# are the values of the matrix A follow by the values of matrix B. The
# result matrix is stored after the last value of matrix B.

            li reg0, 0
            ld reg1, 0(reg0)            # reg1 = number of rows of matrix A
            ld reg2, 1(reg0)            # reg2 = number of columns of matrix A
            ld reg3, 2(reg0)            # reg3 = number of rows of matrix B
            ld reg4, 3(reg0)            # reg4 = number of columns of matrix B
            mult reg15, reg1, reg2
            mult reg6, reg3, reg4
            add reg5, reg15, reg6
            addi reg5, reg5, 4          # memory position of the resulting matrix

            li reg6, 0                  # reg6 = i loop index
for_i:      li reg7, 0                  # reg7 = j loop index
for_j:      li reg8, 0                  # reg8 = k loop index
            li reg9, 0                  # sum = 0
for_k:      mult reg10, reg6, reg2      
            add reg10, reg10, reg8      # reg10 = &A[i][k]
            ld reg11, 4(reg10)          # reg11 = A[i][k]
            mult reg12, reg8, reg2
            add reg12, reg12, reg7      
            add reg12, reg12, reg15     # reg12 = &B[k][j]
            ld reg13, 4(reg12)          # reg13 = B[k][j]
            mult reg11, reg11, reg13
            add reg9, reg9, reg11       # sum +=  A[i][k] * B[k][j]
            addi reg8, reg8, 1
            slt reg14, reg8, reg2
            bne reg14, reg0, for_k

            str reg9, 0(reg5)
            addi reg5, reg5, 1
            addi reg7, reg7, 1
            slt reg14, reg7, reg4
            bne reg14, reg0, for_j 

            addi reg6, reg6, 1
            slt reg14, reg6, reg1
            bne reg14, reg0, for_i