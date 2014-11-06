# -*- encoding: utf-8 -*-
import pymysql
import re
import difflib

conn = pymysql.connect(host='127.0.0.1', port=3306, user='root', passwd='', db='bar_poem3', charset='utf8', autocommit=True)
curDB = conn.cursor()
curDB.execute("SET NAMES utf8")

#set to zero before counting match
curDB.execute("UPDATE `academ16` SET `konk_id`=0 WHERE `konk_id` IN (197,258,270,522,528,575,593,606,621,682,700,707,787,796)")
exit()

def delete_punctutaion(name):
    name = name.lower()
    letters = u'йцукенгшщзхъэждлорпавыфячсмитьбюalfieri'
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

    #delete multiple spaces
    n1 = " ".join(n1.split())
    n2 = " ".join(n2.split())
    line1 = " ".join(line1.split())

    #delete name in parentheses
    n2_test = re.sub(r'\([^)]*\)', '', n2)
    if len(n2_test) > 9:
        n2 = n2_test

    n1 = delete_punctutaion(n1)
    n2 = delete_punctutaion(n2)
    line1 = delete_punctutaion(line1)

    #delete small words5
    # n1 = delete_small_words(n1)
    # n2 = delete_small_words(n2)
    # line1 = delete_small_words(line1)

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
    #fuzzy matching
    ratio_n1_n2 = difflib.SequenceMatcher(None, n1, n2).ratio()
    ratio_line1_n2 = difflib.SequenceMatcher(None, line1, n2).ratio()
    if ratio_n1_n2 > 0.87 or ratio_line1_n2 > 0.87:
        print(n1 +' ++' + n2 + ' ++ ' + line1)
        return True

    # print(n1, n2)
    return False

#get all poems from academ
curDB.execute("SELECT * FROM academ16")
# curDB.execute("SELECT * FROM academ16 WHERE id=576")
academ16 = []
for r in curDB.fetchall():
    # print( r[2], delete_punctutaion(r[2]) )
    # print( r[2] )
    # print delete_punctutaion(r[2])
    # print('==========')
    academ16.append(r)

#get all poems from konk
curDB.execute("SELECT * FROM konkordans")
# curDB.execute("SELECT * FROM konkordans WHERE id=762")
konkordans = []
for r in curDB.fetchall():
    konkordans.append(r)

manual_matcher = dict();
# academ16 => konkordans
#manual_matcher[596] = 787

num_found = 0
for academ in academ16:
    if academ[0] in manual_matcher.keys():
        curDB.execute("""UPDATE `academ16` SET `konk_id` = %s WHERE  `id` = %s """, (str(manual_matcher[academ[0]]), str(academ[0])))
        num_found+=1
        continue
    for konk in konkordans:
        if compare_names(academ[2], academ[3], konk[1]):
            # print(konk[4]+' ,,'+konk[1])
            # print(academ[1]+' ,,'+academ[2])
            # print(academ[1]+' ,,'+academ[3])
            # print('=======')
            num_found+=1
            #update DB
            curDB.execute("""UPDATE `academ16` SET `konk_id` = %s WHERE  `id` = %s """, (str(konk[0]), str(academ[0])))

print(num_found)
