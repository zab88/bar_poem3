# -*- coding: utf-8 -*-
class PhoneticModel(object):
    vowels_sound = [u'и', u'ы', u'у', u'э', u'о', u'а']
    vowels_special = [u"я", u"е", u"ё", u"ю"]
    vowels = [u'и', u'ы', u'у', u'э', u'о', u'а', u"я", u"е", u"ё", u"ю"]
    consonants_sound = [u'б', u'в', u'г', u'д', u'з', u'к', u'л', u'м', u'н', u'п', u'р', u'с', u'т', u'ф', u'х', u'ж', u'ш', u'ц', u'ч', u'й']
    # voiced_paired = ['б', 'в', 'г', 'д', 'ж', 'з']
    voiced_paired = [u'б', u'в', u'г', u'д', u'ж', u'з']
    # clunk_paired =  ['п', 'ф', 'к', 'т', 'ш', 'с']
    clunk_paired =  [u'п', u'ф', u'к', u'т', u'ш', u'с']
    #original_word
    #new_ending

    def __init__(self, word, accent=255):
        self.original_word = word

    def get_ending(self):
        #only last two chars
        last = self.original_word[-1:]
        # print(self.original_word, 'я')
        penultimate = self.original_word[-2:-1]
        # print(penultimate, last)

        #penultimate char
        if penultimate in self.vowels_special:
            if penultimate == u'я':
                penultimate = u'а'
            elif penultimate == u'е':
                penultimate = u'э'
            elif penultimate == u'ё':
                penultimate = u'о'
            elif penultimate == u'ю':
                penultimate = u'у'

        if last in self.voiced_paired:
            ind = self.voiced_paired.index(last)
            last = self.clunk_paired[ind]

        self.new_ending = penultimate + last
        return self.new_ending

    #check single vowel and vowels absence
    @staticmethod
    def check_single_accent(w):
        number_of_vowels = 0
        for el in PhoneticModel.vowels:
            if el in w:
                number_of_vowels+=1

        if number_of_vowels == 0:
            return -1
        if number_of_vowels == 1:
            return 0;
        return 255