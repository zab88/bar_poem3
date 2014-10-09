# -*- coding: utf-8 -*-
import sys
from model.PoemModel import PoemModel
import pymysql

poem_id = sys.argv[1]

#connecting DB
conn = pymysql.connect(host='127.0.0.1', port=3306, user='bar_poem3', passwd='ACLQ7E7JcAwE9K3e', db='bar_poem3', charset='utf8')
curDB = conn.cursor()

#reading poem from DB
curDB.execute("SELECT poem_body FROM poems WHERE id="+poem_id)
for r in curDB.fetchall():
    poem1_text = r[0].encode('utf-8')

poem1 = PoemModel('', poem1_text)


num_m, num_f, num_d, num_none = poem1.get_num_rhymes()
# print(num_m, num_f, num_d, num_none)

lines_num = poem1.count_lines()
razmer, stop = poem1.get_metrical_feet()

#writing result
query_str = "INSERT INTO `poems_result` (" \
              "`poem_id`, " \
              "`lines_num`, " \
              "`stop`, " \
              "`razmer`, " \
              "`m_end`, " \
              "`g_end`, " \
              "`d_end`, " \
              "`null_end`" \
              ") VALUES (" \
              "'"+str(poem_id)+"', " \
              "'"+str(lines_num)+"', " \
              "'"+str(stop)+"', " \
              "'"+razmer+"', " \
              "'"+str(num_m)+"', " \
              "'"+str(num_f)+"', " \
              "'"+str(num_d)+"', " \
              "'"+str(num_none)+"')"
# print(query_str)
curDB.execute(query_str)
conn.commit()

curDB.close()