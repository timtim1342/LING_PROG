from re import findall, sub

from os.path import join
from os import getcwd, listdir

from praatio import tgio
from praatio.praatio_scripts import alignBoundariesAcrossTiers

def all_textgrids():  # ищет все текстгриды
    textgrids_names = []
    tdir = join(getcwd(), 'cyrillic')
    dirs = listdir(tdir)
    for file in dirs:
        textgrids_names.extend(findall(r'(\b.+)\.[Tt]ext[Gg]rid\b', file))
    return textgrids_names

def open_tg(tgname):  # переносит грид сюда
    inputFN = join(getcwd(), 'cyrillic', tgname + '.TextGrid')
    try:
        tg = alignBoundariesAcrossTiers(inputFN, maxDifference=0.15)
    except:
        tg = tgio.openTextgrid(inputFN)
    return tg

def tg_tiers(tg):  # переносит слои
    tD = tg.tierDict
    transc_tier, transl_tier, note_tier = tD['1'], tD['2'], \
                                          tD['3']
    return transc_tier, transl_tier, note_tier

def tg_tiers_dial(tg):  # для диалогов
    tD = tg.tierDict
    A_transc_tier, A_transl_tier, B_transc_tier, B_transl_tier, note_tier = tD['1'], tD['2'], tD['3'], tD['4'], tD['5']
    return A_transc_tier, A_transl_tier, B_transc_tier, B_transl_tier, note_tier

def translit_dict():  # делает словарь трансл
    with open('transl_dict.csv', 'r', encoding='UTF-8') as f:
        txt = f.read()
    txt_list = txt.split('\n')
    txt_list = [i.split(';') for i in txt_list]
    translit_dict = {i[0]:i[1] for i in txt_list if len(i) == 2 and i[0] != ''}
    translit_dict_cap = {}
    for key in translit_dict.keys(): #  ad capitals
        translit_dict_cap[key.capitalize()] = translit_dict[key].capitalize()
    translit_dict.update(translit_dict_cap)

    return translit_dict

def new_TG(name):
    tg = open_tg(name)
    final_tier = []
    tt, Tt, nt = tg_tiers(tg)
    transl_dict = translit_dict()
    tEL = tt.entryList


    for start, stop, label in tEL:  # создает шаблон с временными границами по слою с транскр
        russian = findall(r'\[R.*\]', label)
        label = label.lower()  # убрать, если нужны звглавные
        label = label.replace('=', '')  # костины =

        label = label.split()  # меняет ё ю я в начале слов
        for i in range(len(label)):
            if label[i].startswith('я'):
                label[i] = label[i].replace('я', 'ja', 1)
            elif label[i].startswith('ё'):
                label[i] = label[i].replace('ё', 'jo', 1)
            elif label[i].startswith('ю'):
                label[i] = label[i].replace('ю', 'ju', 1)
        label = ' '.join(label)

        for key in sorted(transl_dict.keys(), key = len, reverse=True):

            label = label.replace(key, transl_dict[key])  # транслитит

        if len(russian) > 0:
            print(label)
            russian_transl = findall(r'\[r.*\]', label)
            for i in range(len(russian)):
                label = label.replace(russian_transl[i], russian[i])

        final_tier.append([start, stop, label])

    new_Ttier = tt.new(entryList=final_tier)  # слой c лат
    tg = tgio.Textgrid()
    t_tier = tt  # слой с кир
    Tr_t = t_tier.new(name='speakerid_LTranscription-txt-rut')
    tg.addTier(new_Ttier)
    tg.addTier(Tr_t)
    tg.addTier(Tt)
    tg.addTier(nt)
    inputFN = join(getcwd(), 'latin', name + '.TextGrid')
    tg.save(inputFN)

def new_TG_dial(name):
    tg = open_tg(name)
    final_tier_A = []
    final_tier_B = []
    tt_A, Tt_A, tt_B, Tt_B, nt = tg_tiers_dial(tg)
    transl_dict = translit_dict()
    tEL_A = tt_A.entryList
    tEL_B = tt_B.entryList


    for start, stop, label in tEL_A:  # создает шаблон с временными границами по слою с транскр
        russian = findall(r'\[R.*\]', label)
        label = label.lower()  # убрать, если нужны звглавные

        label = label.split()  # меняет ё ю я в начале слов
        for i in range(len(label)):
            if label[i].startswith('я'):
                label[i] = label[i].replace('я', 'ja', 1)
            elif label[i].startswith('ё'):
                label[i] = label[i].replace('ё', 'jo', 1)
            elif label[i].startswith('ю'):
                label[i] = label[i].replace('ю', 'ju', 1)
        label = ' '.join(label)

        for key in sorted(transl_dict.keys(), key=len, reverse=True):

            label = label.replace(key, transl_dict[key])  # транслитит

        if len(russian) > 0:
            print(label)
            russian_transl = findall(r'\[r.*\]', label)
            for i in range(len(russian)):
                label = label.replace(russian_transl[i], russian[i])

        final_tier_A.append([start, stop, label])

    for start, stop, label in tEL_B:  # то же самое!
        russian = findall(r'\[R.*\]', label)
        label = label.lower()  # убрать, если нужны звглавные

        label = label.split()  # меняет ё ю я в начале слов
        for i in range(len(label)):
            if label[i].startswith('я'):
                label[i] = label[i].replace('я', 'ja', 1)
            elif label[i].startswith('ё'):
                label[i] = label[i].replace('ё', 'jo', 1)
            elif label[i].startswith('ю'):
                label[i] = label[i].replace('ю', 'ju', 1)
        label = ' '.join(label)

        for key in sorted(transl_dict.keys(), key=len, reverse=True):

            label = label.replace(key, transl_dict[key])  # транслитит

        if len(russian) > 0:
            print(label)
            russian_transl = findall(r'\[r.*\]', label)
            for i in range(len(russian)):
                label = label.replace(russian_transl[i], russian[i])

        final_tier_B.append([start, stop, label])

    new_Ttier_A = tt_A.new(entryList=final_tier_A)  # слой c лат
    tg = tgio.Textgrid()
    t_tier_A = tt_A  # слой с кир
    Tr_t_A = t_tier_A.new(name='A_LTranscription-txt-rut')
    tg.addTier(new_Ttier_A)
    tg.addTier(Tr_t_A)
    tg.addTier(Tt_A)

    new_Ttier_B = tt_B.new(entryList=final_tier_B)  # слой c лат
    t_tier_B = tt_B  # слой с кир
    Tr_t_B = t_tier_B.new(name='B_LTranscription-txt-rut')
    tg.addTier(new_Ttier_B)
    tg.addTier(Tr_t_B)
    tg.addTier(Tt_B)
    tg.addTier(nt)

    inputFN = join(getcwd(), 'latin', name + '.TextGrid')
    tg.save(inputFN)

def symb_dict(name):
    tg = open_tg(name)
    symb_d = {}
    tt, Tt, nt = tg_tiers(tg)
    transl_dict = translit_dict()
    tEL = tt.entryList

    for start, stop, label in tEL:  # создает шаблон с временными границами по слою с транскр
        for key in sorted(transl_dict.keys(), key=len, reverse=True):
            label = label.replace(key, transl_dict[key])  # транслитит
        for symb in label:

            if symb in symb_d.keys():
                symb_d[symb] += 1
            else:
                symb_d[symb] = 1
    return symb_d

def wr_symb_dict(symb_d):
    with open('symb.csv', 'w', encoding='utf-8') as f:
        for key in symb_d.keys():
            s = key + '\t' + str(symb_d[key]) + '\n'
            f.write(s)

def wordworms(name):
    tg = open_tg(name)
    wordforms_d = {}
    tt, Tt, nt = tg_tiers(tg)
    transl_dict = translit_dict()
    tEL = tt.entryList

    for start, stop, label in tEL:  # создает шаблон с временными границами по слою с транскр
        for key in sorted(transl_dict.keys(), key=len, reverse=True):
            label = label.replace(key, transl_dict[key])  # транслитит
            label = sub('[,.!?(){};\"]', '', label)
            words = label.split()
        for word in words:
            if word in wordforms_d.keys():
                wordforms_d[word] += 1
            else:
                wordforms_d[word] = 1
    return wordforms_d

def main():
    TGnames = all_textgrids()
    total_worforms_d = {}
    for name in TGnames:
        print(name)
        new_TG(name)  # new_TG_dial(name)
        '''wordforms_d = wordworms(name)  # replace all from here on: new_TG(name)
        for key in wordforms_d.keys():
            if key in total_worforms_d.keys():
                total_worforms_d[key] += wordforms_d[key]
            else:
                total_worforms_d[key] = wordforms_d[key]
    wr_symb_dict(total_worforms_d)'''


if __name__ == '__main__':
    main()