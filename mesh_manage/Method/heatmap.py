#!/usr/bin/env python
# -*- coding: utf-8 -*-

import numpy as np
import open3d as o3d
from tqdm import tqdm

from mesh_manage.Config.color import COLOR_MAP_DICT

def getSpherePointCloud(pointcloud,
                        radius=1.0,
                        resolution=20,
                        print_progress=False):
    sphere_pointcloud = o3d.geometry.PointCloud()
    sphere_points_list = []
    sphere_colors = []
    mesh_sphere = o3d.geometry.TriangleMesh.create_sphere(
        radius=radius,
        resolution=resolution)
    sphere_points = np.array(mesh_sphere.vertices)

    points = np.array(pointcloud.points)
    colors = np.array(pointcloud.colors)
    for_data = range(len(points))
    if print_progress:
        print("[INFO][heatmap::getSpherePointCloud]")
        print("\t start generate sphere pointcloud...")
        for_data = tqdm(for_data)
    for i in for_data:
        new_points = sphere_points + points[i]
        sphere_points_list.append(new_points)
        for _ in sphere_points:
            sphere_colors.append(colors[i])
    points = np.concatenate(sphere_points_list, axis=0)
    colors = np.array(sphere_colors)
    sphere_pointcloud.points = \
        o3d.utility.Vector3dVector(points)
    sphere_pointcloud.colors = \
        o3d.utility.Vector3dVector(colors)
    return sphere_pointcloud

def getHeatMap(partial_mesh_file_path,
               complete_mesh_file_path,
               save_partial_mesh_file_path,
               save_complete_mesh_file_path,
               color_map=COLOR_MAP_DICT["jet"],
               partial_noise_sigma=0,
               error_max=None,
               is_visual=False,
               print_progress=False):
    if print_progress:
        print("[INFO][heatmap::getHeatMap]")
        print("\t start load complete mesh...")
    complete_mesh = o3d.io.read_triangle_mesh(complete_mesh_file_path, print_progress=print_progress)
    complete_pointcloud = o3d.io.read_point_cloud(complete_mesh_file_path, print_progress=print_progress)

    if print_progress:
        print("[INFO][heatmap::getHeatMap]")
        print("\t start load partial mesh...")
    partial_mesh = o3d.io.read_triangle_mesh(partial_mesh_file_path, print_progress=print_progress)
    partial_pointcloud = o3d.io.read_point_cloud(partial_mesh_file_path, print_progress=print_progress)

    threshold = 1.0
    trans_init = np.asarray([[1,0,0,0],
                             [0,1,0,0],
                             [0,0,1,0],
                             [0,0,0,1]])

    reg_p2p = o3d.pipelines.registration.registration_icp(
        partial_pointcloud, complete_pointcloud, threshold, trans_init,
        o3d.pipelines.registration.TransformationEstimationPointToPoint())

    partial_pointcloud.transform(reg_p2p.transformation)
    partial_mesh.transform(reg_p2p.transformation)

    if is_visual:
        print("[INFO][heatmap::getHeatMap]")
        print("\t start show icp result...")
        o3d.visualization.draw_geometries([partial_pointcloud, complete_mesh])

    if partial_noise_sigma > 0:
        partial_points = np.array(partial_pointcloud.points)
        noise_x = np.random.normal(0, partial_noise_sigma, partial_points.shape[0])
        noise_y = np.random.normal(0, partial_noise_sigma, partial_points.shape[0])
        noise_z = np.random.normal(0, partial_noise_sigma, partial_points.shape[0])
        noise = []

        for_data = range(partial_points.shape[0])
        if print_progress:
            print("[INFO][heatmap::getHeatMap]")
            print("\t start generate noise...")
            for_data = tqdm(for_data)
        for i in for_data:
            noise.append([noise_x[i], noise_y[i], noise_z[i]])
        noise = np.array(noise)
        partial_points += noise
        partial_pointcloud.points = o3d.utility.Vector3dVector(partial_points)
        partial_mesh.vertices = o3d.utility.Vector3dVector(partial_points)

    partial_colors = np.array([[101, 91, 82] for _ in np.array(partial_mesh.vertices)],
                              dtype=float)/255.0
    partial_pointcloud.colors = o3d.utility.Vector3dVector(partial_colors)
    partial_mesh.vertex_colors = o3d.utility.Vector3dVector(partial_colors)

    dist_to_partial = complete_pointcloud.compute_point_cloud_distance(partial_pointcloud)

    colors = []
    color_num = len(color_map)
    min_dist = 0
    max_dist = error_max
    if max_dist is None:
        max_dist = np.max(dist_to_partial)
    dist_step = (max_dist - min_dist) / (color_num - 1.0)

    for_data = dist_to_partial
    if print_progress:
        print("[INFO][heatmap::getHeatMap]")
        print("\t start generate heatmap...")
        for_data = tqdm(for_data)
    for dist in for_data:
        dist_divide = dist / dist_step
        color_idx = int(dist_divide)
        if color_idx >= color_num - 1:
            colors.append(color_map[color_num - 1])
            continue

        next_color_weight = dist_divide - color_idx
        color = (1.0 - next_color_weight) * color_map[color_idx]
        if next_color_weight > 0:
            color += next_color_weight * color_map[color_idx + 1]
        colors.append(color)

    colors = np.array(colors, dtype=float) / 255.0
    complete_pointcloud.colors = o3d.utility.Vector3dVector(colors)
    complete_mesh.vertex_colors = o3d.utility.Vector3dVector(colors)

    complete_pointcloud.normals = o3d.utility.Vector3dVector()

    partial_mesh.compute_vertex_normals()
    complete_mesh.compute_vertex_normals()

    #  sphere_complete_pointcloud = getSpherePointCloud(complete_pointcloud,
                                                     #  0.001,
                                                     #  20,
                                                     #  print_progress)

    if is_visual:
        print("[INFO][heatmap::getHeatMap]")
        print("\t start show heatmap result...")
        o3d.visualization.draw_geometries([partial_mesh, complete_pointcloud])

    if print_progress:
        print("[INFO][heatmap::getHeatMap]")
        print("\t start save partial mesh...")
    o3d.io.write_triangle_mesh(save_partial_mesh_file_path, partial_mesh,
                               write_ascii=True, print_progress=print_progress)

    if print_progress:
        print("[INFO][heatmap::getHeatMap]")
        print("\t start save heatmap...")
    o3d.io.write_triangle_mesh(save_complete_mesh_file_path, complete_mesh,
                               write_ascii=True, print_progress=print_progress)
    return True

