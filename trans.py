#!/usr/bin/env python
# -*- coding: utf-8 -*-

from Method.trans_format import transToPLY

# Param
source_pointcloud_file_path = \
    "/home/chli/cad_ws/build/pcl_catkin/pcl_src-prefix/src/pcl_src/test/2d/canny.pcd"

estimate_normals_radius = 0.05
estimate_normals_max_nn = 30

# Process
transToPLY(source_pointcloud_file_path, estimate_normals_radius, estimate_normals_max_nn)

