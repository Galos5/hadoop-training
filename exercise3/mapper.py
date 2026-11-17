#!/usr/bin/env python3
"""mapper.py - Exercise 3 (same mapper as Exercise 2)

Word count with two changes compared to the original mapper:
  1. Trailing commas and dots are stripped from the end of each word
     ("world." -> "world", "end.," -> "end").
  2. Words are lower-cased, so "The", "THE" and "the" are counted together.

Both changes are done in the MAPPER, because the key must already be
normalized before the shuffle: Hadoop partitions and sorts by the exact key,
so "The" and "the" would otherwise reach the reducer as different keys
(possibly even on different reducers).
"""

import sys


def read_input(file):
    for line in file:
        # split the line into words
        yield line.split()


def normalize(word):
    # strip only TRAILING commas/dots (not leading ones, e.g. ".NET"), then lowercase
    return word.rstrip('.,').lower()


def main(separator='\t'):
    # input comes from STDIN (standard input)
    data = read_input(sys.stdin)
    for words in data:
        for word in words:
            word = normalize(word)
            # skip tokens that were only dots/commas, e.g. "..." -> ""
            if word:
                # tab-delimited; the trivial word count is 1
                print('%s%s%d' % (word, separator, 1))


if __name__ == "__main__":
    main()
