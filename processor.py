from numpy import zeros
from re import sub 
from memory import Memory

ARITHMETIC_CYCLES = 1
MEMORY_CYCLES = 10

class Processor:
	def __init__(self, memory, number_registers=10):
		#self._registers = np.zeros(number_registers, dtype=int)
		self.registers = [x for x in range(10)]
		self.clock_cycle = 0
		self.ir = ''
		self.pc = 0
		self.memory = memory
		self.switcher = {
			'add': self.add,
			'sub': self.sub,
			'str': self.store,
			'ld': self.load
		}

		self.execute()	

	def execute(self):
		while(True):
			self.ir = memory.get_instruction(self.pc)
			self.pc += 1
			self.decode(self.ir)

	def decode(self, instruction):
		operation_code = instruction[0]
		self.switcher.get(operation_code)(instruction[1])

	def add(self, params):
		first, second, third = [int(sub('[^0-9]', '', p)) for p in params]
		self.registers[first] = self.registers[second] + self.registers[third]
		self.clock_cycle += ARITHMETIC_CYCLES

	def sub(self, params):
		first, second, third = [int(sub('[^0-9]', '', p)) for p in params]
		self.registers[first] = self.registers[second] - self.registers[third]
		self.clock_cycle += ARITHMETIC_CYCLES

	def store(self, params):
		first, second = [int(sub('[^0-9]', '', p)) for p in params]
		self.memory.write(first, self.registers[second])
		self.clock_cycle += MEMORY_CYCLES

	def load(self, params):
		first, second = [int(sub('[^0-9]', '', p)) for p in params]
		self.registers[second] = self.memory.read(first)
		self.clock_cycle += MEMORY_CYCLES

if __name__ == "__main__":
	memory = Memory(20, 'teste.asm')
	cpu = Processor(memory)
