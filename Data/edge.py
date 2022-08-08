#!/usr/bin/env python
# -*- coding: utf-8 -*-

class Edge(object):
    def __init__(self, start_point_idx, end_point_idx):
        self.start_point_idx = start_point_idx
        self.end_point_idx = end_point_idx
        return

    def getPointIdxList(self):
        point_idx_list = [self.start_point_idx, self.end_point_idx]
        return point_idx_list

    def isSameEdge(self, edge):
        edge_point_idx_list = edge.getPointIdxList()
        if self.start_point_idx not in edge_point_idx_list or \
                self.end_point_idx not in edge_point_idx_list:
            return False
        return True

