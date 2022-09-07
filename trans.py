#!/usr/bin/env python
# -*- coding: utf-8 -*-

from mesh_manage.Method.trans import transFormat

# Param
source_pointcloud_file_path = \
    "/home/chli/chLi/coscan_data/scene_result/matterport3d_05/coscan/2022_9_7_19-3-4_mp3d05_coscan/scene_33.pcd"
target_pointcloud_file_path = \
    "/home/chli/chLi/coscan_data/scene_result/matterport3d_05/coscan/scene_33.ply"

# Process
transFormat(source_pointcloud_file_path,
            target_pointcloud_file_path,
            True)

