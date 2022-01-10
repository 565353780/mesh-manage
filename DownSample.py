#!/usr/bin/env python
# -*- coding: utf-8 -*-

import open3d as o3d

class PointCloudDownSample:
    def __init__(self):
        self.pointcloud_file_path = None
        self.output_format = None
        self.down_sample_multiply = None
        self.down_sample_level_max = None

        self.pointcloud_folder_path = None
        self.pointcloud_file_basename = None
        self.source_pointcloud = None
        return

    def loadPointCloud(self,
                       pointcloud_file_path,
                       output_format,
                       down_sample_multiply,
                       down_sample_level_max):
        self.pointcloud_file_path = pointcloud_file_path
        self.output_format = output_format
        self.down_sample_multiply = down_sample_multiply
        self.down_sample_level_max = down_sample_level_max

        pointcloud_file_path_split = self.pointcloud_file_path.split("/")
        pointcloud_file_name = pointcloud_file_path_split[len(pointcloud_file_path_split) - 1]
        self.pointcloud_file_basename = pointcloud_file_name.split(".")[0]
        self.pointcloud_folder_path = self.pointcloud_file_path.split(pointcloud_file_name)[0]

        print("start reading pointcloud...", end="")
        self.source_pointcloud = o3d.io.read_point_cloud(self.pointcloud_file_path)
        print("SUCCESS!")
        return True

    def downSample(self, down_sample_cluster_num):
        down_sampled_pointcloud_file_path = \
            self.pointcloud_folder_path + \
            self.pointcloud_file_basename + "_DownSample_" + str(down_sample_cluster_num) + \
            "." + self.output_format

        print("start down sampling pointcloud, level = " + str(down_sample_cluster_num) + "...", end="")
        down_sampled_pointcloud = o3d.geometry.PointCloud.uniform_down_sample(
            self.source_pointcloud, down_sample_cluster_num)

        o3d.io.write_point_cloud(down_sampled_pointcloud_file_path, down_sampled_pointcloud)
        print("SUCCESS!")
        return True

    def generateDownSampledPointCloud(self):
        down_sample_cluster_num = self.down_sample_multiply

        for i in range(self.down_sample_level_max):
            self.downSample(down_sample_cluster_num)
            down_sample_cluster_num *= self.down_sample_multiply
        return True

if __name__ == "__main__":
    pointcloud_file_path = "./masked_pc/office/office.ply"
    output_format = "pcd"
    down_sample_multiply = 2
    down_sample_level_max = 5

    pointcloud_down_sample = PointCloudDownSample()
    pointcloud_down_sample.loadPointCloud(pointcloud_file_path,
                                          output_format,
                                          down_sample_multiply,
                                          down_sample_level_max)
    pointcloud_down_sample.generateDownSampledPointCloud()

