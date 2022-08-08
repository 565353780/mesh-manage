#!/usr/bin/env python
# -*- coding: utf-8 -*-

from Data.channel_pointcloud import ChannelPointCloud
from Data.edge_set import EdgeSet
from Data.face_set import FaceSet

class ChannelMesh(object):
    def __init__(self):
        self.channel_pointcloud = ChannelPointCloud()
        self.edge_set = EdgeSet()
        self.face_set = FaceSet()
        return

    def reset(self):
        self.channel_pointcloud.reset()
        self.edge_set.reset()
        self.face_set.reset()
        return True

    def loadOBJFile(self, obj_file_path):
        print(obj_file_path)
        return True
