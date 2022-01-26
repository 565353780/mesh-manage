#!/usr/bin/env python
# -*- coding: utf-8 -*-

from PointCloudClass.channel_pointcloud import ChannelPointCloud

xyz_pointcloud_file_path = "./masked_pc/home/home_cut.pcd"
xyz_pointcloud_channel_name_list = ["x", "y", "z"]
xyz_pointcloud_channel_idx_list = [0, 1, 2]

label_pointcloud_file_path = "./masked_pc/home/home_DownSample_8_masked.pcd"
label_pointcloud_channel_name_list = ["x", "y", "z", "label"]
label_pointcloud_channel_idx_list = [0, 1, 2, 4]

xyz_pointcloud = ChannelPointCloud()
xyz_pointcloud.loadData(xyz_pointcloud_file_path,
                        xyz_pointcloud_channel_name_list,
                        xyz_pointcloud_channel_idx_list)

label_pointcloud = ChannelPointCloud()
label_pointcloud.loadData(label_pointcloud_file_path,
                          label_pointcloud_channel_name_list,
                          label_pointcloud_channel_idx_list)

merge_pointcloud = ChannelPointCloud()
merge_pointcloud.copyChannelValue(xyz_pointcloud, ["x", "y", "z"])
merge_pointcloud.setChannelValueByKDTree(label_pointcloud, ["label"])
merge_pointcloud.removeOutlierPoints(0.05)
merge_pointcloud.savePointCloud(xyz_pointcloud_file_path[:-4] + "_merged.pcd")

