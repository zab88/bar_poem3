# -*- coding: utf-8 -*-
from model.PoemModel import PoemModel
import pymysql

poem1_file = open('poems/test.txt', 'r')
poem1_text = poem1_file.read()
poem1 = PoemModel('', poem1_text)

# poem1_words = []
# for line in poem1.lines:
#     for w in line.words:
#         # print(w.word_original)
#         poem1_words.append(w.word_original)

num_m, num_f, num_d, num_none = poem1.get_num_rhymes()
print(num_m, num_f, num_d, num_none)
#
print( poem1.get_metrical_feet() )
print('number of lines is: ' + str( poem1.count_lines() ) )

strf = poem1.get_strofika()
print(strf)

partial_line = poem1.get_partial_line()
print('partial line: '+str(len(partial_line)) )

m_no, g_no, d_no = poem1.get_no_rhymes()
print(m_no, g_no, d_no)

strofika_type = poem1.get_strofika_type()
print strofika_type