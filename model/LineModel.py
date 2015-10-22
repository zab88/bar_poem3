# -*- coding: utf-8 -*-
import nltk
import string
from WordModel import WordModel
import SettingsModel
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
    ACCENT_TYPE_None = None

    def __init__(self, line_original):
        self.line_original = line_original.decode('utf-8').lower().encode('utf-8')
        SettingsModel.CURRENT_LINE_ORIGINAL = self.line_original.decode('utf-8')
        self.words = []
        self.__init_words__()
        self.__init_accent_type__()

    def __init_words__(self):
        #tokenization
        global stopwords
        ololo_tokens = self.line_original.replace('?', ' ').replace('!', ' ')
        tokens = nltk.word_tokenize( ololo_tokens )
        tokens = [i for i in tokens if ( i not in string.punctuation )]
        tokens = [i for i in tokens if ( i not in ['...', '—', '»', '«', '“', ',', "„", ':', "."] )]
        #now we do not need stop words elimination
        if False:
            tokens = [i for i in tokens if ( i not in stopwords )]
        for w in tokens:
            new_word_model = WordModel(w)
            #print(new_word_model.word_original)
            if new_word_model.word_original != '':
                self.words.append(new_word_model)

    def __init_accent_type__(self):
        if len(self.words) < 1:
            self.accent_type = self.ACCENT_TYPE_None
            return
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
        # print(w.word_original, self.accent_type)

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

    #http://www.dialog-21.ru/digests/dialog2006/materials/pdf/Kozmin.pdf
    #getting metrical feet for single line
    def get_metrical_feet(self):
        #split on syllables
        vowels = [u'а', u'у', u'о', u'ы', u'и', u'э', u'я', u'ю', u'ё', u'е',
                  u'А', u'У', u'О', u'Ы', u'И', u'Э', u'Я', u'Ю', u'Ё', u'Е',]
        vector = []
        for w in self.words:
            vector_word = []
            #each syllable define as 1, getting vector_word of 1
            for letter in w.word_original:
                if letter in vowels:
                    vector_word.append(1)
            #continue if no vowels in the word
            if len(vector_word) < 1:
                continue
            #set accent only if one variant possible
            #1 - syllables without accent
            #2 - one syllable word accent
            #3 - stressed syllable on first position in 2 syllable words
            #4 - stressed syllable on second position in 2 syllable words
            #5 - stressed syllable in long words
            if len(w.accent) == 1 and w.accent[0] != 255:
                num = 1
                accent = w.accent[0]
                if len(vector_word) == 1:
                    num = 2
                elif len(vector_word) == 2:
                    if accent == 1:
                        num = 3
                    elif accent == 0:
                        num = 4
                elif len(vector_word) > 2:
                    num = 5

                #substitution
                #print(vector_word, accent, w)
                vector_word[ len(vector_word) - accent - 1 ] = num
            else:
                #no information about accent. lets omit it
                #print(w.word_original)
                return None, None
            vector = vector + vector_word

        #ok, we have vector, let's check it
        test41 = vector[0::2]
        is_ymb = False
        # print(vector)
        if 3 not in test41 and 4 not in test41 and 5 not in test41:
            if self.checkpoint5('yamb', vector) is True:
                is_ymb = True
            # is_ymb = any(x in [1, 2] for x in test41)

        test42 = vector[1::2]
        is_horey = False
        if 3 not in test42 and 4 not in test42 and 5 not in test42:
            if self.checkpoint5('horey', vector) is True:
                is_horey = True
            # is_horey = any(x in [1, 2] for x in test42)

        is_daktil_1 = any(x in [1, 2, 3] for x in vector[1::3])
        is_daktil_2 = any(x in [1, 2, 4] for x in vector[2::3])
        is_daktil = False
        if is_daktil_1 and is_daktil_2:
            if self.checkpoint5('daktil', vector) is True:
                is_daktil = True

        is_anapest_1 = any(x in [1, 2, 3] for x in vector[0::3])
        is_anapest_2 = any(x in [1, 2, 4] for x in vector[1::3])
        is_anapest = False
        if is_anapest_1 and is_anapest_2:
            if self.checkpoint5('anapest', vector) is True:
                is_anapest = True

        is_amfibrahii_1 = any(x in [1, 2, 3] for x in vector[2::3])
        is_amfibrahii_2 = any(x in [1, 2, 4] for x in vector[0::3])
        is_amfibrahii = False
        if is_amfibrahii_1 and is_amfibrahii_2:
            if self.checkpoint5('amfibrahii', vector) is True:
                is_amfibrahii = True

        if is_ymb:
            return 'yamb', float( len(vector) )/2.
        if is_horey:
            return 'horey', float( len(vector) )/2.
        if is_daktil:
            return 'daktil', float( len(vector) )/3.
        if is_anapest:
            return 'anapest', float( len(vector) )/3.
        if is_amfibrahii:
            return 'amfibrahii', float( len(vector) )/3.

        #TODO: more check

        return None, None
        # return vector
    def checkpoint5(self, type, vector):
        if type == 'yamb':
            vector_check = vector[1::2]
        elif type == 'horey':
            vector_check = vector[0::2]
        elif type == 'daktil':
            vector_check = vector[0::3]
        elif type == 'amfibrahii':
            vector_check = vector[1::3]
        elif type == 'anapest':
            vector_check = vector[2::3]

        a_sum = 0
        for a in vector_check:
            if a == 1:
                a_sum += 1
        if len(vector_check)==0:
            return False
        if ( float(a_sum)/float(len(vector_check)) ) > 0.345:
            return False
        return True

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
