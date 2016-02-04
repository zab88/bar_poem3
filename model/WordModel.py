# -*- coding: utf-8 -*-
import pymorphy2
import pymysql
from PhoneticModel import PhoneticModel
import SettingsModel

#init pymorphy2
MorphEngine = pymorphy2.MorphAnalyzer()
#init pymysql
conn = pymysql.connect(host='127.0.0.1', port=3306, user='bar_poem3', passwd='ACLQ7E7JcAwE9K3e', db='bar_poem3', charset='utf8', autocommit = True)
curDB = conn.cursor()
curDB.execute('set names utf8')
HomonimArray = []

#read homonyms
# conn = pymysql.connect(host='127.0.0.1', port=3306, user='root', passwd='', db='sample', charset='utf8')
# curDB = conn.cursor()

# curDB.execute("SELECT * FROM words WHERE html LIKE '%2 variant%' LIMIT 100") #35, 68
# curDB.execute("SELECT * FROM words WHERE html LIKE '%2 variant:%'")
# i = 0
# for r in curDB.fetchall():
#     HomonimArray.append(r)

class WordModel(object):
    #!word_original = ''
    #!accent = []
    isHomonim = False
    id_zaliznyak = 0
    is_debug = False
    word_lat = ''

    parsed = []
    homonym_norm = []
    homonym_pos = []

    def __init__(self, word_original):
        self.word_original = word_original.replace(",", "")
        self.word_original = self.word_original.replace(".", "")
        self.word_original = self.word_original.replace("!", "")
        self.word_original = self.word_original.replace("?", "")
        self.word_original = self.word_original.replace(":", "")
        self.word_original = self.word_original.replace(";", "")
        self.word_original = self.word_original.replace("„", "")
        self.word_original = self.word_original.replace("„", "")
        self.word_original = self.word_original.replace("«", "")
        self.word_original = self.word_original.replace("»", "")
        self.word_original = self.word_original.replace("“", "")
        if self.word_original == '':
            print('empty word')

        self.word_original = self.word_original.decode('utf-8')
        self.accent = []
        self.makeMorphAnalyse()

        self.get_aot_accent()

    def makeMorphAnalyse(self):
        global MorphEngine
        self.parsed = MorphEngine.parse( self.word_original )
        if len(self.parsed) > 1:

            #!!!searh in starling
            # res = self.searh_starling_rinet(self.word_original)
            # if res > -1:
            #     self.isHomonim = True

            #search only in pymorphy2
            self.get_norm_homonyms_forms()
            if len(self.homonym_norm) > 1:
                self.isHomonim = True

            #!!
            # if self.id_zaliznyak > -1:
            #     print(HomonimArray[self.id_zaliznyak][2])
            # else:
            #     print(self.word_original)
            #out
            if self.is_debug:
                print(self.word_original)
                for variant in self.parsed:
                    print(variant.normal_form)
                print('----------------------------------')

    def get_norm_homonyms_forms(self):
        self.homonym_norm = []
        self.homonym_pos = []
        for el in self.parsed:
            if el.tag.POS not in self.homonym_pos:
                self.homonym_norm.append(el.normal_form)
                self.homonym_pos.append(el.tag.POS)



    def get_aot_accent(self, unique=True):
        #check for single vowel
        simple_check = PhoneticModel.check_single_accent(self.word_original)
        if simple_check == 0:
            self.accent = [0]
            return
        elif simple_check == -1:
            self.accent = [255]
            return
        global curDB
        curDB.execute("SELECT * FROM accent_aot WHERE word_form LIKE '"+self.word_original+"'")
        self.accent = []
        for r in curDB.fetchall():
            if r[2] != '255':
                self.accent.append( int(r[2]) )

        #merge if all accents equal
        if unique == True:
            set_accent = list(set(self.accent))
            # print(set_accent)
            if len(set(self.accent)) == 1:
                self.accent = self.accent[0:1]
            elif len(set_accent) == 2 and (set_accent[0]=='255' or set_accent[1]=='255'):
                #aot - getting defined variant if 255 and defined exist
                if set_accent[0]!='255':
                    self.accent = [set_accent[0]]
                else:
                    self.accent = [set_accent[1]]
            else:
                #try search for accent among manually prepared
                log_accent = self.search_and_log_accent()
                if log_accent != 255:
                    self.accent = [log_accent]
                    # print(self.accent)

    def draw_accent(self):
        # print(self.word_original)
        # print(self.word_original, self.word_original.encode('utf-8'))
        # print(self.word_original[0:1], self.word_original.encode('utf-8')[0:1], u'д')
        # return self.word_original.encode('utf-8')
        # return self.word_original
        vowels = [u'а', u'у', u'о', u'ы', u'и', u'э', u'я', u'ю', u'ё', u'е',
                  u'А', u'У', u'О', u'Ы', u'И', u'Э', u'Я', u'Ю', u'Ё', u'Е',]
        if len(self.accent) == 1 and self.accent[0] != 255:
            html = ''
            aaa = -1
            lennn = len(self.word_original)
            for i in range(0, lennn, 1):
                if self.word_original[lennn-i-1] in vowels:
                    aaa += 1
                    if int(self.accent[0]) == aaa:
                        html = self.word_original[0:lennn-i-1] + '<b>' + self.word_original[lennn-i-1:lennn-i] + '</b>' + self.word_original[lennn-i:]
                        return html
        else:
            #return as is
            return self.word_original

    def draw_accent_sign(self):
        vowels = [u'а', u'у', u'о', u'ы', u'и', u'э', u'я', u'ю', u'ё', u'е',
                  u'А', u'У', u'О', u'Ы', u'И', u'Э', u'Я', u'Ю', u'Ё', u'Е',]
        lennn = len(self.word_original)
        html = ''

        if len(self.accent) == 1 and self.accent[0] != 255:
            aaa = -1
            for i in range(0, lennn, 1):
                if self.word_original[lennn-i-1] in vowels:
                    aaa += 1
                    if int(self.accent[0]) == aaa:
                        html = '`'+html
                    else:
                        html = '-'+html
        else:
            #return ?
            for i in range(0, lennn, 1):
                if self.word_original[i] in vowels:
                    html += '?'

        return ' '+html+' '

    def draw_accent_prediction(self, pos, step, offset):
        # MorphEngine.parse(self.word_original)
        vowels = [u'а', u'у', u'о', u'ы', u'и', u'э', u'я', u'ю', u'ё', u'е',
                  u'А', u'У', u'О', u'Ы', u'И', u'Э', u'Я', u'Ю', u'Ё', u'Е',]
        lennn = len(self.word_original)
        html = ''
        vowels_num = 0
        already_predicted = False

        # if we know accent exactly, return only number of vowels
        if len(self.accent) == 1 and self.accent[0] != 255:
            for i in range(0, lennn, 1):
                if self.word_original[lennn-i-1] in vowels:
                    vowels_num += 1
                    html = ''
        else:
            for i in range(0, lennn, 1):
                if self.word_original[lennn-i-1] in vowels:
                    vowels_num += 1
                    # generate everything about word
                    if ((pos+vowels_num)%step == offset) and not already_predicted:
                        #predicted
                        html = 'predicted: '+ self.word_original[0:lennn-i-1] + '<b>' + self.word_original[lennn-i-1:lennn-i] + '</b>' + self.word_original[lennn-i:]
                        html += '<br />'
                        already_predicted = True

        return html, vowels_num

    def search_and_log_accent(self):
        # log only for batch
        if SettingsModel.CURRENT_POEM_ID < 0:
            return 255
        global curDB
        #print(SettingsModel.CURRENT_LINE_ORIGINAL, self.word_original)
        curDB.execute("SELECT * FROM accent_log WHERE poem_id='"+ str(SettingsModel.CURRENT_POEM_ID) +"' AND word_form LIKE '"+self.word_original+"' AND line_original LIKE '"+SettingsModel.CURRENT_LINE_ORIGINAL+"' ")
        accent_log = []
        for r in curDB.fetchall():
            accent_log.append( int(r[2]) )
        if len(accent_log)==1 and accent_log[0] != '255':
            return accent_log[0]

        #adding
        if len(accent_log) < 1:
            sql_add = "INSERT INTO `accent_log` (`id`, `word_form`, `accent`, `poem_id`, `line_original`) VALUES (NULL, '"+self.word_original+"', '255', "+ str(SettingsModel.CURRENT_POEM_ID) +", '"+ SettingsModel.CURRENT_LINE_ORIGINAL +"')"
            #print(sql_add)
            curDB.execute(sql_add)

        return 255

    def get_sound_ending(self):
        ph = PhoneticModel(self.word_original)
        return ph.get_ending()

    def searh_starling_rinet(self, word):
        global HomonimArray
        res = -1
        for k, r in enumerate(HomonimArray):
            if r[1] == word:
                self.id_zaliznyak = k
                self.word_lat = r[2]
                res = k
        return res