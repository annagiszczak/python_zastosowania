import sys
import argparse
import rich
from rich.progress import track
import rich.traceback
from ascii_graph import Pyasciigraph
from ascii_graph import colors
from ascii_graph.colors import *
from ascii_graph.colordata import vcolor
from ascii_graph.colordata import hcolor
import tqdm
import time
import random
import numpy as np


from collections import defaultdict

import collections
from _collections_abc import Iterable 
collections.Iterable = Iterable

'''
Funkcje potrzebne
'''

def load_file(filename: str):
    with open(filename) as book:
        text = book.read().lower()
        words = text.split()

    word_dict = {word: 0 for word in set(words)}

    return word_dict, words

def count_words(word_counts: dict, words):
    '''
    Count words and clean it
    '''
    for word in tqdm.tqdm(words, desc="Words counting"):
        word_dict[word] += 1

    keys_to_remove = [word for word in word_dict if len(word) < args.min_length]
    for key in keys_to_remove:
        del word_dict[key]

    most_common_words = sorted(word_dict.items(), key=lambda item: item[1], reverse=True)

    most_common_words = most_common_words[:args.max]

    return most_common_words


def create_hist(most_common_words):
    graph = Pyasciigraph(
    line_length=120,
    min_graph_length=50,
    separator_length=4,
    multivalue=False,
    human_readable='si',
    graphsymbol='*',
    float_format='{0:,.2f}',
    force_max_value=2000,
    )

    pattern = [Gre, Yel, Red, Yel, Bla, Blu, Gre, Yel, Red, Yel]
    data = vcolor(most_common_words, pattern[:len(most_common_words)])

    for line in graph.graph('Lovely graph', data):
        print(line)


rich.traceback.install()
rich.get_console().clear()
rich.get_console().rule(":raccoon: :raccoon: :raccoon: Hello Everyone! :raccoon: :raccoon: :raccoon:", style="bold magenta")

parser = argparse.ArgumentParser(description="Analysis of words number")
parser.add_argument('--file', '-f', type=str, nargs='+', help="Path to file.")
parser.add_argument('--max', '-m', type=int, default=10, help="Number of words in hist (default 10).")
parser.add_argument('--min_length','-ml', type=int, default=0, help="Min length of words (default 0).")
args = parser.parse_args()

for idx in tqdm.tqdm(range(len(args.file))):
    word_dict, words = load_file(args.file[idx])
    most_common = count_words(word_dict, words)
    create_hist(most_common)

rich.get_console().print("[bold magenta]The endzik[/bold magenta]!", style="italic red")