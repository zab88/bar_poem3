# -*- encoding: utf-8 -*-
import pymysql
import re

conn = pymysql.connect(host='127.0.0.1', port=3306, user='root', passwd='', db='bar_poem3', charset='utf8', autocommit=True)
curDB = conn.cursor()
cursor = conn.cursor(pymysql.cursors.DictCursor)
curDB.execute("SET NAMES utf8")

def get_stop(tt):
    m = re.search("(\d+)", tt)
    if m:
        return m.group()[0]
    return '0'

def get_razmer(tt):
    if u'я' in tt:
        return 'yamb'
    if u'х' in tt:
        return 'horey'
    if u'дол' in tt:
        return 'dolnik'
    if u'д' in tt:
        return 'daktil'
    if u'ам' in tt:
        return 'anapest'
    if u'ан' in tt:
        return 'amfibrahii'
    return 'other'

curDB.execute("TRUNCATE TABLE poems_origin_generated")

query = "SELECT * " \
        "FROM  `academ16` " \
        "LEFT JOIN konkordans ON konkordans.id = academ16.konk_id " \
        "LEFT JOIN poems_info ON poems_info.id = academ16.metr_id " \
        "WHERE academ16.konk_id > 0 AND academ16.metr_id > 0"

curDB.execute(query)
#col_names = [i[0] for i in curDB.description]
for row in curDB.fetchall():
    title = row[2]
    poem_body = row[4]
    year = str( row[1] )

    stop = str( get_stop( row[25] ) )
    lines_num = str( row[27] )
    razmer = str( get_razmer( row[25] ) )
    print(row[12], row[11])
    m_end = str( row[12] )
    g_end = str( row[13] )
    d_end = str( row[14] )
    strofika = str( row[32] )
    partial_line = str( row[18] )
    m_no = str( row[15] )
    g_no = str( row[16] )
    d_no = str( row[17]  )
    strofika_type = row[19]

    query = "INSERT INTO `poems_origin_generated` (" \
            "`title`, " \
            "`poem_body`, " \
            "`year`, " \
            "`stop`, " \
            "`lines_num`, " \
            "`razmer`, " \
            "`m_end`, " \
            "`g_end`, " \
            "`d_end`, " \
            "`strofika`, " \
            "`partial_line`, " \
            "`m_no`, " \
            "`g_no`, " \
            "`d_no`, " \
            "`strofika_type`) " \
            "VALUES (" \
            "'"+title+"', " \
            "'"+poem_body.replace("'", '`')+"', " \
            "'"+year+"', " \
            "'"+stop+"', " \
            "'"+lines_num+"', " \
            "'"+razmer+"', " \
            "'"+m_end+"', " \
            "'"+g_end+"', " \
            "'"+d_end+"', " \
            "'"+strofika+"', " \
            "'"+partial_line+"', " \
            "'"+m_no+"', " \
            "'"+g_no+"', " \
            "'"+d_no+"', " \
            "'"+strofika_type+"');"
    #print(query)
    print(title)

    curDB.execute(query)