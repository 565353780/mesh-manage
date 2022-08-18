#!/usr/bin/env python
# -*- coding: utf-8 -*-

import open3d as o3d

def samplePointCloud(pointcloud_file_path, down_sample_cluster_num, save_pointcloud_file_path, print_progress=False):
    if print_progress:
        print("[INFO][sample::samplePointCloud]")
        print("\t start sampling pointcloud :")
        print("\t down_sample_cluster_num =", down_sample_cluster_num, "...")

    pointcloud = o3d.io.read_point_cloud(pointcloud_file_path, print_progress=print_progress)

    sampled_pointcloud = o3d.geometry.PointCloud.uniform_down_sample(
        pointcloud, down_sample_cluster_num)

    o3d.io.write_point_cloud(
        save_pointcloud_file_path,
        sampled_pointcloud,
        write_ascii=True,
        print_progress=print_progress)
    return True

def sampleMesh(mesh_file_path, vertex_cluster_dist_max, save_mesh_file_path, print_progress=False):
    if print_progress:
        print("[INFO][sample::sampleMesh]")
        print("\t start sampling mesh:")
        print("\t vertex_cluster_dist_max =", vertex_cluster_dist_max, "...")

    mesh = o3d.io.read_triangle_mesh(mesh_file_path, print_progress=print_progress)

    sample_mesh = mesh.simplify_vertex_clustering(vertex_cluster_dist_max)

    o3d.io.write_triangle_mesh(
        save_mesh_file_path,
        sample_mesh,
        write_ascii=True,
        print_progress=print_progress)
    return True

