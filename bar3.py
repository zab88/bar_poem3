# -*- coding: utf-8 -*-
from model.PoemModel import PoemModel

poem1_file = open('poems/2.txt', 'r')
poem1_text = poem1_file.read()
poem1 = PoemModel('', poem1_text)

# poem1_words = []
# for line in poem1.lines:
#     for w in line.words:
#         # print(w.word_original)
#         poem1_words.append(w.word_original)
num_m, num_f, num_d, num_none = poem1.get_num_rhymes()
print(num_m, num_f, num_d, num_none)