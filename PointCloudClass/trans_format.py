#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import open3d as o3d

def transFormat(source_pointcloud_file_path,
                target_pointcloud_file_path,
                estimate_normals_radius,
                estimate_normals_max_nn):
    if not os.path.exists(source_pointcloud_file_path):
        print("[ERROR][transFormat]")
        print("source_file not exist!")
        return False

    pointcloud = o3d.io.read_point_cloud(source_pointcloud_file_path, print_progress=True)
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

def transToPCD(source_pointcloud_file_path,
               estimate_normals_radius,
               estimate_normals_max_nn):
    if ".pcd" == source_pointcloud_file_path[-4:]:
        return True
    target_pointcloud_file_path = source_pointcloud_file_path[:-4] + ".pcd"
    return transFormat(source_pointcloud_file_path,
                       target_pointcloud_file_path,
                       estimate_normals_radius,
                       estimate_normals_max_nn)

def transToPLY(source_pointcloud_file_path,
               estimate_normals_radius,
               estimate_normals_max_nn):
    if ".ply" == source_pointcloud_file_path[-4:]:
        return True
    target_pointcloud_file_path = source_pointcloud_file_path[:-4] + ".ply"
    return transFormat(source_pointcloud_file_path,
                       target_pointcloud_file_path,
                       estimate_normals_radius,
                       estimate_normals_max_nn)

