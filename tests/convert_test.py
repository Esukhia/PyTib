import sys
import os
path = os.path.dirname(sys.modules[__name__].__file__)
path = os.path.join(path, '..')
sys.path.insert(0, path)

from pytib import getSylComponents, Agreement, Segment, AntTib

with open('./files/Lamrim_cut.txt', 'r', -1, 'utf-8-sig') as f:
    content = [line.strip() for line in f.readlines()]

#seg = []
#for c in content:
#    if c != '':
#        seg.append(Segment().segment(c, ant_segment=0, unknown=1))
#    else:
#        seg.append(c)

ant = []
for s in content:
    if s != '':
        ant.append(AntTib().to_ant_text(s))
    else:
        ant.append(s)

with open('./files/ant.txt', 'w', -1, 'utf-8-sig') as f:
    f.write('\n'.join(ant))

#with open('./files/ant.txt', 'r', -1, 'utf-8-sig') as f:
#    ant = [line.strip() for line in f.readlines()]
uni = []
for a in ant:
    if a != '':
        uni.append(AntTib().from_ant_text(a))
    else:
        uni.append(a)

with open('./files/lamrim_commentary_uni.txt', 'w', -1, 'utf-8-sig') as f:
    f.write('\n'.join(uni))
