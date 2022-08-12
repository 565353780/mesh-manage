#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import open3d as o3d

def transFormat(source_pointcloud_file_path,
                target_pointcloud_file_path,
                need_estimate_normals=True,
                estimate_normals_radius=0.05,
                estimate_normals_max_nn=30):
    if not os.path.exists(source_pointcloud_file_path):
        print("[ERROR][trans::transFormat]")
        print("source_file not exist!")
        return False

    pointcloud = o3d.io.read_point_cloud(source_pointcloud_file_path, print_progress=True)
    if need_estimate_normals:
        pointcloud.estimate_normals(
            search_param=o3d.geometry.KDTreeSearchParamHybrid(
                radius=estimate_normals_radius,
                max_nn=estimate_normals_max_nn))

    o3d.io.write_point_cloud(
        target_pointcloud_file_path,
        pointcloud,
        write_ascii=True,
        print_progress=True)
    return True

