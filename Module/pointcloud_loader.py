#!/usr/bin/env python
# -*- coding: utf-8 -*-

from tqdm import tqdm

from Data.channel_pointcloud import ChannelPointCloud

from Method.path import getValidFilePath

class PointCloudLoader(object):
    def __init__(self):
        self.channel_pointcloud = ChannelPointCloud()
        return

    def reset(self):
        self.channel_pointcloud.reset()
        return True

    def loadPLY(self, ply_file_path):
        valid_file_path = getValidFilePath(ply_file_path)
        if valid_file_path is None:
            print("[ERROR][loadPLY]")
            print("\t getValidFilePath failed!")
            return False

        channel_name_list = []
        lines = []
        with open(valid_file_path, "r") as f:
            lines = f.readlines()

        point_num = -1
        loaded_point_num = 0
        find_start_line = False
        for line in tqdm(lines):
            if "property" in line:
                channel_name = line.split("\n")[0].split(" ")[2]
                channel_name_list.append(channel_name)
                continue

            if "element vertex" in line:
                point_num = int(line.split("\n")[0].split(" ")[2])
                continue

            if not find_start_line and "end_header" in line:
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
        return True

    def loadPCD(self, pcd_file_path):
        valid_file_path = getValidFilePath(pcd_file_path)
        if valid_file_path is None:
            print("[ERROR][loadPCD]")
            print("\t getValidFilePath failed!")
            return False

        channel_name_list = []
        lines = []
        with open(valid_file_path, "r") as f:
            lines = f.readlines()

        point_num = -1
        loaded_point_num = 0
        find_start_line = False
        for line in tqdm(lines):
            if "FIELDS" in line:
                channel_name_list = line.split("\n")[0].split("FIELDS ")[1].split(" ")
                continue

            if "POINTS" in line:
                point_num = int(line.split("\n")[0].split(" ")[1])
                continue

            if not find_start_line and "DATA ascii" in line:
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
        return True

    def loadData(self, pointcloud_file_path):
        self.reset()

        print("[INFO][PointCloudLoader::loadData]")
        print("\t start load pointcloud :")
        print("\t pointcloud_file_path =", pointcloud_file_path)

        if pointcloud_file_path[-4:] == ".pcd":
            if not self.loadPCD(pointcloud_file_path):
                print("[ERROR][PointCloudLoader::loadData]")
                print("\t loadPCD failed!")
                return False

            self.channel_pointcloud.updateKDTree()
            return True

        if pointcloud_file_path[-4:] == ".ply":
            if not self.loadPLY(pointcloud_file_path):
                print("[ERROR][PointCloudLoader::loadData]")
                print("\t loadPLY failed!")
                return False

            self.channel_pointcloud.updateKDTree()
            return True

        print("[ERROR][PointCloudLoader::loadData]")
        print("\t pointcloud_file type not valid!")
        return False

def demo():
    pointcloud_file_path = \
        "/home/chli/cad_ws/build/pcl_catkin/pcl_src-prefix/src/pcl_src/test/2d/canny.ply"

    pointcloud_loader = PointCloudLoader()
    pointcloud_loader.loadData(pointcloud_file_path)
    pointcloud_loader.channel_pointcloud.outputInfo()
    return True

