#!/usr/bin/env python3
"""reducer.py - Exercise 3

Outputs only the 3 words with the highest counts, sorted by count descending.

The change is in the REDUCER: only the reducer sees the final total of each
word. A mapper only sees its own input split, so it cannot know which words
are the global top 3.

Must be run with  -numReduceTasks 1 : every reducer prints its own top 3,
so with 3 reducers we would get 3 x 3 = 9 lines instead of 3.

Instead of keeping all words in memory and sorting them, we keep a min-heap
of at most 3 items, so memory stays O(3) no matter how big the vocabulary is.
"""

from itertools import groupby
from operator import itemgetter
import heapq
import sys

TOP_N = 3


def read_mapper_output(file, separator='\t'):
    for line in file:
        yield line.rstrip().split(separator, 1)


def main(separator='\t'):
    # input comes from STDIN (standard input), already sorted by word by Hadoop
    data = read_mapper_output(sys.stdin, separator=separator)

    top = []  # min-heap of (count, word); top[0] is the smallest of the current top 3

    for current_word, group in groupby(data, itemgetter(0)):
        try:
            total_count = sum(int(count) for _, count in group)
        except ValueError:
            # count was not a number (or line was malformed), so discard this item
            continue

        if len(top) < TOP_N:
            heapq.heappush(top, (total_count, current_word))
        elif total_count > top[0][0]:
            # bigger than the smallest of the current top 3 -> replace it
            heapq.heapreplace(top, (total_count, current_word))

    # print highest count first
    for total_count, word in sorted(top, reverse=True):
        print('%s%s%d' % (word, separator, total_count))


if __name__ == "__main__":
    main()
