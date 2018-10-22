class Cache:
	def __init__(self, set_count, line_size, line_per_set, main_memory):

		self.set_count = set_count
		self.memory = [[{'tag': None, 'line': [0]*line_size} \
						for _ in range(line_per_set)] \
					 	for _ in range(set_count)]
		self.block_size = block_size
		self.main_memory = main_memory
		self.miss_count = 0
		self.hit_cout = 0

	def read(address, word):
		tag, set_number = divmod(address, self.set_count)

		for line in memory[set_number]:
		  	if block['tag'] == tag:
            	return block['line'][word]
		else:
			self.miss_count += 1
			return self.get_from_memory(address, word)
		

	def write(tag, set_number, word):
		pass

	def get_from_memory(address, word):
		pass

	def save_to_memory():
		pass

		