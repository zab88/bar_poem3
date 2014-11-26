# -*- encoding: utf-8 -*-
import pymysql
import re

conn = pymysql.connect(host='127.0.0.1', port=3306, user='root', passwd='', db='bar_poem3', charset='utf8', autocommit=True)
curDB = conn.cursor()
curDB.execute("SET NAMES utf8")

#set to zero before counting match
curDB.execute("UPDATE `academ16` SET `metr_id`=0")
#curDB.execute("UPDATE `academ16` SET `metr_id`=0 WHERE `metr_id` IN (147,153,208,309,361,421,437,508,786)")
#exit()

#replace everything, except russian letters on space
def delete_punctutaion(name):
    name = name.lower()
    letters = u'йцукенгшщзхъэждлорпавыфячсмитьбю1234567890'
    new_name = ''
    for l in name:
        if l in letters:
            new_name += l
        else:
            new_name += u' '
    return new_name
#deletes all words of one letter and also deletes double spaces
def delete_small_words(text):
    text = text.replace(u" гр ", ' ')
    new_text = []
    text = text.split()
    for word in text:
        if len(word) > 1:
            new_text.append(word)
    new_text = " ".join(new_text)
    return new_text

#extract name and first line from brackets
def get_from_brackets(ll):
    bracket_1 = ll.find(u'(')
    bracket_2 = ll.find(u')')
    if bracket_1 < 0 or bracket_2 < 0:
        return ll, u''
    name = ll[:bracket_1]
    first_line = ll[(bracket_1+1):bracket_2]
    return name, first_line

def clean_me(tt):
    tt = delete_punctutaion(tt)
    #tt = delete_small_words(tt)
    tt = " ".join(tt.split())
    return tt

def compare_names(n1, line1, n2):
    n2_origin = n2
    #delete name in parentheses
    # n2 = re.sub(r'\([^)]*\)', '', n2)

    n1 = delete_punctutaion(n1)
    n2 = delete_punctutaion(n2)
    line1 = delete_punctutaion(line1)

    #delete small words5
    n1 = delete_small_words(n1)
    n2_test = delete_small_words(n2)
    line1 = delete_small_words(line1)
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

#with small words
def compare_names2(n1, line1, y1, n2, line2, y2):
    #names in french are empty
    if n1=='' or line1=='':
        return 0
    cut_length = min(len(line1), len(line2))
    line1_cutted = line1[:cut_length]
    line2_cutted = line2[:cut_length]
    n1_small = delete_small_words(n1)
    n2_small = delete_small_words(n2)
    # if line1 == line2 and (line1.find(' ')>-1):
    year_diff = abs(y2-y1)
    #RUL 1
    # if line1 == line2 and (y1==y2) and y1!=0 and n1!=u'ода':
    #     return True
    #RUL 2
    # if line1 == line2 and year_diff<3 and y1!=0 and n1!=u'ода':
    #     return True
    #RUL 3
    # if n1 == n2 and year_diff<3 and (n1.find(' ')>-1):
    #     return True
    #RUL 4 - very cool rule!
    if n1 == n2 and line2=='' and (year_diff<3 or year_diff>1800):
        return 0.7
    #RUL 5
    elif line2 != '' and line1_cutted==line2_cutted and (line2_cutted.count(' ')>0) and (year_diff<3 or year_diff>1800):
        return 0.9
    elif n1_small==n2_small and (len(n1_small)>3):
        return 0.2

    # if n2 == u'сестра братья' and n1 == u'сестра братья':
    #     print(n1+u' <> '+line1+u' <> '+n2+u' <> '+str(line2))
    # print(n1, n2)
    # exit()
    # print(n1+u' <> '+line1+u' <> '+n2+u' <> '+line2)
    # if line2 != '':
    #     if line1==line2 and len(line1)>1:
    #         #print(n1+u' <> '+line1+u' <> '+n2+u' <> '+line2)
    #         return True
    #     cut_length = min(len(line1), len(line2))
    #     line1_cutted = line1[:cut_length]
    #     line2_cutted = line2[:cut_length]
    #
    # else:
    #     if n1==n2 and len(n1)>1:
    #         #print(n1+u' <> '+line1+u' <> '+n2+u' <> '+line2)
    #         return True
    return 0

#get all poems from academ
curDB.execute("SELECT * FROM academ16")
academ16 = []
for r in curDB.fetchall():
    # print( r[2], delete_punctutaion(r[2]) )
    # print( r[2] )
    # print delete_punctutaion(r[2])
    # print('==========')
    rr = dict()
    rr['id'] = r[0]
    rr['a_title'] = clean_me(r[2])
    rr['a_line'] = clean_me(r[3])
    rr['year'] = int('0'+str(r[1]))
    academ16.append(rr)

#get all poems from konk
curDB.execute("SELECT * FROM poems_info")
metr_spr = []
for r in curDB.fetchall():
    rr = dict()
    new_name, new_line = get_from_brackets(r[1])
    rr['id'] = r[0]
    rr['m_title'] = clean_me(new_name)
    rr['m_line'] = clean_me(new_line)
    rr['year'] = int('0'+str(r[3]))
    metr_spr.append(rr)

num_found = 0
already_filled = set()
weights = dict()
for academ in academ16:
    nothing_found = True
    for mm in metr_spr:
        new_weight = compare_names2(academ['a_title'], academ['a_line'], academ['year'], mm['m_title'], mm['m_line'], mm['year'])
        #let's remember all weight
        if new_weight>0:
            add_weight = dict()
            add_weight['id'] = mm['id']
            add_weight['weight'] = new_weight
            if academ['id'] not in already_filled:
                weights[academ['id']] = list()
            weights[academ['id']].append(add_weight)
            nothing_found = False

        continue
    if nothing_found:
        #print(academ['a_title']+' ! '+academ['a_line']+' ! '+str(academ['year']))
        continue

        # if compare_names(academ[2], academ[3], mm[1]):
        if compare_names2(academ['a_title'], academ['a_line'], academ['year'], mm['m_title'], mm['m_line'], mm['year']):
            # print(str(mm[3])+' ,,'+mm[1])
            # print(academ[1]+' ,,'+academ[2])
            # print(academ[1]+' ,,'+academ[3])
            # print('=======')
            if academ['id'] in already_filled:
                print(str(academ['id'])+'!'+str(mm['id'])+'!'
                      +academ['a_title']+'!'+academ['a_line']+'!'
                      +mm['m_title']+'!'+mm['m_line'])
            else:
                already_filled.add(academ['id'])
                num_found+=1
            #update DB
            #curDB.execute("""UPDATE `academ16` SET `metr_id` = %s WHERE  `id` = %s """, (str(mm[0]), str(academ[0])))

#Ok, we have all possible combinations, now let's find with the most weight
#print(weights)
#{2: [{'id': 399, 'weight': 0.7}], 4: [{'id': 288, 'weight': 0.7}]}
for key in weights:
    biggest = 0
    id_now = 0
    for m in weights[key]: #m - dict
        if m['weight']>biggest:
            id_now = m['id']
    if id_now>0:
        curDB.execute("""UPDATE `academ16` SET `metr_id` = %s WHERE  `id` = %s """, (str(id_now), str(key)))

print(len(weights))

print(num_found)
