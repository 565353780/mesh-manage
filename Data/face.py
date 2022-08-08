#!/usr/bin/env python
# -*- coding: utf-8 -*-

class Face(object):
    def __init__(self, point_1_idx, point_2_idx, point_3_idx):
        self.point_1_idx = point_1_idx
        self.point_2_idx = point_2_idx
        self.point_3_idx = point_3_idx
        return

    def getPointIdxList(self):
        point_idx_list = [self.point_1_idx, self.point_2_idx, self.point_3_idx]
        return point_idx_list

    def isSameFace(self, face):
        face_point_idx_list = face.getPointIdxList()
        if self.point_1_idx not in face_point_idx_list or \
                self.point_2_idx not in face_point_idx_list or\
                self.point_3_idx not in face_point_idx_list:
            return False
        return True

