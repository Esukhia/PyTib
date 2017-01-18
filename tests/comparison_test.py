import time
import ngram
from fuzzywuzzy import fuzz, process
from difflib import SequenceMatcher

l = ['ཆོས་', 'ཀྱི་', 'སྐུ་', 'ལ་', 'གནས་']
test_l = ['ཆོས་', 'ཀྱི', 'ྐུ', 'ལ་', 'གནས་']

string = 'ཆོས་ཀྱི་སྐུ་ལ་གནས་'
test_str = 'ཆོས་ཀྱིྐུ་ལ་གནས་'

import jellyfish
import Levenshtein

Z = time.time()
z = jellyfish.jaro_winkler(string*10, test_str*10, long_tolerance=True)

Y = time.time()
lev = Levenshtein.jaro_winkler(string*10, test_str*10)

X = time.time()
model = ngram.NGram()
model.add(string)

C = time.time()
truc1 = model.search(test_str, threshold=0)

D = time.time()
tt = fuzz.ratio(string, test_str)

DD = time.time()
last = SequenceMatcher(a=string, b=test_str).real_quick_ratio()

E = time.time()
print('jellyfish', Y-Z)
print(z)

print('orig_list :', D-C)
print(truc1)

print('fw orig_list:', DD-D)
print(tt)

print('difflib orig_list', E-DD)
print(last)

print('Lev:', X-Y)
print(lev)

