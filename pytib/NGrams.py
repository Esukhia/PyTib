from .common import DefaultOrderedDict, open_file, pre_process, temp_object
from itertools import tee, islice
import os
import sys
from subprocess import Popen, PIPE


def text2ngram(string, min=3, max=10, freq=5, windows=False):
    path = os.path.abspath(os.path.join(os.path.dirname(__file__), os.path.sep.join(['..', 'third_parties', 'ngramtool', 'unix'])))
    sys.path.insert(0, path)
    #my_env = os.environ.copy()
    #my_env["PATH"] = my_env["PATH"] + os.pathsep + path
    #print(my_env['PATH'])
    #if path not in sys.path:
    #    sys.path.append(path)
    temp_file = temp_object(string)

    # equivalent of: text2ngram -n3 -m10 -f5 file

    raw_grams = Popen([path+'text2ngram', '-n'+str(min), '-m'+str(max), '-f'+str(freq),
                       temp_file.name], shell=False, stdout=PIPE)
    return bytes.decode(raw_grams.communicate()[0])


def strreduction(string, algo='a2', freq='3'):
    temp_file = temp_object(string)

    # strreduction -a2 -s -f 3 < input > output
    processed = Popen(['third_parties / ngramtool / unix / strreduction', '-' + algo, '-s', '-f' + str(freq), '<',
                       temp_file.name], shell=False, stdout=PIPE)
    return bytes.decode(processed.communicate()[0])


class NGrams:
    def __init__(self):
        self.punct_regex = r'([༄༅༆༇༈།༎༏༐༑༔\s]+)'

    def __ngram_generator(self, iterable, n):
        # http://locallyoptimal.com/blog/2013/01/20/elegant-n-gram-generation-in-python/
        return zip(*((islice(seq, i, None) for i, seq in enumerate(tee(iterable, n)))))

    def _raw_ngrams(self, l, min=3, max=12):
        ngrams = DefaultOrderedDict(int)
        for a in range(min, max+1):
            grams = self.__ngram_generator(l, a)
            for g in grams:
                ngrams[g] += 1
        return [entry for entry in ngrams.items() if entry[1] > 1]

    def _ngrams_by_freq(self, raw, freq=10):
        ngrams = sorted(raw, key=lambda x: x[1], reverse=True)
        return [(n[1], ' '.join(n[0]), len(n[0])) for n in ngrams if n[1] >= freq]

    def _format_ngrams(self, l, sep='\t'):
        return '\n'.join([str(n[0]) + sep + n[1] + sep + str(n[2]) for n in l])

    def ngrams(self, l, freq=10, min=3, max=12):
        raw = self._raw_ngrams(l, min, max)
        by_freq = self._ngrams_by_freq(raw, freq)
        formatted = self._format_ngrams(by_freq)
        return formatted

    def __reduce_substrings(self, l, longer, level):
        shorter = set(self._raw_ngrams(l, level, level))
        substrings = set([s for s in shorter for l in longer if ''.join(s[0]) in ''.join(l[0]) and s[1] < l[1]])
        return list(shorter.difference(substrings))

    def no_substring_ngrams(self, l, min, max, freq=1, raw_output=False):
        levels = []
        for i in reversed(range(min, max+1)):
            # fetch higher level for comparison in filtered_level()
            if len(levels) != 0:
                levels.append(self.__reduce_substrings(l, levels[-1], i))
            else:
                # adds the highest level without filtering it
                up_level = self._raw_ngrams(l, i+1, i+1)
                levels.append(self.__reduce_substrings(l, up_level, i))

        # flatten the levels in a single list
        grams = [gram for level in levels for gram in level]

        # return the frequence-sorted n-grams
        # similar to _ngrams_by_freq() except that it starts with a list, so there is no .items() method called
        by_freq = sorted(grams, key=lambda x: x[1], reverse=True)
        by_freq = [(n[0], n[1]) for n in by_freq if n[1] >= freq]
        if raw_output:
            return by_freq
        else:
            return self._format_ngrams(by_freq)


def ngrams_by_folder(input_path, freq=2, min=3, max=12, unit='words'):
    ng = NGrams()
    ngram_total = DefaultOrderedDict(int)
    for f in os.listdir(input_path):
        raw = open_file(input_path+f)
        syls = pre_process(raw, mode=unit).tsheks_only()
        ngrams = ng._raw_ngrams(syls, min, max)
        for n in ngrams:
            ngram_total[n[0]] += n[1]
    ngram_total = ng._ngrams_by_freq(ngram_total, freq)
    return ng._format_ngrams(ngram_total)

#def syl_differing_strings(orig_list, ngrams):
