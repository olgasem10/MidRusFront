
def for_markup(input_conllu):
    if input_conllu == 'Вы ввели текст не в формате conllu!':
        return input_conllu
    try:
        tokens = input_conllu.strip('\n').split('\n')
        words = [w.split('\t') for w in tokens if not w.startswith('#')]
        all_words = [{'word':w[1], 'lemma':w[2], 'POS':w[3], 'features':w[5]} for w in words]
        return all_words
    except:
        return input_conllu