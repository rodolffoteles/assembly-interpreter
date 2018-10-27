from os.path import exists
from os import remove
from numpy import zeros
from re import sub 
from memory import MainMemory
from cache import Cache
import sys

ALU_CYCLES = 1
MEMORY_CYCLES = 10
JUMP_CYCLES = 5

class Processor:
    def __init__(self, main_memory, cache, register_count=10):
        self.registers = zeros(register_count, dtype=int)
        self.clock_cycle = 0
        self.ir = ''
        self.pc = 0
        self.main_memory = main_memory
        self.cache = cache
        self.switcher = {
            'add': self.add,
            'addi': self.addi,
            'sub': self.sub,
            'subi': self.subi,
            'mult': self.mult,
            'multi': self.multi,
            'div': self.div,
            'divi': self.divi,
            'str': self.store,
            'ld': self.load,
            'ldd': self.loadd,
            'li': self.li,
            'mov': self.move,
            'jp': self.jump,
            'beq': self.beq,
            'bne': self.bne,
            'slt': self.slt
        }

        self.execute()  

    def execute(self):
        while(True):
            self.write_registers()
            self.ir = self.main_memory.get_instruction(self.pc)
            self.pc += 1
            if not self.decode(self.ir):
                self.main_memory.save()
                print(f'MISS RATE = {self.cache.get_miss_rate()}')
                break

    def decode(self, instruction):
        operation_code = instruction[0]
        if operation_code == 'eof':
            return False
        else:
            self.switcher.get(operation_code)(instruction[1])
            return True

    def add(self, params):
        destination, first, second = [int(sub('[^0-9]', '', p)) for p in params]
        self.registers[destination] = self.registers[first] + self.registers[second]
        self.clock_cycle += ALU_CYCLES

    def addi(self, params):
        destination, first, immediate = [int(sub('[^0-9]', '', p)) for p in params]
        self.registers[destination] = self.registers[first] + immediate
        self.clock_cycle += ALU_CYCLES

    def sub(self, params):
        destination, first, second = [int(sub('[^0-9]', '', p)) for p in params]
        self.registers[destination] = self.registers[first] - self.registers[second]
        self.clock_cycle += ALU_CYCLES

    def subi(self, params):
        destination, first, immediate = [int(sub('[^0-9]', '', p)) for p in params]
        self.registers[destination] = self.registers[first] - immediate
        self.clock_cycle += ALU_CYCLES

    def mult(self, params):
        destination, first, second = [int(sub('[^0-9]', '', p)) for p in params]
        self.registers[destination] = self.registers[first] * self.registers[second]
        self.clock_cycle += ALU_CYCLES

    def multi(self, params):
        destination, first, immediate = [int(sub('[^0-9]', '', p)) for p in params]
        self.registers[destination] = self.registers[first] * immediate
        self.clock_cycle += ALU_CYCLES

    def div(self, params):
        destination, first, second = [int(sub('[^0-9]', '', p)) for p in params]
        self.registers[destination] = self.registers[first] / self.registers[second]
        self.clock_cycle += ALU_CYCLES

    def divi(self, params):
        destination, first, immediate = [int(sub('[^0-9]', '', p)) for p in params]
        self.registers[destination] = self.registers[first] / immediate
        self.clock_cycle += ALU_CYCLES

    def store(self, params):
        source, destination, offset = [int(sub('[^0-9]', '', p)) for p in params]
        address = self.registers[destination]
        data = self.registers[source]
        self.cache.write(address + offset, data)
        self.clock_cycle += MEMORY_CYCLES

    def li(self, params):
        destination, immediate = [int(sub('[^0-9]', '', p)) for p in params]
        self.registers[destination] = immediate
        self.clock_cycle += MEMORY_CYCLES

    def load(self, params):
        destination, source, offset = [int(sub('[^0-9]', '', p)) for p in params]
        address = self.registers[source]
        self.registers[destination] = self.cache.read(address + offset)
        self.clock_cycle += MEMORY_CYCLES

    def loadd(self, params):
        destination, source, offset = [int(sub('[^0-9]', '', p)) for p in params]
        self.registers[destination] = self.cache.read(source + offset)
        self.clock_cycle += MEMORY_CYCLES

    def move(self, params):
        destination, source = [int(sub('[^0-9]', '', p)) for p in params]
        self.registers[destination] = self.registers[source]
        self.clock_cycle += ALU_CYCLES

    def jump(self, params):
        address = int(sub('[^0-9]', '', params[0]))
        self.pc = address
        self.clock_cycle += JUMP_CYCLES

    def beq(self, params):
        first, second, address= [int(sub('[^0-9]', '', p)) for p in params]
        self.clock_cycle += JUMP_CYCLES
        if self.registers[first] == self.registers[second]:
            self.pc = address

    def bne(self, params):
        first, second, address = [int(sub('[^0-9]', '', p)) for p in params]
        self.clock_cycle += JUMP_CYCLES
        if self.registers[first] != self.registers[second]:
            self.pc = address

    def slt(self, params):
        destination, first, second = [int(sub('[^0-9]', '', p)) for p in params]
        self.clock_cycle += ALU_CYCLES
        if self.registers[first] < self.registers[second]:
            self.registers[destination] = 1
        else:
            self.registers[destination] = 0

    def write_registers(self):
        with open('registers.txt','a') as file:
            file.write(f'pc = {self.pc}\n') 
            file.write(f'clock = {self.clock_cycle}\n')
            if self.ir is not '':
                file.write(f'instruction = {self.ir[0]} {" ".join(self.ir[1])}\n') 
            file.write(f'registers = {" ".join([str(r) for r in self.registers])}\n')
            file.write(f'{"-"*10}\n')

if __name__ == '__main__':
    if exists('registers.txt'): remove('registers.txt')
    if len(sys.argv) != 3: 
        print('Usage: python processor.py <program_file> <data_file>')
        sys.exit(1)

    memory = MainMemory(mem_size=500, 
                        block_size =3,
                        program_file=sys.argv[1], 
                        data_file=sys.argv[2])
    cache = Cache(cache_size=50,
                  block_size=3,
                  set_count=2, 
                  algorithm='FIFO',
                  main_memory=memory)
    cpu = Processor(memory, cache)
