#!/usr/bin/env python
# -*- coding: utf-8 -*-

from Method.trans_format import transFormat

# Param
source_pointcloud_file_path = \
    "/home/chli/chLi/OBJs/OpenGL/bunny_1.ply"
target_pointcloud_file_path = \
    "/home/chli/chLi/OBJs/OpenGL/bunny_1.pcd"

# Process
transFormat(source_pointcloud_file_path, target_pointcloud_file_path)
#  transFormat(source_pointcloud_file_path, source_pointcloud_file_path)

