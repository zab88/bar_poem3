# -*- coding: utf-8 -*-
from model.PoemModel import PoemModel
import pymysql
# from model.SettingsModel import
import model.SettingsModel as SettingsModel

#metric type
HOREY_ID = 1
YAMB_ID = 2
DAKTIL_ID = 3
AMFIBRAHII_ID = 4
ANAPEST_ID = 5
file_path = 'poems/compare.txt'

conn = pymysql.connect(host='127.0.0.1', port=3306, user='root', passwd='', db='bar_poem3', charset='utf8', autocommit = True)
curDB = conn.cursor()
curDB.execute("SET NAMES utf8")

file = open(file_path, 'w')
# curDB.execute("SELECT * FROM poems_origin_generated LIMIT 70, 100000")
curDB.execute("SELECT * FROM poems_origin_generated") #35, 68
for r in curDB.fetchall():
    SettingsModel.CURRENT_POEM_ID = r[0]
    print(r[1])
    #TODO make perfect academ 16
    if len(r[2]) < 10:
        continue
    poem_text = r[2].encode('utf-8') #text
    poem1 = PoemModel('', poem_text)

    #counting all parameters
    m_end, g_end, d_end, num_none = poem1.get_num_rhymes()
    razmer, stop = poem1.get_metrical_feet()
    lines_num = poem1.count_lines()
    strofika = poem1.get_strofika()
    partial_line = len(poem1.get_partial_line())
    m_no, g_no, d_no = poem1.get_no_rhymes()
    strofika_type = poem1.get_strofika_type()

    pp = dict()
    pp[5] = 'stop'
    pp[6] = 'lines_num'
    pp[7] = 'razmer'
    pp[8] = 'm_end'
    pp[9] = 'g_end'
    pp[10] = 'd_end'
    # pp[11] = 'lines_num'
    pp[12] = 'strofika'
    pp[13] = 'partial_line'
    pp[14] = 'm_no'
    pp[15] = 'g_no'
    pp[16] = 'd_no'
    pp[17] = 'strofika_type'

    file.write( r[1].encode('utf-8') + ' ('+str(r[3])+') id='+str(r[0])+' second-counted\n')

    for k, el in pp.items():
        tmp_val = globals()[el]
        tmp_val = str(tmp_val).encode('utf-8')
        r_db = str(r[k]).encode('utf-8')
        if tmp_val != r_db:
            file.write(el + ': ')
            file.write(r_db + ' ')
            file.write(tmp_val+ '\n')

    #lines_num
    file.write('lines_num '+str(r[6])+' '+str(lines_num))
    if lines_num == r[6]:
        file.write(' OK\n')
    else:
        file.write(' NOK\n')


    file.write('==========================\n')

curDB.close()
conn.close()