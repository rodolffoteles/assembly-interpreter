import sys
import matplotlib.pyplot as plt
from numpy import random

from memory import MainMemory
from cache import Cache
from processor import Processor

def plot(cache_sizes, set_counts, miss_rate):
    fig, ax = plt.subplots()

    x_positions = list(range(len(cache_sizes)))
    bar_width = 0.1 
    colors = [random.rand(1,3) for _ in range(len(set_counts))]

    bars = []
    for index, count in enumerate(set_counts):
        bar = ax.bar(
            x=[x + (bar_width*index) for x in x_positions],
            height=miss_rate[count], 
            width=bar_width, 
            color=colors[index]
        )
        bars.append(bar)

    ax.set_ylabel('Miss rate')
    ax.set_xticks([x + (bar_width/len(cache_sizes)) for x in x_positions])
    ax.set_xlabel('Cache size')
    ax.set_xticklabels(cache_sizes)

    set_labels =  [str(s) + (' set' if s == 1 else ' sets') for s in set_counts]
    ax.legend(bars, set_labels)

    plt.show()


if __name__ == '__main__':
    if len(sys.argv) != 3: 
        print('Usage: python processor.py <program_file> <data_file>')
        sys.exit(1)

    cache_sizes = [32, 64, 128, 256, 512]
    set_counts = [1, 2, 4, 8]
    miss_rate = {count: [] for count in set_counts}

    for size in cache_sizes:
        for count in set_counts:
            # Only ovewrite the secondary memory on the last loop to 
            # prevent the algorithm from running with different data input
            save_flag = size == cache_sizes[-1] and count == set_counts[-1]

            memory = MainMemory(
                mem_size=3000, 
                block_size=4,
                program_file=sys.argv[1], 
                data_file=sys.argv[2],
                save_allowed=save_flag
                )
            cache = Cache(
                cache_size=size,
                set_count=count, 
                policy='FIFO',
                main_memory=memory
                )
            cpu = Processor(memory, cache)

            miss_rate[count].append(cache.get_miss_rate())

    plot(cache_sizes, set_counts, miss_rate)

    