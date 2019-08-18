from re import sub, search, match
from numpy import zeros
from math import ceil

NO_INSTRUCTION_REGEX = '^\s*(#.*)?\s*$'
COMMENT_REGEX = '#.*$'
LABEL_REGEX = '.*:'

class MainMemory:
    '''Simulates the behaviour of a RAM memory'''

    def __init__(self, mem_size, block_size, program_file, data_file, save_allowed):
        '''
        Parameters:
            mem_size - Total number of words in memory
            block_size - Size of blocks in which memory is divided
            program_file - Path assembly file to be loaded in memory
            data_file - Path of file where the data is stored
            save_allowed - Indicates whether or not to update secondary memory 
        '''

        self.save_allowed = save_allowed
        self.mem_size = mem_size
        self.block_size = block_size
        self.block_count = ceil(mem_size/block_size)

        self.instructions = []
        self.load_program(program_file)

        self.data = zeros((self.block_count, block_size), dtype=int)
        self.data_file = data_file
        self.load_data(data_file)

    def link_jumps(self, labels_addresses, jump_addresses):
        '''Replaces the label's names with their proper addresses in jump instructions'''

        for address in jump_addresses:
            instruction = self.instructions[address]
            j = 0 if instruction['opcode'] == 'jp' else 2
            self.instructions[address]['operands'][j] = labels_addresses[instruction['operands'][j]]

    def load_program(self, program_file):
        '''Loads and tokenize the assembly code'''

        labels_addresses = {}
        jump_addresses = []

        with open(program_file,'r') as file:
            body = [l for l in file.readlines() if not match(NO_INSTRUCTION_REGEX, l)]

            for index, line in enumerate(body): 
                code = sub(COMMENT_REGEX, '', line)
                label = search(LABEL_REGEX, code)

                if label:
                    # The instruction has a label, save both the label 
                    # name and the instruction address to link later
                    begin, end = label.span()
                    labels_addresses[code[begin:end-1]] = str(index)
                    code = code[end:]
                
                code = code.strip().split(' ')

                if code[0] in ['jp', 'beq', 'bne']:
                    jump_addresses.append(index)

                self.instructions.append({
                    'opcode': code[0],
                    'operands': code[1:]
                    })   

        self.link_jumps(labels_addresses, jump_addresses)

    def load_data(self, data_file):
        '''Loads data from a secondary memory'''

        with open(data_file, 'r') as file:
            for index in range(self.mem_size):
                value = file.readline()

                # Reached end of secondary memory, stop reading
                if not value: break

                i, j = divmod(index, self.block_size)
                self.data[i][j] = int(value)

    def save(self):
        '''Save the current memory state back to secondary memory'''
        
        if self.save_allowed:
            with open(self.data_file, 'w') as file:
                for block in range(self.block_count):
                    file.write('\n'.join([str(b) for b in self.data[block]]))
                    file.write('\n')

    def get_instruction(self, address):
        return self.instructions[address] if address < len(self.instructions) else None

    def write(self, address, data):
        block, word = divmod(address, self.block_size)
        self.data[block][word] = data

    def read(self, address):
        block, word = divmod(address, self.block_size)
        return self.data[block][word]

    def read_block(self, address):
        block, word = divmod(address, self.block_size)
        return self.data[block]