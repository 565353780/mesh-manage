#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os

from Config.color import d3_40_colors_rgb

from Module.channel_pointcloud import ChannelPointCloud

class PointCloudPainter(object):
    def __init__(self):
        self.channel_pointcloud_dict = {}
        self.merge_channel_pointcloud = ChannelPointCloud()
        return

    def reset(self):
        self.channel_pointcloud_dict = {}
        self.merge_channel_pointcloud = ChannelPointCloud()
        return True

    def addChannelPointCloud(self, pointcloud_file_path, pointcloud_name):
        if not os.path.exists(pointcloud_file_path):
            print("[WARN][PointCloudPainter::addChannelPointCloud]")
            print("\t pointcloud_file not exist!")
            return False

        if pointcloud_name in self.channel_pointcloud_dict.keys():
            print("[ERROR][PointCloudPainter::addChannelPointCloud]")
            print("\t pointcloud_name already exist!")
            return False

        channel_pointcloud = ChannelPointCloud(pointcloud_file_path)
        self.channel_pointcloud_dict[pointcloud_name] = channel_pointcloud
        return True

    def loadPointCloudFilePathDict(self, pointcloud_file_path_dict):
        for pointcloud_name, pointcloud_file_path in pointcloud_file_path_dict:
            if not self.addChannelPointCloud(pointcloud_file_path, pointcloud_name):
                print("[ERROR][PointCloudPainter::loadPointCloudFilePathDict]")
                print("\t addChannelPointCloud failed!")
                return False
        return True

    def mergeChannelPointCloud(self, merge_pointcloud_dict):
        self.merge_channel_pointcloud = ChannelPointCloud()

        if len(merge_pointcloud_dict.keys()) == 0:
            return True

        source_pointcloud_name = merge_pointcloud_dict["source_name"]
        if source_pointcloud_name not in self.channel_pointcloud_dict.keys():
            print("[ERROR][PointCloudPainter::mergeChannelPointCloud]")
            print("\t source_pointcloud", source_pointcloud_name, "not found!")
            return False

        self.merge_channel_pointcloud.copyChannelValue(
            self.channel_pointcloud_dict[source_pointcloud_name],
            merge_pointcloud_dict["source_channel_list"])

        for merge_pointcloud_name, merge_channel_name_list in merge_pointcloud_dict["merge"]:
            if merge_pointcloud_name not in self.channel_pointcloud_dict.keys():
                print("[ERROR][PointCloudPainter::mergeChannelPointCloud]")
                print("\t merge_pointcloud_name", merge_pointcloud_name, "not found!")
                return False
            self.merge_channel_pointcloud.setChannelValueByKDTree(
                self.channel_pointcloud_dict[merge_pointcloud_name],
                merge_channel_name_list)
        return True

    def removeOutlierPoints(self, outlier_dist_max):
        self.merge_channel_pointcloud.removeOutlierPoints(outlier_dist_max)
        return True

    def paintColor(self, paint_channel_name, color_list):
        self.merge_channel_pointcloud.paintByLabel(paint_channel_name, color_list)
        return True

    def savePaintedPointCloud(self, save_file_path):
        self.merge_channel_pointcloud.savePointCloud(save_file_path)
        return True

def demo_merge():
    pointcloud_file_path_dict = {
        "xyz": "./masked_pc/office/office_cut.ply",
        "label": "./masked_pc/office/office_DownSample_8_masked.pcd",
    }
    merge_pointcloud_dict = {
        "source_name": "xyz",
        "source_channel_list": ["x", "y", "z"],
        "merge": {
            "label": ["label"],
        }
    }
    outlier_dist_max = 0.05
    save_file_path = "./masked_pc/office/office_cut_merged.ply"

    pointcloud_painter = PointCloudPainter()
    pointcloud_painter.loadPointCloudFilePathDict(pointcloud_file_path_dict)
    pointcloud_painter.mergeChannelPointCloud(merge_pointcloud_dict)
    pointcloud_painter.removeOutlierPoints(outlier_dist_max)
    pointcloud_painter.savePaintedPointCloud(save_file_path)
    return True

def demo_paint():
    pointcloud_file_path_dict = {
        "xyz": "./masked_pc/front_3d/04_masked.pcd",
    }
    paint_channel_name = "label"
    save_file_path = "./masked_pc/front_3d/04_masked_painted.ply"

    pointcloud_painter = PointCloudPainter()
    pointcloud_painter.loadPointCloudFilePathDict(pointcloud_file_path_dict)
    pointcloud_painter.paintColor(paint_channel_name, d3_40_colors_rgb)
    pointcloud_painter.savePaintedPointCloud(save_file_path)
    return True

def demo_auto_paint():
    pointcloud_file_path_dict = {
        "xyz": "./masked_pc/office/office_cut.ply",
        "label": "./masked_pc/office/office_DownSample_8_masked.pcd",
    }
    merge_pointcloud_dict = {
        "source_name": "xyz",
        "source_channel_list": ["x", "y", "z"],
        "merge": {
            "label": ["label"],
        }
    }
    outlier_dist_max = 0.05
    paint_channel_name = "label"
    save_file_path = "./masked_pc/office/office_cut_painted.ply"

    pointcloud_painter = PointCloudPainter()
    pointcloud_painter.loadPointCloudFilePathDict(pointcloud_file_path_dict)
    pointcloud_painter.mergeChannelPointCloud(merge_pointcloud_dict)
    pointcloud_painter.removeOutlierPoints(outlier_dist_max)
    pointcloud_painter.paintColor(paint_channel_name, d3_40_colors_rgb)
    pointcloud_painter.savePaintedPointCloud(save_file_path)
    return True

