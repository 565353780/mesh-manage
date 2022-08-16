#!/usr/bin/env python
# -*- coding: utf-8 -*-

from Data.channel_pointcloud import ChannelPointCloud
from Method.trans import transFormat

# Param
xyz_pointcloud_file_path = "./masked_pc/home/home_cut.pcd"
label_pointcloud_file_path = "./masked_pc/home/home_DownSample_8_masked.pcd"

outlier_dist_max = 0.05
estimate_normals_radius = 0.05
estimate_normals_max_nn = 30

# Process
merged_pointcloud_file_path = xyz_pointcloud_file_path[:-4] + "_merged.pcd"

xyz_pointcloud = ChannelPointCloud()
xyz_pointcloud.loadData(xyz_pointcloud_file_path)

label_pointcloud = ChannelPointCloud()
label_pointcloud.loadData(label_pointcloud_file_path)

merge_pointcloud = ChannelPointCloud()
merge_pointcloud.copyChannelValue(xyz_pointcloud, ["x", "y", "z"])
merge_pointcloud.setChannelValueByKDTree(label_pointcloud, ["label"])
merge_pointcloud.removeOutlierPoints(outlier_dist_max)
merge_pointcloud.savePointCloud(merged_pointcloud_file_path)

transFormat(merged_pointcloud_file_path, merged_pointcloud_file_path[:-4] + ".ply")

