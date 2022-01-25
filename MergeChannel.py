#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
from tqdm import tqdm
from scipy.spatial import KDTree

from channel_pointcloud import ChannelPoint, ChannelPointCloud

class MergeChannel:
    def __init__(self):
        self.rgb_pointcloud = ChannelPointCloud()
        self.kd_tree = None
        self.pointcloud_list = []
        self.merge_channel_name_list = []
        self.merge_channel_in_pointcloud_idx_list = []
        self.merge_pointcloud_valid = True
        return

    def reset(self):
        self.rgb_pointcloud.reset()
        self.kd_tree = None
        self.pointcloud_list.clear()
        self.merge_channel_name_list.clear()
        self.merge_channel_in_pointcloud_idx_list.clear()
        self.merge_pointcloud_valid = True
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

        if not pointcloud.loadData(pointcloud_file_path,
                                   channel_name_list,
                                   channel_idx_list):
            print("MergeChannel::loadPointCloud :")
            print("loadData failed!")
            return None
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

    merged_pointcloud.savePointCloud(merged_pointcloud_file_path)
    return True

if __name__ == "__main__":
    demo()

