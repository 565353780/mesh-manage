#!/usr/bin/env python
# -*- coding: utf-8 -*-

class EdgeSet(object):
    def __init__(self):
        self.edge_list = []
        return

    def reset(self):
        self.edge_list = []
        return True

    def getEdgeIdx(self, edge):
        if len(self.edge_list) == 0:
            return None

        for i in range(len(self.edge_list)):
            if not self.edge_list[i].isSameEdge(edge):
                continue
            return i

        return None

    def isHaveEdge(self, edge):
        edge_idx = self.getEdgeIdx(edge)
        if edge_idx is None:
            return False
        return True

    def addEdge(self, edge, no_repeat=False):
        if no_repeat:
            if self.isHaveEdge(edge):
                return True

        self.edge_list.append(edge)
        return True

