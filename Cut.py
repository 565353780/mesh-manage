#!/usr/bin/env python
# -*- coding: utf-8 -*-

import open3d as o3d

class PointCloudCut:
    def __init__(self):
        return

    def loadPointCloud(self, pointcloud_file_path):
        return True

if __name__ == "__main__":
    pointcloud_file_path = "./masked_pc/home/home.ply"

    pointcloud_cut = PointCloudCut()
    pointcloud_cut.loadPointCloud(pointcloud_file_path)

