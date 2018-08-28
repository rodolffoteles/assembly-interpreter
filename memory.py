from numpy import zeros

class Memory:
	def __init__(self, mem_size, program_file):
		self.instructions = self.load_program(program_file)
		self.data = np.zeros(mem_size, dtype=int)

	def load_program(self, program_file):
		instructions = []
		with open(program_file,'r') as file:
			for line in file: 
				code = line.strip().split(' ')
				instructions.append([code[0], code[1:]])
		return instructions

	def get_instruction(self, index):
		return self.instructions[index]

	def write(self, index, data):
		self.data[index] = data

	def read(self, index):
		return self.data[index]

if __name__ == "__main__":
	memory = Memory(20, 'teste.asm')
	
