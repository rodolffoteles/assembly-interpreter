from math import ceil

class Cache:
    def __init__(self, cache_size, block_size, set_count, algorithm, main_memory):
        self.line_per_set = ceil((cache_size/block_size)/set_count)
        self.set_count = set_count
        self.block_size = block_size
        self.memory = [[{'tag': None, 'line': [0]*block_size} \
                        for _ in range(self.line_per_set)] \
                        for _ in range(set_count)]
        self.algorithm = algorithm
        self.lru_tag = [[] for _ in range(set_count)]
        self.fifo_tag = [0]*set_count
        self.main_memory = main_memory
        self.miss_count = 0
        self.hit_count = 0

    def read(self, address):
        block, word = divmod(address, self.block_size)
        tag, set_number = divmod(block, self.set_count)

        for line in self.memory[set_number]:
            if line['tag'] == tag:
                self.hit_count += 1
                if self.algorithm == 'LRU':
                    self.lru_tag[set_number] = [t for t in self.lru_tag[set_number] \
                                                if t != tag] + [tag]
                return line['line'][word]
        else:
            self.miss_count += 1
            return self.replace_line(address, set_number, tag, word)
        

    def write(self, address, data):
        self.main_memory.write(address, data)
        block, word = divmod(address, self.block_size)
        tag, set_number = divmod(block, self.set_count)
    
        for line in self.memory[set_number]:
            if line['tag'] == tag:
                self.hit_count += 1
                if self.algorithm == 'LRU':
                    self.lru_tag[set_number] = [t for t in self.lru_tag[set_number] \
                                                if t != tag] + [tag]
                line['line'][word] = data
                break
        else:
            self.miss_count += 1
            self.replace_line(address, set_number, tag, word)        

    def replace_line(self, address, set_number, new_tag, word):
        tags = [l['tag'] for l in self.memory[set_number]]
        new_line = self.main_memory.read_block(address)

        if None in tags:
            tag = tags.index(None)
        else:
            if self.algorithm == 'FIFO':
                tag = self.fifo_tag[set_number]
                self.fifo_tag[set_number] = (self.fifo_tag[set_number] + 1) \
                                            % self.line_per_set
            elif self.algorithm == 'LRU':
                tag = self.lru_tag[set_number].pop(0)
                self.lru_tag[set_number] += [new_tag] 


        self.memory[set_number][tag] = {'tag': new_tag, 'line': new_line} 
        return new_line[word]
    
    def get_miss_rate(self):
        return self.miss_count/(self.hit_count + self.miss_count)

    def get_miss_count(self):
        return self.miss_count

    def get_hit_count(self):
        return self.hit_count

    def get_cache(self):
        string = ''
        for set_number in range(self.set_count):
            string += f'SET {set_number}\n'
            for line in self.memory[set_number]:
                string += '\tTAG= {}\tBLOCO= {}\n' \
                            .format(line['tag'], '\t'.join([str(l) for l in line['line']]))
            string += '\n'
        return string

    