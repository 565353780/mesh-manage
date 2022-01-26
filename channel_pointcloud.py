#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
from scipy.spatial.kdtree import KDTree
from tqdm import tqdm

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

    def outputInfo(self, info_level=0):
        line_start = "\t" * info_level
        print(line_start + "Channel:")
        print(line_start + "\t name: " + self.name)
        print(line_start + "\t value: " + str(self.value))
        print(line_start + "\t size: " + str(self.size))
        print(line_start + "\t type: " + self.type)
        print(line_start + "\t count: " + str(self.count))
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

    def setChannelValueList(self, channel_name_list, channel_value_list):
        for i in range(len(channel_name_list)):
            self.setChannelValue(channel_name_list[i], channel_value_list[i])
        return True

    def getChannelValue(self, channel_name):
        if len(self.channel_list) == 0:
            return None

        for exist_channel in self.channel_list:
            if exist_channel.name != channel_name:
                continue
            return exist_channel.value
        return None

    def getChannelValueList(self, channel_name_list):
        channel_value_list = []
        for channel_name in channel_name_list:
            channel_value_list.append(self.getChannelValue(channel_name))
        return channel_value_list

    def outputInfo(self, info_level=0):
        line_start = "\t" * info_level
        print(line_start + "ChannelPoint:")
        for channel in self.channel_list:
            channel.outputInfo(info_level + 1)
        return True

class ChannelPointCloud(object):
    def __init__(self):
        self.point_list = []
        self.kd_tree = None
        return

    def reset(self):
        self.point_list.clear()
        self.kd_tree = None
        return True

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

    def updateKDTree(self):
        self.kd_tree = None
        xyz_list = self.getChannelListValueList(["x", "y", "z"])
        if len(xyz_list) == 0:
            return False
        if xyz_list[0][0] is None:
            return False
        self.kd_tree = KDTree(xyz_list)
        return True

    def loadData(self, pointcloud_file_path, channel_name_list, channel_idx_list):
        if not os.path.exists(pointcloud_file_path):
            print("ChannelPointCloud::loadData :")
            print("file not exist!")
            return False

        self.reset()

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

            channel_value_list = []
            for i in range(len(channel_name_list)):
                channel_idx = channel_idx_list[i]
                channel_value_list.append(float(line_data[channel_idx]))

            new_point = ChannelPoint()
            new_point.setChannelValueList(channel_name_list, channel_value_list)
            self.point_list.append(new_point)
            loaded_point_num += 1

            if loaded_point_num == point_num:
                break
        print("loaded", loaded_point_num, "points from poitncloud!")
        self.updateKDTree()
        return True

    def getNearestPointInfo(self, x, y, z):
        if self.kd_tree is None:
            return None, None
        if len(self.point_list) == 0:
            return None, None
        nearest_dist, nearest_point_idx = self.kd_tree.query([x, y, z])
        return nearest_dist, nearest_point_idx

    def getNearestPoint(self, x, y, z):
        _, nearest_point_idx = self.getNearestPointInfo(x, y, z)
        if nearest_point_idx is None:
            return None
        return self.point_list[nearest_point_idx]

    def getNearestChannelValueListValue(self, x, y, z, channel_name_list):
        nearest_channel_value_list = []
        if len(channel_name_list) == 0:
            return nearest_channel_value_list
        nearest_point = self.getNearestPoint(x, y, z)
        if nearest_point is None:
            return None
        for channel_name in channel_name_list:
            nearest_channel_value_list.append(
                nearest_point.getChannelValue(channel_name))
        return nearest_channel_value_list

    def copyChannelValue(self, target_pointcloud, channel_name_list):
        pointcloud_size = len(self.point_list)
        target_pointcloud_size = len(target_pointcloud.point_list)
        if target_pointcloud_size == 0:
            print("ChannelPointCloud::copyChannelValue :")
            print("target pointcloud is empty!")
            return False

        if pointcloud_size > 0 and pointcloud_size != target_pointcloud_size:
            print("ChannelPointCloud::copyChannelValue :")
            print("pointcloud size not matched!")
            return False

        first_point_channel_value_list = \
            target_pointcloud.point_list[0].getChannelValueList(channel_name_list)
        if None in first_point_channel_value_list:
            print("ChannelPointCloud::copyChannelValue :")
            print("target_pointcloud doesn't have all channels needed!")
            return False

        print("start copy channel value...")
        channel_list_value_list = \
            target_pointcloud.getChannelListValueList(channel_name_list)

        if pointcloud_size == 0:
            for channel_value_list in tqdm(channel_list_value_list):
                new_point = ChannelPoint()
                new_point.setChannelValueList(channel_name_list, channel_value_list)
                self.point_list.append(new_point)
            return True

        for i in tqdm(pointcloud_size):
            channel_value_list = channel_list_value_list[i]
            self.point_list[i].setChannelValueList(channel_name_list, channel_value_list)
        return True

    def setChannelValueByKDTree(self, target_pointcloud, channel_name_list):
        if len(self.point_list) == 0:
            return True

        if len(target_pointcloud.point_list) == 0:
            print("ChannelPointCloud::setChannelValueByKDTree :")
            print("target pointcloud is empty!")
            return False

        first_point_xyz = self.point_list[0].getChannelValueList(["x", "y", "z"])
        if None in first_point_xyz:
            print("ChannelPointCloud::setChannelValueByKDTree :")
            print("pointcloud xyz not found!")
            return False

        first_point_channel_value_list = \
            target_pointcloud.getNearestChannelValueListValue(
                first_point_xyz[0],
                first_point_xyz[1],
                first_point_xyz[2],
                channel_name_list)
        if None in first_point_channel_value_list:
            print("ChannelPointCloud::setChannelValueByKDTree :")
            print("target_pointcloud doesn't have all channels needed!")
            return False

        print("start set channel value by KDTree...")
        for point in tqdm(self.point_list):
            xyz = point.getChannelValueList(["x", "y", "z"])
            channel_value_list = \
                target_pointcloud.getNearestChannelValueListValue(xyz[0],
                                                                  xyz[1],
                                                                  xyz[2],
                                                                  channel_name_list)
            point.setChannelValueList(channel_name_list, channel_value_list)
        return True

    def getPCDHeader(self):
        channel_list = []

        point_num = len(self.point_list)
        if point_num > 0:
            channel_list = self.point_list[0].channel_list

        pcd_header = "# .PCD v0.7 - Point Cloud Data file format\n"
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

    def savePointCloud(self, save_pointcloud_file_path):
        print("start save pointcloud to", save_pointcloud_file_path, "...")
        with open(save_pointcloud_file_path, "w") as f:
            pcd_header = self.getPCDHeader()
            f.write(pcd_header)
            for point in tqdm(self.point_list):
                last_channel_idx = len(point.channel_list) - 1
                for i in range(last_channel_idx + 1):
                    f.write(str(point.channel_list[i].value))
                    if i < last_channel_idx:
                        f.write(" ")
                    else:
                        f.write("\n")
        return True

    def outputInfo(self, info_level=0):
        line_start = "\t" * info_level
        print(line_start + "ChannelPointCloud:")
        for point in self.point_list:
            point.outputInfo(info_level + 1)
        return True

def demo():
    source_pointcloud = ChannelPointCloud()

    source_pointcloud.loadData("./masked_pc/home/home_cut.ply",
                               ["x", "y", "z", "r", "g", "b"],
                               [0, 1, 2, 3, 4, 5])

    label_pointcloud = ChannelPointCloud()
    label_pointcloud.loadData("./masked_pc/home/home_DownSample_8_masked.pcd",
                              ["x", "y", "z", "instance_label"],
                              [0, 1, 2, 4])

    merge_pointcloud = ChannelPointCloud()

    merge_pointcloud.copyChannelValue(source_pointcloud, ["x", "y", "z", "r", "g", "b"])
    merge_pointcloud.setChannelValueByKDTree(label_pointcloud, ["instance_label"])

    merge_pointcloud.savePointCloud("./test.pcd")
    return True

if __name__ == "__main__":
    demo()

