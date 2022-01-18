#!/usr/bin/env python
# -*- coding: utf-8 -*-

import numpy as np
from tqdm import tqdm
import open3d as o3d

class PointCloudCut:
    def __init__(self):
        self.pointcloud_file_path = None
        self.labeled_pointcloud_file_path = None
        self.label_channel_idx = None
        self.cut_labels = None

        self.pointcloud = None
        self.labeled_pointcloud = None
        return

    def loadPointCloud(self,
                       pointcloud_file_path,
                       labeled_pointcloud_file_path,
                       label_channel_idx,
                       cut_labels):
        self.pointcloud_file_path = pointcloud_file_path
        self.labeled_pointcloud_file_path = labeled_pointcloud_file_path
        self.label_channel_idx = label_channel_idx
        self.cut_labels = cut_labels

        print("start loading pointcloud...", end="")
        self.pointcloud = o3d.io.read_point_cloud(
            self.pointcloud_file_path, print_progress=True)
        print("SUCCESS!")

        print("start loading labeled pointcloud...", end="")
        self.labeled_pointcloud = o3d.io.read_point_cloud(
            self.labeled_pointcloud_file_path, print_progress=True)
        print("SUCCESS!")
        return True

    def cut(self):
        print("start reading labels...")
        lines = None
        with open(self.labeled_pointcloud_file_path, "r") as f:
            lines = f.readlines()

        label_list = []
        find_start_line = False
        for line in tqdm(lines):
            if "DATA ascii" in line:
                find_start_line = True
                continue
            if not find_start_line:
                continue
            line_data = line.split("\n")[0].split(" ")
            if len(line_data) < 5:
                continue
            label_list.append(int(line_data[self.label_channel_idx]))

        print("start read points in pointcloud...", end="")
        points = np.asarray(self.pointcloud.points).tolist()
        if len(points) != len(label_list):
            print("PointCloudCut::cut : label size not matched!")
            return False
        print("SUCCESS!")

        print("start read colors in pointcloud...", end="")
        colors = np.asarray(self.pointcloud.colors).tolist()
        print("SUCCESS!")

        show_points = []
        show_colors = []

        print("start cutting pointcloud...")
        cut_point_num = 0
        for i in tqdm(range(len(points))):
            label = label_list[i]
            if label in self.cut_labels:
                cut_point_num += 1
                continue

            show_points.append(points[i])
            show_colors.append(colors[i])

        cutted_pointcloud = o3d.geometry.PointCloud()
        cutted_pointcloud.points = o3d.utility.Vector3dVector(np.array(show_points))
        cutted_pointcloud.colors = o3d.utility.Vector3dVector(np.array(show_colors))

        o3d.visualization.draw_geometries([cutted_pointcloud])
        return True

if __name__ == "__main__":
    pointcloud_file_path = "./masked_pc/home/home_DownSample_32.pcd"
    labeled_pointcloud_file_path = "./masked_pc/home/home_DownSample_32_cut.pcd"
    label_channel_idx = 4
    cut_labels = [1]

    pointcloud_cut = PointCloudCut()
    pointcloud_cut.loadPointCloud(pointcloud_file_path,
                                  labeled_pointcloud_file_path,
                                  label_channel_idx,
                                  cut_labels)
    pointcloud_cut.cut()

