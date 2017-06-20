# -*- coding: utf-8 -*-

__author__ = """Drupchen Dorje"""
__email__ = 'hhdrupchen@gmail.com'
__version__ = '0.0.0'

import os
import json
from .SylComponents import SylComponents
from .common import open_file

# all the paths in use
this_dir = os.path.split(__file__)[0]
uncompound_path = os.path.join(this_dir, "data", "uncompound_lexicon.txt")
particles_path = os.path.join(this_dir, "data", "particles.json")
monlam_verbs_path = os.path.join(this_dir, "data", "monlam1_verbs.txt")
exceptions_path = os.path.join(this_dir, "data", "exceptions.txt")
vocab_path = os.path.join(this_dir, "user_vocabs")
compound_path = os.path.join(this_dir, "data", "compound_lexicon.csv")
ancient_path = os.path.join(this_dir, "data", "ancient.txt")
syl_components_path = os.path.join(this_dir, "data", "SylComponents.json")
agreement_path = os.path.join(this_dir, "data", "Agreement.json")

# lexicon used by Segment
lexicon = [line.strip() for line in open_file(uncompound_path).strip().split('\n')]
# extensions to the lexicon : exceptions (sskrt + others), particles
lexicon.extend(json.loads(open_file(particles_path))['particles'])
lexicon.extend([line for line in open_file(monlam_verbs_path).strip().split('\n')])
exceptions = [line.strip() for line in open_file(exceptions_path).strip().split('\n') if not line.startswith('#')]
lexicon.extend(exceptions)
# calculate the sizes of words in the lexicon, for segment()
len_word_syls = list(set([len(word.split('་')) for word in lexicon]))
len_word_syls = sorted(len_word_syls, reverse=True)

# Include user vocabulary lists in the lexicon
user_vocabs = {}
for f in os.listdir(vocab_path):
    origin = f.replace('.txt', '')
    entries = [line.strip() for line in open_file(os.path.join(vocab_path, f)).strip().split('\n') if not line.startswith('#')]
    user_vocabs[origin] = entries

# compound words to join by default
raw = [line.strip() for line in open_file(compound_path).strip().split('\n')]
# parse the data in the compound lexicon
compound = ([], [])
for line in raw[1:]:
    if line.strip().strip(',') != '' and not line.startswith('#'):
        # Todo : change to \t when putting in production
        parts = line.split(',')
        # list of words as created by the base segmentation
        compound[0].append(parts[2].replace('-', '').replace('+', '').split(' '))
        # list of words with the markers to split('+') and merge ('-')
        compound[1].append((parts[1].split(' '), parts[2].split(' '), parts[3].split(' ')))

# ancient spelling
ancient = [line.strip() for line in open_file(ancient_path).strip().split('\n')]

# data for SylComponents
data = json.loads(open_file(syl_components_path))
dadrag = data['dadrag']
roots = data['roots']
suffixes = data['suffixes']
Csuffixes = data['Csuffixes']
special = data['special']
wazurs = data['wazurs']
ambiguous = data['ambiguous']
m_roots = data['m_roots']
m_exceptions = data['m_exceptions']
m_wazurs = data['m_wazurs']
# hack to turn lists to tuples as required for SylComponents
for am in ambiguous:
    ambiguous[am] = (ambiguous[am][0], ambiguous[am][1])

# data for Agreement
a_data = json.loads(open_file(agreement_path))
particles = a_data['particles']
corrections = a_data['corrections']


def getSylComponents():
    if not getSylComponents.instance:
        getSylComponents.instance = SylComponents(dadrag, roots, suffixes, Csuffixes, special, wazurs, ambiguous, m_roots, m_exceptions, m_wazurs)
    return getSylComponents.instance
getSylComponents.instance = None


def Segment():
    from .Segmentation import Segment, strip_list, search
    SC = getSylComponents()
    return Segment(lexicon, compound, ancient, exceptions, len_word_syls, user_vocabs, SC)


def Agreement():
    from .Agreement import Agreement
    SC = getSylComponents()
    return Agreement(particles, corrections, SC)


__all__ = ['Segment', 'getSylComponents', 'Agreement']
