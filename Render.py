#!/usr/bin/env python
# -*- coding: utf-8 -*-

import numpy as np
from tqdm import tqdm
import open3d as o3d
import open3d.visualization.rendering as rendering

from channel_pointcloud import ChannelPointCloud

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
                [231, 150, 156], [123, 65, 115], [165, 81, 148], [206, 109, 189], [222, 158, 214]
            ],
            dtype=np.uint8,
        )

        self.pointcloud_file_path = None
        self.label_channel_idx = None
        self.labels = None

        self.pointcloud = None
        self.labeled_point_cluster_list = None
        return

    def splitLabeledPoints(self):
        self.labeled_point_cluster_list = []

        print("start reading labels...")
        lines = None
        with open(self.pointcloud_file_path, "r") as f:
            lines = f.readlines()

        label_list = []
        find_start_line = False
        for line in tqdm(lines):
            if "DATA ascii" in line:
                find_start_line = True
                continue
            if not find_start_line:
                continue
            line_data = line.split("\n")[0].split(" ")
            if len(line_data) < self.label_channel_idx:
                continue
            label_list.append(int(float(line_data[self.label_channel_idx])))

        print("start reading points in pointcloud...", end="")
        points = np.asarray(self.pointcloud.points).tolist()
        if len(points) != len(label_list):
            print("PointCloudRender::createColor : label size not matched!")
            return False
        print("SUCCESS!")

        labeled_point_list = []
        for _ in range(len(self.labels)):
            labeled_point_list.append([])

        print("start clustering points in pointcloud...")
        for i in tqdm(range(len(points))):
            point = points[i]
            label = label_list[i]
            labeled_point_list[label].append(point)

        for labeled_point_cluster in labeled_point_list:
            self.labeled_point_cluster_list.append(labeled_point_cluster)
        return True

    def loadPointCloud(self,
                       pointcloud_file_path,
                       label_channel_idx,
                       labels):
        self.pointcloud_file_path = pointcloud_file_path
        self.label_channel_idx = label_channel_idx
        self.labels = labels

        print("start loading pointcloud...", end="")
        self.pointcloud = o3d.io.read_point_cloud(
            self.pointcloud_file_path, print_progress=True)
        print("SUCCESS!")

        self.splitLabeledPoints()
        return True

    def getRenderedPointCloud(self, show_labels):
        rendered_pointcloud = o3d.geometry.PointCloud()

        render_points = []
        render_colors = []
        print("start create rendered pointcloud...")
        for render_label in show_labels:
            render_point_cluster = self.labeled_point_cluster_list[render_label]
            if len(render_point_cluster) == 0:
                continue
            print("\t for label " + str(render_label) + "...")
            for render_point in tqdm(render_point_cluster):
                render_points.append(render_point)
                render_colors.append(self.d3_40_colors_rgb[render_label % len(self.d3_40_colors_rgb)] / 255.0)

        rendered_pointcloud.points = o3d.utility.Vector3dVector(np.array(render_points))
        rendered_pointcloud.colors = o3d.utility.Vector3dVector(np.array(render_colors))

        rendered_pointcloud.estimate_normals(
            search_param=o3d.geometry.KDTreeSearchParamHybrid(radius=0.1, max_nn=30))
        return rendered_pointcloud

    def render(self, show_labels):
        rendered_pointcloud = self.getRenderedPointCloud(show_labels)

        radii = [0.05, 0.1, 0.2, 0.4]
        mesh = o3d.geometry.TriangleMesh.create_from_point_cloud_ball_pivoting(
            rendered_pointcloud, o3d.utility.DoubleVector(radii))

        #  mesh = None
        #  depth = 6
        #  with o3d.utility.VerbosityContextManager(o3d.utility.VerbosityLevel.Debug) as cm:
            #  mesh, densities = o3d.geometry.TriangleMesh.create_from_point_cloud_poisson(rendered_pointcloud, depth=depth)

        o3d.visualization.draw_geometries([mesh])
        return True

def demo():
    pointcloud_file_path = "./masked_pc/home/home_DownSample_8_masked_merged.pcd"
    label_channel_idx = 7

    #  labels = [
        #  "ZERO", "table", "chair", "sofa", "lamp",
        #  "bed", "cabinet", "lantern", "light", "wall",
        #  "painting", "refrigerator"]
    #  show_labels = [0, 1, 2, 3, 4, 5, 6, 7, 8, 10, 11]

    labels = [
        "BG",
        "person", "bicycle", "car", "motorcycle", "airplane",
        "bus", "train", "truck", "boat", "traffic light",
        "fire hydrant", "stop sign", "parking meter", "bench", "bird",
        "cat", "dog", "horse", "sheep", "cow",
        "elephant", "bear", "zebra", "giraffe", "backpack",
        "umbrella", "handbag", "tie", "suitcase", "frisbee",
        "skis", "snowboard", "sports ball", "kite", "baseball bat",
        "baseball glove", "skateboard", "surfboard", "tennis racket", "bottle",
        "wine glass", "cup", "fork", "knife", "spoon",
        "bowl", "banana", "apple", "sandwich", "orange",
        "broccoli", "carrot", "hot dog", "pizza", "donut",
        "cake", "chair", "couch", "potted plant", "bed",
        "dining table", "toilet", "tv", "laptop", "mouse",
        "remote", "keyboard", "cell phone", "microwave", "oven",
        "toaster", "sink", "refrigerator", "book", "clock",
        "vase", "scissors", "teddy bear", "hair drier", "toothbrush"
    ]
    show_labels = [
        #  0,
        1, 2, 3, 4, 5,
        6, 7, 8, 9, 10,
        11, 12, 13, 14, 15,
        16, 17, 18, 19, 20,
        21, 22, 23, 24, 25,
        26, 27, 28, 29, 30,
        31, 32, 33, 34, 35,
        36, 37, 38, 39, 40,
        41, 42, 43, 44, 45,
        46, 47, 48, 49, 50,
        51, 52, 53, 54, 55,
        56, 57, 58, 59, 60,
        61, 62, 63, 64, 65,
        66, 67, 68, 69, 70,
        71, 72, 73, 74, 75,
        76, 77, 78, 79, 80
    ]


    pointcloud_render = PointCloudRender()
    pointcloud_render.loadPointCloud(pointcloud_file_path,
                                     label_channel_idx,
                                     labels)
    pointcloud_render.render(show_labels)
    return True

if __name__ == "__main__":
    demo()

