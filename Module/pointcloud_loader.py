#!/usr/bin/env python
# -*- coding: utf-8 -*-

from Data.channel_pointcloud import ChannelPointCloud

class PointCloudLoader(object):
    def __init__(self):
        self.channel_pointcloud = ChannelPointCloud()
        return

def demo():
    pointcloud_loader = PointCloudLoader()
    return True

