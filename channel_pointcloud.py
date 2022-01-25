#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
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
            new_point = ChannelPoint()
            for i in range(len(channel_name_list)):
                channel_name = channel_name_list[i]
                channel_idx = channel_idx_list[i]
                channel_value = float(line_data[channel_idx])
                new_point.setChannelValue(channel_name, channel_value)
            self.point_list.append(new_point)
            loaded_point_num += 1

            if loaded_point_num == point_num:
                break
        print("loaded", loaded_point_num, "points from poitncloud!")
        return True

    def getPCDHeader(self):
        channel_list = []

        point_num = len(self.point_list)
        if point_num > 0:
            channel_list = self.point_list[0].channel_list

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

