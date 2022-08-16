#!/usr/bin/env python
# -*- coding: utf-8 -*-

from Config.color import d3_40_colors_rgb

from Data.channel_pointcloud import ChannelPointCloud

from Method.trans import transToPLY

# Param
pointcloud_file_path = "./masked_pc/front_3d/04_masked.pcd"
label_channel_name = "label"

estimate_normals_radius = 0.05
estimate_normals_max_nn = 30

# Process
painted_pointcloud_file_path = pointcloud_file_path[:-4] + "_painted.pcd"

pointcloud = ChannelPointCloud()
pointcloud.loadData(pointcloud_file_path)
pointcloud.paintByLabel(label_channel_name, d3_40_colors_rgb)
pointcloud.savePointCloud(painted_pointcloud_file_path)

transToPLY(painted_pointcloud_file_path, estimate_normals_radius, estimate_normals_max_nn)

