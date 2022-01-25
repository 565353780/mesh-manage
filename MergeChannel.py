#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import numpy as np
from tqdm import tqdm
from scipy.spatial import KDTree

class Channel(object):
    def __init__(self):
        self.name = ""
        self.value = 0
        self.size = 0
        self.type = ""
        self.count = 1
        return

    def updateName(self):
        if self.name in ["x", "y", "z", "nx", "ny", "nz"]:
            self.size = 4
            self.type = "F"
            self.count = 1
            return True
        if self.name in ["r", "g", "b", "rgb", "instance_label"]:
            self.size = 4
            self.type = "U"
            self.count = 1
            return True
        self.size = 4
        self.type = "F"
        self.count = 1
        return True

    def setName(self, name):
        self.name = name
        return self.updateName()

    def updateValue(self):
        if self.type == "F":
            self.value = float(self.value)
            return True
        if self.type == "U":
            self.value = int(self.value)
            return True
        if self.type == "I":
            self.value = int(self.value)
            return True
        return True

    def setValue(self, value):
        self.value = value
        self.updateValue()
        return True

class ChannelPoint(object):
    def __init__(self):
        self.channel_list = []
        return

    def updateFloatRGB(self):
        r = self.getChannelValue("r")
        g = self.getChannelValue("g")
        b = self.getChannelValue("b")
        if r is None or g is None or b is None:
            return False
        rgb = r << 16 | g << 8 | b | 1<<24
        self.setChannelValue("rgb", rgb)
        return True

    def setChannelValue(self, channel_name, channel_value):
        set_rgb = channel_name == "rgb"
        if len(self.channel_list) == 0:
            new_channel = Channel()
            new_channel.setName(channel_name)
            new_channel.setValue(channel_value)
            self.channel_list.append(new_channel)
            return True
        for exist_channel in self.channel_list:
            if exist_channel.name == channel_name:
                exist_channel.setValue(channel_value)
                if channel_name in ["r", "g", "b"] and not set_rgb:
                    self.updateFloatRGB()
                return True

        new_channel = Channel()
        new_channel.setName(channel_name)
        new_channel.setValue(channel_value)
        self.channel_list.append(new_channel)
        if channel_name in ["r", "g", "b"] and not set_rgb:
            self.updateFloatRGB()
        return True

    def getChannelValue(self, channel_name):
        if len(self.channel_list) == 0:
            return None

        for exist_channel in self.channel_list:
            if exist_channel.name != channel_name:
                continue
            return exist_channel.value
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
        return [self.getChannelValue("r"), self.getChannelValue("g"), self.getChannelValue("b"), self.getChannelValue("rgb")]

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
        self.kd_tree = None
        self.pointcloud_list = []
        self.merge_channel_name_list = []
        self.merge_channel_in_pointcloud_idx_list = []
        self. merge_pointcloud_valid = True
        return

    def reset(self):
        self.rgb_pointcloud.reset()
        self.kd_tree = None
        self.pointcloud_list.clear()
        self.merge_channel_name_list.clear()
        self.merge_channel_in_pointcloud_idx_list.clear()
        self. merge_pointcloud_valid = True
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

            if not find_start_line and "DATA ascii" in line or "end_header" in line:
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
        print("loaded", loaded_point_num, "points from poitncloud!")
        return pointcloud

    def loadRGBPointCloud(self,
                          pointcloud_file_path,
                          pointcloud_xyzrgb_channel_idx_list):
        if not self.isMergePointCloudValid():
            print("MergeChannel::loadRGBPointCloud :")
            print("isMergePointCloudValid failed!")
            return False
        self.rgb_pointcloud = self.loadPointCloud(
            pointcloud_file_path,
            ["x", "y", "z", "r", "g", "b"],
            pointcloud_xyzrgb_channel_idx_list
        )
        xyz = self.rgb_pointcloud.getChannelListValueList(["x", "y", "z"])
        self.kd_tree = KDTree(xyz)
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

    def getNearestRGB(self, x, y, z):
        nearest_rgb = [0, 0, 0, 0]
        if len(self.rgb_pointcloud.point_list) == 0:
            return nearest_rgb
        _, nearest_ponit_idx = self.kd_tree.query([x, y, z])
        nearest_rgb = self.rgb_pointcloud.point_list[nearest_ponit_idx].getRGB()
        return nearest_rgb

    def getMergedPointCloud(self, ordered_merge_channel_name_list):
        merged_pointcloud = ChannelPointCloud()

        if len(self.pointcloud_list) == 0:
            print("MergeChannel::getMergedPointCloud :")
            print("pointcloud_list is empty!")
            return merged_pointcloud

        if not self.isMergePointCloudValid():
            print("MergeChannel::getMergedPointCloud :")
            print("isMergePointCloudValid failed!")
            return merged_pointcloud

        need_to_add_color = False
        x_in_pointcloud_idx = -1
        y_in_pointcloud_idx = -1
        z_in_pointcloud_idx = -1

        ordered_merge_channel_name_idx_list = []
        for ordered_merge_channel_name in ordered_merge_channel_name_list:
            if ordered_merge_channel_name == "r":
                ordered_merge_channel_name_idx_list.append(-1)
                need_to_add_color = True
                continue
            if ordered_merge_channel_name == "g":
                ordered_merge_channel_name_idx_list.append(-2)
                need_to_add_color = True
                continue
            if ordered_merge_channel_name == "b":
                ordered_merge_channel_name_idx_list.append(-3)
                need_to_add_color = True
                continue
            if ordered_merge_channel_name == "rgb":
                ordered_merge_channel_name_idx_list.append(-4)
                need_to_add_color = True
                continue
            for i in range(len(self.merge_channel_name_list)):
                if self.merge_channel_name_list[i] != ordered_merge_channel_name:
                    continue
                ordered_merge_channel_name_idx_list.append(i)
                if ordered_merge_channel_name == "x":
                    x_in_pointcloud_idx = self.merge_channel_in_pointcloud_idx_list[i]
                elif ordered_merge_channel_name == "y":
                    y_in_pointcloud_idx = self.merge_channel_in_pointcloud_idx_list[i]
                elif ordered_merge_channel_name == "z":
                    z_in_pointcloud_idx = self.merge_channel_in_pointcloud_idx_list[i]
                break

        if need_to_add_color:
            if x_in_pointcloud_idx == -1 or y_in_pointcloud_idx == -1 or z_in_pointcloud_idx == -1:
                print("MergeChannel::getMergedPointCloud :")
                print("xyz data not found! will not add color into pointcloud!")
                need_to_add_color = False

        merge_point_num = len(self.pointcloud_list[0].point_list)
        
        if merge_point_num == 0:
            print("MergeChannel::getMergedPointCloud :")
            print("all pointcloud size is 0!")
            return merged_pointcloud

        print("start merge pointcloud...")
        for i in tqdm(range(merge_point_num)):
            new_point = ChannelPoint()
            nearest_rgb = []
            if need_to_add_color:
                x = self.pointcloud_list[x_in_pointcloud_idx].point_list[i].getChannelValue("x")
                y = self.pointcloud_list[y_in_pointcloud_idx].point_list[i].getChannelValue("y")
                z = self.pointcloud_list[z_in_pointcloud_idx].point_list[i].getChannelValue("z")
                nearest_rgb = self.getNearestRGB(x, y, z)
            for j in range(len(ordered_merge_channel_name_idx_list)):
                ordered_merge_channel_name_idx = ordered_merge_channel_name_idx_list[j]
                if ordered_merge_channel_name_idx == -1:
                    new_point.setChannelValue("r", nearest_rgb[0])
                    continue
                if ordered_merge_channel_name_idx == -2:
                    new_point.setChannelValue("g", nearest_rgb[1])
                    continue
                if ordered_merge_channel_name_idx == -3:
                    new_point.setChannelValue("b", nearest_rgb[2])
                    continue
                if ordered_merge_channel_name_idx == -4:
                    new_point.setChannelValue("rgb", nearest_rgb[3])
                    continue
                merge_channel_name = self.merge_channel_name_list[ordered_merge_channel_name_idx]
                merge_channel_in_pointcloud_idx = \
                    self.merge_channel_in_pointcloud_idx_list[ordered_merge_channel_name_idx]
                merge_channel_value = \
                    self.pointcloud_list[merge_channel_in_pointcloud_idx].point_list[i].getChannelValue(merge_channel_name)
                new_point.setChannelValue(merge_channel_name, merge_channel_value)
            merged_pointcloud.point_list.append(new_point)
        return merged_pointcloud

    def getPCDHeader(self, pointcloud):
        '''
        PCD :
        # .PCD v0.7 - Point Cloud Data file format
        VERSION 0.7
        FIELDS x y z rgb
        SIZE 4 4 4 4
        TYPE F F F F
        COUNT 1 1 1 1
        WIDTH 9351496
        HEIGHT 1
        VIEWPOINT 0 0 0 1 0 0 0
        POINTS 9351496
        DATA ascii
        '''
        channel_list = []

        point_num = len(pointcloud.point_list)
        if point_num > 0:
            channel_list = pointcloud.point_list[0].channel_list

        pcd_header = ""
        pcd_header += "# .PCD v0.7 - Point Cloud Data file format\n"
        pcd_header += "VERSION 0.7\n"

        pcd_header += "FIELDS"
        for channel in channel_list:
            pcd_header += " " + channel.name
        pcd_header += "\n"

        pcd_header += "SIZE"
        for channel in channel_list:
            pcd_header += " " + str(channel.size)
        pcd_header += "\n"

        pcd_header += "TYPE"
        for channel in channel_list:
            pcd_header += " " + channel.type
        pcd_header += "\n"

        pcd_header += "COUNT"
        for channel in channel_list:
            pcd_header += " " + str(channel.count)
        pcd_header += "\n"

        pcd_header += "WIDTH " + str(point_num) + "\n"

        pcd_header += "HEIGHT 1\n"
        pcd_header += "VIEWPOINT 0 0 0 1 0 0 0\n"

        pcd_header += "POINTS " + str(point_num) + "\n"

        pcd_header += "DATA ascii\n"
        return pcd_header

    def savePointCloud(self, pointcloud, save_pointcloud_file_path):
        print("start save pointcloud...")
        with open(save_pointcloud_file_path, "w") as f:
            pcd_header = self.getPCDHeader(pointcloud)
            f.write(pcd_header)
            for point in tqdm(pointcloud.point_list):
                last_channel_idx = len(point.channel_list) - 1
                for i in range(last_channel_idx + 1):
                    f.write(str(point.channel_list[i].value))
                    if i < last_channel_idx:
                        f.write(" ")
                    else:
                        f.write("\n")
        return True

def demo():
    merge_info_list = []
    merge_info_list.append([
        "./masked_pc/home/home_DownSample_8_masked_cut.pcd",
        ["x", "y", "z", "instance_label"],
        [0, 1, 2, 6]])
    merge_info_list.append([
        "./masked_pc/home/home_DownSample_8_masked_cut_normal.ply",
        ["nx", "ny", "nz"],
        [3, 4, 5]])
    rgb_pointcloud_file_path = "./masked_pc/home/home_cut_DownSample_8.ply"
    rgb_pointcloud_xyzrgb_channel_idx_list = [0, 1, 2, 3, 4, 5]
    ordered_merge_channel_name_list = ["x", "y", "z", "nx", "ny", "nz", "rgb", "instance_label"]
    merged_pointcloud_file_path = "./masked_pc/home/home_DownSample_8_masked_merged.pcd"

    merge_channel = MergeChannel()

    for merge_info in merge_info_list:
        merge_channel.loadMergePointCloud(merge_info[0], merge_info[1], merge_info[2])

    merge_channel.loadRGBPointCloud(rgb_pointcloud_file_path,
                                    rgb_pointcloud_xyzrgb_channel_idx_list)

    merged_pointcloud = merge_channel.getMergedPointCloud(ordered_merge_channel_name_list)

    merge_channel.savePointCloud(merged_pointcloud, merged_pointcloud_file_path)
    return True

if __name__ == "__main__":
    demo()

