class PrepareTib:
    def __init__(self, tibstring):
        self.raw = tibstring.replace('\n', '')  # fast hack to get rid of all returns
        self.punct = [" ",
                      "༄", "༅", "࿓", "࿔", "༇", "༆", "༈",
                      "།", "༎", "༏", "༐", "༑", "༔",
                      "་", "༌",
                      "༼", "༽", "༒", "༓", "ཿ"]

    def gen_tuples(self):
        syllables = []
        puncts = []
        syl = ''
        for index, char in enumerate(self.raw):
            if index == 0:
                if char in self.punct:
                    puncts.append(char)
                else:
                    syl += char
            else:
                if char not in self.punct and self.raw[index-1] in self.punct:
                    syllables.append((syl, puncts))
                    puncts = []
                    syl = char
                elif char not in self.punct:
                    syl += char
                elif char in self.punct:
                    puncts.append(char)
        # add last syllable + its pre_process
        if syl != '':
            syllables.append((syl, puncts))
        return syllables

    def syl_tuples(self):
        tuples = PrepareTib.gen_tuples(self)
        return [(t[0], ''.join(t[1])) for t in tuples]

    def all_punct(self):
        tuples = PrepareTib.syl_tuples(self)
        return [t[0]+t[1] for t in tuples]

    def syls_only(self):
        tuples = PrepareTib.gen_tuples(self)
        return [t[0] for t in tuples]

    def tsheks_only(self):
        tuples = PrepareTib.syl_tuples(self)
        return [t[0]+'་' for t in tuples]

    def no_tshek(self):
        tuples = PrepareTib.syl_tuples(self)
        no_tshek = []
        for t in tuples:
            if '་' in t[1]:
                no_tshek.append(t[0]+t[1].replace('་', ''))
            else:
                no_tshek.append(t[0]+t[1])
        return no_tshek
