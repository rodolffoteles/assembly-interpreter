class Cache:
    def __init__(self, cache_size, block_size, set_count, algorithm, main_memory):
        self.line_per_set =int((cache_size/block_size)/set_count)
        self.set_count = set_count
        self.block_size = block_size
        self.memory = [[{'tag': None, 'line': [0]*block_size} \
                        for _ in range(line_per_set)] \
                        for _ in range(set_count)]
        self.algorithm = algorithm
        self.lru_tag = [[] for _ in range(set_count)]
        self.fifo_tag = [0]*set_count
        self.main_memory = main_memory
        self.miss_count = 0
        self.hit_cout = 0

    def read(address):
        block, word = divmod(address, self.block_size)
        tag, set_number = divmod(block, self.set_count)

        for line in self.memory[set_number]:
            if line['tag'] == tag:
                self.lru_tag[set_number] = [t for t in self.lru_tag if t != tag] + [tag]
                return line['line'][word]
        else:
            self.miss_count += 1
            return self.replace_line(address, set_number, tag)
        

    def write(address, data):
        block, word = divmod(address, self.block_size)
        tag, set_number = divmod(block, self.set_count)
        self.main_memory.write(address, data)

        for line in self.memory[set_number]:
            if line['tag'] == tag:
                self.lru_tag[set_number] = [t for t in self.lru_tag[set_number] if t != tag] + [tag]
                line['line'][word] = data
        else:
            self.replace_line(address, set_number, tag)        

    def replace_line(address, set_number, new_tag):
        if None in [l['tag'] for l in self.memory[set_number]]:
            new_line = self.main_memory.read_block(address)
        else:
            if algorithm == 'FIFO':
                tag = self.fifo_tag[set_count]
                self.fifo_tag[set_count] = (self.fifo_tag[set_count] + 1) % self.line_per_set
                self.memory[set_number][tag] = {'tag': new_tag, 'line': new_line} 

            elif algorithm == 'LRU':
                tag = self.lru_tag[set_number].pop(0)
                self.lru_tag[set_number] = [t for t in self.lru_tag[set_number] if t != tag] + [new_tag]
                self.memory[set_number][tag] = {'tag': new_tag, 'line': new_line} 

        return new_line
        