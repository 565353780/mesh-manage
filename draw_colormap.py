#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import numpy as np
import open3d as o3d

from GRNetDetector.GRNet_Detector import GRNet_Detector

red_white_color_map = np.array([
    [255, 255, 255],
    [228, 177, 171], [228, 177, 171],
    [227, 150, 149], [227, 150, 149],
    [223, 115, 115], [223, 115, 115],
    [218, 85, 82],
    [204, 68, 75], [204, 68, 75],
    [204, 68, 75], [204, 68, 75],
], dtype=np.float)

red_blue_color_map = np.array([
    [179, 222, 226],
    [234, 242, 215],
    [239, 207, 227],
    [234, 154, 178],
    [226, 115, 150], [226, 115, 150],
    [226, 115, 150], [226, 115, 150],
    [226, 115, 150], [226, 115, 150],
    [226, 115, 150], [226, 115, 150],
    [226, 115, 150], [226, 115, 150],
], dtype=np.float)

COLOR_MAP = red_white_color_map

def getSpherePointCloud(pointcloud,radius=1.0, resolution=20):
    sphere_pointcloud = o3d.geometry.PointCloud()
    sphere_points_list = []
    sphere_colors = []
    mesh_sphere = o3d.geometry.TriangleMesh.create_sphere(
        radius=radius,
        resolution=resolution)
    sphere_points = np.array(mesh_sphere.vertices)

    points = np.array(pointcloud.points)
    colors = np.array(pointcloud.colors)
    for i in range(len(points)):
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

def Open3DVisualizer(geometry_list):
    visualizer = o3d.visualization.Visualizer()
    visualizer.create_window(window_name="test")

    view_control = visualizer.get_view_control()

    render_option = visualizer.get_render_option()
    render_option.line_width = 1.0
    render_option.point_size = 10.0
    render_option.background_color = np.array([255.0, 255.0, 255.0])/255.0

    for geometry_object in geometry_list:
        visualizer.add_geometry(geometry_object)

    visualizer.run()
    visualizer.destroy_window()
    return True

def getHeatMap():
    partial_mesh_file_path = \
        "/home/chli/chLi/coscan_data/incomplete_chair_1.ply"
    complete_mesh_file_path = \
        "/home/chli/chLi/coscan_data/chari-complete_4.ply"

    complete_mesh = o3d.io.read_triangle_mesh(complete_mesh_file_path)
    complete_pointcloud = o3d.io.read_point_cloud(complete_mesh_file_path)

    partial_mesh = o3d.io.read_triangle_mesh(partial_mesh_file_path)
    partial_pointcloud = o3d.io.read_point_cloud(partial_mesh_file_path)
    sigma = 0
    if sigma > 0:
        partial_points = np.array(partial_pointcloud.points)
        noise_x = np.random.normal(0, sigma, partial_points.shape[0])
        noise_y = np.random.normal(0, sigma, partial_points.shape[0])
        noise_z = np.random.normal(0, sigma, partial_points.shape[0])
        noise = []
        for i in range(partial_points.shape[0]):
            noise.append([noise_x[i], noise_y[i], noise_z[i]])
        noise = np.array(noise)
        partial_points += noise
        partial_pointcloud.points = o3d.utility.Vector3dVector(partial_points)
        partial_mesh.vertices = o3d.utility.Vector3dVector(partial_points)

    partial_colors = np.array([[101, 91, 82] for _ in np.array(partial_mesh.vertices)],
                              dtype=np.float)/255.0
    partial_pointcloud.colors = o3d.utility.Vector3dVector(partial_colors)
    partial_mesh.vertex_colors = o3d.utility.Vector3dVector(partial_colors)

    dist_to_partial = complete_pointcloud.compute_point_cloud_distance(
        partial_pointcloud)

    colors = []
    color_num = len(COLOR_MAP)
    min_dist = 0
    max_dist = np.max(dist_to_partial)
    dist_step = (max_dist - min_dist) / (color_num - 1.0)

    for dist in dist_to_partial:
        dist_divide = dist / dist_step
        color_idx = int(dist_divide)
        if color_idx >= color_num - 1:
            colors.append(COLOR_MAP[color_num - 1])
            continue

        next_color_weight = dist_divide - color_idx
        color = (1.0 - next_color_weight) * COLOR_MAP[color_idx]
        if next_color_weight > 0:
            color += next_color_weight * COLOR_MAP[color_idx + 1]
        colors.append(color)

    colors = np.array(colors, dtype=np.float) / 255.0
    complete_pointcloud.colors = o3d.utility.Vector3dVector(colors)
    complete_mesh.vertex_colors = o3d.utility.Vector3dVector(colors)

    complete_pointcloud.normals = o3d.utility.Vector3dVector()

    partial_mesh.compute_vertex_normals()
    complete_mesh.compute_vertex_normals()

    #  sphere_complete_pointcloud = getSpherePointCloud(complete_pointcloud, 0.001, 20)

    o3d.visualization.draw_geometries([
        partial_mesh,
        complete_pointcloud
    ])

    partial_mesh_path = "/home/chli/chLi/coscan_data/chair_partial_mesh.ply"
    complete_mesh_path = "/home/chli/chLi/coscan_data/chair_complete_mesh.ply"
    o3d.io.write_triangle_mesh(partial_mesh_path, partial_mesh, write_ascii=True)
    o3d.io.write_triangle_mesh(complete_mesh_path, complete_mesh, write_ascii=True)

    return True

def demo():
    model_path = os.environ['HOME'] + "/.ros/GRNet-ShapeNet.pth"
    pcd_file_path = "/home/chli/chLi/2022_5_9_18-35-42/scan12.ply"

    grnet_detector = GRNet_Detector()
    grnet_detector.load_model(model_path)
    pointcloud_result = grnet_detector.detect_pcd_file(pcd_file_path)

    complete_pointcloud = o3d.geometry.PointCloud()
    complete_pointcloud.points = o3d.utility.Vector3dVector(pointcloud_result)
    return True

if __name__ == "__main__":
    #  demo()
    getHeatMap()

