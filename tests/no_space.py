import sys
import os
import re
path = os.path.dirname(sys.modules[__name__].__file__)
path = os.path.join(path, '..')
sys.path.insert(0, path)

from pytib import getSylComponents, Agreement, Segment


with open('/home/drupchen/Documents/TibTAL/Current/manual segmentation review/yoyo_js.txt', 'r', -1, 'utf-8-sig') as f:
    content = [line.strip() for line in f.readlines()]

out = []
for c in content:
    clean = re.sub(r'[\?\+\-\!]+', ' ', c)
    out.append(clean)#AntTib().no_space(clean))

with open('/home/drupchen/Documents/TibTAL/Current/manual segmentation review/ཤེར་ཕྱིན། ཀ_rev.txt', 'w', -1, 'utf-8-sig') as f:
    f.write('\n'.join(out))

