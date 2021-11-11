from re import findall

from os.path import join
from os import getcwd, listdir

from praatio import tgio
from praatio.praatio_scripts import alignBoundariesAcrossTiers

def all_textgrids():  # ищет все текстгриды
    textgrids_names = []
    tdir = join(getcwd(), 'grids')
    dirs = listdir(tdir)
    for file in dirs:
        textgrids_names.extend(findall(r'(\b.+)\.[Tt]ext[Gg]rid\b', file))
    return textgrids_names

def corr():  # выравнивает границы по слоям
    alltg = all_textgrids()
    for tgname in alltg:
        inputFN = join(getcwd(), 'grids', tgname + '.TextGrid')
        tg = alignBoundariesAcrossTiers(inputFN)
        tg.save(join(getcwd(), 'grids', tgname + '.TextGrid'))

def main():
    alltg = all_textgrids()
    with open('konkord15_4_19.csv', 'w', encoding='utf-16') as f:
        pass
    with open('konkord15_4_19_2.csv', 'w', encoding='utf-16') as f:
        pass
    CHA = {}
    lCHA = {}
    pCHA = {}
    tokens = 0
    for tgname in alltg:
        inputFN = join(getcwd(), 'grids', tgname + '.TextGrid')
        tg = tgio.openTextgrid(inputFN)
        #tNL = tg.tierNameList
        tD = tg.tierDict
        transc, morph, gloss, lemma, pos, transl = [tD[name] for name in ['speakerid_Transcription-txt-rut',
                                                                               'speakerid_Morph-txt-rut',
                                                                               'speakerid_Gloss-txt-en',
                                                                               'speakerid_Lemma-txt-rut',
                                                                               'speakerid_POS-txt-en',
                                                                               'speakerid_Translation-gls-en']]

        TOT = []
        for minterval in morph.entryList:
            if minterval.label == '':
                continue
            mstart = minterval.start
            mend = minterval.end
            glabel, llabel, plabel, tClabel, tLlabel = 'non', 'non', 'non', 'non', 'non'
            for ginterval in gloss.entryList:
                if mstart == ginterval.start and mend == ginterval.end:
                    glabel = ginterval.label
                    break
            for linterval in lemma.entryList:
                if mstart == linterval.start and mend == linterval.end:
                    llabel = linterval.label
            for pinterval in pos.entryList:
                if mstart == pinterval.start and mend == pinterval.end:
                    plabel = pinterval.label

            for tCinterval in transc.entryList:
                if mstart >= tCinterval.start and mend <= tCinterval.end:
                    tClabel = tCinterval.label
            for tLinterval in transl.entryList:
                if mstart >= tLinterval.start and mend <= tLinterval.end:
                    tLlabel = tLinterval.label

            TOT.append(tuple([mstart, mend, minterval.label, glabel, llabel, plabel, tClabel, tLlabel, tgname]))

            key = plabel + '\t' + llabel + '\t' + minterval.label + '\t' + glabel
            if key in CHA.keys():
                CHA[key] += 1
            else:
                CHA[key] = 1

            lkey = plabel + '\t' + llabel
            if lkey in lCHA.keys():
                lCHA[lkey] += 1
            else:
                lCHA[lkey] = 1

            if plabel in pCHA.keys():
                pCHA[plabel] += 1
            else:
                pCHA[plabel] = 1
        tokens += len(TOT)
        with open('konkord15_4_19.csv', 'a', encoding='utf-16') as f:
            for i in range(len(TOT)):
                f.write(str(TOT[i][0]) + '\t' + str(TOT[i][1]) + '\t' + str(TOT[i][2]) + '\t' + str(TOT[i][3]) + '\t'
                        + str(TOT[i][4]) + '\t' + str(TOT[i][5]) + '\t' + str(TOT[i][6]) + '\t' + str(TOT[i][7])
                        + '\t' + tgname + '\n')

    with open('konkord15_4_19_2.csv', 'a', encoding='utf-16') as f:
        for k in CHA.keys():
            lk = k.split('\t')[0] + '\t' + k.split('\t')[1]
            f.write(str(lCHA[lk]) + '\t' + k + '\t' + str(CHA[k]) + '\n')
        for k in pCHA.keys():
            f.write(k + '\t' + str(pCHA[k]) + '\n')
        f.write('Lemmas:' + '\t' + str(len(lCHA)) + '\n')
        f.write('Wordforms:' + '\t' + str(len(CHA)) + '\n')
        f.write('Tokens:' + '\t' + str(tokens))


if __name__ == '__main__':
    corr()
    main()
