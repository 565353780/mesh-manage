#!/usr/bin/env python
# -*- coding: utf-8 -*-

import open3d as o3d

input_pointcloud_file_path = "./test1.pcd"
output_pointcloud_file_path = "./test1.ply"

pointcloud = o3d.io.read_point_cloud(input_pointcloud_file_path, print_progress=True)

o3d.io.write_point_cloud(
    output_pointcloud_file_path,
    pointcloud,
    write_ascii=True,
    print_progress=True)

