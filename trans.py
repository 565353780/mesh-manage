#!/usr/bin/env python
# -*- coding: utf-8 -*-

from Method.trans_format import transFormat

# Param
source_pointcloud_file_path = \
    "/home/chli/cad_ws/build/pcl_catkin/pcl_src-prefix/src/pcl_src/test/2d/canny.pcd"
target_pointcloud_file_path = \
    "/home/chli/cad_ws/build/pcl_catkin/pcl_src-prefix/src/pcl_src/test/2d/canny.ply"

# Process
transFormat(source_pointcloud_file_path, target_pointcloud_file_path)
transFormat(source_pointcloud_file_path, source_pointcloud_file_path)

