import ufal.udpipe
import sys
import conllu

class Model:
    def __init__(self, path):
        """Load given model."""
        self.model = ufal.udpipe.Model.load(path)
        if not self.model:
            raise Exception("Cannot load UDPipe model from file '%s'" % path)

    def tokenize(self, text):
        """Tokenize the text and return list of ufal.udpipe.Sentence-s."""
        tokenizer = self.model.newTokenizer(self.model.DEFAULT)
        if not tokenizer:
            raise Exception("The model does not have a tokenizer")
        return self._read(text, tokenizer)

    def read(self, text, in_format):
        """Load text in the given format (conllu|horizontal|vertical) and return list of ufal.udpipe.Sentence-s."""
        input_format = ufal.udpipe.InputFormat.newInputFormat(in_format)
        if not input_format:
            raise Exception("Cannot create input format '%s'" % in_format)
        return self._read(text, input_format)

    def _read(self, text, input_format):
        input_format.setText(text)
        error = ufal.udpipe.ProcessingError()
        sentences = []

        sentence = ufal.udpipe.Sentence()
        while input_format.nextSentence(sentence, error):
            sentences.append(sentence)
            sentence = ufal.udpipe.Sentence()
        if error.occurred():
            raise Exception(error.message)

        return sentences

    def tag(self, sentence):
        """Tag the given ufal.udpipe.Sentence (inplace)."""
        self.model.tag(sentence, self.model.DEFAULT)

    def parse(self, sentence):
        """Parse the given ufal.udpipe.Sentence (inplace)."""
        self.model.parse(sentence, self.model.DEFAULT)

    def write(self, sentences, out_format):
        """Write given ufal.udpipe.Sentence-s in the required format (conllu|horizontal|vertical)."""

        output_format = ufal.udpipe.OutputFormat.newOutputFormat(out_format)
        output = ''
        for sentence in sentences:
            output += output_format.writeSentence(sentence)
        output += output_format.finishDocument()

        return output

def main():
    model = Model('rnc6,5.udpipe')
    with open(sys.argv[1], 'r', encoding='utf8') as f:
        text = f.read()
    sentences = model.read(text, 'conllu')
    for s in sentences:
        model.tag(s)
    print(model.write(sentences, 'conllu'))


def output(lemmatized, tagged):
    ids_forms_and_lemmas = []
    lemmas = conllu.parse(lemmatized) # отсюда тащим айдишники, словоформы и леммы
    for i in range(len(lemmas)):
        for j in range(len(lemmas[i])):
            id = lemmas[i][j]['id']
            form = lemmas[i][j]['form']
            lemma = lemmas[i][j]['lemma']
            id_form_and_lemma = str(id) + "\t" + form + "\t" + lemma + '\t' # склеиваем
            ids_forms_and_lemmas.append(id_form_and_lemma)
    evr_else = []
    tags = conllu.parse(tagged) # а отсюда части речи и фичи
    for i in range(len(tags)):
        for j in range(len(tags[i])):
            upos = tags[i][j]['upostag']
            feats = tags[i][j]['feats']
            if feats == None:
                feats = '_'
            else:
                feats = "|".join(["{}={}".format(k, v) for k, v in feats.items()]) # танцы с бубном, потому что
                # формат фичей изначально OrderedDict, который не склеивается с другими переменными
            el = upos + "\t" + '_' + "\t" + feats + '\t' + '_' + "\t" + '_' + "\t" + '_' + '\t'+ '_' # склеиваем
            evr_else.append(el)
    sents = ''
    for ifl, ee in zip(ids_forms_and_lemmas, evr_else):
        sent = ifl + ee
        sents += sent + '\n'
    return sents


def tag_text(text, model1, model2, toks, lemmas):

    #И токенизация и лемматизация
    if toks and lemmas:
        sentences = model2.read(text, 'horizontal')
        for s in sentences:
            model2.tag(s)
        lemmatized = model2.write(sentences, 'conllu')
        for s in sentences:
            model1.tag(s)
        tagged = model1.write(sentences, 'conllu')
        result = output(lemmatized, tagged)
        return result

    # Без токенизации и без лемматизации
    if not toks and not lemmas:
        try:
            sentences = model1.read(text, 'conllu')
            for s in sentences:
                model1.tag(s)
            result = model1.write(sentences, 'conllu')
        except:
            result = 'Вы ввели текст не в формате conllu!'
        return result

    # Токенизировать, но не лемматизировать
    if toks and not lemmas:
        sentences = model2.read(text, 'horizontal')
        for s in sentences:
            model1.tag(s)
        result = model1.write(sentences, 'conllu')
        return result

    # Без токенизации, но с лемматизацией
    if not toks and lemmas:
        try:
            sentences = model2.read(text, 'conllu')
            for s in sentences:
                model2.tag(s)
            lemmatized = model2.write(sentences, 'conllu')
            for s in sentences:
                model1.tag(s)
            tagged = model1.write(sentences, 'conllu')
            result = output(lemmatized, tagged)
        except:
            result = 'Вы ввели текст не в формате conllu!'
        return result


if __name__ == '__main__':
    main()