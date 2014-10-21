# -*- coding: utf-8 -*-
import pymysql

f = open('C:\MyPrograms\python2\\bar_poem2\pushkin/pushkin_aleksandr_polnoe_sobranie_stihotvoreniy.txt', 'r')
all_lines = f.readlines()
f.close()

def make_poems(lines):
    made_poems = []

    current_poem_text = 'first!'
    current_poem_name = ''
    for l in lines:
        if l[0] == ' ' or l[0] == "\t":
            #deleting leading tabs
            l = l.replace("\t", "")
            current_poem_text += l

            if current_poem_name[0:5] == "* * *":
                #print(l)
                current_poem_name = l
                current_poem_name = current_poem_name.replace("\n", '').strip()
                if current_poem_name[-1] in (",", ";", ".", "?", ":", "!"):
                    current_poem_name = list(current_poem_name)
                    current_poem_name[-1] = ''
                    current_poem_name = "".join(current_poem_name)
                    current_poem_name += "..."
                else:
                    current_poem_name += "..."
                #print(current_poem_name)
        elif l[0] == "\n":
            continue
        else:
            made_poems.append( {'name':current_poem_name, 'text':current_poem_text} )
            current_poem_name = l
            current_poem_name = current_poem_name.replace("\n", '')
            current_poem_text = ''
    return made_poems

def compare_names(n1, n2):
    #leave only letters
    n1_new = n1
    n2_new = n2
    if n1_new == n2_new:
        return True
    return False

made_poems = make_poems(all_lines)
# kmd = 200
# print(made_poems[kmd]['name'])
# print(made_poems[kmd]['text'])
# exit()


conn = pymysql.connect(host='127.0.0.1', port=3306, user='root', passwd='', db='bar_poem3', charset='utf8', autocommit=True)
curDB = conn.cursor()
curDB.execute("SET NAMES utf8")

curDB.execute("SELECT * FROM poems_info")
i = 0
for r in curDB.fetchall():
    j=0
    for el in made_poems:
        # if el['name'] == r[1].encode('utf-8'):
        if compare_names(el['name'], r[1].encode('utf-8')):
            i += 1
            j += 1
            if j > 1:
                print(el['name']+' twice!!')
            # print(el['name']+' '+r[1].encode('utf-8'))
            #ok, found, let's write to DB
            curDB.execute("""UPDATE `poems_info` SET `poem_body` = %s WHERE  `id` = %s """, (el['text'], str(r[0])))

print(i)