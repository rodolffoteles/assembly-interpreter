import numpy as np

class Memory:
	def __init__(self, program_file, data_file):
		self.instructions = []
		self.load_program(program_file)
		self.data_file = data_file
		self.data = np.zeros(100, dtype=int)
		self.load_data(data_file)

	def load_program(self, program_file):
		with open(program_file,'r') as file:
			for line in file: 
				code = line.strip().split(' ')
				self.instructions.append([code[0], code[1:]])

	def load_data(self, data_file):
		with open(data_file,'r') as file:
			for index, value in enumerate(file.readlines()): 
				self.data[index] = value

	def get_instruction(self, address):
		return self.instructions[address]

	def write(self, address, data):
		self.data[address] = data

	def read(self, address):
		return self.data[address]

	def save(self):
		with open(self.data_file,'w') as file:
			file.write('\n'.join([str(m) for m in self.data]))
	
