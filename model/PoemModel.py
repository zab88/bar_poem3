# -*- coding: utf-8 -*-
from LineModel import LineModel
import math

class PoemModel(object):
    original_title = ''
    original_text = ''

    #lines = []

    def __init__(self, original_title, original_text, years=[]):
        self.original_title = original_title
        self.original_text = original_text
        self.lines = []
        self.__init_lines__()
        # for line in self.lines:
        #     print(line.line_original)
        # exit()

    #splits text into lines
    def __init_lines__(self):
        lines = self.original_text.split("\n")
        for line in lines:
            new_line = LineModel(line)#.strip()
            self.lines.append(new_line)
            #print(self.lines[len(self.lines)-1].line_original)
            #print(len(self.lines))

    def get_poem_homonyms(self):
        out_html = ''
        for l in self.lines:
            #print(l.line_original)
            homonym_line = l.getHighlightingHomonyms()
            #let's also count homonyms
            all_homonyms = l.countHomonyms()

            if homonym_line is not None:
                #print(homonym_line)
                out_html += homonym_line + "<br />\n"

        if out_html != '':
            return out_html, all_homonyms
        else:
            return None, all_homonyms

    def count_lines(self):
        num_lines = 0
        for l in self.lines:
            if len(l.words) > 0:
                num_lines += 1
        return num_lines

    def get_num_rhymes(self):
        global ACCENT_TYPE_M, ACCENT_TYPE_F, ACCENT_TYPE_D, ACCENT_TYPE_N
        num_m, num_f, num_d, num_none = 0, 0, 0, 0
        for l in self.lines:
            if l.accent_type == LineModel.ACCENT_TYPE_N:
                num_none+=1
            elif l.accent_type == LineModel.ACCENT_TYPE_M:
                num_m+=1
            elif l.accent_type == LineModel.ACCENT_TYPE_F:
                num_f+=1
            elif l.accent_type == LineModel.ACCENT_TYPE_D:
                num_d+=1
        return num_m, num_f, num_d, num_none

    def get_metrical_feet(self):
        variants = []
        stops = []
        for l in self.lines:
            variant, stop = l.get_metrical_feet()
            variants.append( variant )
            stops.append( stop )
        res = max(set(variants), key=variants.count)
        res_stop = round( float(sum(stops))/float(len(stops)) )
        #TODO make threshold on number of occurrences
        # return variants
        return res, int( res_stop )