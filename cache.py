from math import ceil

class Cache:
    '''Simulates the behaviour of a cache memory'''

    def __init__(self, cache_size, set_count, policy, main_memory):
        '''
        Parameters:
            cache_size - Size of the cache memory
            set_count - Quantity of sets to divide the memory
            policy - Cache replacement policy (LRU or FIFO)
            main_memory - Memory from which words are loaded
        '''

        self.main_memory = main_memory
        self.policy = policy

        self.block_size = main_memory.block_size
        self.set_count = set_count
        self.line_per_set = ceil((cache_size/self.block_size)/set_count)
        
        self.memory = [[{'tag': None, 'line': [0]*self.block_size} \
                        for _ in range(self.line_per_set)] \
                        for _ in range(set_count)]
        
        # Data structures to help decide which line to replace on cache
        self.lru_tag = [[] for _ in range(set_count)]
        self.fifo_tag = [0]*set_count

        self.miss_count = 0
        self.hit_count = 0

    def read(self, address):
        block, word = divmod(address, self.block_size)
        tag, set_number = divmod(block, self.set_count)

        if self.policy == 'LRU': 
            self.update_recently_used_tags(set_number, tag)

        for line in self.memory[set_number]:
            if line['tag'] == tag:
                self.hit_count += 1
                return line['line'][word]
        else:
            self.miss_count += 1
            return self.load_line(address, set_number, tag, word)
        

    def write(self, address, data):
        # Write-through to the main memory
        self.main_memory.write(address, data)
        block, word = divmod(address, self.block_size)
        tag, set_number = divmod(block, self.set_count)

        if self.policy == 'LRU': 
            self.update_recently_used_tags(set_number, tag)
    
        for line in self.memory[set_number]:
            if line['tag'] == tag:
                self.hit_count += 1
                line['line'][word] = data
                break
        else:
            self.miss_count += 1
            self.load_line(address, set_number, tag, word)        

    def load_line(self, address, set_number, new_tag, word):
        tags = [l['tag'] for l in self.memory[set_number]]
        new_line = self.main_memory.read_block(address)

        if None in tags:
            # There is empty space on the set, just insert the new line there
            tag = tags.index(None)
        else:
            # The set if full, get the index of the line that must be replaced
            tag = self.get_tag_to_replace(set_number)

        self.memory[set_number][tag] = {'tag': new_tag, 'line': new_line} 
        return new_line[word]

    def get_tag_to_replace(self, set_number):
        '''Determine which line in the set must be replaced'''

        if self.policy == 'FIFO':
            tag = self.fifo_tag[set_number]
            self.fifo_tag[set_number] += 1
            self.fifo_tag[set_number] %= self.line_per_set
        elif self.policy == 'LRU':
            tag = self.lru_tag[set_number].pop()
            for index, line in enumerate(self.memory[set_number]):
                if line['tag'] == tag:
                    tag = index 
                    break

        return tag

    def update_recently_used_tags(self, set_number, tag):
        '''Reallocates the recent used tag to the begining of the list'''

        self.lru_tag[set_number] = [tag] + [t for t in self.lru_tag[set_number] if t != tag]  

    def get_miss_rate(self):
        return self.miss_count/(self.hit_count + self.miss_count)

    def get_miss_count(self):
        return self.miss_count

    def get_hit_count(self):
        return self.hit_count    