#!/usr/bin/env python
# -*- coding: utf-8 -*-

import open3d as o3d

def downSample(pointcloud_file_path, down_sample_cluster_num, save_pointcloud_file_path):
    print("[INFO][downSample]")
    print("\t start down sampling pointcloud :")
    print("\t down_sample_cluster_num = " + str(down_sample_cluster_num) + "...")
    pointcloud = o3d.io.read_point_cloud(pointcloud_file_path, print_progress=True)

    down_sampled_pointcloud = o3d.geometry.PointCloud.uniform_down_sample(
        pointcloud, down_sample_cluster_num)

    o3d.io.write_point_cloud(
        save_pointcloud_file_path,
        down_sampled_pointcloud,
        write_ascii=True,
        print_progress=True)
    print("SUCCESS!")
    return True

