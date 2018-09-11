import numpy as np
from re import sub, search, match

class Memory:
	def __init__(self, mem_size, program_file, data_file):
		self.instructions = []
		self.load_program(program_file)
		self.data_file = data_file
		self.data = np.zeros(mem_size, dtype=int)
		self.load_data(data_file)

	def link_jumps(self, jump_labels, jump_addresses):
		for index in jump_addresses:
			instruction = self.instructions[index]
			j = 0 if instruction[0] is 'jp' else 2
			self.instructions[index][1][j] = jump_labels[instruction[1][j]]

	def load_program(self, program_file):
		jump_labels = {}
		jump_addresses = []

		with open(program_file,'r') as file:
			body = enumerate([i for i in file.readlines() if not match('^\s*$', i)])

			for index, line in body: 
				code = sub('#.*$', '', line)
				label = search('.*:', code)

				if label is not None:
					begin, end = label.span()
					jump_labels[code[begin:end-1]] = str(index)
					code = code[end:]
				
				code = code.strip().split(' ')

				if code[0] in ['jp', 'beq', 'bne']:
					jump_addresses.append(index)

				self.instructions.append([code[0], code[1:]])	
		self.link_jumps(jump_labels, jump_addresses)

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
	
