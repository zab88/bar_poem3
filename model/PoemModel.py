# -*- coding: utf-8 -*-
from LineModel import LineModel
import math

class PoemModel(object):
    original_title = ''
    original_text = ''

    #lines = []
    strofika = None

    razmer, stop = 'other', 0

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

    def get_sound_endings(self):
        endings = []
        for l in self.lines:
            if len(l.words) > 0:
                # print(l.words[-1:][0].word_original)
                # endings.append(l.words[-1:][0].word_original[-2:])
                endings.append(l.words[-1:][0].get_sound_ending())
        return endings
    def check_abab(self, l):
        yes_vote = 0
        no_vote = 0
        if len(l)<1:
            return False
        for chunk in l:
            if len(chunk) < 4:
                continue
            # print(chunk[0] +'!'+chunk[2])
            if chunk[0] == chunk[2] and chunk[1]==chunk[3]:
                yes_vote+=1
            else:
                no_vote+=1
        if (yes_vote+no_vote)==0:
            return False
        if float(yes_vote)/float(yes_vote+no_vote) > 0.66:
            return True
        else:
            return False
    def check_abba(self, l):
        yes_vote = 0
        no_vote = 0
        if len(l)<1:
            return False
        for chunk in l:
            # print(chunk[0] +'!'+chunk[2])
            if len(chunk) < 4:
                continue
            if chunk[0] == chunk[3] and chunk[1]==chunk[2]:
                yes_vote+=1
            else:
                no_vote+=1
        if (yes_vote+no_vote)==0:
            return False
        if float(yes_vote)/float(yes_vote+no_vote) > 0.66:
            return True
        else:
            return False
    def check_aabb(self, l):
        yes_vote = 0
        no_vote = 0
        if len(l)<1:
            return False
        for chunk in l:
            if len(chunk) < 4:
                continue
            # print(chunk[0] +'!'+chunk[1]+'&'+chunk[2] +'!'+chunk[3])
            if chunk[0]==chunk[1] and chunk[2]==chunk[3]:
                yes_vote+=1
            else:
                no_vote+=1

        if (yes_vote+no_vote)==0:
            return False
        if float(yes_vote)/float(yes_vote+no_vote) > 0.66:
            return True
        else:
            return False

    def get_strofika(self):
        #split by empty lines
        #split by 4
        #test abab
        endings = self.get_sound_endings()
        # for e in endings:
        #     print(e)

        test_4 = [endings[i:i+4] for i in range(0, len(endings), 4)]
        if self.check_abab(test_4):
            self.strofika = 'abab'
            return 'abab';
        if self.check_aabb(test_4):
            self.strofika = 'aabb'
            return 'aabb';
        if self.check_abba(test_4):
            self.strofika = 'abba'
            return 'abba';
        self.strofika = 'sv.str.'
        return self.strofika

    def get_partial_line(self):
        return []

    def get_no_rhymes(self):
        m_no, g_no, d_no = 0, 0, 0
        if self.strofika is not None and self.strofika != 'sv.str.' and len(self.strofika) == 4:
            #check for length of 4
            last_m_ending, last_g_ending, last_d_ending = None, None, None
            a1_endings, a2_endings = [], []
            b1_endings, b2_endings = [], []
            if self.strofika == 'abab' or self.strofika == 'baba':
                a1, a2, b1, b2 = 0, 2, 1, 3
            if self.strofika == 'abba' or self.strofika == 'baab':
                a1, a2, b1, b2 = 0, 3, 1, 2
            if self.strofika == 'aabb' or self.strofika == 'bbaa':
                a1, a2, b1, b2 = 0, 1, 2, 3
            for line_num, l in enumerate( self.lines ):
                if len(l.words)==0:
                    continue
                if a1==(line_num%4):
                    a1_endings.append(l)
                if a2==(line_num%4):
                    a2_endings.append(l)
                if b1==(line_num%4):
                    b1_endings.append(l)
                if b2==(line_num%4):
                    b2_endings.append(l)

            if len(a1_endings) > len(a2_endings):
                a2_endings.append(None)
            for a_index, a in enumerate(a1_endings):
                if a2_endings[a_index] is None:
                    if a1_endings[a_index].accent_type == LineModel.ACCENT_TYPE_M:
                        m_no+=1
                    if a1_endings[a_index].accent_type == LineModel.ACCENT_TYPE_F:
                        g_no+=1
                    if a1_endings[a_index].accent_type == LineModel.ACCENT_TYPE_D:
                        d_no+=1
                elif a1_endings[a_index].words[-1:][0].word_original[-2:] == a2_endings[a_index].words[-1:][0].word_original[-2:]:
                    continue
                else:
                    if a1_endings[a_index].accent_type == LineModel.ACCENT_TYPE_M:
                        m_no+=1
                    if a1_endings[a_index].accent_type == LineModel.ACCENT_TYPE_F:
                        g_no+=1
                    if a1_endings[a_index].accent_type == LineModel.ACCENT_TYPE_D:
                        d_no+=1

            if len(b1_endings) > len(b2_endings):
                b2_endings.append(None)
            for b_index, b in enumerate(b1_endings):
                if b2_endings[b_index] is None:
                    if b1_endings[b_index].accent_type == LineModel.ACCENT_TYPE_M:
                        m_no+=1
                    if b1_endings[b_index].accent_type == LineModel.ACCENT_TYPE_F:
                        g_no+=1
                    if b1_endings[b_index].accent_type == LineModel.ACCENT_TYPE_D:
                        d_no+=1
                elif b1_endings[b_index].words[-1:][0].word_original[-2:] == b2_endings[b_index].words[-1:][0].word_original[-2:]:
                    continue
                else:
                    if b1_endings[b_index].accent_type == LineModel.ACCENT_TYPE_M:
                        m_no+=1
                    if b1_endings[b_index].accent_type == LineModel.ACCENT_TYPE_F:
                        g_no+=1
                    if b1_endings[b_index].accent_type == LineModel.ACCENT_TYPE_D:
                        d_no+=1
        return m_no, g_no, d_no
    def get_strofika_type(self):
        #if parnaya rifmovka
        if self.strofika == 'aabb' or self.strofika == 'bbaa':
            return 4
        return 2

    def get_draw_accent(self):
        html = u''
        for l in self.lines:
            for w in l.words:
                html += w.draw_accent() + u' '
            html += u'<br />' + u"\r\n"
        return html

    def get_draw_accent_sign(self):
        html = u''
        for l in self.lines:
            for w in l.words:
                html += w.draw_accent_sign() + u' '
            html += u'<br />' + u"\r\n"
        return html

    def get_accent_prediction(self):
        html = u'<br /><br />'
        if self.razmer == 'horey':
            offset = 0
            step = 2
        elif self.razmer == 'yamb':
            offset = 1
            step = 2
        elif self.razmer == 'daktil':
            offset = 0
            step = 3
        elif self.razmer == 'anapest':
            offset = 1
            step = 3
        elif self.razmer == 'amfibrahii':
            offset = 2
            step = 3
        else:
            return ''

        for l in self.lines:
            cur_pos = 0
            for w in l.words:
                html_new, shift = w.draw_accent_prediction(cur_pos, step, offset)
                cur_pos += shift
                html += html_new + u' '
            # html += u'<br />' + u"\r\n"
            html += u"\r\n"
        return html


    def get_metrical_feet(self):
        variants = []
        stops = []
        for l in self.lines:
            if len(l.words) < 1:
                continue
            variant, stop = l.get_metrical_feet()
            #ignore lines with undefined accent
            if variant is None:
                continue
            variants.append( variant )
            stops.append( stop )
        if len(variants) < 1:
            print "NOTHING!!"
            return 'other', 0
        res = max(set(variants), key=variants.count)
        res_stop = round( float(sum(stops))/float(len(stops)) )
        #TODO make threshold on number of occurrences
        # return variants
        self.razmer = res
        self.stop = int(res_stop)
        return res, int( res_stop )