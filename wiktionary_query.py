# -*- coding: utf-8 -*-
import re
from neo4jrestclient.client import GraphDatabase
from neo4jrestclient.constants import RAW
from neo4jrestclient.client import Node

gdb = GraphDatabase("http://localhost:7474/db/data/")

def get_groups(words, depth=2):
    global gdb
    all_res = []

    q = u'MATCH (a { name:"'+words[0]+'" }),(b { name:"'+words[1]+'" }), p = allShortestPaths((a)-[*..'+str(depth)+']->(b)) RETURN DISTINCT p'
    returns = (int, unicode, Node)
    # results = gdb.query(q=q, returns=(client.Node, unicode, client.Relationship))
    # results = gdb.query(q=q, params={}, returns=returns)
    results = gdb.query(q=q, returns=RAW)
    for links in results:
        # print(links)
        for link in links:
            # print(link)
            n_nodes = []
            for linked_word in link['nodes']:
                # print(linked_word)
                n = gdb.nodes.get(linked_word)
                if n is not None:
            #        print n['name']
                    n_nodes.append(n['name'])

            r_rels = []
            for relationship in link['relationships']:
                # print(relationship)
                relationship_id = relationship[int(relationship.rfind('/'))+1:]
                r = gdb.relationships.get(relationship_id)
                if r is not None:
                    print(r.type, r.start.id, r.end.id)
                    r_rels.append(r.type)
            #print('------------')
            res = [j for i in zip(n_nodes, r_rels) for j in i]
            # n_nodes = n_nodes[-1:][0]
            res.append(n_nodes[-1:][0])
            # print(res)
            res = " -> ".join(res)
            all_res.append(res)

    return all_res

def getIdFromUrl(url):
    res_id = url[int(url.rfind('/'))+1:]
    res_id = int(res_id)
    return res_id

def mergeWordsSet(word_set):
    grouped_words = word_set.copy()
    for w1 in word_set:
        for w2 in word_set:
            if w1 == w2:
                continue
            if word_set[w1] == None or word_set[w2] == None:
                continue
            tmp_set = word_set[w1] & word_set[w2]
            #if common elements exist, let's merge
            if len(tmp_set) > 0:
                new_word = w1 + ',' + w2
                new_set = word_set[w1] | word_set[w2]
                del grouped_words[w2], grouped_words[w1]
                grouped_words[new_word] = new_set

                return True, grouped_words
    return False, grouped_words

def get_linked_groups(words, depth=2):
    global gdb
    #sort words
    words.sort()

    #dict array
    words_vector = dict.fromkeys(words, None)

    groups = []
    for w1 in words:
        for w2 in words:
            if w1 >= w2:
                continue
            print(w1 +' '+ w2)
            q = 'MATCH (a { name:"'+w1+'" }),(b { name:"'+w2+'" }), p = allShortestPaths((a)-[*..'+str(depth)+']-(b)) RETURN DISTINCT p'
            results = gdb.query(q=q)
            for result in results:
                for possible_path in result:
                    # print(result)
                    #now check if we have
                    for node in possible_path['nodes']:
                        node_id = getIdFromUrl(node)
                        if words_vector[w1] is None:
                            words_vector[w1] = set()
                        if words_vector[w2] is None:
                            words_vector[w2] = set()
                        words_vector[w1].add(node_id)
                        words_vector[w2].add(node_id)

    print(words_vector)
    isMerged = True
    while isMerged:
        isMerged, words_vector = mergeWordsSet(words_vector)
    print(words_vector)
    for el in words_vector.keys():
        print(el)

def get_betweenness(words, depth=2):
    global gdb
    #sorting for perfect order
    words.sort()

    NN = dict()

    groups = []
    for w1 in words:
        for w2 in words:
            if w1 >= w2:
                continue
            print(w1 +' '+ w2)
            q = 'MATCH (a { name:"'+w1+'" }),(b { name:"'+w2+'" }), p = allShortestPaths((a)-[*..'+str(depth)+']-(b)) RETURN DISTINCT p'
            results = gdb.query(q=q)
            for result in results:
                for possible_path in result:
                    # print(result)
                    # removing first and last node
                    possible_path['nodes'] = possible_path['nodes'][1:-1]
                    #now check if we have
                    for node in possible_path['nodes']:
                        node_id = getIdFromUrl(node)
                        plus1 = NN.get(node_id, 0);
                        plus1 += 1
                        NN[node_id] = plus1

    return NN

def measureDistance(rels=[]):
    weights = {'SYNONYMY':1, 'HYPERONYMY':4, 'HYPONYMY':3, 'HOLONYMY':4, 'MERONYMY':3}
    w_sum = 0
    for el in rels:
        w_sum += weights.get(el, 0)
    return w_sum

# words = [u'собака', u'пилот']
# get_groups(words, 5)


if __name__ == '__main__':
    # words = [u'собака', u'человек']
    words = [u'собака', u'кот', u'человек', u'море']
    # words = [u'корм', u'питание']
    # all_res = get_groups(words, 2)
    # for chain in all_res:
    #     print(chain)

    all_groups = get_linked_groups(words, 2)
    # all_groups = get_groups(words, 2)
    # betweenness = get_betweenness(words, 2)
    # print(betweenness)


