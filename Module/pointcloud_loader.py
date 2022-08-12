#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
from tqdm import tqdm

from Data.channel_pointcloud import ChannelPointCloud

class PointCloudLoader(object):
    def __init__(self):
        self.channel_pointcloud = ChannelPointCloud()
        return

    def reset(self):
        self.channel_pointcloud.reset()
        return True

    def loadData(self, pointcloud_file_path):
        if not os.path.exists(pointcloud_file_path):
            print("[ERROR][PointCloudLoader::loadData]")
            print("\t file not exist!")
            return False

        self.reset()

        print("[INFO][PointCloudLoader::loadData]")
        print("\t start load pointcloud :")
        print("\t pointcloud_file_path = " + pointcloud_file_path)
        channel_name_list = []
        lines = []
        with open(pointcloud_file_path, "r") as f:
            lines = f.readlines()

        point_num = -1
        loaded_point_num = 0
        find_start_line = False
        for line in tqdm(lines):
            # load fields
            if "property" in line:
                channel_name = line.split("\n")[0].split(" ")[2]
                channel_name_list.append(channel_name)
                continue
            if "FIELDS" in line:
                channel_name_list = line.split("\n")[0].split("FIELDS ")[1].split(" ")
                continue

            # load point_num
            if "element vertex" in line:
                point_num = int(line.split("\n")[0].split(" ")[2])
                continue
            if "POINTS" in line:
                point_num = int(line.split("\n")[0].split(" ")[1])
                continue

            if not find_start_line and "DATA ascii" in line or "end_header" in line:
                find_start_line = True
                continue

            if not find_start_line:
                continue

            line_data = line.split("\n")[0].split(" ")

            channel_value_list = []
            for i in range(len(channel_name_list)):
                channel_value_list.append(float(line_data[i]))

            self.channel_pointcloud.addChannelPoint(channel_name_list, channel_value_list)
            loaded_point_num += 1

            if loaded_point_num == point_num:
                break
        print("[INFO][PointCloudLoader::loadData]")
        print("\t loaded", loaded_point_num, "points from poitncloud!")

        self.channel_pointcloud.updateKDTree()
        return True

def demo():
    pointcloud_file_path = \
        "/home/chli/cad_ws/build/pcl_catkin/pcl_src-prefix/src/pcl_src/test/2d/canny.ply"

    pointcloud_loader = PointCloudLoader()
    pointcloud_loader.loadData(pointcloud_file_path)
    return True

