#!/usr/bin/env python
# -*- coding: utf-8 -*-

class FaceSet(object):
    def __init__(self):
        self.face_list = []
        return

    def reset(self):
        self.face_list = []
        return True

    def getFaceIdx(self, face):
        if len(self.face_list) == 0:
            return None

        for i in range(len(self.face_list)):
            if not self.face_list[i].isSameFace(face):
                continue
            return i

        return None

    def isHaveFace(self, face):
        face_idx = self.getFaceIdx(face)
        if face_idx is None:
            return False
        return True

    def addFace(self, face, no_repeat=False):
        if no_repeat:
            if self.isHaveFace(face):
                return True

        self.face_list.append(face)
        return True
