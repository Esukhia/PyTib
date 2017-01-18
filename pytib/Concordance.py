def lexicon_concs(string, left, right):
    words = string.replace('\n', '').split()
    concordances = {}
    for i in range(len(words)-1):
        match = words[i]
        if match.startswith('#'):

            left_context = []
            l = 1
            while i-l >= 0 and i-l >= i-left:
                left_context.insert(0, words[i-l])
                l += 1

            right_context = []
            r = 1
            while i+r <= len(words) and i+r <= i+right:
                right_context.append(words[i+r])
                r += 1
            if match in concordances.keys():
                concordances[match].append((' '.join(left_context), match, ' '.join(right_context)))
            else:
                concordances[match] = [(' '.join(left_context), match, ' '.join(right_context))]

    sorted_concs = sorted(concordances, key=lambda x: len(concordances[x]), reverse=True)
    return [(conc,  concordances[conc]) for conc in sorted_concs]


def no_tab_lexicon_concs(string):
    out = ''
    for a, conc in enumerate(lexicon_concs(string, 5, 5)):
        out += '\t' + str(a+1) + '\t' + conc[0] + '\n'
        for b, occ in enumerate(conc[1]):
            out += str(b + 1) + '\t' + occ[0] + ' ' + occ[1] + ' ' + occ[2] + '\n'
        out += '\n'
    return out

