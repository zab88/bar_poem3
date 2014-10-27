# -*- coding: utf-8 -*-
import csv

for i in range(1, 15, 2):
    if i < 10:
        ii = '0'+str(i)
    else:
        ii = str(i)
    # csvfile = open('info_02/'+ii+'.csv', 'r')
    with open('info_02/'+ii+'.csv', 'r', encoding='utf-8') as csvfile:
        is_first_line = True
        info_reader = csv.reader(csvfile, delimiter=',', quotechar='"')
        for line in csvfile:
            if is_first_line:
                is_first_line = False
                continue
            # cells = line.split(',')
            # print(cells[1])
            print(', '.join(line) )