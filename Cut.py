#!/usr/bin/env python
# -*- coding: utf-8 -*-

import open3d as o3d

class PointCloudCut:
    def __init__(self):
        self.pointcloud_file_path = None
        self.cut_axis = None
        self.cut_range = None

        self.pointcloud = None
        return

    def loadPointCloud(self,
                       pointcloud_file_path,
                       cut_axis,
                       cut_range):
        self.pointcloud_file_path = pointcloud_file_path
        self.cut_axis = cut_axis
        self.cut_range = cut_range

        self.pointcloud = o3d.io.read_point_cloud(self.pointcloud_file_path)
        return True

    def cut(self):
        cutted_pointcloud = o3d.geometry.PointCloud()

        o3d.visualization.draw_geometries([self.pointcloud])
        return True

if __name__ == "__main__":
    pointcloud_file_path = "./masked_pc/home/home.ply"
    cut_axis = "x"
    cut_range = [0.5, 1.0]

    pointcloud_cut = PointCloudCut()
    pointcloud_cut.loadPointCloud(pointcloud_file_path,
                                  cut_axis,
                                  cut_range)
    pointcloud_cut.cut()

