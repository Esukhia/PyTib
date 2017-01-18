import sys
import os
path = os.path.dirname(sys.modules[__name__].__file__)
path = os.path.join(path, '..')
sys.path.insert(0, path)
from pytib.common import pre_process, open_file, write_file

in_file = '3-grams_raw.txt'
in_path = '/home/drupchen/Documents/TibTAL/ngram/kangyur_results_raw/'
kangyur_ngrams = open_file(in_path+in_file).split('\n')
out = [' '.join(b) for b in sorted([a.split(' ') for a in kangyur_ngrams if a != ''], key=lambda x: int(x[-1]), reverse=True)]
write_file(in_path+in_file, '\n'.join(out))
