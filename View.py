#!/usr/bin/env python
# -*- coding: utf-8 -*-

import open3d as o3d

class PointCloudView:
    def __init__(self):
        self.pointcloud_file_path = None

        self.pointcloud = None
        return

    def loadPointCloud(self, pointcloud_file_path):
        self.pointcloud_file_path = pointcloud_file_path

        self.pointcloud = o3d.io.read_point_cloud(
            self.pointcloud_file_path, print_progress=True)
        return True

    def view(self):
        o3d.visualization.draw_geometries([self.pointcloud])
        return True

if __name__ == "__main__":
    pointcloud_file_path = "./masked_pc/RUN_LOG/2022_1_16_16-35-51/scene_68.pcd"

    pointcloud_view = PointCloudView()

    pointcloud_view.loadPointCloud(pointcloud_file_path)

    pointcloud_view.view()

