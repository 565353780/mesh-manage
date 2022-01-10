#!/usr/bin/env python
# -*- coding: utf-8 -*-

import numpy as np
from tqdm import tqdm
import open3d as o3d
import pandas as pd

class PointCloudRender:
    def __init__(self):
        self.d3_40_colors_rgb = np.array(
            [
                [164, 218, 252], [120, 173, 219], [253, 147, 81], [252, 234, 163], [0, 128, 128],
                [132, 220, 198], [255, 104, 107], [255, 166, 158], [148, 103, 189], [189, 147, 189],
                [140, 86, 75], [146, 94, 120], [227, 119, 194], [247, 182, 210], [127, 127, 127],
                [199, 199, 199], [188, 189, 34], [219, 219, 141], [23, 190, 207], [158, 218, 229],
                [57, 59, 121], [82, 84, 163], [107, 110, 207], [156, 158, 222], [99, 121, 57],
                [140, 162, 82], [181, 207, 107], [206, 219, 156], [140, 109, 49], [189, 158, 57],
                [231, 186, 82], [231, 203, 148], [132, 60, 57], [173, 73, 74], [214, 97, 107],
                [231, 150, 156], [123, 65, 115], [165, 81, 148], [206, 109, 189], [222, 158, 214],
            ],
            dtype=np.uint8,
        )

        self.labels = None
        self.pointcloud_file_path = None

        self.pointcloud = None
        self.labeled_point_cluster_list = None
        return

    def splitLabeledPoints(self):
        self.labeled_point_cluster_list = []

        print("start reading labels...")
        label_list = []
        with open(self.pointcloud_file_path, "r") as f:
            lines = f.readlines()
            find_start_line = False
            for line in tqdm(lines):
                if "DATA ascii" in line:
                    find_start_line = True
                    continue
                if not find_start_line:
                    continue
                line_data = line.split("\n")[0].split(" ")
                if len(line_data) < 5:
                    continue
                label_list.append(int(line_data[3]))

        print("start reading points in pointcloud...", end="")
        np_points = np.asarray(self.pointcloud.points)
        if np_points.shape[0] != len(label_list):
            print("PointCloudRender::createColor : label size not matched!")
            return False
        print("SUCCESS!")

        labeled_point_list = []
        for _ in range(len(self.labels)):
            labeled_point_list.append([])

        print("start clustering points in pointcloud...")
        for i in tqdm(range(np_points.shape[0])):
            point = np_points[i]
            label = label_list[i]
            labeled_point_list[label].append([point[0], point[1], point[2]])

        for labeled_point_cluster in labeled_point_list:
            self.labeled_point_cluster_list.append(labeled_point_cluster)
        return True

    def loadPointCloud(self,
                       pointcloud_file_path,
                       labels):
        self.pointcloud_file_path = pointcloud_file_path
        self.labels = labels

        print("start loading pointcloud...", end="")
        self.pointcloud = o3d.io.read_point_cloud(self.pointcloud_file_path)
        print("SUCCESS!")

        self.splitLabeledPoints()
        return True

    def render(self, show_labels):
        rendered_pointcloud = o3d.geometry.PointCloud()

        render_points = []
        render_colors = []
        print("start create rendered pointcloud...")
        for render_label in show_labels:
            render_point_cluster = self.labeled_point_cluster_list[render_label]
            print("\t for label " + str(render_label) + "...")
            for render_point in tqdm(render_point_cluster):
                render_points.append(render_point)
                render_colors.append(self.d3_40_colors_rgb[render_label % len(self.d3_40_colors_rgb)] / 255.0)

        rendered_pointcloud.points = o3d.utility.Vector3dVector(np.array(render_points))
        rendered_pointcloud.colors = o3d.utility.Vector3dVector(np.array(render_colors))

        o3d.visualization.draw_geometries([rendered_pointcloud])
        return True

if __name__ == "__main__":
    pointcloud_file_path = "./masked_pc/front_3d/01.pcd"
    labels = [
        "ZERO", "table", "chair", "sofa", "lamp",
        "bed", "cabinet", "lantern", "light", "wall",
        "painting", "refrigerator"]
    show_labels = [
           1, 2, 3, 4,
        5, 6, 7, 8,
        10, 11]

    pointcloud_render = PointCloudRender()
    pointcloud_render.loadPointCloud(pointcloud_file_path,
                                     labels)
    pointcloud_render.render(show_labels)

