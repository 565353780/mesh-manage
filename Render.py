#!/usr/bin/env python
# -*- coding: utf-8 -*-

import numpy as np
import open3d as o3d

class PointCloudRender:
    def __init__(self):
        self.d3_40_colors_rgb = np.array(
            [
                [164, 218, 252], [120, 173, 219], [253, 147, 81], [252, 234, 163], [0, 128, 128],
                [132, 220, 198], [255, 104, 107], [255, 166, 158], [148, 103, 189], [189, 147, 189],
                [140, 86, 75], [146, 94, 120], [227, 119, 194], [247, 182, 210], [127, 127, 127],
                [199, 199, 199], [188, 189, 34], [219, 219, 141], [23, 190, 207], [158, 218, 229],
                [57, 59, 121], [82, 84, 163], [107, 110, 207], [156, 158, 222], [99, 121, 57],
                [140, 162, 82], [181, 207, 107], [206, 219, 156], [140, 109, 49], [189, 158, 57],
                [231, 186, 82], [231, 203, 148], [132, 60, 57], [173, 73, 74], [214, 97, 107],
                [231, 150, 156], [123, 65, 115], [165, 81, 148], [206, 109, 189], [222, 158, 214],
            ],
            dtype=np.uint8,
        )

        self.pointcloud_file_path = None

        self.pointcloud = None
        return

    def loadPointCloud(self,
                       pointcloud_file_path):
        self.pointcloud_file_path = pointcloud_file_path

        self.pointcloud = o3d.io.read_point_cloud(self.pointcloud_file_path)

    def render(self):
        pointcloud_colors = o3d.utility.Vector3dVector((self.d3_40_colors_rgb(original_point_cloud[:, 3]) / 255.0))
        print(pointcloud_colors.shape)
        return True

if __name__ == "__main__":
    pointcloud_file_path = "./masked_pc/front_3d/01.pcd"

    pointcloud_render = PointCloudRender()
    pointcloud_render.loadPointCloud(pointcloud_file_path)
    pointcloud_render.render()

