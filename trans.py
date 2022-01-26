#!/usr/bin/env python
# -*- coding: utf-8 -*-

from PointCloudClass.trans_format import transToPLY

# Param
source_pointcloud_file_path = "./masked_pc/office/office_cut.pcd"

estimate_normals_radius = 0.05
estimate_normals_max_nn = 30

# Process
transToPLY(source_pointcloud_file_path, estimate_normals_radius, estimate_normals_max_nn)

