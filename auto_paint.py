#!/usr/bin/env python
# -*- coding: utf-8 -*-

from Config.color import d3_40_colors_rgb

from Data.channel_pointcloud import ChannelPointCloud

from Method.trans import transToPLY

# Param
xyz_pointcloud_file_path = "./masked_pc/office/office_cut.ply"

label_pointcloud_file_path = "./masked_pc/office/office_DownSample_8_masked.pcd"
label_channel_name = "label"

outlier_dist_max = 0.05
estimate_normals_radius = 0.05
estimate_normals_max_nn = 30

# Process
painted_pointcloud_file_path = xyz_pointcloud_file_path[:-4] + "_painted.pcd"

xyz_pointcloud = ChannelPointCloud()
xyz_pointcloud.loadData(xyz_pointcloud_file_path)

label_pointcloud = ChannelPointCloud()
label_pointcloud.loadData(label_pointcloud_file_path)

merge_pointcloud = ChannelPointCloud()
merge_pointcloud.copyChannelValue(xyz_pointcloud, ["x", "y", "z"])
merge_pointcloud.setChannelValueByKDTree(label_pointcloud, ["label"])
merge_pointcloud.removeOutlierPoints(outlier_dist_max)
merge_pointcloud.paintByLabel(label_channel_name, d3_40_colors_rgb)
merge_pointcloud.savePointCloud(painted_pointcloud_file_path)

transToPLY(painted_pointcloud_file_path, estimate_normals_radius, estimate_normals_max_nn)

