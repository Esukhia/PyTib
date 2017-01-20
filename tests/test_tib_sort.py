import sys
import os
path = os.path.dirname(sys.modules[__name__].__file__)
path = os.path.join(path, '..')
sys.path.insert(0, path)
from pytib.common import tib_sort

liste = ['སྲོལ་རྒྱུན', 'སྲོལ་རྫུན', 'སླ་བོ', 'སླ་མོ', 'སླ་ཤོས', 'སླད', 'སླར་ཡང', 'སླེ་གྲུག', 'སླེབས', 'སླར', 'སླེབས་པ', 'སློང', 'སྲོལ་བཙུགས']
print(liste)
print(tib_sort(liste))
