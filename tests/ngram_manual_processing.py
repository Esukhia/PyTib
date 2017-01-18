import sys
import os
path = os.path.dirname(sys.modules[__name__].__file__)
path = os.path.join(path, '..')
sys.path.insert(0, path)
from pytib.common import pre_process, open_file, write_file

#content = open_file('/home/drupchen/Documents/TibTAL/ngram/merged_ekangyur.txt')
#write_file('/home/drupchen/Documents/TibTAL/ngram/merged_ekangyur_pre-processed.txt', pre_process(content, 'syls'))

# filter ngrams that have been chosen manually from the X-grams_processed.csv and save to X-grams_processed.txt
file_num = 11
in_file = str(file_num)+'-grams_processed.csv'
in_path = '/home/drupchen/Documents/TibTAL/ngram/kangyur_results/'
kangyur_ngrams = open_file(in_path+in_file).split('\n')
out = []
for o in kangyur_ngrams:
    if 'o' in o:
       out.append(o.split('\t')[1])
write_file(in_path+in_file.replace('.csv', '.txt'), '\n'.join(out))




# filter all substrings of the chosen ngram from X-grams_processed.txt and write to X-grams_nosub.txt
def is_substring(string, substring):
    if substring in string:
        return True
    else:
        return False

lower_in_file = str(file_num-1)+'-grams.txt'
lower_level_file = open_file(in_path+lower_in_file).split('\n')
lower_out = []
for lower_gram in lower_level_file:
    lower_g = lower_gram.replace(' '+lower_gram.split(' ')[-1], '')
    substring = False
    for o in out:
        higher_g = o.replace(' '+o.split(' ')[-1], '')
        if is_substring(higher_g, lower_g):
            substring = True

    if not substring:
        lower_out.append(lower_gram)

write_file(in_path+lower_in_file.replace('.txt', '_nosub.txt'), '\n'.join(lower_out))
