#!/usr/bin/env python
# -*- coding: utf-8 -*-

from mesh_manage.Method.trans import transFormat

# Param
source_pointcloud_file_path = \
    "/home/chli/.ros/RUN_LOG/PointCloud2ToObjectVecConverterServer/2022_9_4_19-32-7_coscan/scene_19.pcd"
target_pointcloud_file_path = \
    "/home/chli/.ros/RUN_LOG/PointCloud2ToObjectVecConverterServer/2022_9_4_19-32-7_coscan/scene_19.ply"

# Process
transFormat(source_pointcloud_file_path,
            target_pointcloud_file_path,
            True)

