#!/usr/bin/env python
# -*- coding: utf-8 -*-

from mesh_manage.Method.trans import transFormat

# Param
source_pointcloud_file_path = \
    "/home/chli/chLi/coscan_data/scene_result/matterport3d_01/coscan/2022_9_7_15-16-21_mp3d01_coscan/scene_29.pcd"
target_pointcloud_file_path = \
    "/home/chli/chLi/coscan_data/scene_result/matterport3d_01/coscan/scene_29.ply"

# Process
transFormat(source_pointcloud_file_path,
            target_pointcloud_file_path,
            True)

