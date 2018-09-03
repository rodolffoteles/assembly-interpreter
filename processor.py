from os.path import exists
from os import remove
from numpy import zeros
from re import sub 
from memory import Memory

ARITHMETIC_CYCLES = 1
MEMORY_CYCLES = 10

class Processor:
	def __init__(self, memory, number_registers=10):
		self.registers = zeros(number_registers, dtype=int)
		self.clock_cycle = 0
		self.ir = ''
		self.pc = 0
		self.memory = memory
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
			'mov': self.move,
			'jp': self.jump,
			'beq': self.beq,
			'bnq': self.bnq,
			'slt': self.slt		
		}

		self.execute()	

	def execute(self):
		while(True):
			self.ir = memory.get_instruction(self.pc)
			self.write_registers()
			self.pc += 1
			if not self.decode(self.ir): break

	def decode(self, instruction):
		operation_code = instruction[0]
		if operation_code == 'eof':
			return False
		else:
			self.switcher.get(operation_code)(instruction[1])
			return True

	def add(self, params):
		first, second, third = [int(sub('[^0-9]', '', p)) for p in params]
		self.registers[first] = self.registers[second] + self.registers[third]
		self.clock_cycle += ARITHMETIC_CYCLES

	def addi(self, params):
		first, second, third = [int(sub('[^0-9]', '', p)) for p in params]
		self.registers[first] = self.registers[second] + third
		self.clock_cycle += ARITHMETIC_CYCLES

	def sub(self, params):
		first, second, third = [int(sub('[^0-9]', '', p)) for p in params]
		self.registers[first] = self.registers[second] - self.registers[third]
		self.clock_cycle += ARITHMETIC_CYCLES

	def subi(self, params):
		first, second, third = [int(sub('[^0-9]', '', p)) for p in params]
		self.registers[first] = self.registers[second] - third
		self.clock_cycle += ARITHMETIC_CYCLES

	def mult(self, params):
		first, second, third = [int(sub('[^0-9]', '', p)) for p in params]
		self.registers[first] = self.registers[second] * self.registers[third]
		self.clock_cycle += ARITHMETIC_CYCLES

	def multi(self, params):
		first, second, third = [int(sub('[^0-9]', '', p)) for p in params]
		self.registers[first] = self.registers[second] * third
		self.clock_cycle += ARITHMETIC_CYCLES

	def div(self, params):
		first, second, third = [int(sub('[^0-9]', '', p)) for p in params]
		self.registers[first] = self.registers[second] / self.registers[third]
		self.clock_cycle += ARITHMETIC_CYCLES

	def divi(self, params):
		first, second, third = [int(sub('[^0-9]', '', p)) for p in params]
		self.registers[first] = self.registers[second] / third
		self.clock_cycle += ARITHMETIC_CYCLES

	def store(self, params):
		first, second = [int(sub('[^0-9]', '', p)) for p in params]
		self.memory.write(first, self.registers[second])
		self.clock_cycle += MEMORY_CYCLES

	def load(self, params):
		first, second = [int(sub('[^0-9]', '', p)) for p in params]
		self.registers[second] = self.memory.read(first)
		self.clock_cycle += MEMORY_CYCLES

	def move(self, params):
		first, second = [int(sub('[^0-9]', '', p)) for p in params]
		self.registers[first] = self.registers[second]
		self.clock_cycle += ARITHMETIC_CYCLES

	def jump(self, params):
		first = int(sub('[^0-9]', '', params[0]))
		self.pc = first
		self.clock_cycle += ARITHMETIC_CYCLES

	def beq(self, params):
		first, second, third = [int(sub('[^0-9]', '', p)) for p in params]
		if self.registers[first] == self.registers[second]:
			self.pc = third

	def bnq(self, params):
		first, second, third = [int(sub('[^0-9]', '', p)) for p in params]
		if self.registers[first] != self.registers[second]:
			self.pc = third

	def slt(self, params):
		first, second, third = [int(sub('[^0-9]', '', p)) for p in params]
		if self.registers[second] != self.registers[third]:
			self.registers[first] = 0
		else:
			self.registers[first] = 1

	def write_registers(self):
		with open('registers.text','a') as file:
			file.write(f'{self.pc} º INSTRUCAO {self.ir}\n')
			for index, value in enumerate(self.registers):
				file.write(f'{index} registrador: {value}\n')

if __name__ == "__main__":
	if exists('registers.text'): remove('registers.text')
	memory = Memory('teste.asm', 'data.txt')
	cpu = Processor(memory)
