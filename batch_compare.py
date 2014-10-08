# -*- coding: utf-8 -*-
from model.PoemModel import PoemModel
import pymysql

#metric type
HOREY_ID = 1
YAMB_ID = 2
DAKTIL_ID = 3
AMFIBRAHII_ID = 4
ANAPEST_ID = 5

conn = pymysql.connect(host='127.0.0.1', port=3306, user='root', passwd='', db='bar_poem3', charset='utf8', autocommit = True)
curDB = conn.cursor()
curDB.execute("SET NAMES utf8")

curDB.execute("SELECT * FROM poems") #35, 68
for r in curDB.fetchall():
    #print(r[2])
    poem_text = r[2].encode('utf-8') #text
    poem_obj = PoemModel('', poem_text)
    metric, stop = poem_obj.get_metrical_feet()

    print(r[1])
    print(metric, stop)
    print(r[4], r[5])

curDB.close()
conn.close()