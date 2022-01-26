#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
from scipy.spatial.kdtree import KDTree
from tqdm import tqdm

from PointCloudClass.channel_point import ChannelPoint

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
            print("[ERROR][ChannelPointCloud::loadData]")
            print("\t file not exist!")
            return False

        self.reset()

        print("[INFO][ChannelPointCloud::loadData]")
        print("\t start load pointcloud :")
        print("\t pointcloud_file_path = " + pointcloud_file_path)
        print("\t channel_name_list = [", end="")
        for channel_name in channel_name_list:
            print(" " + channel_name, end="")
        print(" ]...")
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
        print("[INFO][ChannelPointCloud::loadData]")
        print("\t loaded", loaded_point_num, "points from poitncloud!")
        self.updateKDTree()
        return True

    def getNearestPointInfo(self, x, y, z):
        if self.kd_tree is None:
            return None, None
        if len(self.point_list) == 0:
            return None, None
        nearest_dist, nearest_point_idx = self.kd_tree.query([x, y, z])
        return nearest_dist, nearest_point_idx

    def getNearestDist(self, x, y, z):
        nearest_dist, _ = self.kd_tree.query([x, y, z])
        return nearest_dist

    def getSelfNearestDist(self, point_idx):
        if self.kd_tree is None:
            return None
        if len(self.point_list) == 0:
            return None
        if point_idx >= len(self.point_list):
            return None
        xyz = self.point_list[point_idx].getChannelValueList(["x", "y", "z"])
        if None in xyz:
            return None
        nearest_dist_list, _ = self.kd_tree.query([xyz[0], xyz[1], xyz[2]], 2)
        return nearest_dist_list[1]

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
            print("[ERROR][ChannelPointCloud::copyChannelValue]")
            print("\t target pointcloud is empty!")
            return False

        if pointcloud_size > 0 and pointcloud_size != target_pointcloud_size:
            print("[ERROR][ChannelPointCloud::copyChannelValue]")
            print("\t pointcloud size not matched!")
            return False

        first_point_channel_value_list = \
            target_pointcloud.point_list[0].getChannelValueList(channel_name_list)
        if None in first_point_channel_value_list:
            print("[ERROR][ChannelPointCloud::copyChannelValue]")
            print("\t target_pointcloud doesn't have all channels needed!")
            return False

        print("[INFO][ChannelPointCloud::copyChannelValue]")
        print("\t start copy channel value...")
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
            print("[ERROR][ChannelPointCloud::setChannelValueByKDTree]")
            print("\t target pointcloud is empty!")
            return False

        first_point_xyz = self.point_list[0].getChannelValueList(["x", "y", "z"])
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
        print("\t start set channel value by KDTree...")
        for point in tqdm(self.point_list):
            xyz = point.getChannelValueList(["x", "y", "z"])
            channel_value_list = \
                target_pointcloud.getNearestChannelValueListValue(xyz[0],
                                                                  xyz[1],
                                                                  xyz[2],
                                                                  channel_name_list)
            point.setChannelValueList(channel_name_list, channel_value_list)
        return True

    def removeOutlierPoints(self, dist_max):
        if dist_max == 0:
            self.reset()
            return True

        print("[INFO][ChannelPointCloud::removeOutlierPoints]")
        print("\t start remove outerlier points with dist_max = " + str(dist_max) + "...")
        remove_point_idx_list = []
        for i in tqdm(range(len(self.point_list))):
            current_nearest_dist = self.getSelfNearestDist(i)
            if current_nearest_dist > dist_max:
                remove_point_idx_list.append(i)
        if len(remove_point_idx_list) == 0:
            return True
        for i in range(len(remove_point_idx_list)):
            self.point_list.pop(remove_point_idx_list[i] - i)
        print("[INFO][ChannelPointCloud::removeOutlierPoints]")
        print("\t removed " + str(len(remove_point_idx_list)) + " points...")
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
        print("[INFO][ChannelPointCloud::savePointCloud]")
        print("\t start save pointcloud to" + save_pointcloud_file_path + "...")
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
        print(line_start + "[ChannelPointCloud]")
        for point in self.point_list:
            point.outputInfo(info_level + 1)
        return True

def demo():
    source_pointcloud = ChannelPointCloud()

    source_pointcloud.loadData("./masked_pc/test.pcd",
                               ["x", "y", "z", "rgb", "instance_label"],
                               [0, 1, 2, 6, 7])

    label_pointcloud = ChannelPointCloud()
    label_pointcloud.loadData("./masked_pc/home/home_DownSample_8_masked.pcd",
                              ["x", "y", "z", "instance_label"],
                              [0, 1, 2, 4])

    #  merge_pointcloud = ChannelPointCloud()

    #  merge_pointcloud.copyChannelValue(source_pointcloud, ["x", "y", "z", "r", "g", "b"])
    #  merge_pointcloud.setChannelValueByKDTree(label_pointcloud, ["instance_label"])
    source_pointcloud.removeOutlierPoints(0.05)

    source_pointcloud.savePointCloud("./test1.pcd")
    return True

if __name__ == "__main__":
    demo()

