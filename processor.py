from os.path import exists
from os import remove
from numpy import zeros
from re import sub 
from memory import Memory

ARITHMETIC_CYCLES = 1
MEMORY_CYCLES = 10
JUMP_CYCLES = 3

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
			'stro': self.storeoff,
			'ld': self.load,
			'ldo': self.loadoff,
			'mov': self.move,
			'jp': self.jump,
			'jeq': self.jeq,
			'jnq': self.jnq,
			'jlt': self.jlt,
			'jgt': self.jgt	
		}

		self.execute()	

	def execute(self):
		while(True):
			self.write_registers()
			self.ir = memory.get_instruction(self.pc)
			self.pc += 1
			if not self.decode(self.ir):
				self.memory.save()
				break

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

	def storeoff(self, params):
		first, second = [int(sub('[^0-9]', '', p)) for p in params]
		self.memory.write(first, self.registers[second + third])
		self.clock_cycle += MEMORY_CYCLES

	def load(self, params):
		first, second = [int(sub('[^0-9]', '', p)) for p in params]
		self.registers[first] = self.memory.read(second)
		self.clock_cycle += MEMORY_CYCLES

	def loadoff(self, params):
		first, second, third = [int(sub('[^0-9]', '', p)) for p in params]
		self.registers[first] = self.memory.read(second + third)
		self.clock_cycle += MEMORY_CYCLES

	def move(self, params):
		first, second = [int(sub('[^0-9]', '', p)) for p in params]
		self.registers[first] = self.registers[second]
		self.clock_cycle += ARITHMETIC_CYCLES

	def jump(self, params):
		first = int(sub('[^0-9]', '', params[0]))
		self.pc = first
		self.clock_cycle += JUMP_CYCLES

	def jeq(self, params):
		first, second, third = [int(sub('[^0-9]', '', p)) for p in params]
		self.clock_cycle += JUMP_CYCLES
		if self.registers[first] == self.registers[second]:
			self.pc = third

	def jnq(self, params):
		first, second, third = [int(sub('[^0-9]', '', p)) for p in params]
		self.clock_cycle += JUMP_CYCLES
		if self.registers[first] != self.registers[second]:
			self.pc = third

	def jlt(self, params):
		first, second, third = [int(sub('[^0-9]', '', p)) for p in params]
		self.clock_cycle += JUMP_CYCLES
		if self.registers[second] < self.registers[third]:
			self.pc = third

	def jgt(self, params):
		first, second, third = [int(sub('[^0-9]', '', p)) for p in params]
		self.clock_cycle += JUMP_CYCLES
		if self.registers[second] > self.registers[third]:
			self.pc = third

	def write_registers(self):
		with open('registers.text','a') as file:
			file.write(f'pc = {self.pc}\n') 
			file.write(f'clock = {self.clock_cycle}\n')
			if self.ir is not '':
				file.write(f'instruction = {self.ir[0]} {" ".join(self.ir[1])}\n') 
			file.write(f'registers = {" ".join([str(r) for r in self.registers])}\n')
			file.write(f'{"-"*10}\n')

if __name__ == "__main__":
	if exists('registers.text'): remove('registers.text')
	memory = Memory('teste.asm', 'data.txt')
	cpu = Processor(memory)
