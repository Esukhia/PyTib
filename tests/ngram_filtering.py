import sys
import os
path = os.path.dirname(sys.modules[__name__].__file__)
path = os.path.join(path, '..')
sys.path.insert(0, path)
from pytib.common import pre_process, open_file, write_file

#content = open_file('/home/drupchen/Documents/TibTAL/ngram/merged_ekangyur.txt')
#write_file('/home/drupchen/Documents/TibTAL/ngram/merged_ekangyur_pre-processed.txt', pre_process(content, 'syls'))

# firt run the following command
# ./extractngram -n11 -f70 -i corpus > ./kangyur_results_raw/11-grams_raw.txt

file_num = 3
in_file = str(file_num)+'-grams_raw.txt'
in_path = '/home/drupchen/Documents/TibTAL/ngram/kangyur_results_raw/'
kangyur_ngrams = open_file(in_path+in_file).split('\n')
out = [' '.join(b) for b in sorted([a.split(' ') for a in kangyur_ngrams if a != ''], key=lambda x: int(x[-1]), reverse=True)]
filtered = []
agreement = []
for o in out:
    parts = o.split(' ')
    first = parts[0]
    last = parts[-2]
    if '_' not in o and '།' not in o and '༄' not in o:
        if first not in ['དང་', 'ནི་', 'པར་', 'བར་', 'པའི་', 'བའི་', 'པ་', 'བ་', 'པོ་', 'ཅེས་', 'ཅིང་', 'ཞེས་', 'སུ་', 'ཏེ་', 'ཀྱི་', 'གྱི་', 'ཀྱིས་', 'གྱིས་', 'ཏུ་', 'པོས་', 'པས་', 'རྣམས་']:
            if last not in ['དང་', 'ལ་', 'ཡང་', 'གང་', 'ནི་']:
                if not last.endswith('འི་') or not last.endswith('འི') or not last.endswith('འོ་') or not last.endswith('འོ') or not last.endswith('འམ་') or not last.endswith('འམ') or last not in ['གི', 'ཀྱི', 'གྱི', 'ཡི', 'གིས', 'ཀྱིས', 'གྱིས', 'ཡིས', 'སུ', 'ཏུ', 'དུ', 'རུ', 'སྟེ', 'ཏེ', 'དེ', 'ཀྱང', 'འང', 'གམ', 'ངམ', 'དམ', 'ནམ', 'བམ', 'མམ', 'འམ', 'རམ', 'ལམ', 'སམ', 'ཏམ', 'གོ', 'ངོ', 'དོ', 'ནོ', 'མོ', 'འོ', 'རོ', 'ལོ', 'སོ', 'ཏོ', 'ཅིང', 'ཅེས', 'ཅེའོ', 'ཅེ', 'ཅིག', 'ཞིང', 'ཞེས', 'ཞེའོ', 'ཞེ', 'ཞིག', 'ཤིང', 'ཤེའོ', 'ཤེ', 'ཤིག', 'པར', 'བར', 'པའི', 'བའི', 'པོར', 'གི་', 'ཀྱི་', 'གྱི་', 'ཡི་', 'གིས་', 'ཀྱིས་', 'གྱིས་', 'ཡིས་', 'སུ་', 'ཏུ་', 'དུ་', 'རུ་', 'སྟེ་', 'ཏེ་', 'དེ་', 'ཀྱང་', 'འང་', 'གམ་', 'ངམ་', 'དམ་', 'ནམ་', 'བམ་', 'མམ་', 'འམ་', 'རམ་', 'ལམ་', 'སམ་', 'ཏམ་', 'གོ་', 'ངོ་', 'དོ་', 'ནོ་', 'མོ་', 'འོ་', 'རོ་', 'ལོ་', 'སོ་', 'ཏོ་', 'ཅིང་', 'ཅེས་', 'ཅེའོ་', 'ཅེ་', 'ཅིག་', 'ཞིང་', 'ཞེས་', 'ཞེའོ་', 'ཞེ་', 'ཞིག་', 'ཤིང་', 'ཤེའོ་', 'ཤེ་', 'ཤིག་', 'པར་', 'བར་', 'པའི་', 'བའི་', 'པོར་']:
                    filtered.append(o)
    # find all trigrams or higher containing particles somewhere between the 2nd and 2nd-last syllable
    if len(parts) >= 3:
        middle = parts[1:-2]
        particles = ['འི་', 'འི', 'འོ་', 'འོ', 'འམ་', 'འམ', 'གི', 'ཀྱི', 'གྱི', 'ཡི', 'གིས', 'ཀྱིས', 'གྱིས', 'ཡིས', 'སུ', 'ཏུ', 'དུ', 'རུ', 'སྟེ', 'ཏེ', 'དེ', 'ཀྱང', 'འང', 'གམ', 'ངམ', 'དམ', 'ནམ', 'བམ', 'མམ', 'འམ', 'རམ', 'ལམ', 'སམ', 'ཏམ', 'གོ', 'ངོ', 'དོ', 'ནོ', 'མོ', 'འོ', 'རོ', 'ལོ', 'སོ', 'ཏོ', 'ཅིང', 'ཅེས', 'ཅེའོ', 'ཅེ', 'ཅིག', 'ཞིང', 'ཞེས', 'ཞེའོ', 'ཞེ', 'ཞིག', 'ཤིང', 'ཤེའོ', 'ཤེ', 'ཤིག', 'པར', 'བར', 'པའི', 'བའི', 'པོར', 'གི་', 'ཀྱི་', 'གྱི་', 'ཡི་', 'གིས་', 'ཀྱིས་', 'གྱིས་', 'ཡིས་', 'སུ་', 'ཏུ་', 'དུ་', 'རུ་', 'སྟེ་', 'ཏེ་', 'དེ་', 'ཀྱང་', 'འང་', 'གམ་', 'ངམ་', 'དམ་', 'ནམ་', 'བམ་', 'མམ་', 'འམ་', 'རམ་', 'ལམ་', 'སམ་', 'ཏམ་', 'གོ་', 'ངོ་', 'དོ་', 'ནོ་', 'མོ་', 'འོ་', 'རོ་', 'ལོ་', 'སོ་', 'ཏོ་', 'ཅིང་', 'ཅེས་', 'ཅེའོ་', 'ཅེ་', 'ཅིག་', 'ཞིང་', 'ཞེས་', 'ཞེའོ་', 'ཞེ་', 'ཞིག་', 'ཤིང་', 'ཤེའོ་', 'ཤེ་', 'ཤིག་', 'པར་', 'བར་', 'པའི་', 'བའི་', 'པོར་']
        has_particle = False
        # Todo : should not apply to the first element but to the element preceding the particle. (works only until 3-grams)
        if '_' not in first and '།' not in first and '༄' not in first:
            for p in particles:
                if p in middle:
                    has_particle = True
            if has_particle:
                agreement.append(o)

write_file(in_path.replace('_raw', '')+in_file.replace('_raw', ''), '\n'.join(filtered))
write_file(in_path.replace('_raw', '')+in_file.replace('_raw', '_agreement'), '\n'.join(agreement))
