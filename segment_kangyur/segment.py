import sys
import os
path = os.path.dirname(sys.modules[__name__].__file__)
path = os.path.join(path, '..')
sys.path.insert(0, path)
import pytib
from pytib.common import open_file, write_file

seg = pytib.Segment()
in_path = 'raw_kangyur'
for f in os.listdir(in_path):
    content = open_file('{}/{}'.format(in_path, f))
    segmented = seg.segment(content)
    write_file('output/'+f.replace('.txt', '_seg.txt'), segmented)
