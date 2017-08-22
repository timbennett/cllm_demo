from collections import *
from random import random
import argparse

parser = argparse.ArgumentParser(description='Generate new list items using an existing \
                                             list and a character-level language model')

parser.add_argument('-filename', action="store", dest="filename",
                    help='Name of the file containing the sample text.')
parser.add_argument('-order', action="store", dest="order", type=int, default=4,
                    help='Split lines into fragments of this many characters; the higher \
                    this number, the more entries will be duplicates of the source text. \
                    Default 4, practical values 2-10.')
parser.add_argument('-nletters', action="store", dest="nletters", type=int, default=1000,
                    help='Generate this many characters of output (duplicate checking \
                    will then occur, so the end result may be shorter) Default 1000.')
parser.add_argument('-maxlength', action="store", dest="maxlength", type=int, default=1000,
                    help='Remove generated strings longer than this many characters. \
                    Default 1000.')

args = parser.parse_args()

# * Generate new list items using an existing list and a character-level language model
# * Remove items that were in the original list (generate wholly novel items)
# * Built on http://nbviewer.jupyter.org/gist/yoavg/d76121dfde2618422139
# * Requires python 2
#
# Usage: python text_generator.py filename order nletters
#       * e.g.: python text.txt 4 10000
#       * filename: a list file with entries on separate lines
#       * order: split lines into fragments of this many characters; the higher this 
#         number, the more entries will be duplicates of the source text.
#       * nletters: generate this many characters of output (before duplicate checking)

filename = args.filename
order = args.order
nletters = args.nletters

def train_char_lm(data, order=4):
    lm = defaultdict(Counter)
    pad = "~" * order
    data = pad + data
    for i in xrange(len(data)-order):
        history, char = data[i:i+order], data[i+order]
        lm[history][char]+=1
    def normalize(counter):
        s = float(sum(counter.values()))
        return [(c,cnt/s) for c,cnt in counter.iteritems()]
    outlm = {hist:normalize(chars) for hist, chars in lm.iteritems()}
    return outlm

def generate_letter(lm, history, order):
        history = history[-order:]
        dist = lm[history]
        x = random()
        for c,v in dist:
            x = x - v
            if x <= 0: return c
            
def generate_text(lm, order, nletters=1000):
    history = "~" * order
    out = []
    for i in xrange(nletters):
        c = generate_letter(lm, history, order)
        history = history[-order:] + c
        out.append(c)
    return "".join(out)

with open(filename, 'r') as f:
    data = u''+f.read().decode('utf-8')
    lines = data.split('\n')

lm = train_char_lm(data, order=order)
#print lm

generated_text = generate_text(lm, order, nletters=nletters).split('\n')

cleaned_text = []
for line in generated_text[:-1]:
    if line not in lines:
        if len(line) <= args.maxlength:
            cleaned_text.append(line)

print("\n".join(cleaned_text))