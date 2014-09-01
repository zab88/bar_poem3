# -*- coding: utf-8 -*-
import networkx as nx

class NetX:
    G = None
    nodes = dict()
    edges = None

    def __init__(self):
        self.G = nx.Graph()

    def addNeoNodes(self):
        self.G.add_nodes_from(self.nodes)


