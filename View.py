#!/usr/bin/env python
# -*- coding: utf-8 -*-

import open3d as o3d

pointcloud_file_path = "./masked_pc/home.ply"

pointcloud = o3d.io.read_point_cloud(pointcloud_file_path)

o3d.visualization.draw_geometries([pointcloud])

