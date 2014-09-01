# -*- coding: utf-8 -*-
import nltk
import string
from WordModel import WordModel
stopwords = nltk.corpus.stopwords.words('russian')
# stopwords.extend([u'ТАК'.encode('utf-8'), u'ЧТО'.encode('utf-8'), u'ВОТ'.encode('utf-8'), u'ЭТО'.encode('utf-8'), u'КАК'.encode('utf-8')])
# stopwords.extend([u'БЫТЬ'.encode('utf-8'), u'a'.encode('utf-8')])
stopwords.extend(['а'])

ALL_HOMONYMS = {}

class LineModel():
    line_original = ''
    #words = []
    #accent_type

    ACCENT_TYPE_M = 'M'
    ACCENT_TYPE_F = 'F'
    ACCENT_TYPE_D = 'D'
    ACCENT_TYPE_N = 'N'

    def __init__(self, line_original):
        self.line_original = line_original.decode('utf-8').lower().encode('utf-8')
        self.words = []
        self.__init_words__()
        self.__init_accent_type__()

    def __init_words__(self):
        #tokenization
        global stopwords
        tokens = nltk.word_tokenize( self.line_original )
        tokens = [i for i in tokens if ( i not in string.punctuation )]
        tokens = [i for i in tokens if ( i not in stopwords )]
        for w in tokens:
            new_word_model = WordModel(w)
            #print(new_word_model.word_original)
            self.words.append(new_word_model)

    def __init_accent_type__(self):
        w = self.words[-1:][0]
        if len(w.accent) == 1:
            if w.accent[0] == 255:
                self.accent_type = self.ACCENT_TYPE_N
            elif w.accent[0] == 0:
                self.accent_type = self.ACCENT_TYPE_M
            elif w.accent[0] == 1:
                self.accent_type = self.ACCENT_TYPE_F
            elif w.accent[0] > 1:
                self.accent_type = self.ACCENT_TYPE_D
        else:
            self.accent_type = self.ACCENT_TYPE_N

    def getHighlightingHomonyms(self):
        homonym_exists = False
        #print(self.line_original)
        new_line = str(self.line_original)
        for w in self.words:
            if w.isHomonim:
                #print(w.word_original)
                homonym_exists = True
                new_line = self.highlight_words(new_line, w)
        if homonym_exists is True:
            return new_line
        else:
            return None

    def countHomonyms(self):
        global ALL_HOMONYMS, ALL_HOMONYMS_NUM
        for w in self.words:
            if w.isHomonim:
                #searchiong for place of word
                num = ALL_HOMONYMS.get(w.word_original, 0)
                num += 1
                ALL_HOMONYMS[w.word_original] = num

                # if w.word_original in ALL_HOMONYMS:
                #     index = ALL_HOMONYMS.index(w.word_original)
                # else:
                #     index = -1
                #
                # if index < 0:
                #     ALL_HOMONYMS.append(w.word_original)
                #     ALL_HOMONYMS_NUM.append(1)
                # else:
                #     ALL_HOMONYMS_NUM[index] = ALL_HOMONYMS_NUM[index] + 1
        return ALL_HOMONYMS


    def highlight_words(self, line, word):
        #print(line, word)
        old_line = str(line)
        line = line.decode('utf-8')
        word_to_replace = u"<a target='_blank' href='http://starling.rinet.ru/cgi-bin/morph.cgi?word=["+word.word_lat+u"]'>"+\
                          word.word_original+u"</a>"

        word_to_replace = word.word_original + u" <span style='color:green'>("+\
                          u", ".join(word.homonym_norm)+u" -- "+u", ".join(word.homonym_pos)+u")</span> "
        #word_to_replace = word_to_replace.encode('utf-8')
        #print(line, word_to_replace)
        line = line.replace(word.word_original, word_to_replace )

        line = line.encode('utf-8')
        if old_line == line:
            print line
            print word.word_original
        return line

        # indexes = [i for i in range(len(line)) if line.startswith(word, i)]
        # length = len(word)
        # for id in indexes:
        #     new_line = ''
