#!/usr/bin/env python
# -*- coding: utf-8 -*-

from Method.down_sample import downSample

# Param
pointcloud_file_path = "./masked_pc/home/home_cut.pcd"
down_sample_cluster_num = 8

# Process
save_pointcloud_file_path = pointcloud_file_path[:-4] + "_downSampled_" + str(down_sample_cluster_num) + ".pcd"
downSample(pointcloud_file_path, down_sample_cluster_num, save_pointcloud_file_path)

