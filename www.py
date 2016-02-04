# -*- coding: utf-8 -*-
import sys
from model.PoemModel import PoemModel
import pymysql

poem_id = sys.argv[1]

#connecting DB
#what a hell, "setsebool -P httpd_can_network_connect_db 1" helped!
conn = pymysql.connect(user='bar_poem3', passwd='ACLQ7E7JcAwE9K3e', db='bar_poem3', charset='utf8')
curDB = conn.cursor()
curDB.execute("SET NAMES utf8")

#reading poem from DB
curDB.execute("SELECT poem_body FROM poems WHERE id="+poem_id)
for r in curDB.fetchall():
    poem1_text = r[0].encode('utf-8')

poem1 = PoemModel('', poem1_text)


num_m, num_f, num_d, num_none = poem1.get_num_rhymes()
# print(num_m, num_f, num_d, num_none)

lines_num = poem1.count_lines()
razmer, stop = poem1.get_metrical_feet()

strofika = poem1.get_strofika()
partial_line = poem1.get_partial_line()
m_no, g_no, d_no = poem1.get_no_rhymes()
strofika_type = poem1.get_strofika_type()
accent_log = poem1.get_draw_accent()
accent_sign = poem1.get_draw_accent_sign()

accent_sign = poem1.get_accent_prediction()

#writing result
query_str = "INSERT INTO `poems_result` (" \
              "`poem_id`, " \
              "`lines_num`, " \
              "`stop`, " \
              "`razmer`, " \
              "`m_end`, " \
              "`g_end`, " \
              "`d_end`, " \
              "`null_end`," \
              "`strofika`," \
              "`partial_line`," \
              "`m_no`," \
              "`g_no`," \
              "`d_no`," \
              "`accent_log`," \
              "`accent_sign`," \
              "`strofika_type`" \
              ") VALUES (" \
              "'"+str(poem_id)+"', " \
              "'"+str(lines_num)+"', " \
              "'"+str(stop)+"', " \
              "'"+razmer+"', " \
              "'"+str(num_m)+"', " \
              "'"+str(num_f)+"', " \
              "'"+str(num_d)+"', " \
              "'"+str(num_none)+"', " \
              "'"+str(strofika)+"', " \
              "'"+str(len(partial_line))+"', " \
              "'"+str(m_no)+"', " \
              "'"+str(g_no)+"', " \
              "'"+str(d_no)+"', " \
              "'"+accent_log+"', " \
              "'"+accent_sign+"', " \
              "'"+str(strofika_type)+"')"
# print(query_str)
curDB.execute(query_str)
conn.commit()

curDB.close()