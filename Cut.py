#!/usr/bin/env python
# -*- coding: utf-8 -*-

import numpy as np
from tqdm import tqdm
import open3d as o3d

class PointCloudCut:
    def __init__(self):
        self.pointcloud_file_path = None
        self.cut_save_range = None

        self.pointcloud = None
        return

    def loadPointCloud(self,
                       pointcloud_file_path,
                       cut_save_range):
        self.pointcloud_file_path = pointcloud_file_path
        self.cut_save_range = cut_save_range

        print("start load pointcloud...", end="")
        self.pointcloud = o3d.io.read_point_cloud(self.pointcloud_file_path)
        print("SUCCESS!")
        return True

    def cut(self):
        print("start read points in pointcloud...", end="")
        np_points = np.asarray(self.pointcloud.points)
        if np_points.shape[0] == 0:
            print("PointCloudCut::cut : pointcloud is empty!")
            return False
        point_list = np_points.tolist()
        print("SUCCESS!")

        print("start analyzing pointcloud...")
        x_min = point_list[0][0]
        x_max = x_min
        y_min = point_list[0][1]
        y_max = y_min
        z_min = point_list[0][2]
        z_max = z_min
        for point in tqdm(point_list):
            x_min = min(x_min, point[0])
            x_max = max(x_max, point[0])
            y_min = min(y_min, point[1])
            y_max = max(y_max, point[1])
            z_min = min(z_min, point[2])
            z_max = max(z_max, point[2])

        x_diff = x_max - x_min
        y_diff = y_max - y_min
        z_diff = z_max - z_min

        print("start read colors in pointcloud...", end="")
        np_colors = np.asarray(self.pointcloud.colors)
        color_list = np_colors.tolist()
        print("SUCCESS!")

        show_points = []
        show_colors = []

        print("start cutting pointcloud...")
        for i in tqdm(range(np_points.shape[0])):
            point = point_list[i]
            point_x_diff = point[0] - x_min
            point_y_diff = point[1] - y_min
            point_z_diff = point[2] - z_min

            if x_diff > 0:
                unit_x = point_x_diff / x_diff
                if unit_x < self.cut_save_range[0][0] or unit_x > self.cut_save_range[0][1]:
                    continue
            if y_diff > 0:
                unit_y = point_y_diff / y_diff
                if unit_y < self.cut_save_range[1][0] or unit_y > self.cut_save_range[1][1]:
                    continue
            if z_diff > 0:
                unit_z = point_z_diff / z_diff
                if unit_z < self.cut_save_range[2][0] or unit_z > self.cut_save_range[2][1]:
                    continue

            show_points.append(point)
            show_colors.append(color_list[i])

        cutted_pointcloud = o3d.geometry.PointCloud()
        cutted_pointcloud.points = o3d.utility.Vector3dVector(np.array(show_points))
        cutted_pointcloud.colors = o3d.utility.Vector3dVector(np.array(show_colors))

        o3d.visualization.draw_geometries([cutted_pointcloud])
        return True

if __name__ == "__main__":
    pointcloud_file_path = "./masked_pc/home/home.ply"
    cut_save_range = [[0.5, 1.0], [0, 1], [0, 1]]

    pointcloud_cut = PointCloudCut()
    pointcloud_cut.loadPointCloud(pointcloud_file_path,
                                  cut_save_range)
    pointcloud_cut.cut()

