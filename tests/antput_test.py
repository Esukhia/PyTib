import sys
import os
path = os.path.dirname(sys.modules[__name__].__file__)
path = os.path.join(path, '..')
sys.path.insert(0, path)

from pytib import AntPut

with open('files/AntPut/In/antconc_keyword list.txt', 'r', -1, 'utf-8-sig') as f:
    content_a = f.read()
kwl = AntPut().keyword_list(content_a)

with open('files/AntPut/In/antconc_cluster.txt', 'r', -1, 'utf-8-sig') as f:
    content_b = f.read()
clt = AntPut().cluster(content_b)

with open('files/AntPut/In/antconc_collocates.txt', 'r', -1, 'utf-8-sig') as f:
    content_c = f.read()
clc = AntPut().collocates(content_c)

with open('files/AntPut/In/antconc_concordance.txt', 'r', -1, 'utf-8-sig') as f:
    content_d = f.read()
ccd = AntPut().concordance(content_d)

with open('files/AntPut/In/antconc_ngram.txt', 'r', -1, 'utf-8-sig') as f:
    content_e = f.read()
ngr = AntPut().ngram(content_e)

with open('files/AntPut/In/antconc_word list.txt', 'r', -1, 'utf-8-sig') as f:
    content_f = f.read()
wdl = AntPut().word_list(content_f)

with open('files/AntPut/In/antprofiler_level list.txt', 'r', -1, 'utf-8-sig') as f:
    content_g = f.read()
pll = AntPut().words(content_g)

with open('files/AntPut/In/antprofiler_level tags.txt', 'r', -1, 'utf-8-sig') as f:
    content_h = f.read()
plt = AntPut().profiler_tags(content_h)

with open('files/AntPut/In/Level 1 - 1000 words.txt', 'r', -1, 'utf-8-sig') as f:
    content_i = f.read()
pws = AntPut().words(content_i)

with open('files/AntPut/In/antprofiler_statistics.txt', 'r', -1, 'utf-8-sig') as f:
    content_j = f.read()
pst = AntPut().profiler_stats(content_j)

results = {
    # Antconc
    'keyword_list': kwl,  # AntPut().keyword_list()
    'cluster': clt,       # AntPut().cluster()
    'collocates': clc,    # AntPut().collocates()
    'concordance': ccd,   # AntPut().concordance()
    'n_gram': ngr,         # AntPut().n_gram()
    'word_list': wdl,     # AntPut().word_list()
    # Word profiler
    'level_list': pll,    # AntPut().words()
    'level_tags': plt,    # Antput().profiler_tags() same for 'non level tags' files
    '1000_words': pws,    # AntPut().words() same for 'level list' files
    'statistics': pst,    # AntPut().profiler_stats()
}
for result in results:
    with open('files/AntPut/Out/'+result+'_uni.csv', 'w', -1, 'utf-8-sig') as f:
        f.write(results[result])
