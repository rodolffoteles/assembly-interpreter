from numpy import zeros
from re import sub, search

ALU_CYCLES = 1
MEMORY_CYCLES = 100
JUMP_CYCLES = 5

class Processor:
    '''Simulates the behaviour of a CPU'''

    def __init__(self, main_memory, cache, register_count=16):
        '''
        Parameters:
            main_memory - Main memory of the processor
            cache - Cache memory of the processor
            register_count - Quantity of registers in the processor (default is 16)
        '''

        self.main_memory = main_memory
        self.cache = cache
        self.registers = zeros(register_count, dtype=int)
        self.clock_cycle = 0
        self.ir = ''
        self.program_counter = 0

        self.operand_regex = {
            'register': '(?<=reg)\d*',
            'immediate': '\d*',
            'offset': '\d*(?=\(reg\d*\))'
            }

        self.switcher = {
            'add': {'function': self.add, 'operands': ['register', 'register', 'register']},
            'addi': {'function': self.addi, 'operands': ['register', 'register', 'immediate']},
            'sub': {'function': self.sub, 'operands': ['register', 'register', 'register']},
            'subi': {'function': self.subi, 'operands': ['register', 'register', 'immediate']},
            'mult': {'function': self.mult, 'operands': ['register', 'register', 'register']},
            'multi': {'function': self.multi, 'operands': ['register', 'register', 'immediate']},
            'div': {'function': self.div, 'operands': ['register', 'register', 'register']},
            'divi': {'function': self.divi, 'operands': ['register', 'register', 'immediate']},
            'str': {'function': self.store, 'operands': ['register', ['offset', 'register']]},
            'ld': {'function': self.load, 'operands': ['register', ['offset', 'register']]},
            'li': {'function': self.li, 'operands':  ['register', 'immediate']},
            'mov': {'function': self.move, 'operands': ['register', 'register']},
            'jp': {'function': self.jump, 'operands': ['immediate']},
            'beq': {'function': self.beq, 'operands': ['register', 'register', 'immediate']},
            'bne': {'function': self.bne, 'operands': ['register', 'register', 'immediate']},
            'slt': {'function': self.slt, 'operands': ['register', 'register', 'register']},
            }

        self.execute()

    def execute(self):
        while(True):
            self.ir = self.main_memory.get_instruction(self.program_counter)

            # No instruction to execute, save the data to the secondary memory and stop
            if not self.ir:
                break

            self.program_counter += 1
            self.decode(**self.ir)

    def decode(self, opcode, operands):
        self.switcher[opcode]['function'](opcode, operands)
        
    def process_operands(self, opcode, operands):
        operands_category = self.switcher[opcode]['operands']

        if len(operands) != len(operands_category):
            raise Exception(f'Wrong number of operands for {opcode} instruction')
        
        processed_operands = []
        for operand, categories in zip(operands, operands_category):
            # The inner for loop is needed in order to extract both the offset and register 
            # from the second operand of load/store insctrution since they look like "0(reg1)"
            category_list = categories if isinstance(categories, list) else [categories]

            for category in category_list:
                matched = search(self.operand_regex[category], operand)

                if not matched:
                    raise Exception(f'Wrong operands for {opcode} instruction, expected a {category}')
                
                start, end = matched.span()
                processed_operands.append(int(operand[start:end]))
        
        return processed_operands

    def add(self, opcode, operands):
        destination, first, second = self.process_operands(opcode, operands)
        self.registers[destination] = self.registers[first] + self.registers[second]
        self.clock_cycle += ALU_CYCLES

    def addi(self, opcode, operands):
        destination, first, immediate = self.process_operands(opcode, operands)
        self.registers[destination] = self.registers[first] + immediate
        self.clock_cycle += ALU_CYCLES

    def sub(self, opcode, operands):
        destination, first, second = self.process_operands(opcode, operands)
        self.registers[destination] = self.registers[first] - self.registers[second]
        self.clock_cycle += ALU_CYCLES

    def subi(self, opcode, operands):
        destination, first, immediate = self.process_operands(opcode, operands)
        self.registers[destination] = self.registers[first] - immediate
        self.clock_cycle += ALU_CYCLES

    def mult(self, opcode, operands):
        destination, first, second = self.process_operands(opcode, operands)
        self.registers[destination] = self.registers[first] * self.registers[second]
        self.clock_cycle += ALU_CYCLES

    def multi(self, opcode, operands):
        destination, first, immediate = self.process_operands(opcode, operands)
        self.registers[destination] = self.registers[first] * immediate
        self.clock_cycle += ALU_CYCLES

    def div(self, opcode, operands):
        destination, first, second = self.process_operands(opcode, operands)
        self.registers[destination] = self.registers[first] / self.registers[second]
        self.clock_cycle += ALU_CYCLES

    def divi(self, opcode, operands):
        destination, first, immediate = self.process_operands(opcode, operands)
        self.registers[destination] = self.registers[first] / immediate
        self.clock_cycle += ALU_CYCLES

    def store(self, opcode, operands):
        source, offset, destination = self.process_operands(opcode, operands)
        data = self.registers[source]
        address = self.registers[destination]
        self.cache.write(address + offset, data)
        self.clock_cycle += MEMORY_CYCLES

    def li(self, opcode, operands):
        destination, immediate = self.process_operands(opcode, operands)
        self.registers[destination] = immediate
        self.clock_cycle += MEMORY_CYCLES

    def load(self, opcode, operands):
        destination, offset, source = self.process_operands(opcode, operands)
        address = self.registers[source]
        self.registers[destination] = self.cache.read(address + offset)
        self.clock_cycle += MEMORY_CYCLES

    def move(self, opcode, operands):
        destination, source = self.process_operands(opcode, operands)
        self.registers[destination] = self.registers[source]
        self.clock_cycle += ALU_CYCLES

    def jump(self, opcode, operands):
        address = self.process_operands(opcode, operands)
        self.program_counter = address
        self.clock_cycle += JUMP_CYCLES

    def beq(self, opcode, operands):
        first, second, address = self.process_operands(opcode, operands)
        self.clock_cycle += JUMP_CYCLES
        if self.registers[first] == self.registers[second]:
            self.program_counter = address

    def bne(self, opcode, operands):
        first, second, address = self.process_operands(opcode, operands)
        self.clock_cycle += JUMP_CYCLES
        if self.registers[first] != self.registers[second]:
            self.program_counter = address

    def slt(self, opcode, operands):
        destination, first, second = self.process_operands(opcode, operands)
        self.clock_cycle += ALU_CYCLES
        if self.registers[first] < self.registers[second]:
            self.registers[destination] = 1
        else:
            self.registers[destination] = 0