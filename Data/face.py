#!/usr/bin/env python
# -*- coding: utf-8 -*-

class Face(object):
    def __init__(self, point_idx_list):
        self.point_idx_list = point_idx_list
        return

    def isSameFace(self, face):
        face_point_idx_list = face.point_idx_list

        if len(self.point_idx_list) != len(face_point_idx_list):
            return False

        for point_idx in self.point_idx_list:
            if point_idx not in face_point_idx_list:
                return False
        return True

