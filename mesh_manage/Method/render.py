#!/usr/bin/env python
# -*- coding: utf-8 -*-

import open3d as o3d

def render(pointcloud_file_path, estimate_normals_radius, estimate_normals_max_nn):
    pointcloud = o3d.io.read_point_cloud(pointcloud_file_path, print_progress=True)
    pointcloud.estimate_normals(
        search_param=o3d.geometry.KDTreeSearchParamHybrid(
            radius=estimate_normals_radius,
            max_nn=estimate_normals_max_nn))
    o3d.visualization.draw_geometries([pointcloud])
    return True

