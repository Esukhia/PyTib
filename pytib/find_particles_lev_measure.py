import Levenshtein
# we take for granted any particle could be mistaken for another in the same list
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
    ['པར', 'བར'],
    ['པའི', 'བའི'],
    ['པོར', 'བོར']
            ]
all_particles = [a for group in particles for a in group]


def find_min_max(part_list, algo=''):
    min = 100.00
    max = 0.00
    for group in part_list:
        for i in range(len(group)-1):
            remainder = [a for a in group if a != group[i]]
            for r in remainder:
                if algo == 'jaro_winkler':
                    # with jaro_winkler, the minimal value must be 66.66 and maximal 95.33
                    measure = Levenshtein.jaro_winkler(group[i], r)*100
                if algo == 'jaro':
                    # with jaro, the minimal value must be 66.66 and maximal 93.33
                    measure = Levenshtein.jaro(group[i], r)*100
                if measure < min:
                    min = measure
                if measure > max:
                    max = measure
    return min, max


def differences(all_particles, algo1='', algo2='', threshold1=66, threshold2=63):
    def _generate(all_particles):
        results1 = []
        results2 = []
        for i in range(len(all_particles) - 1):
            remainder = [a for a in all_particles if a != all_particles[i]]
            # generate all tuples
            for r in remainder:
                j = Levenshtein.jaro(all_particles[i], r) * 100
                jw = Levenshtein.jaro_winkler(all_particles[i], r) * 100
                if j >= threshold1 and jw >= threshold2:
                    continue
                elif j >= threshold1:
                    results1.append((all_particles[i], r))
                elif jw >= threshold2:
                    results2.append((all_particles[i], r))
        return results1, results2

    if algo1 == 'jaro' and algo2 == 'jaro_winkler':
        algo1_only, algo2_only = _generate(all_particles)
        print(len(algo1_only))
        print(len(algo2_only))
        return algo1_only, algo2_only

mm = find_min_max(particles, 'jaro_winkler')
print('min', mm[0])
print('max', mm[1])
m = find_min_max(particles, 'jaro')
print('min', m[0])
print('max', m[1])

diff = differences(all_particles, 'jaro', 'jaro_winkler', threshold1=80, threshold2=80)
print('jaro only:\n', diff[0])
print('jaro_winkler only:\n', diff[1])
for d in diff[1]:
    print(Levenshtein.jaro(d[0], d[1]))