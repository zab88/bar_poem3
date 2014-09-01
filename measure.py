# -*- coding: utf-8 -*-
from model.PoemModel import PoemModel
import wiktionary_query

poem1_file = open('poems/2.txt', 'r')
poem1_text = poem1_file.read()
poem1 = PoemModel('', poem1_text)

poem2_file = open('poems/4.txt', 'r')
poem2_text = poem2_file.read()
poem2 = PoemModel('', poem2_text)

poem1_words = []
for line in poem1.lines:
    for w in line.words:
        # print(w.word_original)
        poem1_words.append(w.word_original)

poem2_words = []
for line in poem2.lines:
    for w in line.words:
        poem2_words.append(w.word_original)

linked_words1 = wiktionary_query.get_linked_groups(poem1_words)
print('+++++++')
linked_words2 = wiktionary_query.get_linked_groups(poem2_words)