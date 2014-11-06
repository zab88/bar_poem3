# -*- encoding: utf-8 -*-
import pymysql
import re

conn = pymysql.connect(host='127.0.0.1', port=3306, user='root', passwd='', db='bar_poem3', charset='utf8', autocommit=True)
curDB = conn.cursor()
curDB.execute("SET NAMES utf8")

#set to zero before counting match
curDB.execute("UPDATE `academ16` SET `metr_id`=0 WHERE `metr_id` IN (147,153,208,309,361,421,437,508,786)")
exit()

def delete_punctutaion(name):
    name = name.lower()
    letters = u'йцукенгшщзхъэждлорпавыфячсмитьбю'
    new_name = ''
    for l in name:
        if l in letters:
            new_name += l
        else:
            new_name += u' '
    return new_name
def delete_small_words(text):
    new_text = []
    text = text.split()
    for word in text:
        if len(word) > 1:
            new_text.append(word)
    new_text = " ".join(new_text)
    return new_text

def compare_names(n1, line1, n2):
    n2_origin = n2
    #delete name in parentheses
    # n2 = re.sub(r'\([^)]*\)', '', n2)

    n1 = delete_punctutaion(n1)
    n2 = delete_punctutaion(n2)
    line1 = delete_punctutaion(line1)

    #delete small words5
    # n1 = delete_small_words(n1)
    n2_test = delete_small_words(n2)
    # line1 = delete_small_words(line1)
    if len(n2_test)>8:
        n1 = delete_small_words(n1)
        n2 = n2_test
        line1 = delete_small_words(line1)

    #delete multiple spaces
    n1 = " ".join(n1.split())
    n2 = " ".join(n2.split())
    line1 = " ".join(line1.split())

    if len(n2) < 3:
        print(n2)
        print(n2_origin)
        return False

    if n1 == n2 or line1 == n2:
        return True
    # get first chars
    n2_length = len(n2)
    n1_cutted = n1[:n2_length]
    if n1_cutted == n2 and n2_length>12:
        print(n2)
        return True

    return False

#get all poems from academ
curDB.execute("SELECT * FROM academ16")
academ16 = []
for r in curDB.fetchall():
    # print( r[2], delete_punctutaion(r[2]) )
    # print( r[2] )
    # print delete_punctutaion(r[2])
    # print('==========')
    academ16.append(r)

#get all poems from konk
curDB.execute("SELECT * FROM poems_info")
metr_spr = []
for r in curDB.fetchall():
    metr_spr.append(r)

num_found = 0
for academ in academ16:
    for mm in metr_spr:
        if compare_names(academ[2], academ[3], mm[1]):
            # print(str(mm[3])+' ,,'+mm[1])
            # print(academ[1]+' ,,'+academ[2])
            # print(academ[1]+' ,,'+academ[3])
            # print('=======')
            num_found+=1
            #update DB
            curDB.execute("""UPDATE `academ16` SET `metr_id` = %s WHERE  `id` = %s """, (str(mm[0]), str(academ[0])))

print(num_found)
