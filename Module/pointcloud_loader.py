#!/usr/bin/env python
# -*- coding: utf-8 -*-

from Data.channel_pointcloud import ChannelPointCloud

class PointCloudLoader(object):
    def __init__(self):
        self.channel_pointcloud = ChannelPointCloud()
        return

    def reset(self):
        self.channel_pointcloud.reset()
        return True

    def loadData(self, pointcloud_file_path):
        if not self.channel_pointcloud.loadData(pointcloud_file_path):
            print("[ERROR][PointCloudLoader::loadData]")
            print("\t loadData failed!")
        return True

def demo():
    pointcloud_file_path = \
        "/home/chli/chLi/OBJs/OpenGL/bunny_1.ply"

    pointcloud_loader = PointCloudLoader()
    pointcloud_loader.loadData(pointcloud_file_path)
    pointcloud_loader.channel_pointcloud.outputInfo()
    return True

