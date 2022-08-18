#!/usr/bin/env python
# -*- coding: utf-8 -*-

from Data.channel_pointcloud import ChannelPointCloud

def demo():
    pointcloud_file_path = \
        "/home/chli/chLi/OBJs/OpenGL/bunny_1.ply"

    channel_pointcloud = ChannelPointCloud()
    channel_pointcloud.loadData(pointcloud_file_path)
    channel_pointcloud.outputInfo()
    return True

