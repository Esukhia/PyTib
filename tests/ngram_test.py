import sys
import os
path = os.path.dirname(sys.modules[__name__].__file__)
path = os.path.join(path, '..')
sys.path.insert(0, path)
import time
import Levenshtein
from collections import defaultdict
from pytib import Segment
from pytib.common import write_file, open_file, tib_sort, pre_process
from tqdm import tqdm

particles = [
    ['འི', 'གི', 'ཀྱི', 'གྱི', 'ཡི', 'གིས', 'ཀྱིས', 'གྱིས', 'ཡིས'],
    ['སུ', 'ཏུ',  'དུ', 'རུ'],
    ['སྟེ', 'ཏེ', 'དེ'],
    ['ཀྱང', 'འང'],
    ['གམ', 'ངམ', 'དམ', 'ནམ', 'བམ', 'མམ', 'འམ', 'རམ', 'ལམ', 'སམ', 'ཏམ'],
    ['གོ', 'ངོ', 'དོ', 'ནོ', 'མོ', 'འོ', 'རོ', 'ལོ', 'སོ', 'ཏོ'],
    ['ཅིང', 'ཞིང', 'ཤིང'],
    ['ཅེས', 'ཞེས'],
    ['ཅེའོ', 'ཞེའོ', 'ཤེའོ'],
    ['ཅེ', 'ཞེ', 'ཤེ'],
    ['ཅིག', 'ཞིག', 'ཤིག'],
    ['པ', 'བ', 'པས', 'བས', 'པར', 'བར', 'པའི', 'བའི', 'པོར', 'བོར']
            ]

def no_trailing_tsek(string):
    if string.endswith('་'):
        return string[:-1]
    else:
        return string


def no_punct(string):
    punct = ['༄', '༅', '།', '་', '༌', '༑', '༎', '༏', '༐', '༔', '_']
    for p in punct:
        string = string.replace(p, '')
    return string


def ngram_minimal_pairs(orig_list, ngram_list, similarity=72):
    matches = {}
    for n_gram in tqdm(ngram_list[:1000]):
        orig_ngram = n_gram[-1]+' '+''.join(n_gram[:-1])
        matches[orig_ngram] = defaultdict(int)
        ngram_indexes = [a for a in range(len(n_gram)-1)]
        hollowed_ngram_indexes = [(j, [a for a in ngram_indexes if a != j]) for j in ngram_indexes]
        for i in range(len(orig_list)-1):
            for h in hollowed_ngram_indexes:
                hole = h[0]
                if i + hole <= len(orig_list) - 1:
                    hole_syl_orig = no_trailing_tsek(orig_list[i + hole])
                    hole_syl_ngram = no_trailing_tsek(n_gram[hole])
                    lev_index = Levenshtein.jaro_winkler(hole_syl_orig, hole_syl_ngram)*100
                    if lev_index < 100 and lev_index >= similarity and no_punct(hole_syl_ngram) != no_punct(hole_syl_orig):
                        hollowed_orig_slice = ''.join([orig_list[i + j] for j in h[1] if i + j <= len(orig_list) - 1])
                        hollowed_ngram_list = ''.join([n_gram[j] for j in h[1]])
                        if no_trailing_tsek(hollowed_orig_slice) == no_trailing_tsek(hollowed_ngram_list):
                            matches[orig_ngram][''.join(orig_list[i:i + len(n_gram)-1])] += 1
    # formatting
    output = ''
    for t in sorted(matches, reverse=True):
        if matches[t]:
            output += t + '\n'
            for occ in tib_sort(matches[t]):
                output += '\t'+occ+'\t'+str(matches[t][occ])+'\n'
            output += '\n'
    return output


def is_match(string1, string2, threshold=66):
    measure = Levenshtein.jaro_winkler(string1, string2) * 100
    # reducing the measure of 10 if the two particles are not in the same group
    similar_group = False
    for group in particles:
        if string1 in group and string2 in group:
            similar_group = True
    if measure > threshold and not similar_group:
        measure -= 10
    if 100 > measure >= threshold:
        return True
    else:
        return False


def find_wrong_agreement(orig_list, ngram_list, similarity=80, left=5, right=5):
    matches = defaultdict(list)
    all_particles = [a for group in particles for a in group]
    for n_gram in tqdm(ngram_list):
        orig_ngram = n_gram[-1]+' '+''.join(n_gram[:-1])
        ngram_indexes = [a for a in range(len(n_gram)-1)]
        total_holes = [a for a in ngram_indexes if no_trailing_tsek(n_gram[a]) in all_particles]
        # creates a list of triplets : (hole, list-of-other-holes, other-syllables)
        hollowed_ngram_indexes = [(j, [t for t in total_holes if t != j], [b for b in ngram_indexes if b != j and b not in total_holes]) for j in ngram_indexes if j != 0 and j != len(ngram_indexes)-1 and j in total_holes]
        # for the index of every syllable in orig_list
        for i in range(len(orig_list)-1):
            # for every ngram triplet
            for h in hollowed_ngram_indexes:
                hole = h[0]
                # if the syllable corresponding to the hole is a particle (first checks if the index exists in orig_list)
                if i + hole <= len(orig_list) - 1 and no_trailing_tsek(n_gram[hole]) in all_particles:
                    # then the levenstein index is calculated between the original syllable and the ngram one.
                    hole_syl_orig = no_trailing_tsek(orig_list[i + hole])
                    hole_syl_ngram = no_trailing_tsek(n_gram[hole])
                    lev_index = is_match(hole_syl_orig, hole_syl_ngram, similarity)
                    # if the levenstein measure is not 100% (syllables are same) and that it is higher than the similarity threshold
                    # also checks that the syllables are different once the punctuation has been stripped
                    if lev_index and no_punct(hole_syl_ngram) != no_punct(hole_syl_orig):
                        # then the other syllables in the ngram are checked :
                        # 1st check the levenstein measure for the other holes are higher than the threshold
                        remaining_holes = [t for t in total_holes if t != hole]
                        if True not in [is_match(no_trailing_tsek(orig_list[i+a]), no_trailing_tsek(n_gram[a]), similarity) for a in remaining_holes if i+a <= len(orig_list)-1]:
                        # 2nd check all other syllables are the same
                            hollowed_orig_slice = ''.join([orig_list[i + j] for j in h[2] if i + j <= len(orig_list) - 1])
                            hollowed_ngram_list = ''.join([n_gram[j] for j in h[2]])
                            if no_trailing_tsek(hollowed_orig_slice) == no_trailing_tsek(hollowed_ngram_list):
                                # then the syllables from orig_list can be considered a valid candidate and be added to the matches
                                # right and left contexts are also added, tackling the edge effects
                                left_idx = i-left
                                if left_idx < 0:
                                    left_idx = 0
                                right_idx = len(n_gram)-1+right
                                if right_idx >= len(orig_list)-1:
                                    right_idx = len(orig_list)-1
                                matches[orig_ngram].append(''.join(orig_list[left_idx:right_idx]))
    # formatting
    output = ''
    for t in sorted(matches, reverse=True):
        if matches[t]:
            output += t + '\n'
            # create a set then a list of the set to eliminate all the duplicates
            for occ in tib_sort(list(set(matches[t]))):
                output += '\t'+occ+'\n'
            output += '\n'
    return output

#raw_string = open_file('/home/drupchen/PycharmProjects/nalanda_corpus/gyu_raw/རྒྱུད། པུ།.txt').replace('\n', '')
#syls = Segment().segment(raw_string.replace('༌', '་'), ant_segment=1, unknown=0, space_at_punct=True)
#write_file('syls_seperated.txt', ''.join(syls))

# finding variants of a the ngrams
#original = open_file('./syls_seperated.txt').split(' ')
#ngrams = [a.split(' ')[:-1] for a in open_file('./reduced_algo3.txt').split('\n')]
#A = time.time()
#write_file('test.txt', ngram_minimal_pairs(original, ngrams))
#B = time.time()
#print(B-A)

# kangyur bigram agreement
#agrmnt_path = '/home/drupchen/Documents/TibTAL/ngram/kangyur_results/'+'5-grams_agreement.txt'
#text_path = '/home/drupchen/PycharmProjects/nalanda_corpus/gyu_raw/རྒྱུད། ཟི།.txt'
#text_path = '/home/drupchen/PycharmProjects/sandbox/Classes/tests/ngram_input/'+'ཤེར་ཕྱིན། ཉ།.txt'
out_path = './5-gram_agreement-check_རྒྱུད། ཟི།.txt'
# segmenting on syllables without separating the fusioned particles
#original = pre_process(open_file(text_path).replace('\n', '').replace('༌', '་'), mode='syls')
# segmenting on syllables separating fusioned particles
#original = Segment().segment(open_file(text_path).replace('\n', '').replace('༌', '་'), ant_segment=1, unknown=0, space_at_punct=True).split(' ')
#ngrams = [a.split(' ') for a in open_file(agrmnt_path).split('\n')]
#write_file(out_path, find_wrong_agreement(original, ngrams, similarity=80, left=6, right=6).replace('_', ' '))

# test
print(find_wrong_agreement(['དེ་', 'ནི་', 'བརྩོན་', 'འགྲུས་', 'ཀྱི་', 'ཕ་', 'རོལ་', 'དུ་', 'ཕྱིན་', 'པ་', 'རྣམ་', 'པར་', 'དག་', 'པས་', 'རབ་'], [['རོལ་', 'ཏུ་', 'ཕྱིན་', 'པའི་', 'རྣམ་', '2']], similarity=70, left=6, right=6).replace('_', ' '))
