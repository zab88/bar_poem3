# -*- coding: utf-8 -*-
import re
import pymysql

all_poems = []
poem = []
line_number = 0
counter = 0
for line in open('info_01.html', 'r'):
    line_number+=1
    ll = line.strip()
    ll = re.sub('<[^>]*>', '', ll)
    if ll == "": continue;

    if counter > 0:
        poem.append(ll)

    if re.match("\d+\.", ll):
        #print(ll)
        counter = 6
        all_poems.append(poem)
        poem = []


    counter -= 1

all_poems = all_poems[1:]
# for el in all_poems[798]:
#     print el
# exit()

conn = pymysql.connect(host='127.0.0.1', port=3306, user='root', passwd='', db='bar_poem3', charset='utf8', autocommit=True)
curDB = conn.cursor()
curDB.execute("SET NAMES utf8")

for k, el in enumerate(all_poems):
    curDB.execute("""INSERT INTO  `poems_info` (
        `id` ,
        `title` ,
        `year` ,
        `year_end` ,
        `lines_num` ,
        `metric` ,
        `strofika`
        )
        VALUES (%s, %s, %s, 0, %s, %s, %s)""", (str(k+1), el[0], el[1], el[2], el[3], el[4]))

curDB.close()
conn.close()