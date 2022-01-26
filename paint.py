#!/usr/bin/env python
# -*- coding: utf-8 -*-

from tqdm import tqdm
from PointCloudClass.channel_pointcloud import ChannelPointCloud

# Param
pointcloud_file_path = "./test.pcd"
channel_name_list = ["x", "y", "z", "label"]
channel_idx_list = [0, 1, 2, 7]
label_channel_name = "label"
save_pointcloud_file_path = "./test_paint.pcd"

d3_40_colors_rgb = [
    [164, 218, 252], [120, 173, 219], [253, 147, 81], [252, 234, 163], [0, 128, 128],
    [132, 220, 198], [255, 104, 107], [255, 166, 158], [148, 103, 189], [189, 147, 189],
    [140, 86, 75], [146, 94, 120], [227, 119, 194], [247, 182, 210], [127, 127, 127],
    [199, 199, 199], [188, 189, 34], [219, 219, 141], [23, 190, 207], [158, 218, 229],
    [57, 59, 121], [82, 84, 163], [107, 110, 207], [156, 158, 222], [99, 121, 57],
    [140, 162, 82], [181, 207, 107], [206, 219, 156], [140, 109, 49], [189, 158, 57],
    [231, 186, 82], [231, 203, 148], [132, 60, 57], [173, 73, 74], [214, 97, 107],
    [231, 150, 156], [123, 65, 115], [165, 81, 148], [206, 109, 189], [222, 158, 214]]

# Process
pointcloud = ChannelPointCloud()
pointcloud.loadData(pointcloud_file_path, channel_name_list, channel_idx_list)

print("start paint pointcloud...")
for point in tqdm(pointcloud.point_list):
    label_value = point.getChannelValue(label_channel_name)
    rgb = d3_40_colors_rgb[label_value % len(d3_40_colors_rgb)]
    point.setChannelValueList(["r", "g", "b"], rgb)

pointcloud.savePointCloud(save_pointcloud_file_path)

