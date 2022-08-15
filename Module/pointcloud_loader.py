#!/usr/bin/env python
# -*- coding: utf-8 -*-

from tqdm import tqdm

from Data.channel_pointcloud import ChannelPointCloud

from Method.io import loadFileData

class PointCloudLoader(object):
    def __init__(self):
        self.channel_pointcloud = ChannelPointCloud()
        return

    def reset(self):
        self.channel_pointcloud.reset()
        return True

    def loadData(self, pointcloud_file_path):
        self.reset()

        print("[INFO][PointCloudLoader::loadData]")
        print("\t start load pointcloud :")
        print("\t pointcloud_file_path =", pointcloud_file_path)

        channel_name_list, channel_value_list_list = loadFileData(pointcloud_file_path, True)

        if channel_name_list == [] or channel_value_list_list == []:
            print("[ERROR][PointCloudLoader::loadData]")
            print("\t loadFileData failed!")
            return False

        for channel_value_list in tqdm(channel_value_list_list):
            self.channel_pointcloud.addChannelPoint(channel_name_list, channel_value_list)

        self.channel_pointcloud.updateKDTree()
        return True

def demo():
    pointcloud_file_path = \
        "/home/chli/chLi/OBJs/OpenGL/bunny_1.ply"

    pointcloud_loader = PointCloudLoader()
    pointcloud_loader.loadData(pointcloud_file_path)
    pointcloud_loader.channel_pointcloud.outputInfo()
    return True

