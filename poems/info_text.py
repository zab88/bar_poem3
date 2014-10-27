# -*- coding: utf-8 -*-
import pymysql
import string

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
    new_symbols = u' …«»–— '
    string.punctuation += new_symbols
    # string.punctuation = string.punctuation.encode('utf-8')
    # print(string.punctuation)
    n1 = n1.decode('utf-8').lower()
    n2 = n2.decode('utf-8').lower()
    n1_new = (c for c in n1 if c not in string.punctuation)
    n1_new = ''.join(n1_new)
    n2_new = (c for c in n2 if c not in string.punctuation)
    n2_new = ''.join(n2_new)
    # n1_new = n1
    # n2_new = n2
    #search shortest
    if len(n1_new) < len(n2_new):
        n_short = n1_new
        n_long = n2_new
    else:
        n_short = n2_new
        n_long = n1_new
    # if len(n_short.decode('utf-8'))>10 and n_short in n_long:
    #     return True
    # print(n1_new)
    if n1_new[:12] == n2_new[:12]:
        return True
    if n1_new == n2_new:
        # print(n1_new+' good')
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
jj = 0
for r in curDB.fetchall():
    j=0
    for el in made_poems:
        # if el['name'] == r[1].encode('utf-8'):
        if compare_names(el['name'], r[1].encode('utf-8')):
            i += 1
            j += 1
            if j > 1:
                jj += 1
                print(el['name']+' twice!!')
            # print(el['name']+' '+r[1].encode('utf-8'))
            #ok, found, let's write to DB
            curDB.execute("""UPDATE `poems_info` SET `poem_body` = %s WHERE  `id` = %s """, (el['text'], str(r[0])))
    # break
print(i)
print(jj)