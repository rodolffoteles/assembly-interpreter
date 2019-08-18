# Assembly interpreter
Interpreter for a made-up assembly language. It simulates the code execution with different cache sizes and set quantities and then plots a graph comparing the miss rate.

![Barchart](https://user-images.githubusercontent.com/30675058/63219793-f3e59f80-c14f-11e9-905e-031a4a639a50.png)

This project was developed as an assigment for a computer architecture course to teach the principles of a cache memory.

## Language syntax
The language designed was based on the MIPS assembly so its has a similar syntax. The code must contain only one instruction per line, each one of them is compost of an optional label follow by a instrution's mnemonic and it's operands. Since this is a load/store architecture, only these two instructions can access memory. All other operantions must occur between registers, to access one use the `reg` keyword follow by the register's number. Comments are denoted with a `#`.

```assembly
# This is a comment
label: addi reg1, reg2, 2 
```
## Instructions available
<table>
    <tr>
        <th>Instruction</th>
        <th>Syntax</th>
        <th>Description</th>
    </tr>
    <tr>
        <th colspan="3">Arithmetic instructions</th>
      </tr>
    <tr>
       <td>Add</td>
       <td><code>add reg1, reg2, reg3</code></td>
       <td>Adds reg2 plus reg3 and stores the result in reg1</td>
    </tr>
    <tr>
       <td>Add immediate</td>
       <td><code>addi reg1, reg2, 1</code></td>
       <td>Adds reg2 plus one and stores the result in reg1</td>
    </tr>
    <tr>
       <td>Subtract</td>
       <td><code>sub reg1, reg2, reg3</code></td>
       <td>Subtracts reg2 minus reg3 and stores the result in reg1</td>
    </tr>
    <tr>
       <td>Subtract immediate</td>
       <td><code>subi reg1, reg2, 1</code></td>
       <td>Subtracts reg2 minus one and stores the result in reg1</td>
    </tr>
    <tr>
       <td>Multiply</td>
       <td><code>mult reg1, reg2, reg3</code></td>
       <td>Multiplies reg2 by reg3 and stores the result in reg1</td>
    </tr>
    <tr>
       <td>Multiply immediate</td>
       <td><code>multi reg1, reg2, 2</code></td>
       <td>Multiplies reg2 by two and stores the result in reg1</td>
    </tr>
    <tr>
       <td>Divide</td>
       <td><code>div reg1, reg2, reg3</code></td>
       <td>Divides reg2 by reg3 and stores the result in reg1</td>
    </tr>
    <tr>
       <td>Divide immediate</td>
       <td><code>divi reg1, reg2, 3</code></td>
       <td>Divides reg2 by three and stores the result in reg1</td>
    </tr>
    <tr>
        <th colspan="3">Data movement instructions</th>
    </tr>
    <tr>
       <td>Store</td>
       <td><code>str reg4, 0(reg2)</code></td>
       <td>Stores the reg4 value at the calculated address (reg2 + 0)</td>
    </tr>
    <tr>
       <td>Load</td>
       <td><code>ld reg1, 2(reg0)</code></td>
       <td>Loads into reg1 the value from the calculated address (reg0 + 2)</td>
    </tr>
    <tr>
       <td>Load immediate</td>
       <td><code>li reg1, 5</code></td>
       <td>Loads the immediate value five into reg1</td>
    </tr>
    <tr>
       <td>Move</td>
       <td><code>mov reg1, reg2</code></td>
       <td>Copies the reg2 to the reg1</td>
    </tr>
    <tr>
        <th colspan="3">Control flow instructions</th>
    </tr>
    <tr>
       <td>Jump</td>
       <td><code>jp target</code></td>
       <td>Jumps to the instruction with label "target"</td>
    </tr>
    <tr>
       <td>Branch on equal</td>
       <td><code>beq reg1, reg0, target</code></td>
       <td>Branches if the two registers are equal</td>
    </tr>
    <tr>
       <td>Branch on not equal</td>
       <td><code>bnq reg1, reg0, target</code></td>
       <td>Branches if the two registers are not equal</td>
    </tr>
    <tr>
       <td>Set on less than</td>
       <td><code>slt reg1, reg2, reg3</code></td>
       <td>If reg2 is less than reg3, reg1 is set to one. It gets zero otherwise.</td>
    </tr>
</table>

## Dependencies
To run this project you need to have both [python 3](https://www.python.org/) and the packages below installed. To install these, simply run the command `pip install <package>`.
 - numpy
 - matplotlib

## Usage
Run the `main.py` script passing the paths for the assembly file and secondary memory file as parameters.
```
python main.py <program_file> <data_file>
```
The secondary memory file follows a flat memory model and contains the data that will be processed, it must be arranged so that the n-th line contains only one integer that represents the data on the n-th memory position.