#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
from tqdm import tqdm
from scipy.spatial.kdtree import KDTree

from Data.channel_point import ChannelPoint

class ChannelPointCloud(object):
    def __init__(self):
        self.channel_point_list = []
        self.kd_tree = None
        self.xyz_changed = True

        self.save_ignore_channel_name_list = ["r", "g", "b"]
        return

    def reset(self):
        self.channel_point_list.clear()
        self.kd_tree = None
        self.xyz_changed = True
        return True

    def getChannelValueList(self, channel_name):
        channel_value_list = []
        for channel_point in self.channel_point_list:
            channel_value_list.append(channel_point.getChannelValue(channel_name))
        return channel_value_list

    def getChannelListValueList(self, channel_name_list):
        channel_list_value_list = []
        for channel_point in self.channel_point_list:
            channel_value_list = []
            for channel_name in channel_name_list:
                channel_value_list.append(channel_point.getChannelValue(channel_name))
            channel_list_value_list.append(channel_value_list)
        return channel_list_value_list

    def updateKDTree(self):
        if not self.xyz_changed:
            return True

        self.kd_tree = None
        xyz_list = self.getChannelListValueList(["x", "y", "z"])
        if len(xyz_list) == 0:
            return False
        if None in xyz_list[0]:
            return False
        self.kd_tree = KDTree(xyz_list)
        self.xyz_changed = False
        return True

    def loadData(self, pointcloud_file_path):
        if not os.path.exists(pointcloud_file_path):
            print("[ERROR][ChannelPointCloud::loadData]")
            print("\t file not exist!")
            return False

        self.reset()

        print("[INFO][ChannelPointCloud::loadData]")
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

            new_point = ChannelPoint()
            new_point.setChannelValueList(channel_name_list, channel_value_list)
            self.channel_point_list.append(new_point)
            loaded_point_num += 1

            if loaded_point_num == point_num:
                break
        print("[INFO][ChannelPointCloud::loadData]")
        print("\t loaded", loaded_point_num, "points from poitncloud!")

        self.updateKDTree()
        return True

    def getNearestPointInfo(self, x, y, z):
        self.updateKDTree()

        if self.kd_tree is None:
            return None, None
        if len(self.channel_point_list) == 0:
            return None, None
        nearest_dist, nearest_point_idx = self.kd_tree.query([x, y, z])
        return nearest_dist, nearest_point_idx

    def getNearestDist(self, x, y, z):
        self.updateKDTree()

        if self.kd_tree is None:
            return None
        if len(self.channel_point_list) == 0:
            return None
        nearest_dist, _ = self.kd_tree.query([x, y, z])
        return nearest_dist

    def getSelfNearestDist(self, point_idx):
        self.updateKDTree()

        if self.kd_tree is None:
            return None
        if len(self.channel_point_list) == 0:
            return None
        if point_idx >= len(self.channel_point_list):
            return None
        xyz = self.channel_point_list[point_idx].getChannelValueList(["x", "y", "z"])
        if None in xyz:
            return None
        nearest_dist_list, _ = self.kd_tree.query([xyz[0], xyz[1], xyz[2]], 2)
        return nearest_dist_list[1]

    def getNearestPoint(self, x, y, z):
        _, nearest_point_idx = self.getNearestPointInfo(x, y, z)
        if nearest_point_idx is None:
            return None
        return self.channel_point_list[nearest_point_idx]

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
        pointcloud_size = len(self.channel_point_list)
        target_pointcloud_size = len(target_pointcloud.channel_point_list)
        if target_pointcloud_size == 0:
            print("[ERROR][ChannelPointCloud::copyChannelValue]")
            print("\t target pointcloud is empty!")
            return False

        if pointcloud_size > 0 and pointcloud_size != target_pointcloud_size:
            print("[ERROR][ChannelPointCloud::copyChannelValue]")
            print("\t pointcloud size not matched!")
            return False

        first_point_channel_value_list = \
            target_pointcloud.channel_point_list[0].getChannelValueList(channel_name_list)
        if None in first_point_channel_value_list:
            print("[ERROR][ChannelPointCloud::copyChannelValue]")
            print("\t target_pointcloud doesn't have all channels needed!")
            return False

        print("[INFO][ChannelPointCloud::copyChannelValue]")
        print("\t start copy channel value :")
        print("\t channel_name_list = [", end="")
        for channel_name in channel_name_list:
            print(" " + channel_name, end="")
        print(" ]...")
        channel_list_value_list = \
            target_pointcloud.getChannelListValueList(channel_name_list)

        if pointcloud_size == 0:
            for channel_value_list in tqdm(channel_list_value_list):
                new_point = ChannelPoint()
                new_point.setChannelValueList(channel_name_list, channel_value_list)
                self.channel_point_list.append(new_point)

            self.updateKDTree()
            return True

        for i in tqdm(pointcloud_size):
            channel_value_list = channel_list_value_list[i]
            self.channel_point_list[i].setChannelValueList(channel_name_list, channel_value_list)

        self.updateKDTree()
        return True

    def setChannelValueByKDTree(self, target_pointcloud, channel_name_list):
        self.updateKDTree()

        if len(self.channel_point_list) == 0:
            return True

        if len(target_pointcloud.channel_point_list) == 0:
            print("[ERROR][ChannelPointCloud::setChannelValueByKDTree]")
            print("\t target pointcloud is empty!")
            return False

        first_point_xyz = self.channel_point_list[0].getChannelValueList(["x", "y", "z"])
        if None in first_point_xyz:
            print("[ERROR][ChannelPointCloud::setChannelValueByKDTree]")
            print("\t pointcloud xyz not found!")
            return False

        first_point_channel_value_list = \
            target_pointcloud.getNearestChannelValueListValue(
                first_point_xyz[0],
                first_point_xyz[1],
                first_point_xyz[2],
                channel_name_list)
        if None in first_point_channel_value_list:
            print("[ERROR][ChannelPointCloud::setChannelValueByKDTree]")
            print("\t target_pointcloud doesn't have all channels needed!")
            return False

        print("[INFO][ChannelPointCloud::setChannelValueByKDTree]")
        print("\t start set channel value by KDTree :")
        print("\t channel_name_list = [", end="")
        for channel_name in channel_name_list:
            print(" " + channel_name, end="")
        print(" ]...")
        for channel_point in tqdm(self.channel_point_list):
            xyz = channel_point.getChannelValueList(["x", "y", "z"])
            channel_value_list = \
                target_pointcloud.getNearestChannelValueListValue(xyz[0],
                                                                  xyz[1],
                                                                  xyz[2],
                                                                  channel_name_list)
            channel_point.setChannelValueList(channel_name_list, channel_value_list)
        return True

    def removeOutlierPoints(self, outlier_dist_max):
        self.updateKDTree()

        if self.kd_tree is None:
            print("[ERROR][ChannelPointCloud::removeOutlierPoints]")
            print("\t kd_tree is None!")
            return False

        if outlier_dist_max == 0:
            print("[ERROR][ChannelPointCloud::removeOutlierPoints]")
            print("\t outlier_dist_max is 0!")
            return False

        print("[INFO][ChannelPointCloud::removeOutlierPoints]")
        print("\t start remove outerlier points with outlier_dist_max = " + str(outlier_dist_max) + "...")
        remove_point_idx_list = []
        for i in tqdm(range(len(self.channel_point_list))):
            current_nearest_dist = self.getSelfNearestDist(i)
            if current_nearest_dist > outlier_dist_max:
                remove_point_idx_list.append(i)
        if len(remove_point_idx_list) == 0:
            return True
        for i in range(len(remove_point_idx_list)):
            self.channel_point_list.pop(remove_point_idx_list[i] - i)
        print("[INFO][ChannelPointCloud::removeOutlierPoints]")
        print("\t removed " + str(len(remove_point_idx_list)) + " points...")
        return True

    def paintByLabel(self, label_channel_name, color_map):
        if len(self.channel_point_list) == 0:
            return True

        first_point_label_value = self.channel_point_list[0].getChannelValue(label_channel_name)

        if first_point_label_value is None:
            print("[ERROR][ChannelPointCloud::paintByLabel]")
            print("\t label_channel not found!")
            return False

        color_map_size = len(color_map)

        if color_map_size == 0:
            print("[ERROR][ChannelPointCloud::paintByLabel]")
            print("\t color_map is empty!")
            return False

        print("[INFO][ChannelPointCloud::paintByLabel]")
        print("\t start paint by label...")
        for channel_point in tqdm(self.channel_point_list):
            label_value = channel_point.getChannelValue(label_channel_name)
            rgb = color_map[label_value % color_map_size]
            channel_point.setChannelValueList(["r", "g", "b"], rgb)
        return True

    def getPCDHeader(self):
        channel_list = []

        point_num = len(self.channel_point_list)
        if point_num > 0:
            channel_list = self.channel_point_list[0].channel_list

        pcd_header = "# .PCD v0.7 - Point Cloud Data file format\n"
        pcd_header += "VERSION 0.7\n"

        pcd_header += "FIELDS"
        for channel in channel_list:
            if channel.name in self.save_ignore_channel_name_list:
                continue
            pcd_header += " " + channel.name
        pcd_header += "\n"

        pcd_header += "SIZE"
        for channel in channel_list:
            if channel.name in self.save_ignore_channel_name_list:
                continue
            pcd_header += " " + str(channel.size)
        pcd_header += "\n"

        pcd_header += "TYPE"
        for channel in channel_list:
            if channel.name in self.save_ignore_channel_name_list:
                continue
            pcd_header += " " + channel.type
        pcd_header += "\n"

        pcd_header += "COUNT"
        for channel in channel_list:
            if channel.name in self.save_ignore_channel_name_list:
                continue
            pcd_header += " " + str(channel.count)
        pcd_header += "\n"

        pcd_header += "WIDTH " + str(point_num) + "\n"

        pcd_header += "HEIGHT 1\n"
        pcd_header += "VIEWPOINT 0 0 0 1 0 0 0\n"

        pcd_header += "POINTS " + str(point_num) + "\n"

        pcd_header += "DATA ascii\n"
        return pcd_header

    def savePointCloud(self, save_pointcloud_file_path):
        print("[INFO][ChannelPointCloud::savePointCloud]")
        print("\t start save pointcloud to" + save_pointcloud_file_path + "...")
        with open(save_pointcloud_file_path, "w") as f:
            pcd_header = self.getPCDHeader()
            f.write(pcd_header)
            for channel_point in tqdm(self.channel_point_list):
                last_channel_idx = len(channel_point.channel_list) - 1
                for i in range(last_channel_idx + 1):
                    if channel_point.channel_list[i].name in self.save_ignore_channel_name_list:
                        if i == last_channel_idx:
                               f.write("\n")
                        continue
                    f.write(str(channel_point.channel_list[i].value))
                    if i < last_channel_idx:
                        f.write(" ")
                    else:
                        f.write("\n")
        return True

    def outputInfo(self, info_level=0):
        line_start = "\t" * info_level
        print(line_start + "[ChannelPointCloud]")
        for channel_point in self.channel_point_list:
            channel_point.outputInfo(info_level + 1)
        return True

