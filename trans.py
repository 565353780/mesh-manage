#!/usr/bin/env python
# -*- coding: utf-8 -*-

from Method.trans_format import transFormat

# Param
source_pointcloud_file_path = \
    "/home/chli/cad_ws/build/pcl_catkin/pcl_src-prefix/src/pcl_src/test/2d/canny.pcd"
target_pointcloud_file_path = \
    "/home/chli/cad_ws/build/pcl_catkin/pcl_src-prefix/src/pcl_src/test/2d/canny.ply"
need_estimate_normals = True
estimate_normals_radius = 0.05
estimate_normals_max_nn = 30

# Process
transFormat(source_pointcloud_file_path, target_pointcloud_file_path,
            True, estimate_normals_radius, estimate_normals_max_nn)

transFormat(source_pointcloud_file_path, source_pointcloud_file_path,
            True, estimate_normals_radius, estimate_normals_max_nn)

