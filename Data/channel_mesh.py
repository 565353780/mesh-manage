#!/usr/bin/env python
# -*- coding: utf-8 -*-

from Data.channel_pointcloud import ChannelPointCloud
from Data.face_set import FaceSet

class ChannelMesh(object):
    def __init__(self):
        self.channel_pointcloud = ChannelPointCloud()
        self.face_set = FaceSet()
        return

    def reset(self):
        self.channel_pointcloud.reset()
        self.face_set.reset()
        return True

    def addChannelPoint(self, channel_name_list, channel_value_list):
        return self.channel_pointcloud.addChannelPoint(channel_name_list, channel_value_list)

    def addFace(self, point_idx_list):
        return self.face_set.addFace(point_idx_list)

