#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
from tqdm import tqdm

class Channel(object):
    def __init__(self):
        self.name = ""
        self.value = 0
        return

class ChannelPoint(object):
    def __init__(self):
        self.channel_list = []
        return

    def setChannelValue(self, channel_name, channel_value):
        if len(self.channel_list) == 0:
            new_channel = Channel()
            new_channel.name = channel_name
            new_channel.value = channel_value
            self.channel_list.append(new_channel)
            return True
        for exist_channel in self.channel_list:
            if exist_channel.name == channel_name:
                exist_channel.value = channel_value
                return True

        new_channel = Channel()
        new_channel.name = channel_name
        new_channel.value = channel_value
        self.channel_list.append(new_channel)
        return True

    def getChannelValue(self, channel_name):
        if len(self.channel_list) == 0:
            print("ChannelPoint::getChannelValue :")
            print("channel_list is empty!")
            return None

        for exist_channel in self.channel_list:
            if exist_channel.name != channel_name:
                continue
            return exist_channel.value

        print("ChannelPoint::getChannelValue :")
        print("this channel :", channel_name, "not exist!")
        return None

    def setXYZ(self, x, y, z):
        self.setChannelValue("x", x)
        self.setChannelValue("y", y)
        self.setChannelValue("z", z)
        return True

    def setRGB(self, r, g, b):
        self.setChannelValue("r", r)
        self.setChannelValue("g", g)
        self.setChannelValue("b", b)
        return True

    def getXYZ(self):
        return [self.getChannelValue("x"), self.getChannelValue("y"), self.getChannelValue("z")]
    
    def getRGB(self):
        return [self.getChannelValue("r"), self.getChannelValue("g"), self.getChannelValue("b")]

class ChannelPointCloud(object):
    def __init__(self):
        self.point_list = []
        return

    def reset(self):
        self.point_list.clear()
        return True

    def addPoint(self, x, y, z, r, g, b):
        new_point = ChannelPoint()
        new_point.setXYZ(x, y, z)
        new_point.setRGB(r, g, b)
        self.point_list.append(new_point)
        return True

    def setPointChannelValue(self, point_idx, channel_name, channel_value):
        if point_idx >= len(self.point_list):
            print("ChannelPointCloud::setPointChannelValue :")
            print("point_idx out of range!")
            return False
        return self.point_list[point_idx].setChannelValue(channel_name, channel_value)

    def getChannelValueList(self, channel_name):
        channel_value_list = []
        for point in self.point_list:
            channel_value_list.append(point.getChannelValue(channel_name))
        return channel_value_list

    def getChannelListValueList(self, channel_name_list):
        channel_list_value_list = []
        for point in self.point_list:
            channel_value_list = []
            for channel_name in channel_name_list:
                channel_value_list.append(point.getChannelValue(channel_name))
            channel_list_value_list.append(channel_value_list)
        return channel_list_value_list

class MergeChannel:
    def __init__(self):
        self.rgb_pointcloud = ChannelPointCloud()
        self.pointcloud_list = []
        self.merge_channel_name_list = []
        self.merge_channel_in_pointcloud_idx_list = []
        self.merged_pointcloud = ChannelPointCloud()
        return

    def reset(self):
        self.rgb_pointcloud.reset()
        self.pointcloud_list.clear()
        self.merge_channel_name_list.clear()
        self.merge_channel_in_pointcloud_idx_list.clear()
        self.merged_pointcloud.reset()
        return True

    def loadPointCloud(self,
                       pointcloud_file_path,
                       channel_name_list,
                       channel_idx_list):
        if not os.path.exists(pointcloud_file_path):
            print("MergeChannel::loadPointCloud :")
            print("file not exist!")
            return None

        pointcloud = ChannelPointCloud()

        print("start load pointcloud :", pointcloud_file_path, "...")
        lines = []
        with open(pointcloud_file_path, "r") as f:
            lines = f.readlines()

        point_num = -1
        loaded_point_num = 0
        find_start_line = False
        for line in tqdm(lines):
            if "element vertex" in line:
                point_num = int(line.split("\n")[0].split(" ")[2])
                continue

            if "POINTS" in line:
                point_num = int(line.split("\n")[0].split(" ")[1])
                continue

            if "DATA ascii" in line or "end_header" in line:
                find_start_line = True
                continue

            if not find_start_line:
                continue

            line_data = line.split("\n")[0].split(" ")
            new_point = ChannelPoint()
            for i in range(len(channel_name_list)):
                channel_name = channel_name_list[i]
                channel_idx = channel_idx_list[i]
                channel_value = float(line_data[channel_idx])
                new_point.setChannelValue(channel_name, channel_value)
                pointcloud.point_list.append(new_point)
            loaded_point_num += 1

            if loaded_point_num == point_num:
                break
        print("loaded", point_num, "points from poitncloud!")
        return pointcloud

    def loadRGBPointCloud(self,
                          pointcloud_file_path,
                          pointcloud_xyzrgb_channel_idx_list):
        self.rgb_pointcloud = self.loadPointCloud(
            pointcloud_file_path,
            ["x", "y", "z", "r", "g", "b"],
            pointcloud_xyzrgb_channel_idx_list
        )
        return True

    def loadMergePointCloud(self,
                            pointcloud_file_path,
                            pointcloud_channel_name_list,
                            pointcloud_channel_idx_list):
        for channel_name in pointcloud_channel_name_list:
            if channel_name in self.merge_channel_name_list:
                print("MergeChannel::loadMergePointCloud :")
                print("channel_name :", channel_name, "already loaded from other file!")
                return False

        self.pointcloud_list.append(self.loadPointCloud(
            pointcloud_file_path,
            pointcloud_channel_name_list,
            pointcloud_channel_idx_list))

        for channel_name in pointcloud_channel_name_list:
            self.merge_channel_name_list.append(channel_name)
            self.merge_channel_in_pointcloud_idx_list.append(len(self.pointcloud_list) - 1)
        return True

    def isMergePointCloudValid(self):
        if len(self.pointcloud_list) == 0:
            return False

        merge_point_num = len(self.pointcloud_list[0].point_list)
        for pointcloud in self.pointcloud_list:
            if len(pointcloud.point_list) != merge_point_num:
                print("MergeChannel::isMergePointCloudValid :")
                print("pointcloud size not matched!")
                return False
        return True

    def updateMergedPointCloud(self, ordered_merge_channel_name_list):
        self.merged_pointcloud.reset()
        if len(self.pointcloud_list) == 0:
            return True

        if not self.isMergePointCloudValid():
            return False

        ordered_merge_channel_name_idx_list = []
        for ordered_merge_channel_name in ordered_merge_channel_name_list:
            for i in range(len(self.merge_channel_name_list)):
                if self.merge_channel_name_list[i] != ordered_merge_channel_name:
                    continue
                ordered_merge_channel_name_idx_list.append(i)
                break
        print(ordered_merge_channel_name_idx_list)

        merge_point_num = len(self.pointcloud_list[0].point_list)

        for i in range(merge_point_num):
            new_point = ChannelPoint()
            #  for j in range(len(ordered_merge_channel_name_idx_list)):

        for i in range(len(self.merge_channel_name_list)):
            merge_channel_name = self.merge_channel_name_list[i]
            merge_channel_in_pointcloud_idx = self.merge_channel_in_pointcloud_idx_list[i]
            merge_pointcloud = self.pointcloud_list[merge_channel_in_pointcloud_idx]
            #  for point in merge_pointcloud.point_list:

if __name__ == "__main__":
    rgb_pointcloud_file_path = "./masked_pc/home/home_cut_DownSample_8.ply"
    rgb_pointcloud_xyzrgb_channel_idx_list = [0, 1, 2, 3, 4, 5]
    merge_info_list = []
    merge_info_list.append([
        "./masked_pc/home/home_DownSample_8_masked_cut.pcd",
        ["x", "y", "z", "instance_label"],
        [0, 1, 2, 6]])
    merge_info_list.append([
        "./masked_pc/home/home_DownSample_8_masked_cut_normal.ply",
        ["nx", "ny", "nz"],
        [3, 4, 5]])
    ordered_merge_channel_name_list = ["x", "y", "z", "nx", "ny", "nz", "instance_label"]
    merged_pointcloud_file_path = "./masked_pc/home/home_DownSample_8_masked_merged.pcd"

    merge_channel = MergeChannel()

    merge_channel.loadRGBPointCloud(rgb_pointcloud_file_path,
                                    rgb_pointcloud_xyzrgb_channel_idx_list)
    for merge_info in merge_info_list:
        merge_channel.loadMergePointCloud(merge_info[0], merge_info[1], merge_info[2])

    merge_channel.updateMergedPointCloud(ordered_merge_channel_name_list)

